#!/usr/bin/env python3
"""
拡張版Kemenyルールのブラックボックステスト用サンプルデータ

このモジュールは拡張版Kemenyルールの動作を検証するための
様々なテストケースとサンプルデータを提供します。

Author: 倉持誠 (Makoto Kuramochi)
"""

import sys
import os
from typing import Dict, List, Tuple, Any
import json

# 親ディレクトリのalgorithmsフォルダをパスに追加
algorithms_path = os.path.join(os.path.dirname(__file__), '..', 'algorithms')
sys.path.insert(0, algorithms_path)

from extended_kemeny_rule import ExtendedKemenyRule


class ExtendedKemenyTestData:
    """拡張版Kemenyルールのテストデータクラス"""
    
    def __init__(self):
        """テストデータの初期化"""
        self.test_cases = self._create_test_cases()
    
    def _create_test_cases(self) -> Dict[str, Dict[str, Any]]:
        """
        テストケースを作成
        
        Returns:
            Dict[str, Dict[str, Any]]: テストケース辞書
        """
        return {
            # ケース1: 基本的なケース（3つの候補者）
            "basic_3_candidates": {
                "description": "3つの候補者での基本的なケース",
                "subjective_preference": [2, 1, 0],  # 候補者2>1>0の順
                "fitness_scores": [0.8, 0.9, 0.7],   # 候補者0:0.8, 1:0.9, 2:0.7
                "preference_weight": 1.0,
                "fitness_weight": 1.0,
                "expected_result": [2, 1, 0],  # 期待される結果
                "expected_score": 2.0
            },
            
            # ケース2: 主観的選好と客観的フィット度が完全に一致
            "perfect_alignment": {
                "description": "主観的選好と客観的フィット度が完全に一致する場合",
                "subjective_preference": [0, 1, 2],
                "fitness_scores": [0.9, 0.7, 0.5],   # 0>1>2の順でフィット度も一致
                "preference_weight": 1.0,
                "fitness_weight": 1.0,
                "expected_result": [0, 1, 2],
                "expected_score": 0.0
            },
            
            # ケース3: 主観的選好と客観的フィット度が完全に逆
            "complete_disagreement": {
                "description": "主観的選好と客観的フィット度が完全に逆の場合",
                "subjective_preference": [0, 1, 2],
                "fitness_scores": [0.3, 0.5, 0.9],   # 2>1>0の順でフィット度は逆
                "preference_weight": 1.0,
                "fitness_weight": 1.0,
                "expected_result": [0, 1, 2],  # 主観的選好が優先される（同点の場合）
                "expected_score": 3.0
            },
            
            # ケース4: 主観的選好を重視（重み2倍）
            "preference_weighted": {
                "description": "主観的選好を重視する場合（重み2倍）",
                "subjective_preference": [0, 1, 2],
                "fitness_scores": [0.3, 0.5, 0.9],
                "preference_weight": 2.0,
                "fitness_weight": 1.0,
                "expected_result": [0, 1, 2],  # 主観的選好に近づく
                "expected_score": 3.0
            },
            
            # ケース5: 客観的フィット度を重視（重み2倍）
            "fitness_weighted": {
                "description": "客観的フィット度を重視する場合（重み2倍）",
                "subjective_preference": [0, 1, 2],
                "fitness_scores": [0.3, 0.5, 0.9],
                "preference_weight": 1.0,
                "fitness_weight": 2.0,
                "expected_result": [2, 1, 0],  # フィット度順に近づく
                "expected_score": 3.0
            },
            
            # ケース6: 4つの候補者の場合
            "four_candidates": {
                "description": "4つの候補者でのより複雑なケース",
                "subjective_preference": [3, 2, 1, 0],
                "fitness_scores": [0.9, 0.8, 0.6, 0.7],  # 0>1>3>2の順
                "preference_weight": 1.0,
                "fitness_weight": 1.0,
                "expected_result": [3, 2, 1, 0],  # 実際の最適解
                "expected_score": 5.0
            },
            
            # ケース7: 同点のフィット度スコア
            "tied_fitness_scores": {
                "description": "同点のフィット度スコアがある場合",
                "subjective_preference": [0, 1, 2],
                "fitness_scores": [0.8, 0.8, 0.6],  # 0と1が同点
                "preference_weight": 1.0,
                "fitness_weight": 1.0,
                "expected_result": [0, 1, 2],  # 主観的選好が優先される
                "expected_score": 1.0
            },
            
            # ケース8: 極端なフィット度の差
            "extreme_fitness_difference": {
                "description": "極端なフィット度の差がある場合",
                "subjective_preference": [0, 1, 2],
                "fitness_scores": [0.1, 0.2, 0.9],  # 2が圧倒的に高い
                "preference_weight": 1.0,
                "fitness_weight": 1.0,
                "expected_result": [0, 1, 2],  # 同点の場合は主観的選好が優先
                "expected_score": 3.0
            },
            
            # ケース11: フィット度が結果を変えるケース
            "fitness_overrides_preference": {
                "description": "フィット度が主観的選好を上回って結果を変えるケース",
                "subjective_preference": [0, 1, 2, 3],  # 0>1>2>3の順
                "fitness_scores": [0.1, 0.2, 0.3, 0.9],  # 3が圧倒的に高い（3>2>1>0の順）
                "preference_weight": 1.0,
                "fitness_weight": 2.0,  # フィット度重み2倍
                "expected_result": [3, 2, 1, 0],  # フィット度順に近づく
                "expected_score": 8.0
            },
            
            # ケース12: 微妙なバランスケース
            "subtle_balance_case": {
                "description": "主観的選好とフィット度の微妙なバランスケース",
                "subjective_preference": [0, 1, 2],
                "fitness_scores": [0.3, 0.7, 0.4],  # 1が最高、次に2、最後に0
                "preference_weight": 1.0,
                "fitness_weight": 1.5,  # フィット度を少し重視
                "expected_result": [1, 2, 0],  # フィット度の影響で順序が変わる
                "expected_score": 2.5
            },
            
            # ケース13: 強いフィット度コントラストケース
            "strong_fitness_contrast": {
                "description": "非常に強いフィット度コントラストがあるケース",
                "subjective_preference": [0, 1, 2, 3],
                "fitness_scores": [0.05, 0.1, 0.15, 0.95],  # 3が圧倒的
                "preference_weight": 1.0,
                "fitness_weight": 3.0,  # フィット度重み3倍
                "expected_result": [3, 2, 1, 0],  # フィット度の強い影響
                "expected_score": 6.0
            },
            
            # ケース9: 重みが0の場合（主観的選好のみ）
            "preference_only": {
                "description": "主観的選好のみを考慮（フィット度重み=0）",
                "subjective_preference": [0, 1, 2],
                "fitness_scores": [0.3, 0.5, 0.9],
                "preference_weight": 1.0,
                "fitness_weight": 0.0,
                "expected_result": [0, 1, 2],
                "expected_score": 0.0
            },
            
            # ケース10: 重みが0の場合（客観的フィット度のみ）
            "fitness_only": {
                "description": "客観的フィット度のみを考慮（選好重み=0）",
                "subjective_preference": [0, 1, 2],
                "fitness_scores": [0.3, 0.5, 0.9],
                "preference_weight": 0.0,
                "fitness_weight": 1.0,
                "expected_result": [2, 1, 0],
                "expected_score": 0.0
            },

            # 追加: フィット度差分(gap)モード境界テスト（重み付け=1.0同士）
            "boundary_gap_small_diff": {
                "description": "gapモード: 差分が小さいため主観的選好が維持される (0.51 vs 0.50)",
                "subjective_preference": [0, 1, 2],  # 0>1>2
                "fitness_scores": [0.51, 0.50, 0.10],  # 0と1の差が僅少
                "preference_weight": 1.0,
                "fitness_weight": 1.0,
                "fitness_mode": "gap",
                # 差が極小のため主観的順を維持すると期待
                "expected_result": [0, 1, 2],
                "expected_score": None  # gap距離は実数になるので検証対象外
            },
            "boundary_gap_medium_diff": {
                "description": "gapモード: 中程度差分 (0.60 vs 0.40, 差=0.20) では単一ペア逆転コスト(=1)を上回らないため主観的順保持",
                "subjective_preference": [0, 1, 2],  # 0>1>2
                "fitness_scores": [0.40, 0.60, 0.10],  # 1が0より0.20高い
                "preference_weight": 1.0,
                "fitness_weight": 1.0,
                "fitness_mode": "gap",
                # 差分0.20 < 逆転による主観距離(=1) のため逆転は起きない
                "expected_result": [0, 1, 2],
                "expected_score": None
            },
            "boundary_gap_large_diff": {
                "description": "gapモード: 大きな差分 (0.80 vs 0.30, 差=0.50) でも 0.50 < 1 のためまだ逆転せず",
                "subjective_preference": [0, 1, 2],
                "fitness_scores": [0.30, 0.80, 0.10],
                "preference_weight": 1.0,
                "fitness_weight": 1.0,
                "fitness_mode": "gap",
                # 逆転には差分 > 1 (重み比1:1の閾値) が必要だがスコア範囲[0,1]では単一ペアでは到達不可
                "expected_result": [0, 1, 2],
                "expected_score": None
            },
            "boundary_gap_tie_vs_third": {
                "description": "gapモード: 上位2名接近(0.50 vs 0.49) + 最下位(0.05) 大差でも主観 2>0>1 を覆うには逆転3ペア総和>主観距離必要",
                "subjective_preference": [2, 0, 1],  # 2>0>1
                "fitness_scores": [0.49, 0.50, 0.05],  # 0と1接近 / 2が最下位
                "preference_weight": 1.0,
                "fitness_weight": 1.0,
                "fitness_mode": "gap",
                # 累積ペナルティ0.90 < 逆転に必要な主観距離(>=2) のため主観順維持
                "expected_result": [2, 0, 1],
                "expected_score": None
            },
            "boundary_gap_three_way": {
                "description": "gapモード: 漸次差 (0.70,0.50,0.30) 逆向きでも累積ペナルティ0.80 < 主観距離(3) で逆転せず (閾値示唆)",
                "subjective_preference": [2, 1, 0],  # 2>1>0
                "fitness_scores": [0.70, 0.50, 0.30],  # 0>1>2 (完全逆 + 均等差)
                "preference_weight": 1.0,
                "fitness_weight": 1.0,
                "fitness_mode": "gap",
                # 逆転には累積差分 > 3 が必要だがスコア範囲では到達不可
                "expected_result": [2, 1, 0],
                "expected_score": None
            }
        }
    
    def run_test_case(self, test_name: str) -> Dict[str, Any]:
        """
        指定されたテストケースを実行
        
        Args:
            test_name: テストケース名
            
        Returns:
            Dict[str, Any]: テスト結果
        """
        if test_name not in self.test_cases:
            raise ValueError(f"テストケース '{test_name}' が見つかりません")
        
        test_case = self.test_cases[test_name]
        
        # ExtendedKemenyRuleインスタンスを作成
        # fitness_mode は後方互換のためオプション扱い
        fitness_mode = test_case.get("fitness_mode", "ordinal")
        extended_kemeny = ExtendedKemenyRule(
            preference_weight=test_case["preference_weight"],
            fitness_weight=test_case["fitness_weight"],
            fitness_mode=fitness_mode
        )
        
        # テスト実行
        result_ranking, details = extended_kemeny.aggregate_preferences(
            test_case["subjective_preference"],
            test_case["fitness_scores"]
        )
        
        # 結果をまとめる
        test_result = {
            "test_name": test_name,
            "description": test_case["description"],
            "input": {
                "subjective_preference": test_case["subjective_preference"],
                "fitness_scores": test_case["fitness_scores"],
                "preference_weight": test_case["preference_weight"],
                "fitness_weight": test_case["fitness_weight"]
            },
            "expected": {
                "ranking": test_case["expected_result"],
                "score": test_case["expected_score"]
            },
            "actual": {
                "ranking": result_ranking,
                "score": details["best_score"]
            },
            "passed": result_ranking == test_case["expected_result"],
            "details": details
        }
        
        return test_result
    
    def run_all_tests(self) -> Dict[str, Any]:
        """
        全てのテストケースを実行
        
        Returns:
            Dict[str, Any]: 全テスト結果のサマリー
        """
        results = []
        passed_count = 0
        
        print("=== 拡張版Kemenyルール ブラックボックステスト実行 ===\n")
        
        for test_name in self.test_cases.keys():
            print(f"テスト実行中: {test_name}")
            result = self.run_test_case(test_name)
            results.append(result)
            
            if result["passed"]:
                passed_count += 1
                print(f"✓ PASS: {result['description']}")
            else:
                print(f"✗ FAIL: {result['description']}")
                print(f"  期待値: {result['expected']['ranking']}")
                print(f"  実際値: {result['actual']['ranking']}")
            print()
        
        # サマリー
        total_tests = len(self.test_cases)
        summary = {
            "total_tests": total_tests,
            "passed_tests": passed_count,
            "failed_tests": total_tests - passed_count,
            "pass_rate": passed_count / total_tests * 100,
            "results": results
        }
        
        print("=== テスト結果サマリー ===")
        print(f"実行テスト数: {summary['total_tests']}")
        print(f"成功: {summary['passed_tests']}")
        print(f"失敗: {summary['failed_tests']}")
        print(f"成功率: {summary['pass_rate']:.1f}%")
        
        return summary
    
    def save_test_results(self, results: Dict[str, Any], filename: str = "extended_kemeny_test_results.json"):
        """
        テスト結果をJSONファイルに保存
        
        Args:
            results: テスト結果辞書
            filename: 保存ファイル名
        """
        # NumPy配列がある場合はリストに変換
        def convert_numpy(obj):
            if hasattr(obj, 'tolist'):
                return obj.tolist()
            return obj
        
        # 詳細な計算結果は除外して保存（サイズ削減のため）
        simplified_results = {
            "total_tests": results["total_tests"],
            "passed_tests": results["passed_tests"],
            "failed_tests": results["failed_tests"],
            "pass_rate": results["pass_rate"],
            "test_summary": []
        }
        
        for result in results["results"]:
            simplified_result = {
                "test_name": result["test_name"],
                "description": result["description"],
                "input": result["input"],
                "expected": result["expected"],
                "actual": result["actual"],
                "passed": result["passed"]
            }
            simplified_results["test_summary"].append(simplified_result)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(simplified_results, f, ensure_ascii=False, indent=2, default=convert_numpy)
        
        print(f"テスト結果を {filename} に保存しました")
    
    def get_test_case_names(self) -> List[str]:
        """
        利用可能なテストケース名の一覧を取得
        
        Returns:
            List[str]: テストケース名のリスト
        """
        return list(self.test_cases.keys())
    
    def print_test_case_info(self, test_name: str):
        """
        指定されたテストケースの詳細情報を表示
        
        Args:
            test_name: テストケース名
        """
        if test_name not in self.test_cases:
            print(f"テストケース '{test_name}' が見つかりません")
            return
        
        test_case = self.test_cases[test_name]
        print(f"=== テストケース: {test_name} ===")
        print(f"説明: {test_case['description']}")
        print(f"主観的選好: {test_case['subjective_preference']}")
        print(f"客観的フィット度: {test_case['fitness_scores']}")
        print(f"選好重み: {test_case['preference_weight']}")
        print(f"フィット度重み: {test_case['fitness_weight']}")
        print(f"期待される結果: {test_case['expected_result']}")
        print(f"期待されるスコア: {test_case['expected_score']}")


def main():
    """メイン実行関数"""
    test_data = ExtendedKemenyTestData()
    
    # 利用可能なテストケースを表示
    print("利用可能なテストケース:")
    for i, test_name in enumerate(test_data.get_test_case_names(), 1):
        print(f"{i}. {test_name}")
    print()
    
    # 全テストを実行
    results = test_data.run_all_tests()
    
    # 結果をファイルに保存
    test_data.save_test_results(results)
    
    # 失敗したテストがあれば詳細を表示
    failed_tests = [r for r in results["results"] if not r["passed"]]
    if failed_tests:
        print("\n=== 失敗したテストの詳細 ===")
        for failed_test in failed_tests:
            print(f"\nテスト: {failed_test['test_name']}")
            print(f"説明: {failed_test['description']}")
            print(f"入力: {failed_test['input']}")
            print(f"期待値: {failed_test['expected']}")
            print(f"実際値: {failed_test['actual']}")


if __name__ == "__main__":
    main()