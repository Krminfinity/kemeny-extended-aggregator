#!/usr/bin/env python3
"""
ケアワーカーと被介護者のマッチングシステム

このモジュールは卒業論文「ケアワーカーと被介護者のマッチングアルゴリズムの開発」で
提案されたマッチングシステムの完全な実装です。

システムの構成:
1. 拡張版Kemenyルール: 主観的選好と客観的フィット度を統合
2. DAアルゴリズム: 安定マッチングを生成

Author: 倉持誠 (Makoto Kuramochi)
"""

from typing import List, Dict, Tuple, Optional
import numpy as np
import json
from extended_kemeny_rule import ExtendedKemenyRule
from deferred_acceptance import DeferredAcceptanceAlgorithm


class CareMatchingSystem:
    """ケアマッチングシステムのメインクラス"""
    
    def __init__(self, preference_weight: float = 1.0, fitness_weight: float = 1.0):
        """
        マッチングシステムの初期化
        
        Args:
            preference_weight: 主観的選好の重み
            fitness_weight: 客観的フィット度の重み
        """
        self.kemeny_rule = ExtendedKemenyRule(preference_weight, fitness_weight)
        self.da_algorithm = DeferredAcceptanceAlgorithm()
        self.preference_weight = preference_weight
        self.fitness_weight = fitness_weight
    
    def generate_sample_data(self) -> Dict:
        """
        論文の例に基づくサンプルデータを生成
        
        Returns:
            Dict: サンプルデータ辞書
        """
        return {
            'care_recipients': [4, 5, 6, 7],
            'caregivers': [1, 2, 3],
            'caregiver_capacities': {1: 1, 2: 1, 3: 2},
            
            # 被介護者の主観的選好（例）
            'recipient_subjective_preferences': {
                4: [1, 3, 2],
                5: [2, 1, 3], 
                6: [2, 1, 3],  # 論文の例: ケアワーカー2>1>3
                7: [3, 1, 2],
            },
            
            # ケアワーカーの主観的選好（例）
            'caregiver_subjective_preferences': {
                1: [7, 4, 6, 5],
                2: [6, 5, 4, 7],
                3: [7, 4, 5, 6],
            },
            
            # 客観的フィット度スコア（被介護者 x ケアワーカー）
            'fitness_scores': {
                4: [0.7, 0.8, 0.6],  # 被介護者4に対する各ケアワーカーのフィット度
                5: [0.9, 0.7, 0.8],
                6: [0.8, 0.9, 0.7],  # 論文の例
                7: [0.6, 0.8, 0.9],
            },
            
            # ケアワーカーから被介護者への客観的フィット度
            'caregiver_fitness_scores': {
                1: [0.8, 0.7, 0.9, 0.6],  # ケアワーカー1の各被介護者へのフィット度
                2: [0.7, 0.8, 0.9, 0.8],
                3: [0.6, 0.8, 0.7, 0.9],
            }
        }
    
    def aggregate_all_preferences(self, data: Dict) -> Tuple[Dict, Dict, Dict]:
        """
        全ての主観的選好と客観的フィット度を統合
        
        Args:
            data: サンプルデータ辞書
            
        Returns:
            Tuple: 統合された被介護者選好、ケアワーカー選好、詳細情報
        """
        recipient_integrated_preferences = {}
        caregiver_integrated_preferences = {}
        integration_details = {'recipients': {}, 'caregivers': {}}
        
        # 被介護者の選好統合
        for recipient_id in data['care_recipients']:
            subjective_pref = data['recipient_subjective_preferences'][recipient_id]
            fitness_scores = data['fitness_scores'][recipient_id]
            
            # 候補者リストはケアワーカーIDそのもの
            candidates = data['caregivers'].copy()
            
            integrated_pref, details = self.kemeny_rule.aggregate_preferences(
                subjective_pref, fitness_scores, candidates
            )
            
            recipient_integrated_preferences[recipient_id] = integrated_pref
            integration_details['recipients'][recipient_id] = details
        
        # ケアワーカーの選好統合
        for caregiver_id in data['caregivers']:
            subjective_pref = data['caregiver_subjective_preferences'][caregiver_id]
            fitness_scores = data['caregiver_fitness_scores'][caregiver_id]
            candidates = data['care_recipients']
            
            integrated_pref, details = self.kemeny_rule.aggregate_preferences(
                subjective_pref, fitness_scores, candidates
            )
            
            caregiver_integrated_preferences[caregiver_id] = integrated_pref
            integration_details['caregivers'][caregiver_id] = details
        
        return recipient_integrated_preferences, caregiver_integrated_preferences, integration_details
    
    def run_complete_matching(self, data: Optional[Dict] = None) -> Dict:
        """
        完全なマッチングプロセスを実行
        
        Args:
            data: 入力データ（省略時はサンプルデータを使用）
            
        Returns:
            Dict: 完全な結果辞書
        """
        if data is None:
            data = self.generate_sample_data()
        
        print("=== ケアワーカーと被介護者のマッチングシステム ===")
        print()
        
        # ステップ1: 選好統合
        print("ステップ1: 拡張版Kemenyルールによる選好統合")
        print("-" * 50)
        
        recipient_prefs, caregiver_prefs, integration_details = self.aggregate_all_preferences(data)
        
        print("統合結果:")
        print("被介護者の統合選好:")
        for recipient_id, pref in recipient_prefs.items():
            print(f"  被介護者{recipient_id}: {pref}")
        
        print("ケアワーカーの統合選好:")
        for caregiver_id, pref in caregiver_prefs.items():
            print(f"  ケアワーカー{caregiver_id}: {pref}")
        print()
        
        # ステップ2: DAアルゴリズムによるマッチング
        print("ステップ2: DAアルゴリズムによるマッチング")
        print("-" * 50)
        
        matches, da_details = self.da_algorithm.create_match(
            data['care_recipients'],
            data['caregivers'],
            recipient_prefs,
            caregiver_prefs,
            data['caregiver_capacities']
        )
        
        # 結果の統合
        complete_results = {
            'input_data': data,
            'integration_details': integration_details,
            'integrated_preferences': {
                'recipients': recipient_prefs,
                'caregivers': caregiver_prefs
            },
            'final_matches': matches,
            'da_details': da_details,
            'system_parameters': {
                'preference_weight': self.preference_weight,
                'fitness_weight': self.fitness_weight
            }
        }
        
        return complete_results
    
    def print_complete_results(self, results: Dict):
        """
        完全な結果を見やすく出力
        
        Args:
            results: run_complete_matchingから返された結果辞書
        """
        print("=== 最終マッチング結果 ===")
        print(f"マッチング: {results['final_matches']}")
        print(f"未マッチ被介護者: {results['da_details']['unmatched_recipients']}")
        print(f"ケアワーカー利用率: {results['da_details']['caregiver_utilization']}")
        print()
        
        # 安定性チェック
        is_stable, blocking_pairs = self.da_algorithm.is_stable_matching(
            results['final_matches'],
            results['integrated_preferences']['recipients'],
            results['integrated_preferences']['caregivers'],
            results['input_data']['caregiver_capacities']
        )
        
        print("=== マッチング品質評価 ===")
        print(f"安定マッチング: {is_stable}")
        if not is_stable:
            print(f"ブロッキングペア: {blocking_pairs}")
        
        # 満足度計算
        self.calculate_satisfaction_scores(results)
    
    def calculate_satisfaction_scores(self, results: Dict):
        """
        マッチング結果の満足度スコアを計算
        
        Args:
            results: 結果辞書
        """
        print()
        print("=== 満足度分析 ===")
        
        recipient_satisfaction = {}
        caregiver_satisfaction = {}
        
        # 被介護者の満足度
        for recipient_id, caregiver_id in results['final_matches'].items():
            pref = results['integrated_preferences']['recipients'][recipient_id]
            if caregiver_id in pref:
                rank = pref.index(caregiver_id) + 1  # 1位、2位、...
                satisfaction = (len(pref) - rank + 1) / len(pref)  # 正規化
                recipient_satisfaction[recipient_id] = satisfaction
                print(f"被介護者{recipient_id}: 第{rank}希望マッチ (満足度: {satisfaction:.2f})")
        
        avg_recipient_satisfaction = np.mean(list(recipient_satisfaction.values()))
        print(f"被介護者平均満足度: {avg_recipient_satisfaction:.3f}")
        
        # ケアワーカーの満足度
        caregiver_matches = {}
        for caregiver_id in results['input_data']['caregivers']:
            caregiver_matches[caregiver_id] = [
                r for r, c in results['final_matches'].items() if c == caregiver_id
            ]
        
        for caregiver_id, matched_recipients in caregiver_matches.items():
            if matched_recipients:
                pref = results['integrated_preferences']['caregivers'][caregiver_id]
                total_satisfaction = 0
                for recipient_id in matched_recipients:
                    if recipient_id in pref:
                        rank = pref.index(recipient_id) + 1
                        satisfaction = (len(pref) - rank + 1) / len(pref)
                        total_satisfaction += satisfaction
                
                avg_satisfaction = total_satisfaction / len(matched_recipients)
                caregiver_satisfaction[caregiver_id] = avg_satisfaction
                print(f"ケアワーカー{caregiver_id}: 平均満足度 {avg_satisfaction:.2f}")
        
        if caregiver_satisfaction:
            avg_caregiver_satisfaction = np.mean(list(caregiver_satisfaction.values()))
            print(f"ケアワーカー平均満足度: {avg_caregiver_satisfaction:.3f}")
    
    def save_results_to_file(self, results: Dict, filename: str):
        """
        結果をJSONファイルに保存
        
        Args:
            results: 結果辞書
            filename: 保存ファイル名
        """
        # numpy配列をリストに変換して保存可能にする
        def convert_numpy(obj):
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            elif isinstance(obj, np.integer):
                return int(obj)
            elif isinstance(obj, np.floating):
                return float(obj)
            return obj
        
        # 結果を保存用に変換
        save_data = json.loads(json.dumps(results, default=convert_numpy))
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, ensure_ascii=False, indent=2)
        
        print(f"結果を {filename} に保存しました")


def main():
    """メイン実行関数"""
    # システムを初期化
    matching_system = CareMatchingSystem(preference_weight=1.0, fitness_weight=1.0)
    
    # 完全なマッチングプロセスを実行
    results = matching_system.run_complete_matching()
    
    # 結果を表示
    matching_system.print_complete_results(results)
    
    # 詳細な統合プロセスを表示（論文の例）
    print("\n=== 詳細: 被介護者6の拡張版Kemenyルール計算 ===")
    recipient_6_details = results['integration_details']['recipients'][6]
    matching_system.kemeny_rule.print_calculation_details(recipient_6_details)
    
    # 詳細なDAプロセスを表示
    print("\n=== 詳細: DAアルゴリズム実行過程 ===")
    matching_system.da_algorithm.print_matching_process(results['da_details'])
    
    # 結果をファイルに保存
    matching_system.save_results_to_file(results, 'matching_results.json')


if __name__ == "__main__":
    main()