#!/usr/bin/env python3
"""
PowerPointファイルをMarkdownファイルに変換するプログラム

このプログラムはMicrosoftのMarkItDownライブラリを使用して、
PowerPoint (.pptx) ファイルをMarkdown形式に変換します。

使用例:
    python pptx_to_markdown.py
    python pptx_to_markdown.py input.pptx output.md
"""

import os
import sys
from pathlib import Path
from typing import Optional

try:
    from markitdown import MarkItDown
except ImportError:
    print("エラー: markitdownライブラリがインストールされていません。")
    print("以下のコマンドでインストールしてください:")
    print("pip install markitdown")
    sys.exit(1)


class PowerPointToMarkdownConverter:
    """PowerPointファイルをMarkdownに変換するクラス"""
    
    def __init__(self):
        """コンバーターを初期化"""
        self.markitdown = MarkItDown()
    
    def convert_file(self, input_path: str, output_path: Optional[str] = None) -> bool:
        """
        PowerPointファイルをMarkdownに変換
        
        Args:
            input_path: 入力するPowerPointファイルのパス
            output_path: 出力先のMarkdownファイルのパス（省略時は自動生成）
        
        Returns:
            bool: 変換が成功した場合True
        """
        input_file = Path(input_path)
        
        # 入力ファイルの存在確認
        if not input_file.exists():
            print(f"エラー: ファイルが見つかりません: {input_path}")
            return False
        
        # 入力ファイルの拡張子確認
        if input_file.suffix.lower() != '.pptx':
            print(f"エラー: PowerPointファイル (.pptx) ではありません: {input_path}")
            return False
        
        # 出力ファイルパスの生成
        if output_path is None:
            output_file = input_file.with_suffix('.md')
        else:
            output_file = Path(output_path)
        
        try:
            print(f"変換中: {input_file} -> {output_file}")
            
            # MarkItDownを使用して変換
            result = self.markitdown.convert(str(input_file))
            
            # 結果をファイルに保存
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(result.text_content)
            
            print(f"変換完了: {output_file}")
            print(f"ファイルサイズ: {output_file.stat().st_size:,} バイト")
            
            return True
            
        except Exception as e:
            print(f"エラー: 変換中にエラーが発生しました: {e}")
            return False
    
    def convert_multiple_files(self, input_directory: str, output_directory: Optional[str] = None) -> int:
        """
        ディレクトリ内の複数のPowerPointファイルを一括変換
        
        Args:
            input_directory: 入力ディレクトリのパス
            output_directory: 出力ディレクトリのパス（省略時は入力ディレクトリと同じ）
        
        Returns:
            int: 変換に成功したファイル数
        """
        input_dir = Path(input_directory)
        output_dir = Path(output_directory) if output_directory else input_dir
        
        if not input_dir.exists():
            print(f"エラー: ディレクトリが見つかりません: {input_directory}")
            return 0
        
        # 出力ディレクトリの作成
        output_dir.mkdir(exist_ok=True)
        
        # PowerPointファイルを検索
        pptx_files = list(input_dir.glob('*.pptx'))
        
        if not pptx_files:
            print(f"PowerPointファイルが見つかりません: {input_directory}")
            return 0
        
        print(f"{len(pptx_files)}個のPowerPointファイルが見つかりました")
        
        success_count = 0
        for pptx_file in pptx_files:
            output_file = output_dir / (pptx_file.stem + '.md')
            if self.convert_file(str(pptx_file), str(output_file)):
                success_count += 1
        
        print(f"変換完了: {success_count}/{len(pptx_files)}個のファイル")
        return success_count


def show_usage():
    """使用方法を表示"""
    print("PowerPoint to Markdown Converter")
    print("=====================================")
    print("Usage:")
    print("  python pptx_to_markdown.py                    # 対話式モード")
    print("  python pptx_to_markdown.py <input.pptx>       # 単一ファイル変換")
    print("  python pptx_to_markdown.py <input.pptx> <output.md>  # 出力ファイル指定")
    print("  python pptx_to_markdown.py --dir <directory>  # ディレクトリ一括変換")
    print("")
    print("Examples:")
    print("  python pptx_to_markdown.py presentation.pptx")
    print("  python pptx_to_markdown.py slides.pptx converted.md")
    print("  python pptx_to_markdown.py --dir ./presentations/")


def interactive_mode():
    """対話式モードでファイル変換"""
    converter = PowerPointToMarkdownConverter()
    
    while True:
        print("\n=== PowerPoint to Markdown Converter ===")
        print("1. 単一ファイル変換")
        print("2. ディレクトリ一括変換")
        print("3. 終了")
        
        choice = input("\n選択してください (1-3): ").strip()
        
        if choice == '1':
            input_path = input("PowerPointファイルのパスを入力してください: ").strip()
            if input_path:
                output_path = input("出力ファイル名（省略可）: ").strip()
                output_path = output_path if output_path else None
                converter.convert_file(input_path, output_path)
        
        elif choice == '2':
            input_dir = input("入力ディレクトリのパスを入力してください: ").strip()
            if input_dir:
                output_dir = input("出力ディレクトリ（省略可）: ").strip()
                output_dir = output_dir if output_dir else None
                converter.convert_multiple_files(input_dir, output_dir)
        
        elif choice == '3':
            print("終了します。")
            break
        
        else:
            print("無効な選択です。1-3を入力してください。")


def main():
    """メイン関数"""
    converter = PowerPointToMarkdownConverter()
    
    # コマンドライン引数の処理
    if len(sys.argv) == 1:
        # 引数なし: 対話式モード
        interactive_mode()
        
    elif len(sys.argv) == 2:
        arg = sys.argv[1]
        
        if arg in ['-h', '--help']:
            show_usage()
        elif arg == '--dir':
            print("エラー: ディレクトリパスを指定してください")
            show_usage()
        else:
            # 単一ファイル変換
            converter.convert_file(arg)
    
    elif len(sys.argv) == 3:
        if sys.argv[1] == '--dir':
            # ディレクトリ一括変換
            converter.convert_multiple_files(sys.argv[2])
        else:
            # 単一ファイル変換（出力ファイル指定）
            converter.convert_file(sys.argv[1], sys.argv[2])
    
    else:
        print("エラー: 引数が多すぎます")
        show_usage()


if __name__ == "__main__":
    main()