# Kemeny Extended Aggregator

このリポジトリには以下のサブプロジェクトが含まれています：

## 📁 powerpoint-to-markdown/

PowerPointファイル（.pptx）をMarkdown形式に変換するツール群です。

### 特徴
- MicrosoftのMarkItDownライブラリを使用
- 日本語ファイル名対応
- 複数の実行方法（CLI、対話式、自動検出）
- 一括変換機能

### 使用方法

1. ディレクトリに移動:
   ```bash
   cd powerpoint-to-markdown/
   ```

2. セットアップ実行:
   ```bash
   python setup.py
   ```

3. PowerPointファイルを変換:
   ```bash
   python convert_pptx.py your_presentation.pptx
   ```

詳細な使用方法については `powerpoint-to-markdown/README.md` をご覧ください。

## その他のファイル

- `卒業論文.pdf` - 卒業論文のPDFファイル
- `卒業論文_発表資料.pptx` - 発表用PowerPointファイル