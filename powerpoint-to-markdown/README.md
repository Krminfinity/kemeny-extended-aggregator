# PowerPoint to Markdown Converter

PowerPointファイル（.pptx）をMarkdown形式に変換するPythonプログラムです。MicrosoftのMarkItDownライブラリを使用して、スライドの内容をテキスト形式で抽出し、Markdownファイルとして保存します。

## 機能

- **単一ファイル変換**: PowerPointファイル1つをMarkdownに変換
- **一括変換**: ディレクトリ内の複数のPowerPointファイルを一度に変換
- **対話式モード**: コマンドライン引数なしで実行すると対話的に操作可能
- **エラーハンドリング**: ファイルの存在確認と適切なエラーメッセージ表示

## インストール

### 1. 必要な依存関係をインストール

```bash
pip install -r requirements.txt
```

または個別にインストール：

```bash
pip install markitdown
```

### 2. プログラムファイルをダウンロード

このリポジトリから以下のファイルをダウンロードしてください：
- `pptx_to_markdown.py` - フル機能版
- `convert_pptx.py` - シンプル版

## 使用方法

### シンプル版（convert_pptx.py）

最も簡単な使用方法：

```bash
# 基本的な使用方法
python convert_pptx.py presentation.pptx

# 出力ファイル名を指定
python convert_pptx.py slides.pptx output.md

# ヘルプを表示
python convert_pptx.py --help

# 詳細出力モード
python convert_pptx.py -v presentation.pptx
```

### フル機能版（pptx_to_markdown.py）

#### 1. 対話式モード（推奨）

```bash
python pptx_to_markdown.py
```

実行すると以下のメニューが表示されます：
```
=== PowerPoint to Markdown Converter ===
1. 単一ファイル変換
2. ディレクトリ一括変換
3. 終了

選択してください (1-3):
```

#### 2. コマンドライン実行

```bash
# 単一ファイル変換（出力ファイル名は自動生成）
python pptx_to_markdown.py presentation.pptx

# 出力ファイル名を指定
python pptx_to_markdown.py slides.pptx converted.md

# ディレクトリ内の全PowerPointファイルを一括変換
python pptx_to_markdown.py --dir ./presentations/

# 使用方法を表示
python pptx_to_markdown.py --help
```

## 実行例

### 単一ファイルの変換

```bash
$ python convert_pptx.py "卒業論文_発表資料.pptx"
変換開始: 卒業論文_発表資料.pptx
変換完了: /Users/username/卒業論文_発表資料.md
出力サイズ: 2,847 文字
```

### 複数ファイルの一括変換

```bash
$ python pptx_to_markdown.py --dir ./slides/
3個のPowerPointファイルが見つかりました
変換中: slide1.pptx -> slide1.md
変換完了: slide1.md
変換中: slide2.pptx -> slide2.md
変換完了: slide2.md
変換中: slide3.pptx -> slide3.md
変換完了: slide3.md
変換完了: 3/3個のファイル
```

## 出力形式

変換されたMarkdownファイルには以下の内容が含まれます：

- スライドのタイトル
- テキストコンテンツ
- 表形式のデータ（Markdownテーブルとして）
- スライドノート（存在する場合）

### 出力例

```markdown
# プレゼンテーションタイトル

## スライド1: 概要

- 要点1
- 要点2
- 要点3

## スライド2: データ分析

| 項目 | 値 | 前年比 |
|------|----|----|
| 売上 | 1000万円 | +10% |
| 利益 | 200万円 | +15% |
```

## トラブルシューティング

### よくあるエラーと解決方法

1. **ModuleNotFoundError: No module named 'markitdown'**
   ```bash
   pip install markitdown
   ```

2. **ファイルが見つからないエラー**
   - ファイルパスが正しいか確認
   - ファイル名に特殊文字が含まれていないか確認

3. **変換に失敗する場合**
   - PowerPointファイルが破損していないか確認
   - ファイルが他のアプリケーションで開かれていないか確認

### ログ出力

詳細なログが必要な場合は、`-v`オプション付きで実行してください：

```bash
python convert_pptx.py -v presentation.pptx
```

## ライセンス

このプログラムはMIT Licenseの下で公開されています。

## 参考資料

- [MarkItDown GitHub リポジトリ](https://github.com/microsoft/markitdown)
- [MarkItDown の詳細な使用方法（Qiita記事）](https://qiita.com/manabian/items/...)

## 更新履歴

- v1.0.0: 初回リリース
  - 単一ファイル変換機能
  - 一括変換機能
  - 対話式モード
  - エラーハンドリング

## サポート

問題や質問がある場合は、GitHubのIssuesページでお知らせください。