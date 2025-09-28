#!/usr/bin/env python3
"""
PDF to Markdown Converter
PDFファイルをMarkdown形式に変換するツール
"""

import os
import sys
import argparse
from pathlib import Path

try:
    import PyPDF2
    import pdfplumber
except ImportError:
    print("必要なライブラリがインストールされていません。")
    print("以下のコマンドでインストールしてください:")
    print("pip install PyPDF2 pdfplumber")
    sys.exit(1)

def extract_text_with_pypdf2(pdf_path):
    """PyPDF2を使用してPDFからテキストを抽出"""
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page_num, page in enumerate(pdf_reader.pages, 1):
                page_text = page.extract_text()
                if page_text.strip():
                    text += f"\n## ページ {page_num}\n\n{page_text}\n"
    except Exception as e:
        print(f"PyPDF2でのテキスト抽出に失敗: {e}")
    return text

def extract_text_with_pdfplumber(pdf_path):
    """pdfplumberを使用してPDFからテキストを抽出（より高精度）"""
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                page_text = page.extract_text()
                if page_text and page_text.strip():
                    # テーブルの抽出も試行
                    tables = page.extract_tables()
                    
                    text += f"\n## ページ {page_num}\n\n"
                    text += page_text + "\n"
                    
                    # テーブルがある場合はMarkdown形式で追加
                    if tables:
                        text += "\n### テーブル\n\n"
                        for table_num, table in enumerate(tables, 1):
                            text += f"**テーブル {table_num}:**\n\n"
                            if table and len(table) > 0:
                                # ヘッダー行
                                if table[0]:
                                    header = " | ".join([str(cell) if cell else "" for cell in table[0]])
                                    text += f"| {header} |\n"
                                    text += "|" + " --- |" * len(table[0]) + "\n"
                                
                                # データ行
                                for row in table[1:]:
                                    if row:
                                        row_text = " | ".join([str(cell) if cell else "" for cell in row])
                                        text += f"| {row_text} |\n"
                            text += "\n"
    except Exception as e:
        print(f"pdfplumberでのテキスト抽出に失敗: {e}")
    return text

def convert_pdf_to_markdown(pdf_path, output_path=None, method="pdfplumber"):
    """PDFをMarkdown形式に変換"""
    
    # 入力ファイルの存在確認
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDFファイルが見つかりません: {pdf_path}")
    
    # 出力パスの設定
    if output_path is None:
        pdf_name = Path(pdf_path).stem
        output_path = Path(pdf_path).parent / f"{pdf_name}.md"
    
    print(f"PDFファイルを変換中: {pdf_path}")
    print(f"出力ファイル: {output_path}")
    print(f"使用方法: {method}")
    
    # テキスト抽出
    if method == "pdfplumber":
        extracted_text = extract_text_with_pdfplumber(pdf_path)
    else:
        extracted_text = extract_text_with_pypdf2(pdf_path)
    
    if not extracted_text.strip():
        print("警告: テキストが抽出できませんでした。別の方法を試してください。")
        return False
    
    # Markdownファイルとして保存
    markdown_content = f"""# {Path(pdf_path).stem}

> PDFから変換されたファイル: {Path(pdf_path).name}
> 変換日時: {__import__('datetime').datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}
> 変換方法: {method}

{extracted_text}

---
*このファイルは自動的にPDFから変換されました。*
"""
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        print(f"変換完了: {output_path}")
        return True
    except Exception as e:
        print(f"ファイル保存エラー: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='PDFファイルをMarkdown形式に変換')
    parser.add_argument('pdf_path', help='変換するPDFファイルのパス')
    parser.add_argument('-o', '--output', help='出力Markdownファイルのパス')
    parser.add_argument('-m', '--method', choices=['pypdf2', 'pdfplumber'], 
                        default='pdfplumber', help='テキスト抽出方法')
    
    args = parser.parse_args()
    
    try:
        success = convert_pdf_to_markdown(args.pdf_path, args.output, args.method)
        if success:
            print("変換が正常に完了しました。")
        else:
            print("変換に失敗しました。")
            sys.exit(1)
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()