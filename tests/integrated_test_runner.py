#!/usr/bin/env python3
"""
統合ブラックボックステスト実行スクリプト

拡張版KemenyルールとDAアルゴリズム両方のテストを実行し、
統合レポートを生成します。

Author: 倉持誠 (Makoto Kuramochi)
"""

from test_data_extended_kemeny import ExtendedKemenyTestData
from test_data_da import DATestData
import json
from datetime import datetime
import sys


class IntegratedTestRunner:
    """統合テスト実行クラス"""
    
    def __init__(self):
        """統合テストランナーの初期化"""
        self.extended_kemeny_tester = ExtendedKemenyTestData()
        self.da_tester = DATestData()
    
    def run_all_tests(self) -> dict:
        """
        全てのテストを実行
        
        Returns:
            dict: 統合テスト結果
        """
        print("=" * 80)
        print("統合ブラックボックステスト実行開始")
        print(f"実行時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)
        print()
        
        # 拡張版Kemenyルールのテスト実行
        print("🔹 拡張版Kemenyルールのテストを実行中...")
        kemeny_results = self.extended_kemeny_tester.run_all_tests()
        print()
        
        # DAアルゴリズムのテスト実行
        print("🔹 DAアルゴリズムのテストを実行中...")
        da_results = self.da_tester.run_all_tests()
        print()
        
        # 統合結果をまとめる
        integrated_results = {
            "test_execution_time": datetime.now().isoformat(),
            "extended_kemeny_rule": kemeny_results,
            "deferred_acceptance": da_results,
            "overall_summary": {
                "total_tests": kemeny_results["total_tests"] + da_results["total_tests"],
                "total_passed": kemeny_results["passed_tests"] + da_results["passed_tests"],
                "total_failed": kemeny_results["failed_tests"] + da_results["failed_tests"],
                "overall_pass_rate": (kemeny_results["passed_tests"] + da_results["passed_tests"]) / 
                                   (kemeny_results["total_tests"] + da_results["total_tests"]) * 100
            }
        }
        
        # 統合サマリーの表示
        self._print_integrated_summary(integrated_results)
        
        return integrated_results
    
    def _print_integrated_summary(self, results: dict):
        """
        統合テスト結果のサマリーを表示
        
        Args:
            results: 統合テスト結果辞書
        """
        print("=" * 80)
        print("🏁 統合テスト結果サマリー")
        print("=" * 80)
        
        # 全体サマリー
        overall = results["overall_summary"]
        print(f"📊 全体結果:")
        print(f"   総テスト数: {overall['total_tests']}")
        print(f"   成功: {overall['total_passed']}")
        print(f"   失敗: {overall['total_failed']}")
        print(f"   全体成功率: {overall['overall_pass_rate']:.1f}%")
        print()
        
        # 拡張版Kemenyルール結果
        kemeny = results["extended_kemeny_rule"]
        print(f"🧮 拡張版Kemenyルール:")
        print(f"   テスト数: {kemeny['total_tests']}")
        print(f"   成功: {kemeny['passed_tests']}")
        print(f"   失敗: {kemeny['failed_tests']}")
        print(f"   成功率: {kemeny['pass_rate']:.1f}%")
        print()
        
        # DAアルゴリズム結果
        da = results["deferred_acceptance"]
        print(f"🤝 DAアルゴリズム:")
        print(f"   テスト数: {da['total_tests']}")
        print(f"   成功: {da['passed_tests']}")
        print(f"   失敗: {da['failed_tests']}")
        print(f"   成功率: {da['pass_rate']:.1f}%")
        print()
        
        # 失敗したテストがあれば警告
        if overall['total_failed'] > 0:
            print("⚠️  注意: 失敗したテストがあります。詳細は個別のテスト結果ファイルを確認してください。")
        else:
            print("✅ 全てのテストが成功しました！")
        
        print("=" * 80)
    
    def save_integrated_results(self, results: dict, filename: str = "integrated_test_results.json"):
        """
        統合テスト結果をJSONファイルに保存
        
        Args:
            results: 統合テスト結果辞書
            filename: 保存ファイル名
        """
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print(f"📄 統合テスト結果を {filename} に保存しました")
    
    def run_specific_algorithm_tests(self, algorithm: str):
        """
        特定のアルゴリズムのテストのみを実行
        
        Args:
            algorithm: "kemeny" または "da"
        """
        if algorithm.lower() == "kemeny":
            print("拡張版Kemenyルールのテストのみを実行...")
            results = self.extended_kemeny_tester.run_all_tests()
            self.extended_kemeny_tester.save_test_results(results)
        elif algorithm.lower() == "da":
            print("DAアルゴリズムのテストのみを実行...")
            results = self.da_tester.run_all_tests()
            self.da_tester.save_test_results(results)
        else:
            print(f"未知のアルゴリズム: {algorithm}")
            print("利用可能なオプション: 'kemeny', 'da'")
    
    def run_specific_test_case(self, algorithm: str, test_name: str):
        """
        特定のテストケースのみを詳細実行
        
        Args:
            algorithm: "kemeny" または "da"
            test_name: テストケース名
        """
        if algorithm.lower() == "kemeny":
            if test_name in self.extended_kemeny_tester.get_test_case_names():
                result = self.extended_kemeny_tester.run_test_case(test_name)
                self.extended_kemeny_tester.print_test_case_info(test_name)
                print(f"\nテスト結果: {'✅ PASS' if result['passed'] else '❌ FAIL'}")
            else:
                print(f"テストケース '{test_name}' が見つかりません")
                print("利用可能なテストケース:")
                for name in self.extended_kemeny_tester.get_test_case_names():
                    print(f"  - {name}")
        elif algorithm.lower() == "da":
            if test_name in self.da_tester.get_test_case_names():
                self.da_tester.run_single_test_with_details(test_name)
            else:
                print(f"テストケース '{test_name}' が見つかりません")
                print("利用可能なテストケース:")
                for name in self.da_tester.get_test_case_names():
                    print(f"  - {name}")
        else:
            print(f"未知のアルゴリズム: {algorithm}")
    
    def list_all_test_cases(self):
        """
        全てのテストケースの一覧を表示
        """
        print("=" * 60)
        print("📋 利用可能なテストケース一覧")
        print("=" * 60)
        
        print("\n🧮 拡張版Kemenyルール:")
        for i, name in enumerate(self.extended_kemeny_tester.get_test_case_names(), 1):
            print(f"  {i:2d}. {name}")
        
        print("\n🤝 DAアルゴリズム:")
        for i, name in enumerate(self.da_tester.get_test_case_names(), 1):
            print(f"  {i:2d}. {name}")
        
        print("\n" + "=" * 60)


def print_usage():
    """使用方法を表示"""
    print("使用方法:")
    print("  python integrated_test_runner.py [オプション]")
    print()
    print("オプション:")
    print("  --all              : 全てのテストを実行（デフォルト）")
    print("  --kemeny           : 拡張版Kemenyルールのテストのみ実行")
    print("  --da               : DAアルゴリズムのテストのみ実行")
    print("  --list             : 利用可能なテストケース一覧を表示")
    print("  --test <alg> <name> : 特定のテストケースを実行")
    print("                      alg: 'kemeny' または 'da'")
    print("                      name: テストケース名")
    print("  --help             : この使用方法を表示")
    print()
    print("例:")
    print("  python integrated_test_runner.py --all")
    print("  python integrated_test_runner.py --kemeny")
    print("  python integrated_test_runner.py --test da basic_paper_example")


def main():
    """メイン実行関数"""
    runner = IntegratedTestRunner()
    
    if len(sys.argv) == 1:
        # デフォルト: 全テスト実行
        results = runner.run_all_tests()
        runner.save_integrated_results(results)
        runner.extended_kemeny_tester.save_test_results(results["extended_kemeny_rule"])
        runner.da_tester.save_test_results(results["deferred_acceptance"])
    
    elif "--help" in sys.argv:
        print_usage()
    
    elif "--list" in sys.argv:
        runner.list_all_test_cases()
    
    elif "--all" in sys.argv:
        results = runner.run_all_tests()
        runner.save_integrated_results(results)
        runner.extended_kemeny_tester.save_test_results(results["extended_kemeny_rule"])
        runner.da_tester.save_test_results(results["deferred_acceptance"])
    
    elif "--kemeny" in sys.argv:
        runner.run_specific_algorithm_tests("kemeny")
    
    elif "--da" in sys.argv:
        runner.run_specific_algorithm_tests("da")
    
    elif "--test" in sys.argv:
        try:
            test_index = sys.argv.index("--test")
            if test_index + 2 < len(sys.argv):
                algorithm = sys.argv[test_index + 1]
                test_name = sys.argv[test_index + 2]
                runner.run_specific_test_case(algorithm, test_name)
            else:
                print("エラー: --test オプションにはアルゴリズムとテストケース名が必要です")
                print_usage()
        except ValueError:
            print("エラー: --test オプションの使用方法が正しくありません")
            print_usage()
    
    else:
        print("不明なオプションです")
        print_usage()


if __name__ == "__main__":
    main()