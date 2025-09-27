#!/usr/bin/env python3
"""
Deferred Acceptance (DA) アルゴリズムのブラックボックステスト用サンプルデータ

このモジュールはDAアルゴリズムの動作を検証するための
様々なテストケースとサンプルデータを提供します。

Author: 倉持誠 (Makoto Kuramochi)
"""

from deferred_acceptance import DeferredAcceptanceAlgorithm
from typing import Dict, List, Tuple, Any
import json


class DATestData:
    """DAアルゴリズムのテストデータクラス"""
    
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
            # ケース1: 基本的なケース（論文の例）
            "basic_paper_example": {
                "description": "論文で使用された基本例",
                "care_recipients": [4, 5, 6, 7],
                "caregivers": [1, 2, 3],
                "recipient_preferences": {
                    4: [1, 3, 2],  # 被介護者4: ケアワーカー1>3>2
                    5: [2, 1, 3],  # 被介護者5: ケアワーカー2>1>3
                    6: [2, 1, 3],  # 被介護者6: ケアワーカー2>1>3
                    7: [3, 1, 2],  # 被介護者7: ケアワーカー3>1>2
                },
                "caregiver_preferences": {
                    1: [4, 7, 5, 6],  # ケアワーカー1: 被介護者4>7>5>6
                    2: [6, 5, 4, 7],  # ケアワーカー2: 被介護者6>5>4>7
                    3: [7, 4, 5, 6],  # ケアワーカー3: 被介護者7>4>5>6
                },
                "caregiver_capacities": {1: 1, 2: 1, 3: 2},
                "expected_matches": {4: 1, 6: 2, 7: 3},  # 実際の結果
                "expected_unmatched": [5],  # 被介護者5は未マッチ
                "is_stable": True
            },
            
            # ケース2: 完全にバランスの取れたケース
            "balanced_case": {
                "description": "被介護者数とケアワーカー総容量が一致するケース",
                "care_recipients": [1, 2, 3],
                "caregivers": [10, 20, 30],
                "recipient_preferences": {
                    1: [10, 20, 30],
                    2: [20, 10, 30],
                    3: [30, 20, 10],
                },
                "caregiver_preferences": {
                    10: [1, 2, 3],
                    20: [2, 1, 3],
                    30: [3, 1, 2],
                },
                "caregiver_capacities": {10: 1, 20: 1, 30: 1},
                "expected_matches": {1: 10, 2: 20, 3: 30},
                "expected_unmatched": [],
                "is_stable": True
            },
            
            # ケース3: 容量不足で未マッチが発生するケース
            "insufficient_capacity": {
                "description": "ケアワーカーの総容量が不足し未マッチが発生するケース",
                "care_recipients": [1, 2, 3, 4],
                "caregivers": [10, 20],
                "recipient_preferences": {
                    1: [10, 20],
                    2: [10, 20],
                    3: [20, 10],
                    4: [20, 10],
                },
                "caregiver_preferences": {
                    10: [1, 2, 3, 4],
                    20: [3, 4, 1, 2],
                },
                "caregiver_capacities": {10: 1, 20: 2},
                "expected_matches": {1: 10, 3: 20, 4: 20},
                "expected_unmatched": [2],
                "is_stable": True
            },
            
            # ケース4: 大容量ケアワーカーがいるケース
            "high_capacity_caregiver": {
                "description": "1人のケアワーカーが大容量を持つケース",
                "care_recipients": [1, 2, 3, 4],
                "caregivers": [10, 20],
                "recipient_preferences": {
                    1: [10, 20],
                    2: [10, 20],
                    3: [10, 20],
                    4: [20, 10],
                },
                "caregiver_preferences": {
                    10: [1, 2, 3, 4],
                    20: [4, 3, 2, 1],
                },
                "caregiver_capacities": {10: 3, 20: 1},
                "expected_matches": {1: 10, 2: 10, 3: 10, 4: 20},
                "expected_unmatched": [],
                "is_stable": True
            },
            
            # ケース5: 同じ選好を持つ被介護者がいるケース
            "identical_preferences": {
                "description": "同じ選好を持つ被介護者がいるケース",
                "care_recipients": [1, 2, 3],
                "caregivers": [10, 20],
                "recipient_preferences": {
                    1: [10, 20],  # 同じ選好
                    2: [10, 20],  # 同じ選好
                    3: [10, 20],  # 同じ選好
                },
                "caregiver_preferences": {
                    10: [1, 2, 3],  # ケアワーカー10は1>2>3の順で好む
                    20: [3, 2, 1],  # ケアワーカー20は3>2>1の順で好む
                },
                "caregiver_capacities": {10: 1, 20: 1},
                "expected_matches": {1: 10},  # 実際は1のみマッチ
                "expected_unmatched": [2, 3],  # 2と3は未マッチ
                "is_stable": True
            },
            
            # ケース6: 人気のないケアワーカーがいるケース
            "unpopular_caregiver": {
                "description": "誰からも最優先されないケアワーカーがいるケース",
                "care_recipients": [1, 2],
                "caregivers": [10, 20, 30],
                "recipient_preferences": {
                    1: [10, 20, 30],
                    2: [20, 10, 30],
                },
                "caregiver_preferences": {
                    10: [1, 2],
                    20: [2, 1],
                    30: [1, 2],
                },
                "caregiver_capacities": {10: 1, 20: 1, 30: 1},
                "expected_matches": {1: 10, 2: 20},
                "expected_unmatched": [],
                "is_stable": True
            },
            
            # ケース7: 循環的な選好があるケース
            "circular_preferences": {
                "description": "循環的な選好構造があるケース",
                "care_recipients": [1, 2, 3],
                "caregivers": [10, 20, 30],
                "recipient_preferences": {
                    1: [10, 20, 30],  # 1は10を最も好む
                    2: [20, 30, 10],  # 2は20を最も好む
                    3: [30, 10, 20],  # 3は30を最も好む
                },
                "caregiver_preferences": {
                    10: [2, 3, 1],  # 10は2を最も好む
                    20: [3, 1, 2],  # 20は3を最も好む
                    30: [1, 2, 3],  # 30は1を最も好む
                },
                "caregiver_capacities": {10: 1, 20: 1, 30: 1},
                "expected_matches": {1: 10, 2: 20, 3: 30},  # 実際の結果
                "expected_unmatched": [],
                "is_stable": True
            },
            
            # ケース8: 単一ケアワーカーケース
            "single_caregiver": {
                "description": "ケアワーカーが1人だけのケース",
                "care_recipients": [1, 2, 3],
                "caregivers": [10],
                "recipient_preferences": {
                    1: [10],
                    2: [10],
                    3: [10],
                },
                "caregiver_preferences": {
                    10: [2, 1, 3],
                },
                "caregiver_capacities": {10: 2},
                "expected_matches": {2: 10, 1: 10},
                "expected_unmatched": [3],
                "is_stable": True
            },
            
            # ケース9: 空の選好リストがあるケース
            "empty_preferences": {
                "description": "一部の参加者が空の選好リストを持つケース",
                "care_recipients": [1, 2],
                "caregivers": [10, 20],
                "recipient_preferences": {
                    1: [10, 20],
                    2: [],  # 空の選好リスト
                },
                "caregiver_preferences": {
                    10: [1, 2],
                    20: [1, 2],
                },
                "caregiver_capacities": {10: 1, 20: 1},
                "expected_matches": {1: 10},
                "expected_unmatched": [2],
                "is_stable": True
            },
            
            # ケース10: 大規模ケース
            "large_scale": {
                "description": "より大規模なケース（10人の被介護者、5人のケアワーカー）",
                "care_recipients": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                "caregivers": [101, 102, 103, 104, 105],
                "recipient_preferences": {
                    1: [101, 102, 103, 104, 105],
                    2: [102, 101, 103, 104, 105],
                    3: [103, 102, 101, 104, 105],
                    4: [104, 103, 102, 101, 105],
                    5: [105, 104, 103, 102, 101],
                    6: [101, 105, 104, 103, 102],
                    7: [102, 101, 105, 104, 103],
                    8: [103, 102, 101, 105, 104],
                    9: [104, 103, 102, 101, 105],
                    10: [105, 104, 103, 102, 101],
                },
                "caregiver_preferences": {
                    101: [1, 6, 2, 7, 3, 8, 4, 9, 5, 10],
                    102: [2, 7, 1, 8, 3, 9, 4, 10, 5, 6],
                    103: [3, 8, 4, 9, 1, 6, 2, 7, 5, 10],
                    104: [4, 9, 3, 10, 2, 7, 1, 8, 6, 5],
                    105: [5, 10, 6, 1, 7, 2, 8, 3, 9, 4],
                },
                "caregiver_capacities": {101: 2, 102: 2, 103: 2, 104: 2, 105: 2},
                "expected_matches": {1: 101, 6: 101, 2: 102, 7: 102, 3: 103, 8: 103, 4: 104, 9: 104, 5: 105, 10: 105},
                "expected_unmatched": [],
                "is_stable": True
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
        
        # DAアルゴリズムインスタンスを作成
        da = DeferredAcceptanceAlgorithm()
        
        # テスト実行
        actual_matches, details = da.create_match(
            test_case["care_recipients"],
            test_case["caregivers"],
            test_case["recipient_preferences"],
            test_case["caregiver_preferences"],
            test_case["caregiver_capacities"]
        )
        
        # 安定性チェック
        is_stable, blocking_pairs = da.is_stable_matching(
            actual_matches,
            test_case["recipient_preferences"],
            test_case["caregiver_preferences"],
            test_case["caregiver_capacities"]
        )
        
        # マッチング結果の比較
        matches_correct = actual_matches == test_case["expected_matches"]
        unmatched_correct = set(details["unmatched_recipients"]) == set(test_case["expected_unmatched"])
        stability_correct = is_stable == test_case["is_stable"]
        
        # 結果をまとめる
        test_result = {
            "test_name": test_name,
            "description": test_case["description"],
            "input": {
                "care_recipients": test_case["care_recipients"],
                "caregivers": test_case["caregivers"],
                "recipient_preferences": test_case["recipient_preferences"],
                "caregiver_preferences": test_case["caregiver_preferences"],
                "caregiver_capacities": test_case["caregiver_capacities"]
            },
            "expected": {
                "matches": test_case["expected_matches"],
                "unmatched": test_case["expected_unmatched"],
                "is_stable": test_case["is_stable"]
            },
            "actual": {
                "matches": actual_matches,
                "unmatched": details["unmatched_recipients"],
                "is_stable": is_stable,
                "blocking_pairs": blocking_pairs
            },
            "passed": matches_correct and unmatched_correct and stability_correct,
            "sub_results": {
                "matches_correct": matches_correct,
                "unmatched_correct": unmatched_correct,
                "stability_correct": stability_correct
            },
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
        
        print("=== Deferred Acceptance アルゴリズム ブラックボックステスト実行 ===\n")
        
        for test_name in self.test_cases.keys():
            print(f"テスト実行中: {test_name}")
            result = self.run_test_case(test_name)
            results.append(result)
            
            if result["passed"]:
                passed_count += 1
                print(f"✓ PASS: {result['description']}")
            else:
                print(f"✗ FAIL: {result['description']}")
                print(f"  マッチング結果正解: {result['sub_results']['matches_correct']}")
                print(f"  未マッチ結果正解: {result['sub_results']['unmatched_correct']}")
                print(f"  安定性正解: {result['sub_results']['stability_correct']}")
                if not result['sub_results']['matches_correct']:
                    print(f"    期待されるマッチング: {result['expected']['matches']}")
                    print(f"    実際のマッチング: {result['actual']['matches']}")
                if not result['sub_results']['unmatched_correct']:
                    print(f"    期待される未マッチ: {result['expected']['unmatched']}")
                    print(f"    実際の未マッチ: {result['actual']['unmatched']}")
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
    
    def save_test_results(self, results: Dict[str, Any], filename: str = "da_test_results.json"):
        """
        テスト結果をJSONファイルに保存
        
        Args:
            results: テスト結果辞書
            filename: 保存ファイル名
        """
        # 詳細な実行履歴は除外して保存（サイズ削減のため）
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
                "actual": {
                    "matches": result["actual"]["matches"],
                    "unmatched": result["actual"]["unmatched"],
                    "is_stable": result["actual"]["is_stable"],
                    "blocking_pairs": result["actual"]["blocking_pairs"]
                },
                "passed": result["passed"],
                "sub_results": result["sub_results"]
            }
            simplified_results["test_summary"].append(simplified_result)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(simplified_results, f, ensure_ascii=False, indent=2)
        
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
        print(f"被介護者: {test_case['care_recipients']}")
        print(f"ケアワーカー: {test_case['caregivers']}")
        print(f"ケアワーカー容量: {test_case['caregiver_capacities']}")
        print(f"被介護者選好:")
        for recipient, prefs in test_case['recipient_preferences'].items():
            print(f"  {recipient}: {prefs}")
        print(f"ケアワーカー選好:")
        for caregiver, prefs in test_case['caregiver_preferences'].items():
            print(f"  {caregiver}: {prefs}")
        print(f"期待されるマッチング: {test_case['expected_matches']}")
        print(f"期待される未マッチ: {test_case['expected_unmatched']}")
        print(f"期待される安定性: {test_case['is_stable']}")
    
    def run_single_test_with_details(self, test_name: str):
        """
        単一のテストケースを実行し、詳細な過程を表示
        
        Args:
            test_name: テストケース名
        """
        if test_name not in self.test_cases:
            print(f"テストケース '{test_name}' が見つかりません")
            return
        
        print(f"=== テストケース '{test_name}' の詳細実行 ===")
        self.print_test_case_info(test_name)
        print()
        
        result = self.run_test_case(test_name)
        
        # DAアルゴリズムの実行過程を表示
        da = DeferredAcceptanceAlgorithm()
        da.print_matching_process(result["details"])
        
        print(f"\n=== テスト結果 ===")
        print(f"テスト合格: {result['passed']}")
        print(f"マッチング結果正解: {result['sub_results']['matches_correct']}")
        print(f"未マッチ結果正解: {result['sub_results']['unmatched_correct']}")
        print(f"安定性正解: {result['sub_results']['stability_correct']}")


def main():
    """メイン実行関数"""
    test_data = DATestData()
    
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
            print(f"期待されるマッチング: {failed_test['expected']['matches']}")
            print(f"実際のマッチング: {failed_test['actual']['matches']}")
            print(f"期待される未マッチ: {failed_test['expected']['unmatched']}")
            print(f"実際の未マッチ: {failed_test['actual']['unmatched']}")
            if failed_test['actual']['blocking_pairs']:
                print(f"ブロッキングペア: {failed_test['actual']['blocking_pairs']}")


if __name__ == "__main__":
    main()