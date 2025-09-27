#!/usr/bin/env python3
"""
整理後のフォルダ構造でテストを実行するスクリプト

Author: 倉持誠 (Makoto Kuramochi)
"""

import sys
import os

# パスを追加してモジュールをインポート可能にする
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'algorithms'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'tests'))

from integrated_test_runner import IntegratedTestRunner

def main():
    """メイン実行関数"""
    # 作業ディレクトリをルートに変更
    original_dir = os.getcwd()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(script_dir)
    os.chdir(root_dir)
    
    try:
        runner = IntegratedTestRunner()
        
        # 全テストを実行
        results = runner.run_all_tests()
        
        # 結果をresultsディレクトリに保存
        os.makedirs('results', exist_ok=True)
        runner.save_integrated_results(results, 'results/integrated_test_results.json')
        runner.extended_kemeny_tester.save_test_results(results["extended_kemeny_rule"], 'results/extended_kemeny_test_results.json')
        runner.da_tester.save_test_results(results["deferred_acceptance"], 'results/da_test_results.json')
        
    finally:
        os.chdir(original_dir)

if __name__ == "__main__":
    main()