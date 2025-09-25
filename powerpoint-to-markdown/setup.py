#!/usr/bin/env python3
"""
PowerPoint to Markdown Converter - セットアップスクリプト

このスクリプトは必要な依存関係をインストールし、
変換ツールをすぐに使用できる状態にします。
"""

import subprocess
import sys
from pathlib import Path


def install_dependencies():
    """必要な依存関係をインストール"""
    print("=== PowerPoint to Markdown Converter セットアップ ===\n")
    
    requirements_file = Path(__file__).parent / "requirements.txt"
    
    if not requirements_file.exists():
        print("エラー: requirements.txt が見つかりません。")
        return False
    
    try:
        print("依存関係をインストール中...")
        print("実行コマンド: pip install -r requirements.txt\n")
        
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
        ], check=True, capture_output=True, text=True)
        
        print("✓ 依存関係のインストールが完了しました！\n")
        print(result.stdout)
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"✗ インストールに失敗しました: {e}")
        print(f"エラー出力: {e.stderr}")
        return False


def show_usage():
    """使用方法を表示"""
    print("=== 使用方法 ===")
    print("1. シンプル版（推奨）:")
    print("   python convert_pptx.py <PowerPointファイル>")
    print("   例: python convert_pptx.py presentation.pptx")
    print()
    print("2. フル機能版:")
    print("   python pptx_to_markdown.py")
    print("   （対話式モードで実行）")
    print()
    print("3. デモ版:")
    print("   python demo.py")
    print("   （現在のディレクトリの.pptxファイルを自動変換）")
    print()
    print("詳細な使用方法については README.md をご覧ください。")


def main():
    print("PowerPoint to Markdown Converter")
    print("=====================================")
    
    # 依存関係のインストール
    if install_dependencies():
        show_usage()
        print("\n✓ セットアップが完了しました！")
        print("変換ツールをお使いいただけます。")
    else:
        print("\n✗ セットアップに失敗しました。")
        print("手動で以下のコマンドを実行してください:")
        print("pip install markitdown[pptx]")
        sys.exit(1)


if __name__ == "__main__":
    main()