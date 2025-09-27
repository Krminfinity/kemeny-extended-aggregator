#!/usr/bin/env python3
"""
詳細テスト結果Excelレポート生成スクリプト

より詳細で読みやすいExcel形式のテスト結果レポートを生成します。

Author: 倉持誠 (Makoto Kuramochi)
"""

import json
from datetime import datetime
from typing import Dict, Any, List
import pandas as pd
import os


class DetailedExcelReportGenerator:
    """詳細Excelレポート生成クラス"""
    
    def __init__(self):
        """レポート生成の初期化"""
        pass
    
    def load_test_results(self) -> Dict[str, Any]:
        """
        テスト結果ファイルを読み込み
        
        Returns:
            Dict[str, Any]: 統合テスト結果
        """
        try:
            with open('integrated_test_results.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print("integrated_test_results.json が見つかりません")
            return {}
    
    def create_kemeny_detailed_table(self, kemeny_results: Dict[str, Any]) -> pd.DataFrame:
        """
        拡張版Kemenyルールの詳細テーブルを作成
        
        Args:
            kemeny_results: 拡張版Kemenyルールのテスト結果
            
        Returns:
            pd.DataFrame: 詳細テーブル
        """
        rows = []
        
        for i, result in enumerate(kemeny_results.get('results', []), 1):
            input_data = result['input']
            expected = result['expected']
            actual = result['actual']
            
            row = {
                'No.': i,
                'テストケース名': result['test_name'],
                '説明': result['description'],
                '主観的選好': str(input_data['subjective_preference']),
                '客観的フィット度': str(input_data['fitness_scores']),
                '選好重み': input_data['preference_weight'],
                'フィット度重み': input_data['fitness_weight'],
                '期待結果': str(expected['ranking']),
                '実際結果': str(actual['ranking']),
                '期待スコア': expected['score'],
                '実際スコア': actual['score'],
                '結果一致': '✓' if result['passed'] else '✗',
                'テスト結果': 'PASS' if result['passed'] else 'FAIL'
            }
            rows.append(row)
        
        return pd.DataFrame(rows)
    
    def create_da_detailed_table(self, da_results: Dict[str, Any]) -> pd.DataFrame:
        """
        DAアルゴリズムの詳細テーブルを作成
        
        Args:
            da_results: DAアルゴリズムのテスト結果
            
        Returns:
            pd.DataFrame: 詳細テーブル
        """
        rows = []
        
        for i, result in enumerate(da_results.get('results', []), 1):
            input_data = result['input']
            expected = result['expected']
            actual = result['actual']
            
            row = {
                'No.': i,
                'テストケース名': result['test_name'],
                '説明': result['description'],
                '被介護者数': len(input_data['care_recipients']),
                'ケアワーカー数': len(input_data['caregivers']),
                '総容量': sum(input_data['caregiver_capacities'].values()),
                '被介護者ID': str(input_data['care_recipients']),
                'ケアワーカーID': str(input_data['caregivers']),
                'ケアワーカー容量': str(input_data['caregiver_capacities']),
                '期待マッチング': str(expected['matches']),
                '実際マッチング': str(actual['matches']),
                '期待未マッチ': str(expected['unmatched']),
                '実際未マッチ': str(actual['unmatched']),
                '安定性': '✓' if actual['is_stable'] else '✗',
                'マッチング一致': '✓' if result['sub_results']['matches_correct'] else '✗',
                '未マッチ一致': '✓' if result['sub_results']['unmatched_correct'] else '✗',
                'テスト結果': 'PASS' if result['passed'] else 'FAIL'
            }
            rows.append(row)
        
        return pd.DataFrame(rows)
    
    def create_kemeny_preference_details(self, kemeny_results: Dict[str, Any]) -> pd.DataFrame:
        """
        拡張版Kemenyルールの被介護者選好詳細テーブルを作成
        
        Args:
            kemeny_results: 拡張版Kemenyルールのテスト結果
            
        Returns:
            pd.DataFrame: 被介護者選好詳細テーブル
        """
        rows = []
        
        for result in kemeny_results.get('results', []):
            input_data = result['input']
            
            row = {
                'テストケース': result['test_name'],
                '主観的選好順位1位': input_data['subjective_preference'][0] if len(input_data['subjective_preference']) > 0 else '',
                '主観的選好順位2位': input_data['subjective_preference'][1] if len(input_data['subjective_preference']) > 1 else '',
                '主観的選好順位3位': input_data['subjective_preference'][2] if len(input_data['subjective_preference']) > 2 else '',
                '主観的選好順位4位': input_data['subjective_preference'][3] if len(input_data['subjective_preference']) > 3 else '',
                'フィット度0番': input_data['fitness_scores'][0] if len(input_data['fitness_scores']) > 0 else '',
                'フィット度1番': input_data['fitness_scores'][1] if len(input_data['fitness_scores']) > 1 else '',
                'フィット度2番': input_data['fitness_scores'][2] if len(input_data['fitness_scores']) > 2 else '',
                'フィット度3番': input_data['fitness_scores'][3] if len(input_data['fitness_scores']) > 3 else '',
            }
            rows.append(row)
        
        return pd.DataFrame(rows)
    
    def create_da_preference_details(self, da_results: Dict[str, Any]) -> pd.DataFrame:
        """
        DAアルゴリズムの選好詳細テーブルを作成
        
        Args:
            da_results: DAアルゴリズムのテスト結果
            
        Returns:
            pd.DataFrame: 選好詳細テーブル
        """
        rows = []
        
        for result in da_results.get('results', []):
            input_data = result['input']
            
            # 被介護者の選好
            for care_recipient, preferences in input_data['recipient_preferences'].items():
                row = {
                    'テストケース': result['test_name'],
                    'タイプ': '被介護者選好',
                    'ID': care_recipient,
                    '第1選好': preferences[0] if len(preferences) > 0 else '',
                    '第2選好': preferences[1] if len(preferences) > 1 else '',
                    '第3選好': preferences[2] if len(preferences) > 2 else '',
                    '第4選好': preferences[3] if len(preferences) > 3 else '',
                    '第5選好': preferences[4] if len(preferences) > 4 else '',
                }
                rows.append(row)
            
            # ケアワーカーの選好
            for caregiver, preferences in input_data['caregiver_preferences'].items():
                row = {
                    'テストケース': result['test_name'],
                    'タイプ': 'ケアワーカー選好',
                    'ID': caregiver,
                    '第1選好': preferences[0] if len(preferences) > 0 else '',
                    '第2選好': preferences[1] if len(preferences) > 1 else '',
                    '第3選好': preferences[2] if len(preferences) > 2 else '',
                    '第4選好': preferences[3] if len(preferences) > 3 else '',
                    '第5選好': preferences[4] if len(preferences) > 4 else '',
                }
                rows.append(row)
        
        return pd.DataFrame(rows)
    
    def generate_excel_report(self, filename: str = "detailed_test_results.xlsx"):
        """
        詳細Excelレポートを生成
        
        Args:
            filename: 出力ファイル名
        """
        print("詳細Excelレポートを生成中...")
        
        # テスト結果を読み込み
        integrated_results = self.load_test_results()
        if not integrated_results:
            print("テスト結果の読み込みに失敗しました")
            return
        
        # ExcelWriterを作成
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            
            # サマリーシート
            summary_data = {
                'アルゴリズム': ['拡張版Kemenyルール', 'DAアルゴリズム', '全体'],
                'テスト数': [
                    integrated_results.get('extended_kemeny_rule', {}).get('total_tests', 0),
                    integrated_results.get('deferred_acceptance', {}).get('total_tests', 0),
                    integrated_results.get('overall_summary', {}).get('total_tests', 0)
                ],
                '成功': [
                    integrated_results.get('extended_kemeny_rule', {}).get('passed_tests', 0),
                    integrated_results.get('deferred_acceptance', {}).get('passed_tests', 0),
                    integrated_results.get('overall_summary', {}).get('total_passed', 0)
                ],
                '失敗': [
                    integrated_results.get('extended_kemeny_rule', {}).get('failed_tests', 0),
                    integrated_results.get('deferred_acceptance', {}).get('failed_tests', 0),
                    integrated_results.get('overall_summary', {}).get('total_failed', 0)
                ],
                '成功率(%)': [
                    integrated_results.get('extended_kemeny_rule', {}).get('pass_rate', 0),
                    integrated_results.get('deferred_acceptance', {}).get('pass_rate', 0),
                    integrated_results.get('overall_summary', {}).get('overall_pass_rate', 0)
                ]
            }
            summary_df = pd.DataFrame(summary_data)
            summary_df.to_excel(writer, sheet_name='サマリー', index=False)
            
            # 拡張版Kemenyルール詳細
            kemeny_df = self.create_kemeny_detailed_table(integrated_results.get('extended_kemeny_rule', {}))
            kemeny_df.to_excel(writer, sheet_name='Kemenyルール詳細', index=False)
            
            # 拡張版Kemenyルール選好詳細
            kemeny_pref_df = self.create_kemeny_preference_details(integrated_results.get('extended_kemeny_rule', {}))
            kemeny_pref_df.to_excel(writer, sheet_name='Kemeny選好詳細', index=False)
            
            # DAアルゴリズム詳細
            da_df = self.create_da_detailed_table(integrated_results.get('deferred_acceptance', {}))
            da_df.to_excel(writer, sheet_name='DA詳細', index=False)
            
            # DAアルゴリズム選好詳細
            da_pref_df = self.create_da_preference_details(integrated_results.get('deferred_acceptance', {}))
            da_pref_df.to_excel(writer, sheet_name='DA選好詳細', index=False)
            
            # 実行情報シート
            execution_info = {
                '項目': ['実行日時', 'テスト総数', '成功総数', '失敗総数', '全体成功率(%)'],
                '値': [
                    integrated_results.get('test_execution_time', 'Unknown'),
                    integrated_results.get('overall_summary', {}).get('total_tests', 0),
                    integrated_results.get('overall_summary', {}).get('total_passed', 0),
                    integrated_results.get('overall_summary', {}).get('total_failed', 0),
                    integrated_results.get('overall_summary', {}).get('overall_pass_rate', 0)
                ]
            }
            info_df = pd.DataFrame(execution_info)
            info_df.to_excel(writer, sheet_name='実行情報', index=False)
        
        print(f"詳細Excelレポートを {filename} に保存しました")
        
        # 各シートの情報を出力
        print("\n=== 生成されたシート ===")
        print("📊 サマリー - テスト結果の概要")
        print("🧮 Kemenyルール詳細 - 拡張版Kemenyルールの詳細結果")
        print("📝 Kemeny選好詳細 - 拡張版Kemenyルールの入力詳細")
        print("🤝 DA詳細 - DAアルゴリズムの詳細結果") 
        print("📝 DA選好詳細 - DAアルゴリズムの選好詳細")
        print("ℹ️ 実行情報 - テスト実行の基本情報")


def main():
    """メイン実行関数"""
    generator = DetailedExcelReportGenerator()
    
    # Excelレポート生成
    generator.generate_excel_report("detailed_test_results.xlsx")
    
    print("\n=== 詳細レポート生成完了 ===")
    print("生成されたファイル:")
    print("📈 detailed_test_results.xlsx - 詳細なテスト結果（Excelファイル）")
    print("\nこのファイルをExcelで開いて、各シートでテスト結果を確認できます。")


if __name__ == "__main__":
    main()