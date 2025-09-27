#!/usr/bin/env python3
"""
テスト結果レポート生成スクリプト

ブラックボックステストの結果を表形式でまとめ、PDFとして出力します。

Author: 倉持誠 (Makoto Kuramochi)
"""

import json
from datetime import datetime
from typing import Dict, Any, List
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os


class TestReportGenerator:
    """テストレポート生成クラス"""
    
    def __init__(self):
        """レポート生成の初期化"""
        self.styles = getSampleStyleSheet()
        
        # 日本語フォントの設定を試行
        try:
            # Windows標準フォントを試行（より確実な方法）
            font_candidates = [
                # MS Gothic (確実に存在)
                ("C:/Windows/Fonts/msgothic.ttc", "MS Gothic"),
                ("C:/Windows/Fonts/MingLiU.ttc", "MingLiU"),
                # Yu Gothic (Windows 8.1以降)
                ("C:/Windows/Fonts/YuGothR.ttc", "Yu Gothic"),
                ("C:/Windows/Fonts/YuGothM.ttc", "Yu Gothic Medium"),
                # Meiryo (Vista以降)
                ("C:/Windows/Fonts/meiryo.ttc", "Meiryo"),
                ("C:/Windows/Fonts/meiryob.ttc", "Meiryo Bold"),
                # Arial Unicode MS (Office同梱)
                ("C:/Windows/Fonts/ARIALUNI.TTF", "Arial Unicode MS"),
            ]
            
            font_registered = False
            font_name = None
            
            for font_path, display_name in font_candidates:
                if os.path.exists(font_path):
                    try:
                        # TTCファイルの場合、subfontIndex=0を指定
                        if font_path.endswith('.ttc'):
                            # .ttcファイルの場合は複数のフォントが含まれているので、最初のフォントを指定
                            pdfmetrics.registerFont(TTFont('Japanese', font_path, subfontIndex=0))
                        else:
                            pdfmetrics.registerFont(TTFont('Japanese', font_path))
                        
                        # フォント登録の検証
                        test_font = pdfmetrics.getFont('Japanese')
                        font_registered = True
                        font_name = display_name
                        print(f"日本語フォント登録成功: {display_name} ({font_path})")
                        break
                    except Exception as font_error:
                        print(f"フォント {display_name} の登録に失敗: {font_error}")
                        continue
            
            if font_registered:
                # 日本語用スタイルを作成
                self.jp_style = ParagraphStyle(
                    'Japanese',
                    parent=self.styles['Normal'],
                    fontName='Japanese',
                    fontSize=9,
                    leading=12,
                    wordWrap='CJK',
                )
                self.jp_title_style = ParagraphStyle(
                    'JapaneseTitle',
                    parent=self.styles['Title'],
                    fontName='Japanese',
                    fontSize=16,
                    leading=20,
                    alignment=1,  # 中央揃え
                    wordWrap='CJK',
                )
                self.jp_heading_style = ParagraphStyle(
                    'JapaneseHeading',
                    parent=self.styles['Heading1'],
                    fontName='Japanese',
                    fontSize=12,
                    leading=16,
                    spaceAfter=12,
                    wordWrap='CJK',
                )
                self.jp_small_style = ParagraphStyle(
                    'JapaneseSmall',
                    parent=self.styles['Normal'],
                    fontName='Japanese',
                    fontSize=8,
                    leading=10,
                    wordWrap='CJK',
                )
                print("日本語フォント設定完了")
            else:
                print("日本語フォントが見つかりません。利用可能なフォントを確認中...")
                # 利用可能なフォントファイルをリスト表示
                import glob
                font_files = glob.glob("C:/Windows/Fonts/*.tt*")
                print(f"フォントファイル数: {len(font_files)}")
                for font_file in font_files[:5]:  # 最初の5個だけ表示
                    print(f"  - {font_file}")
                raise Exception("No Japanese font found")
                
        except Exception as e:
            print(f"日本語フォントの設定に失敗しました: {e}")
            print("デフォルトフォントを使用します（日本語は表示されない可能性があります）")
            self.jp_style = self.styles['Normal']
            self.jp_title_style = self.styles['Title']
            self.jp_heading_style = self.styles['Heading1']
            self.jp_small_style = self.styles['Normal']
            
    def get_font_name(self):
        """現在の日本語フォント名を取得"""
        try:
            # 日本語フォントが登録されているかチェック
            pdfmetrics.getFont('Japanese')
            return 'Japanese'
        except:
            return 'Helvetica'
    
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
    
    def create_kemeny_test_table(self, kemeny_results: Dict[str, Any]) -> List[List[str]]:
        """
        拡張版Kemenyルールのテスト結果テーブルを作成
        
        Args:
            kemeny_results: 拡張版Kemenyルールのテスト結果
            
        Returns:
            List[List[str]]: テーブルデータ
        """
        headers = [
            "テストケース名",
            "説明", 
            "主観的選好",
            "客観的フィット度",
            "選好重み",
            "フィット度重み",
            "期待結果",
            "実際結果",
            "期待スコア",
            "実際スコア",
            "結果"
        ]
        
        rows = [headers]
        
        for result in kemeny_results.get('results', []):
            input_data = result['input']
            expected = result['expected']
            actual = result['actual']
            
            row = [
                result['test_name'],
                result['description'],
                str(input_data['subjective_preference']),
                str(input_data['fitness_scores']),
                str(input_data['preference_weight']),
                str(input_data['fitness_weight']),
                str(expected['ranking']),
                str(actual['ranking']),
                str(expected['score']),
                str(actual['score']),
                "✓ PASS" if result['passed'] else "✗ FAIL"
            ]
            rows.append(row)
        
        return rows
    
    def create_da_test_table(self, da_results: Dict[str, Any]) -> List[List[str]]:
        """
        DAアルゴリズムのテスト結果テーブルを作成
        
        Args:
            da_results: DAアルゴリズムのテスト結果
            
        Returns:
            List[List[str]]: テーブルデータ
        """
        headers = [
            "テストケース名",
            "説明",
            "被介護者",
            "ケアワーカー",
            "容量",
            "期待マッチング",
            "実際マッチング",
            "期待未マッチ",
            "実際未マッチ",
            "安定性",
            "結果"
        ]
        
        rows = [headers]
        
        for result in da_results.get('results', []):
            input_data = result['input']
            expected = result['expected']
            actual = result['actual']
            
            row = [
                result['test_name'],
                result['description'],
                str(input_data['care_recipients']),
                str(input_data['caregivers']),
                str(input_data['caregiver_capacities']),
                str(expected['matches']),
                str(actual['matches']),
                str(expected['unmatched']),
                str(actual['unmatched']),
                str(actual['is_stable']),
                "✓ PASS" if result['passed'] else "✗ FAIL"
            ]
            rows.append(row)
        
        return rows
    
    def create_summary_table(self, integrated_results: Dict[str, Any]) -> List[List[str]]:
        """
        サマリーテーブルを作成
        
        Args:
            integrated_results: 統合テスト結果
            
        Returns:
            List[List[str]]: サマリーテーブルデータ
        """
        summary = integrated_results.get('overall_summary', {})
        kemeny = integrated_results.get('extended_kemeny_rule', {})
        da = integrated_results.get('deferred_acceptance', {})
        
        headers = ["アルゴリズム", "テスト数", "成功", "失敗", "成功率(%)"]
        
        rows = [
            headers,
            [
                "拡張版Kemenyルール",
                str(kemeny.get('total_tests', 0)),
                str(kemeny.get('passed_tests', 0)),
                str(kemeny.get('failed_tests', 0)),
                f"{kemeny.get('pass_rate', 0):.1f}"
            ],
            [
                "DAアルゴリズム",
                str(da.get('total_tests', 0)),
                str(da.get('passed_tests', 0)),
                str(da.get('failed_tests', 0)),
                f"{da.get('pass_rate', 0):.1f}"
            ],
            [
                "全体",
                str(summary.get('total_tests', 0)),
                str(summary.get('total_passed', 0)),
                str(summary.get('total_failed', 0)),
                f"{summary.get('overall_pass_rate', 0):.1f}"
            ]
        ]
        
        return rows
    
    def create_detailed_kemeny_input_table(self, kemeny_results: Dict[str, Any]) -> List[List[str]]:
        """
        拡張版Kemenyルールの詳細入力テーブルを作成
        
        Args:
            kemeny_results: 拡張版Kemenyルールのテスト結果
            
        Returns:
            List[List[str]]: 詳細入力テーブルデータ
        """
        headers = [
            "No.",
            "テストケース名",
            "主観的選好",
            "客観的フィット度",
            "選好重み",
            "フィット度重み",
            "説明"
        ]
        
        rows = [headers]
        
        for i, result in enumerate(kemeny_results.get('results', []), 1):
            input_data = result['input']
            
            row = [
                str(i),
                result['test_name'],
                str(input_data['subjective_preference']),
                str(input_data['fitness_scores']),
                str(input_data['preference_weight']),
                str(input_data['fitness_weight']),
                result['description']
            ]
            rows.append(row)
        
        return rows
    
    def create_detailed_da_input_table(self, da_results: Dict[str, Any]) -> List[List[str]]:
        """
        DAアルゴリズムの詳細入力テーブルを作成
        
        Args:
            da_results: DAアルゴリズムのテスト結果
            
        Returns:
            List[List[str]]: 詳細入力テーブルデータ
        """
        headers = [
            "No.",
            "テストケース名",
            "被介護者数",
            "ケアワーカー数",
            "総容量",
            "説明"
        ]
        
        rows = [headers]
        
        for i, result in enumerate(da_results.get('results', []), 1):
            input_data = result['input']
            total_capacity = sum(input_data['caregiver_capacities'].values())
            
            row = [
                str(i),
                result['test_name'],
                str(len(input_data['care_recipients'])),
                str(len(input_data['caregivers'])),
                str(total_capacity),
                result['description']
            ]
            rows.append(row)
        
        return rows
    
    def generate_pdf_report(self, filename: str = "test_results_report.pdf"):
        """
        PDFレポートを生成
        
        Args:
            filename: 出力ファイル名
        """
        print("テスト結果レポートを生成中...")
        
        # テスト結果を読み込み
        integrated_results = self.load_test_results()
        if not integrated_results:
            print("テスト結果の読み込みに失敗しました")
            return
        
        # PDFドキュメントを作成（横向きレイアウト）
        doc = SimpleDocTemplate(filename, pagesize=landscape(A4), 
                              leftMargin=0.5*inch, rightMargin=0.5*inch,
                              topMargin=0.5*inch, bottomMargin=0.5*inch)
        
        story = []
        
        # タイトル
        title = Paragraph("ブラックボックステスト結果レポート", self.jp_title_style)
        story.append(title)
        story.append(Spacer(1, 0.2*inch))
        
        # 実行日時
        execution_time = integrated_results.get('test_execution_time', 'Unknown')
        if execution_time != 'Unknown':
            try:
                dt = datetime.fromisoformat(execution_time.replace('Z', '+00:00'))
                execution_time = dt.strftime('%Y年%m月%d日 %H:%M:%S')
            except:
                pass
        
        exec_time_para = Paragraph(f"実行日時: {execution_time}", self.jp_style)
        story.append(exec_time_para)
        story.append(Spacer(1, 0.3*inch))
        
        # サマリーテーブル
        summary_heading = Paragraph("1. テスト結果サマリー", self.jp_heading_style)
        story.append(summary_heading)
        story.append(Spacer(1, 0.1*inch))
        
        summary_data = self.create_summary_table(integrated_results)
        summary_table = Table(summary_data, colWidths=[3*inch, 1.2*inch, 1.2*inch, 1.2*inch, 1.5*inch])
        font_name = self.get_font_name()
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), font_name),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('FONTNAME', (0, 1), (-1, -1), font_name),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
        ]))
        story.append(summary_table)
        story.append(Spacer(1, 0.3*inch))
        
        # 拡張版Kemenyルール詳細入力
        kemeny_input_heading = Paragraph("2. 拡張版Kemenyルール - 入力データ", self.jp_heading_style)
        story.append(kemeny_input_heading)
        story.append(Spacer(1, 0.1*inch))
        
        kemeny_input_data = self.create_detailed_kemeny_input_table(integrated_results.get('extended_kemeny_rule', {}))
        kemeny_input_table = Table(kemeny_input_data, colWidths=[0.4*inch, 2*inch, 1.5*inch, 1.5*inch, 1*inch, 1*inch, 3.5*inch])
        font_name = self.get_font_name()
        kemeny_input_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), font_name),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('FONTNAME', (0, 1), (-1, -1), font_name),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightcyan),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        story.append(kemeny_input_table)
        story.append(PageBreak())
        
        # 拡張版Kemenyルール結果
        kemeny_heading = Paragraph("3. 拡張版Kemenyルール - テスト結果", self.jp_heading_style)
        story.append(kemeny_heading)
        story.append(Spacer(1, 0.1*inch))
        
        kemeny_data = self.create_kemeny_test_table(integrated_results.get('extended_kemeny_rule', {}))
        kemeny_table = Table(kemeny_data, colWidths=[1.2*inch, 1.8*inch, 1*inch, 1*inch, 0.6*inch, 0.6*inch, 0.8*inch, 0.8*inch, 0.6*inch, 0.6*inch, 0.7*inch])
        font_name = self.get_font_name()
        kemeny_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), font_name),
            ('FONTSIZE', (0, 0), (-1, 0), 8),
            ('FONTNAME', (0, 1), (-1, -1), font_name),
            ('FONTSIZE', (0, 1), (-1, -1), 7),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightcyan),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        story.append(kemeny_table)
        story.append(PageBreak())
        
        # DAアルゴリズム詳細入力
        da_input_heading = Paragraph("4. DAアルゴリズム - 入力データ", self.jp_heading_style)
        story.append(da_input_heading)
        story.append(Spacer(1, 0.1*inch))
        
        da_input_data = self.create_detailed_da_input_table(integrated_results.get('deferred_acceptance', {}))
        da_input_table = Table(da_input_data, colWidths=[0.4*inch, 2*inch, 1.2*inch, 1.2*inch, 1.2*inch, 4.5*inch])
        font_name = self.get_font_name()
        da_input_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgreen),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), font_name),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('FONTNAME', (0, 1), (-1, -1), font_name),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        story.append(da_input_table)
        story.append(Spacer(1, 0.2*inch))
        
        # DAアルゴリズム結果
        da_heading = Paragraph("5. DAアルゴリズム - テスト結果", self.jp_heading_style)
        story.append(da_heading)
        story.append(Spacer(1, 0.1*inch))
        
        da_data = self.create_da_test_table(integrated_results.get('deferred_acceptance', {}))
        da_table = Table(da_data, colWidths=[1*inch, 1.5*inch, 0.8*inch, 0.8*inch, 0.8*inch, 1.2*inch, 1.2*inch, 0.8*inch, 0.8*inch, 0.6*inch, 0.7*inch])
        font_name = self.get_font_name()
        da_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgreen),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), font_name),
            ('FONTSIZE', (0, 0), (-1, 0), 8),
            ('FONTNAME', (0, 1), (-1, -1), font_name),
            ('FONTSIZE', (0, 1), (-1, -1), 7),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        story.append(da_table)
        
        # PDFを生成
        doc.build(story)
        print(f"PDFレポートを {filename} に保存しました")
    
    def generate_csv_reports(self):
        """
        CSV形式のレポートも生成
        """
        print("CSV形式のレポートを生成中...")
        
        integrated_results = self.load_test_results()
        if not integrated_results:
            return
        
        # 拡張版KemenyルールのCSV
        kemeny_data = self.create_kemeny_test_table(integrated_results.get('extended_kemeny_rule', {}))
        kemeny_df = pd.DataFrame(kemeny_data[1:], columns=kemeny_data[0])
        kemeny_df.to_csv('kemeny_test_results.csv', index=False, encoding='utf-8-sig')
        
        # DAアルゴリズムのCSV
        da_data = self.create_da_test_table(integrated_results.get('deferred_acceptance', {}))
        da_df = pd.DataFrame(da_data[1:], columns=da_data[0])
        da_df.to_csv('da_test_results.csv', index=False, encoding='utf-8-sig')
        
        # サマリーのCSV
        summary_data = self.create_summary_table(integrated_results)
        summary_df = pd.DataFrame(summary_data[1:], columns=summary_data[0])
        summary_df.to_csv('test_summary.csv', index=False, encoding='utf-8-sig')
        
        print("CSVファイルを生成しました:")
        print("- kemeny_test_results.csv")
        print("- da_test_results.csv")
        print("- test_summary.csv")


def main():
    """メイン実行関数"""
    generator = TestReportGenerator()
    
    # PDFレポート生成
    generator.generate_pdf_report("test_results_report.pdf")
    
    # CSVレポートも生成
    generator.generate_csv_reports()
    
    print("\n=== レポート生成完了 ===")
    print("生成されたファイル:")
    print("📄 test_results_report.pdf - 詳細なテスト結果レポート")
    print("📊 kemeny_test_results.csv - 拡張版Kemenyルール結果")
    print("📊 da_test_results.csv - DAアルゴリズム結果")
    print("📊 test_summary.csv - テスト結果サマリー")


if __name__ == "__main__":
    main()