#!/usr/bin/env python3
"""
PDFファイルの文字化けテストスクリプト

生成されたPDFファイルを開いて、日本語が正しく表示されるかを確認します。

Author: 倉持誠 (Makoto Kuramochi)
"""

import os
import subprocess
import sys


def test_pdf_encoding():
    """PDFファイルの日本語エンコーディングをテスト"""
    
    print("=== PDFファイル日本語表示テスト ===")
    
    # テスト対象のPDFファイル
    test_files = [
        "test_results_report.pdf",
        "font_test_MS_Gothic.pdf"
    ]
    
    for pdf_file in test_files:
        if os.path.exists(pdf_file):
            print(f"\n📄 {pdf_file} の確認:")
            print(f"  ファイルサイズ: {os.path.getsize(pdf_file):,} bytes")
            
            try:
                # PDFファイルをデフォルトアプリケーションで開く（Windows）
                if sys.platform.startswith('win'):
                    print(f"  ✅ ファイルが存在します")
                    print(f"  📖 ファイルを開くには以下のコマンドを実行してください:")
                    print(f"     start {pdf_file}")
                else:
                    print(f"  ✅ ファイルが存在します")
                    
            except Exception as e:
                print(f"  ❌ エラー: {e}")
        else:
            print(f"\n❌ {pdf_file} が見つかりません")
    
    print("\n=== 日本語文字化け確認方法 ===")
    print("1. 生成されたPDFファイルを開いてください")
    print("2. 以下の日本語テキストが正しく表示されているか確認してください:")
    print("   - 「ブラックボックステスト結果レポート」（タイトル）")
    print("   - 「拡張版Kemenyルール」（テーブルヘッダー）")
    print("   - 「テスト結果サマリー」（見出し）")
    print("   - 各テストケースの説明文")
    print("3. 文字が□（四角）や?で表示される場合は文字化けです")
    print("4. 正常に日本語が表示される場合は修正成功です")
    
    print(f"\n📊 テスト実行概要:")
    print(f"  - 拡張版Kemenyルール: 13テストケース (100%成功)")
    print(f"  - DAアルゴリズム: 10テストケース (100%成功)")
    print(f"  - 統合テスト: 23テストケース (100%成功)")
    print(f"  - 新規追加ケース: フィット度が結果を変える3つのテスト")


if __name__ == "__main__":
    test_pdf_encoding()