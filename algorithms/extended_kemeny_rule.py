#!/usr/bin/env python3
"""
拡張版Kemenyルールの実装

このモジュールは卒業論文「ケアワーカーと被介護者のマッチングアルゴリズムの開発」で
提案された拡張版Kemenyルールを実装します。

拡張版Kemenyルールは：
1. 主観的選好（個人の好みランキング）
2. 客観的フィット度（数値による適合性評価）
を統合して、最適な選好ランキングを生成します。

【2025年9月更新】厳格な制約条件を実装:
- フィット度は整数のみ
- フィット度は単射（重複なし）
- 人数制限の実装

Author: 倉持誠 (Makoto Kuramochi)
"""

import itertools
from typing import List, Dict, Tuple, Optional, Sequence, Union
import numpy as np
from validation import InputValidator, ConstraintViolationError


class ExtendedKemenyRule:
    """拡張版Kemenyルールの実装クラス

    既存実装はフィット度スコアを順位化してKemeny距離を計算していたため、
    「差の大きさ」が結果に反映されず、境界値テスト（どの差から主観選好を覆すか）
    を行えない課題があった。本修正では差の大きさをペナルティに反映する
    gap（差分）モードを追加し、論文で明示的な重み付けがない場合にも
    自然な形で主観選好 vs 客観的差分のトレードオフを観察できるようにする。
    """
    
    def __init__(self,
                 preference_weight: float = 1.0,
                 fitness_weight: float = 1.0,
                 fitness_mode: str = "ordinal"):
        """
        拡張版Kemenyルールの初期化
        
        Args:
            preference_weight: 主観的選好の重み（既存互換維持）
            fitness_weight: 客観的フィット度の重み（既存互換維持）
            fitness_mode: フィット度距離の算出方法
                - "ordinal": これまで通りフィット度を順位化しKemeny距離
                - "gap": フィット度の差分大きさをペア逆転毎に加算
        """
        self.preference_weight = preference_weight
        self.fitness_weight = fitness_weight
        self.fitness_mode = fitness_mode  # 新規追加
        if self.fitness_mode not in ("ordinal", "gap"):
            raise ValueError("fitness_mode は 'ordinal' か 'gap' を指定してください")
    
    def kemeny_distance(self, ranking1: Sequence[int], ranking2: Sequence[int]) -> int:
        """Kemeny距離（= Kendall tau 距離: ペアの不一致数）を計算

        NOTE: 論文で用いられる Kemeny-Young 法では「多数の投票（選好プロファイル）」に対し
        集計ランキング σ を求める際に Σ_v dist_Kendall(σ, π_v) を最小化する。
        本実装の単一ランキング版はその特殊形 (m=1) であり、距離は Kendall tau 不一致ペア数。

        旧実装はペアごとに ranking2.index(...) を呼び O(n^3) になっていたため、
        位置マップを事前計算し O(n^2) に最適化。
        """
        if len(ranking1) != len(ranking2):
            raise ValueError("ランキングの長さが一致しません")

        # 要素→位置 の辞書を構築（O(n)）
        pos_map = {elem: i for i, elem in enumerate(ranking2)}

        distance = 0
        n = len(ranking1)
        for i in range(n):
            ai = ranking1[i]
            pi = pos_map.get(ai)
            if pi is None:
                # 想定外（完全な順列でない）
                continue
            for j in range(i + 1, n):
                aj = ranking1[j]
                pj = pos_map.get(aj)
                if pj is None:
                    continue
                # ranking1 では ai が aj より前。ranking2 で逆なら不一致
                if pi > pj:
                    distance += 1
        return distance

    def kemeny_distance_profile(self, ranking: Sequence[int], profile: Sequence[Sequence[int]]) -> int:
        """複数の主観的選好プロファイルに対する合計Kemeny距離を計算

        Kemeny-Young の目的関数: Σ_v KendallTau(ranking, π_v)
        プロファイルが1件の場合は単一距離に一致。
        """
        total = 0
        for pref in profile:
            total += self.kemeny_distance(ranking, pref)
        return total
    
    def fitness_distance(self, ranking: List[int], fitness_scores: List[int]) -> float:
        """フィット度距離を計算（モードにより2方式）

        ordinal: 既存方式（順位化→Kemeny距離）
        gap: フィット度差分を考慮。ランキング内の順序がフィット度の大小関係と
             逆転しているペア(a,b)について (fitness[b] - fitness[a]) を加算。
             （bの方が本来高いのに後ろに置かれている状況にはペナルティなし）
             こうすることで「差が大きい逆転ほどコストが高く、境界」が生まれる。
        """
        if len(ranking) != len(fitness_scores):
            raise ValueError("ランキングとフィット度スコアの長さが一致しません")

        if self.fitness_mode == "ordinal":
            # 従来ロジック（順位のみ使用）
            fitness_with_index = [(score, idx) for idx, score in enumerate(fitness_scores)]
            fitness_with_index.sort(key=lambda x: x[0], reverse=True)
            ideal_ranking = [idx for score, idx in fitness_with_index]
            return float(self.kemeny_distance(ranking, ideal_ranking))

        # gap モード
        score_lookup = {i: fitness_scores[i] for i in range(len(fitness_scores))}
        penalty = 0.0
        n = len(ranking)
        # ランキング内の順序 i<j で ranking[i] を上位とする
        for i in range(n):
            a = ranking[i]
            for j in range(i + 1, n):
                b = ranking[j]
                # もし a のフィット度 < b のフィット度 なのに a を上に置いたら差分をペナルティ
                diff = score_lookup[b] - score_lookup[a]
                if diff > 0:  # 逆転（本来 b の方が高い）
                    penalty += diff
        return penalty
    
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
                            subjective_preference: Union[List[int], List[List[int]]],
                            fitness_scores: Union[List[int], List[float]],
                            candidates: Optional[List[int]] = None) -> Tuple[List[int], Dict]:
        """
        主観的選好と客観的フィット度を統合して最適なランキングを生成
        
        【2025年9月更新】厳格な制約条件を実装:
        - フィット度は整数のみ（実数は拒否）
        - フィット度は単射性（重複なし）
        
        Args:
            subjective_preference: 主観的選好ランキング
            fitness_scores: 客観的フィット度スコア（整数のみ）
            candidates: 候補者のリスト（省略時は0からN-1）
            
        Returns:
            Tuple[List[int], Dict]: 最適ランキングと計算詳細
            
        Raises:
            ConstraintViolationError: 制約違反時
        """
        # 制約検証：フィット度の整数性
        InputValidator.validate_fitness_scores_are_integers(fitness_scores)
        
        # 制約検証：フィット度の単射性
        InputValidator.validate_fitness_uniqueness(fitness_scores, "入力フィット度")
        
        # 整数リストに変換（検証済みなので安全）
        validated_fitness_scores: List[int] = [int(score) for score in fitness_scores]
        # プロファイル（複数選好）の場合と単一選好を自動判別
        is_profile = False
        if isinstance(subjective_preference, list) and subjective_preference and isinstance(subjective_preference[0], list):
            # List[List[int]] とみなす
            is_profile = True
            pref_profile: List[List[int]] = subjective_preference  # type: ignore
            n_candidates = len(pref_profile[0])
            # 各ランキング長さ一致チェック
            for pref in pref_profile:
                if len(pref) != n_candidates:
                    raise ValueError("プロファイル内のランキング長さが不一致です")
        else:
            pref_profile = []
            n_candidates = len(subjective_preference)  # type: ignore

        if candidates is None:
            candidates = list(range(n_candidates))

        if n_candidates != len(validated_fitness_scores):
            raise ValueError("主観的選好(単一またはプロファイル)とフィット度スコアの長さが一致しません")
        
        # 全ての可能な順列を生成
        all_permutations = self.generate_all_permutations(candidates)
        
        best_ranking: List[int] = []
        best_score = float('inf')
        calculation_details = []
        
        # 各順列に対してスコアを計算
        for permutation in all_permutations:
            perm_list = permutation.copy()
            
            # 主観的選好との不一致数（プロファイルなら総和）
            if is_profile:
                preference_distance = self.kemeny_distance_profile(perm_list, pref_profile)
            else:
                preference_distance = self.kemeny_distance(perm_list, subjective_preference)  # type: ignore
            
            # 客観的フィット度との不一致（整数のみ）
            fitness_distance = self.fitness_distance(perm_list, validated_fitness_scores)
            
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
            if total_score < best_score:
                best_score = total_score
                best_ranking = perm_list.copy()
            elif total_score == best_score:
                # タイブレーク: プロファイル/単一いずれの場合も preference_distance が小さい方
                if best_ranking:
                    if is_profile:
                        current_pd = self.kemeny_distance_profile(best_ranking, pref_profile)
                    else:
                        current_pd = self.kemeny_distance(best_ranking, subjective_preference)  # type: ignore
                    if preference_distance < current_pd:
                        best_score = total_score
                        best_ranking = perm_list.copy()
                best_score = total_score
                best_ranking = perm_list.copy()
        
        # 計算詳細をスコア順にソート
        calculation_details.sort(key=lambda x: (x['total_score'], x['preference_distance']))
        
        result_details = {
            'best_ranking': best_ranking,
            'best_score': best_score,
            'all_calculations': calculation_details,
            'preference_weight': self.preference_weight,
            'fitness_weight': self.fitness_weight,
            'fitness_mode': self.fitness_mode,
            'preference_profile': pref_profile if is_profile else None
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
    
    # 論文の例に基づいた設定（制約に準拠：整数、単射）
    # 被介護者6の例を再現
    subjective_preference = [2, 1, 0]  # ケアワーカー2,1,0の順
    fitness_scores = [8, 9, 7]   # ケアワーカー0,1,2のフィット度スコア（整数、重複なし）
    
    print("設定:")
    print(f"主観的選好: {subjective_preference} (ケアワーカー2>1>0の順)")
    print(f"客観的フィット度: {fitness_scores} (ケアワーカー0:8, 1:9, 2:7)")
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