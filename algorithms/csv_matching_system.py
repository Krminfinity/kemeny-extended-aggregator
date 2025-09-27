"""
CSV対応ケアワーカー・被介護者マッチングシステム
CSVファイルからデータを読み込んでマッチングを実行する
"""

from csv_input_handler import CSVInputHandler
from extended_kemeny_rule import ExtendedKemenyRule
from deferred_acceptance import DeferredAcceptanceAlgorithm
import json
import os
from typing import Dict, List, Optional

class CSVMatchingSystem:
    """CSV入力対応のマッチングシステム"""
    
    def __init__(self):
        self.csv_handler = CSVInputHandler()
        self.kemeny_rule = ExtendedKemenyRule()
        self.da_algorithm = DeferredAcceptanceAlgorithm()
        
        self.care_receivers_data = {}
        self.care_workers_data = {}
        self.integrated_preferences = {}
        self.matching_result = {}
    
    def load_data_from_csv(self, 
                          receiver_subjective_csv: str,
                          receiver_objective_csv: str,
                          worker_subjective_csv: str,
                          worker_objective_csv: str,
                          worker_capacity_csv: Optional[str] = None):
        """
        CSVファイルからすべてのデータを読み込む
        
        Args:
            receiver_subjective_csv: 被介護者の主観的選好CSV
            receiver_objective_csv: 被介護者の客観的フィット度CSV
            worker_subjective_csv: ケアワーカーの主観的選好CSV
            worker_objective_csv: ケアワーカーの客観的フィット度CSV
            worker_capacity_csv: ケアワーカーの容量CSV（オプション）
        """
        print("=== CSVデータ読み込み開始 ===")
        
        # 被介護者データの読み込み
        self.care_receivers_data = self.csv_handler.load_care_receivers_data(
            receiver_subjective_csv, receiver_objective_csv
        )
        
        # ケアワーカーデータの読み込み
        self.care_workers_data = self.csv_handler.load_care_workers_data(
            worker_subjective_csv, worker_objective_csv, worker_capacity_csv
        )
        
        # データ整合性チェック
        self.csv_handler.validate_data_consistency()
        
        print("=== CSVデータ読み込み完了 ===\n")
    
    def aggregate_preferences(self, w_subjective: float = 1.0, w_objective: float = 1.0):
        """
        拡張版Kemenyルールを使用して選好を統合
        
        Args:
            w_subjective: 主観的選好の重み
            w_objective: 客観的フィット度の重み
        """
        print("=== 拡張版Kemenyルールによる選好統合 ===")
        
        self.integrated_preferences = {
            'care_receivers': {},
            'care_workers': {}
        }
        
        # 重みを設定してKemenyルールインスタンスを再作成
        self.kemeny_rule = ExtendedKemenyRule(w_subjective, w_objective)
        
        # 被介護者の選好統合
        print("\n被介護者の選好統合中...")
        for receiver_id, data in self.care_receivers_data.items():
            candidates = list(data['subjective_preferences'].keys())
            subjective_prefs = data['subjective_preferences']
            objective_fitness = data['objective_fitness']
            
            integrated_ranking = self.kemeny_rule.aggregate_preferences(
                candidates, subjective_prefs, objective_fitness
            )
            
            # タプルの場合、ランキングリストのみを取得
            if isinstance(integrated_ranking, tuple):
                self.integrated_preferences['care_receivers'][receiver_id] = integrated_ranking[0]
            else:
                self.integrated_preferences['care_receivers'][receiver_id] = integrated_ranking
        
        # ケアワーカーの選好統合
        print("\nケアワーカーの選好統合中...")
        for worker_id, data in self.care_workers_data.items():
            candidates = list(data['subjective_preferences'].keys())
            subjective_prefs = data['subjective_preferences']
            objective_fitness = data['objective_fitness']
            
            integrated_ranking = self.kemeny_rule.aggregate_preferences(
                candidates, subjective_prefs, objective_fitness
            )
            
            # タプルの場合、ランキングリストのみを取得
            if isinstance(integrated_ranking, tuple):
                self.integrated_preferences['care_workers'][worker_id] = integrated_ranking[0]
            else:
                self.integrated_preferences['care_workers'][worker_id] = integrated_ranking
        
        print("\n統合結果:")
        print("被介護者の統合選好:")
        for receiver_id, ranking in self.integrated_preferences['care_receivers'].items():
            print(f"  被介護者{receiver_id}: {ranking}")
        
        print("ケアワーカーの統合選好:")
        for worker_id, ranking in self.integrated_preferences['care_workers'].items():
            print(f"  ケアワーカー{worker_id}: {ranking}")
    
    def run_matching(self):
        """
        DAアルゴリズムを使用してマッチングを実行
        """
        print("\n=== DAアルゴリズムによるマッチング ===")
        
        # 容量情報の準備
        capacities = {}
        for worker_id, data in self.care_workers_data.items():
            capacities[worker_id] = data['capacity']
        
        # DAアルゴリズム実行
        care_recipients = list(self.care_receivers_data.keys())
        caregivers = list(self.care_workers_data.keys())
        
        matching, detailed_result = self.da_algorithm.create_match(
            care_recipients,
            caregivers,
            self.integrated_preferences['care_receivers'],
            self.integrated_preferences['care_workers'],
            capacities
        )
        
        # 結果を統一形式に変換
        self.matching_result = {
            'matching': matching,
            'unmatched_care_receivers': [r for r in care_recipients if r not in matching],
            'care_worker_usage': {w: sum(1 for m in matching.values() if m == w) for w in caregivers}
        }
        
        return self.matching_result
    
    def analyze_results(self):
        """
        マッチング結果の詳細分析
        """
        print("\n=== マッチング結果分析 ===")
        
        # 基本統計
        matched_receivers = len(self.matching_result['matching'])
        total_receivers = len(self.care_receivers_data)
        unmatched_receivers = len(self.matching_result['unmatched_care_receivers'])
        
        print(f"マッチング統計:")
        print(f"  総被介護者数: {total_receivers}")
        print(f"  マッチ成功: {matched_receivers}")
        print(f"  未マッチ: {unmatched_receivers}")
        print(f"  マッチング率: {matched_receivers/total_receivers*100:.1f}%")
        
        # 安定性チェック
        capacities = {worker_id: data['capacity'] for worker_id, data in self.care_workers_data.items()}
        is_stable = self.da_algorithm.is_stable_matching(
            self.matching_result['matching'],
            self.integrated_preferences['care_receivers'],
            self.integrated_preferences['care_workers'],
            capacities
        )
        print(f"  安定性: {'安定' if is_stable else '不安定'}")
        
        # 満足度分析
        self._calculate_satisfaction()
        
        # ケアワーカー利用率
        print(f"ケアワーカー利用率:")
        for worker_id, usage in self.matching_result['care_worker_usage'].items():
            capacity = self.care_workers_data[worker_id]['capacity']
            utilization = usage / capacity * 100
            print(f"  ケアワーカー{worker_id}: {usage}/{capacity} ({utilization:.1f}%)")
    
    def _calculate_satisfaction(self):
        """満足度計算"""
        print("\n満足度分析:")
        
        # 被介護者の満足度
        receiver_satisfactions = []
        for receiver_id, worker_id in self.matching_result['matching'].items():
            ranking = self.integrated_preferences['care_receivers'][receiver_id]
            rank = ranking.index(worker_id) + 1
            satisfaction = 1.0 / rank
            receiver_satisfactions.append(satisfaction)
            print(f"  被介護者{receiver_id}: 第{rank}希望マッチ (満足度: {satisfaction:.2f})")
        
        if receiver_satisfactions:
            avg_receiver_satisfaction = sum(receiver_satisfactions) / len(receiver_satisfactions)
            print(f"被介護者平均満足度: {avg_receiver_satisfaction:.3f}")
        
        # ケアワーカーの満足度
        worker_satisfactions = []
        for worker_id in self.care_workers_data.keys():
            matched_receivers = [r for r, w in self.matching_result['matching'].items() if w == worker_id]
            if matched_receivers:
                worker_ranking = self.integrated_preferences['care_workers'][worker_id]
                individual_satisfactions = []
                for receiver_id in matched_receivers:
                    rank = worker_ranking.index(receiver_id) + 1
                    satisfaction = 1.0 / rank
                    individual_satisfactions.append(satisfaction)
                
                avg_satisfaction = sum(individual_satisfactions) / len(individual_satisfactions)
                worker_satisfactions.append(avg_satisfaction)
                print(f"  ケアワーカー{worker_id}: 平均満足度 {avg_satisfaction:.2f}")
        
        if worker_satisfactions:
            avg_worker_satisfaction = sum(worker_satisfactions) / len(worker_satisfactions)
            print(f"ケアワーカー平均満足度: {avg_worker_satisfaction:.3f}")
    
    def save_results(self, filename: str = "csv_matching_results.json"):
        """
        結果をJSONファイルに保存
        """
        results = {
            'input_data': {
                'care_receivers': self.care_receivers_data,
                'care_workers': self.care_workers_data
            },
            'integrated_preferences': self.integrated_preferences,
            'matching_result': self.matching_result,
            'metadata': {
                'total_care_receivers': len(self.care_receivers_data),
                'total_care_workers': len(self.care_workers_data),
                'matched_pairs': len(self.matching_result['matching']),
                'unmatched_receivers': len(self.matching_result['unmatched_care_receivers'])
            }
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print(f"\n結果を {filename} に保存しました")
    
    def run_complete_matching_from_csv(self,
                                     receiver_subjective_csv: str,
                                     receiver_objective_csv: str,
                                     worker_subjective_csv: str,
                                     worker_objective_csv: str,
                                     worker_capacity_csv: Optional[str] = None,
                                     w_subjective: float = 1.0,
                                     w_objective: float = 1.0):
        """
        CSVからの完全なマッチング処理
        """
        print("=== CSV対応ケアワーカー・被介護者マッチングシステム ===")
        
        # データ読み込み
        self.load_data_from_csv(
            receiver_subjective_csv, receiver_objective_csv,
            worker_subjective_csv, worker_objective_csv,
            worker_capacity_csv
        )
        
        # 選好統合
        self.aggregate_preferences(w_subjective, w_objective)
        
        # マッチング実行
        self.run_matching()
        
        # 結果分析
        self.analyze_results()
        
        # 結果保存
        self.save_results()
        
        return self.matching_result

def demo_csv_matching():
    """CSV入力対応マッチングシステムのデモ"""
    print("=== CSV入力対応マッチングシステム デモ ===")
    
    # サンプルCSVファイルの作成
    csv_handler = CSVInputHandler()
    csv_handler.create_sample_csv_files()
    
    print("\n" + "="*60)
    
    # マッチングシステムの実行
    system = CSVMatchingSystem()
    
    result = system.run_complete_matching_from_csv(
        "care_receiver_subjective_preferences.csv",
        "care_receiver_objective_fitness.csv",
        "care_worker_subjective_preferences.csv",
        "care_worker_objective_fitness.csv",
        "care_worker_capacity.csv"
    )
    
    print("\n=== デモ完了 ===")
    return result

if __name__ == "__main__":
    demo_csv_matching()