#!/usr/bin/env python3
"""
PowerPoint to Markdown Converter - デモ用サンプル

このスクリプトは、ワークスペース内のPowerPointファイルを
自動で検出して変換するデモンストレーション用のプログラムです。
"""

import os
from pathlib import Path

try:
    from markitdown import MarkItDown
except ImportError:
    print("エラー: markitdownライブラリがインストールされていません。")
    print("以下のコマンドでインストールしてください:")
    print("pip install markitdown[pptx]")
    exit(1)


def find_and_convert_pptx_files():
    """現在のディレクトリでPowerPointファイルを探して変換"""
    current_dir = Path.cwd()
    print(f"作業ディレクトリ: {current_dir}")
    
    # PowerPointファイルを検索
    pptx_files = list(current_dir.glob("*.pptx"))
    
    if not pptx_files:
        print("PowerPointファイル (.pptx) が見つかりませんでした。")
        return
    
    print(f"\n{len(pptx_files)}個のPowerPointファイルが見つかりました:")
    for file in pptx_files:
        print(f"  - {file.name}")
    
    print("\n変換を開始します...")
    
    markitdown = MarkItDown()
    success_count = 0
    
    for pptx_file in pptx_files:
        try:
            print(f"\n変換中: {pptx_file.name}")
            result = markitdown.convert(str(pptx_file))
            
            # 出力ファイル名を生成
            output_file = pptx_file.with_suffix('.md')
            
            # Markdownファイルに保存
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(result.text_content)
            
            print(f"✓ 変換完了: {output_file.name}")
            print(f"  出力サイズ: {len(result.text_content):,} 文字")
            success_count += 1
            
        except Exception as e:
            print(f"✗ 変換失敗: {pptx_file.name}")
            print(f"  エラー: {e}")
    
    print(f"\n=== 変換結果 ===")
    print(f"成功: {success_count}/{len(pptx_files)}個のファイル")
    
    if success_count > 0:
        print(f"\n生成されたMarkdownファイル:")
        for pptx_file in pptx_files:
            md_file = pptx_file.with_suffix('.md')
            if md_file.exists():
                print(f"  - {md_file.name}")


def main():
    print("=== PowerPoint to Markdown Converter デモ ===")
    print("このプログラムは現在のディレクトリ内の .pptx ファイルを")
    print("自動的に検出して Markdown 形式に変換します。\n")
    
    try:
        find_and_convert_pptx_files()
    except KeyboardInterrupt:
        print("\n\n変換がキャンセルされました。")
    except Exception as e:
        print(f"\n予期しないエラーが発生しました: {e}")


if __name__ == "__main__":
    main()