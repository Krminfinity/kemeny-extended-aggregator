#!/usr/bin/env python3
"""
日本語フォントのテストスクリプト

ReportLabで利用可能な日本語フォントをテストし、結果を表示します。

Author: 倉持誠 (Makoto Kuramochi)
"""

import os
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import A4


def test_japanese_fonts():
    """日本語フォントをテストし、利用可能なものを確認"""
    
    print("=== 日本語フォントテスト開始 ===")
    
    # テスト用のフォント候補
    font_candidates = [
        # MS Gothic (確実に存在)
        ("C:/Windows/Fonts/msgothic.ttc", "MS Gothic", "MS Gothic は最も一般的な日本語フォントです"),
        ("C:/Windows/Fonts/MingLiU.ttc", "MingLiU", "MingLiU は中国語フォントですが日本語も表示可能です"),
        # Yu Gothic (Windows 8.1以降)
        ("C:/Windows/Fonts/YuGothR.ttc", "Yu Gothic", "Yu Gothic は比較的新しい読みやすいフォントです"),
        ("C:/Windows/Fonts/YuGothM.ttc", "Yu Gothic Medium", "Yu Gothic Medium はより太字版です"),
        # Meiryo (Vista以降)
        ("C:/Windows/Fonts/meiryo.ttc", "Meiryo", "Meiryo はクリアなフォントです"),
        ("C:/Windows/Fonts/meiryob.ttc", "Meiryo Bold", "Meiryo Bold は太字版です"),
        # Arial Unicode MS (Office同梱)
        ("C:/Windows/Fonts/ARIALUNI.TTF", "Arial Unicode MS", "Arial Unicode MS は多言語対応フォントです"),
    ]
    
    successful_fonts = []
    
    for font_path, display_name, description in font_candidates:
        print(f"\n--- {display_name} のテスト ---")
        print(f"パス: {font_path}")
        print(f"説明: {description}")
        
        if not os.path.exists(font_path):
            print("❌ ファイルが存在しません")
            continue
            
        try:
            # フォント登録を試行
            font_id = f"Test_{display_name.replace(' ', '_')}"
            if font_path.endswith('.ttc'):
                pdfmetrics.registerFont(TTFont(font_id, font_path, subfontIndex=0))
            else:
                pdfmetrics.registerFont(TTFont(font_id, font_path))
            
            # フォント登録の検証
            test_font = pdfmetrics.getFont(font_id)
            
            print("✅ フォント登録成功")
            successful_fonts.append((font_id, display_name, font_path, description))
            
            # テストPDFを生成
            test_pdf_name = f"font_test_{display_name.replace(' ', '_')}.pdf"
            doc = SimpleDocTemplate(test_pdf_name, pagesize=A4)
            
            # テスト用スタイル
            test_style = ParagraphStyle(
                f'Test_{display_name}',
                fontName=font_id,
                fontSize=12,
                leading=18,
            )
            
            # テスト文字列
            test_strings = [
                "日本語フォントテスト",
                "拡張版Kemenyルールのブラックボックステスト結果レポート",
                "テスト番号：1、2、3、4、5",
                "成功率：100.0%",
                "アルゴリズム：拡張版Kemenyルール、DAアルゴリズム",
                "ひらがな：あいうえおかきくけこ",
                "カタカナ：アイウエオカキクケコ",
                "漢字：日本語文字化け対策完了"
            ]
            
            story = []
            for text in test_strings:
                story.append(Paragraph(text, test_style))
            
            doc.build(story)
            print(f"📄 テストPDF生成: {test_pdf_name}")
            
        except Exception as e:
            print(f"❌ フォント登録失敗: {e}")
    
    # 結果サマリー
    print(f"\n=== テスト結果サマリー ===")
    print(f"テスト対象フォント数: {len(font_candidates)}")
    print(f"成功したフォント数: {len(successful_fonts)}")
    
    if successful_fonts:
        print("\n✅ 利用可能なフォント:")
        for font_id, display_name, font_path, description in successful_fonts:
            print(f"  - {display_name}: {font_path}")
        
        print(f"\n推奨フォント: {successful_fonts[0][1]}")
        print("このフォントをメインレポート生成に使用することを推奨します。")
    else:
        print("\n❌ 利用可能な日本語フォントが見つかりませんでした。")
        print("フォントファイルの場所を確認してください。")


if __name__ == "__main__":
    test_japanese_fonts()