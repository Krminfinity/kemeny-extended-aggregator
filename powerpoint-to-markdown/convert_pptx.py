#!/usr/bin/env python3
"""
PowerPointファイルをMarkdownに変換するシンプルなCLIツール

Usage:
    python convert_pptx.py <input_file.pptx> [output_file.md]
"""

import sys
import argparse
from pathlib import Path

try:
    from markitdown import MarkItDown
except ImportError:
    print("エラー: markitdownライブラリがインストールされていません。")
    print("以下のコマンドでインストールしてください:")
    print("pip install markitdown")
    sys.exit(1)


def convert_pptx_to_markdown(input_file: str, output_file: str = None) -> bool:
    """
    PowerPointファイルをMarkdownに変換する
    
    Args:
        input_file: 入力PowerPointファイルのパス
        output_file: 出力Markdownファイルのパス（省略時は自動生成）
    
    Returns:
        bool: 変換成功時はTrue
    """
    input_path = Path(input_file)
    
    # 入力ファイルの確認
    if not input_path.exists():
        print(f"エラー: ファイルが見つかりません: {input_file}")
        return False
    
    if input_path.suffix.lower() != '.pptx':
        print(f"エラー: PowerPointファイル (.pptx) を指定してください: {input_file}")
        return False
    
    # 出力ファイルパスの設定
    if output_file is None:
        output_path = input_path.with_suffix('.md')
    else:
        output_path = Path(output_file)
    
    try:
        print(f"変換開始: {input_path.name}")
        
        # MarkItDownで変換
        markitdown = MarkItDown()
        result = markitdown.convert(str(input_path))
        
        # Markdownファイルに保存
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(result.text_content)
        
        print(f"変換完了: {output_path}")
        print(f"出力サイズ: {len(result.text_content):,} 文字")
        
        return True
        
    except Exception as e:
        print(f"エラー: 変換に失敗しました: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description='PowerPointファイルをMarkdownに変換します',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  python convert_pptx.py presentation.pptx
  python convert_pptx.py slides.pptx output.md
  python convert_pptx.py "卒業論文_発表資料.pptx" thesis_slides.md
        """
    )
    
    parser.add_argument('input_file', help='変換するPowerPointファイル (.pptx)')
    parser.add_argument('output_file', nargs='?', help='出力するMarkdownファイル (.md) [省略時は自動生成]')
    parser.add_argument('-v', '--verbose', action='store_true', help='詳細な出力を表示')
    
    args = parser.parse_args()
    
    if args.verbose:
        print(f"入力ファイル: {args.input_file}")
        print(f"出力ファイル: {args.output_file or '自動生成'}")
    
    success = convert_pptx_to_markdown(args.input_file, args.output_file)
    
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()