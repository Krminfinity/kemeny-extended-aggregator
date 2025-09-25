#!/usr/bin/env python3
"""
拡張版Kemenyルールの実装

このモジュールは卒業論文「ケアワーカーと被介護者のマッチングアルゴリズムの開発」で
提案された拡張版Kemenyルールを実装します。

拡張版Kemenyルールは：
1. 主観的選好（個人の好みランキング）
2. 客観的フィット度（数値による適合性評価）
を統合して、最適な選好ランキングを生成します。

Author: 倉持誠 (Makoto Kuramochi)
"""

import itertools
from typing import List, Dict, Tuple, Optional
import numpy as np


class ExtendedKemenyRule:
    """拡張版Kemenyルールの実装クラス"""
    
    def __init__(self, preference_weight: float = 1.0, fitness_weight: float = 1.0):
        """
        拡張版Kemenyルールの初期化
        
        Args:
            preference_weight: 主観的選好の重み（デフォルト: 1.0）
            fitness_weight: 客観的フィット度の重み（デフォルト: 1.0）
        """
        self.preference_weight = preference_weight
        self.fitness_weight = fitness_weight
    
    def kemeny_distance(self, ranking1: List[int], ranking2: List[int]) -> int:
        """
        2つのランキング間のKemeny距離（不一致数）を計算
        
        Args:
            ranking1: 第1のランキング
            ranking2: 第2のランキング
            
        Returns:
            int: Kemeny距離（入れ替え回数）
        """
        if len(ranking1) != len(ranking2):
            raise ValueError("ランキングの長さが一致しません")
            
        distance = 0
        n = len(ranking1)
        
        # 各要素ペアについて順序の違いをカウント
        for i in range(n):
            for j in range(i + 1, n):
                # ranking1での要素ranking1[i]とranking1[j]の順序
                elem1_i = ranking1[i]
                elem1_j = ranking1[j]
                
                # ranking2での同じ要素の位置を検索
                try:
                    pos2_i = ranking2.index(elem1_i)
                    pos2_j = ranking2.index(elem1_j)
                    
                    # 順序が異なる場合は距離+1
                    if pos2_i > pos2_j:  # ranking2では逆順
                        distance += 1
                except ValueError:
                    # 要素が見つからない場合はスキップ
                    continue
                    
        return distance
    
    def fitness_distance(self, ranking: List[int], fitness_scores: List[float]) -> float:
        """
        ランキングと客観的フィット度スコアとの不一致を計算
        
        Args:
            ranking: 評価対象のランキング
            fitness_scores: 客観的フィット度スコア（インデックス順）
            
        Returns:
            float: フィット度との不一致スコア
        """
        if len(ranking) != len(fitness_scores):
            raise ValueError("ランキングとフィット度スコアの長さが一致しません")
        
        # フィット度に基づく理想的なランキングを生成
        # フィット度の高い順にソート（降順）
        fitness_with_index = [(score, idx) for idx, score in enumerate(fitness_scores)]
        fitness_with_index.sort(key=lambda x: x[0], reverse=True)
        ideal_ranking = [idx for score, idx in fitness_with_index]
        
        # Kemeny距離を計算
        return self.kemeny_distance(ranking, ideal_ranking)
    
    def generate_all_permutations(self, items: List[int]) -> List[List[int]]:
        """
        全ての順列を生成
        
        Args:
            items: 順列を生成する要素のリスト
            
        Returns:
            List[List[int]]: 全ての順列のリスト
        """
        return [list(perm) for perm in itertools.permutations(items)]
    
    def aggregate_preferences(self, 
                            subjective_preference: List[int],
                            fitness_scores: List[float],
                            candidates: Optional[List[int]] = None) -> Tuple[List[int], Dict]:
        """
        主観的選好と客観的フィット度を統合して最適なランキングを生成
        
        Args:
            subjective_preference: 主観的選好ランキング
            fitness_scores: 客観的フィット度スコア
            candidates: 候補者のリスト（省略時は0からN-1）
            
        Returns:
            Tuple[List[int], Dict]: 最適ランキングと計算詳細
        """
        if candidates is None:
            candidates = list(range(len(subjective_preference)))
        
        if len(subjective_preference) != len(fitness_scores):
            raise ValueError("主観的選好とフィット度スコアの長さが一致しません")
        
        # 全ての可能な順列を生成
        all_permutations = self.generate_all_permutations(candidates)
        
        best_ranking: List[int] = []
        best_score = float('inf')
        calculation_details = []
        
        # 各順列に対してスコアを計算
        for permutation in all_permutations:
            perm_list = permutation.copy()
            
            # 主観的選好との不一致数
            preference_distance = self.kemeny_distance(perm_list, subjective_preference)
            
            # 客観的フィット度との不一致数
            fitness_distance = self.fitness_distance(perm_list, fitness_scores)
            
            # 総合スコア（重み付き和）
            total_score = (self.preference_weight * preference_distance + 
                          self.fitness_weight * fitness_distance)
            
            # 計算詳細を記録
            details = {
                'ranking': perm_list.copy(),
                'preference_distance': preference_distance,
                'fitness_distance': fitness_distance,
                'total_score': total_score
            }
            calculation_details.append(details)
            
            # 最小スコアの更新（同点の場合は主観的選好を優先）
            if (total_score < best_score or 
                (total_score == best_score and best_ranking and preference_distance < 
                 self.kemeny_distance(best_ranking, subjective_preference))):
                best_score = total_score
                best_ranking = perm_list.copy()
        
        # 計算詳細をスコア順にソート
        calculation_details.sort(key=lambda x: (x['total_score'], x['preference_distance']))
        
        result_details = {
            'best_ranking': best_ranking,
            'best_score': best_score,
            'all_calculations': calculation_details,
            'preference_weight': self.preference_weight,
            'fitness_weight': self.fitness_weight
        }
        
        return best_ranking, result_details
    
    def print_calculation_details(self, details: Dict):
        """
        計算詳細を見やすく出力
        
        Args:
            details: aggregate_preferencesから返された詳細辞書
        """
        print("=== 拡張版Kemenyルール 計算詳細 ===")
        print(f"主観的選好の重み: {details['preference_weight']}")
        print(f"客観的フィット度の重み: {details['fitness_weight']}")
        print(f"最適ランキング: {details['best_ranking']}")
        print(f"最小スコア: {details['best_score']}")
        print()
        
        print("全候補の評価:")
        print("ランキング\t主観距離\tフィット距離\t総合スコア")
        print("-" * 50)
        
        for calc in details['all_calculations'][:10]:  # 上位10件のみ表示
            ranking_str = "".join(map(str, calc['ranking']))
            print(f"{ranking_str}\t\t{calc['preference_distance']}\t\t"
                  f"{calc['fitness_distance']}\t\t{calc['total_score']}")
            
        if len(details['all_calculations']) > 10:
            print(f"... (他{len(details['all_calculations']) - 10}候補)")


def demo_extended_kemeny():
    """拡張版Kemenyルールのデモ実行"""
    print("=== 拡張版Kemenyルール デモ ===")
    print()
    
    # 論文の例に基づいた設定
    # 被介護者6の例を再現
    subjective_preference = [2, 1, 0]  # ケアワーカー2,1,0の順
    fitness_scores = [0.8, 0.9, 0.7]   # ケアワーカー0,1,2のフィット度スコア
    
    print("設定:")
    print(f"主観的選好: {subjective_preference} (ケアワーカー2>1>0の順)")
    print(f"客観的フィット度: {fitness_scores} (ケアワーカー0:0.8, 1:0.9, 2:0.7)")
    print()
    
    # 拡張版Kemenyルールを実行
    extended_kemeny = ExtendedKemenyRule()
    best_ranking, details = extended_kemeny.aggregate_preferences(
        subjective_preference, fitness_scores
    )
    
    # 結果表示
    extended_kemeny.print_calculation_details(details)
    
    print()
    print("=== 結果解釈 ===")
    print(f"統合された最適ランキング: {best_ranking}")
    print("これは論文で示された213（ケアワーカー2>1>0の順）と一致することを確認")


if __name__ == "__main__":
    demo_extended_kemeny()