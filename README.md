# Kemeny Extended Aggregator

ケアワーカー・被介護者マッチングシステム
拡張版KemenyルールとDeferred Acceptanceアルゴリズムを組み合わせ、主観的選好と客観的フィット度を統合した安定マッチングを実現するPythonシステムです。

## 概要
- 主観的選好（ランキング）と客観的フィット度（適合度スコア）を統合
- 厳格な制約（人数上限・フィット度整数・単射性）を自動検証
- CSVデータやPython辞書での入力に対応
- 結果はJSON等で出力

## ディレクトリ構成
```
algorithms/
    extended_kemeny_rule.py      # 拡張版Kemenyルール
## クイックスタート
```bash
git clone https://github.com/Krminfinity/kemeny-extended-aggregator.git
## 実行例
```bash
python algorithms/extended_kemeny_rule.py
## 主な機能
- 拡張版Kemenyルール: 主観・客観の統合ランキング
- Deferred Acceptance: 安定マッチング生成
- バリデーション: 人数・整数・単射性の自動検証
- CSV/辞書データ対応

## 制約条件（2025年9月実装）
- 被介護者・ケアワーカー各100人まで
- フィット度は整数のみ・重複禁止
- 入力時に全制約を自動検証

## ドキュメント
- [アルゴリズムフローチャート](docs/algorithm_flowchart.md)
- [CSV入力ガイド](docs/CSV_INPUT_GUIDE.md)
- [制約条件まとめ](thesis/ASSUMPTIONS_AND_CONSTRAINTS.md)

## ライセンス・著者
- 本システムは学術研究目的で開発されています
- Author: 倉持誠 (Makoto Kuramochi)
- Year: 2025
# Kemeny Extended Aggregator# ケアワーカー・被介護者マッチングシステム (Kemeny Extended Aggregator)



**ケアワーカー・被介護者マッチングシステム**拡張版Kemenyルールとdeferred acceptanceアルゴリズムを組み合わせた、ケアワーカーと被介護者の最適マッチングシステムです。主観的選好と客観的フィット度を統合した新しいアプローチで、安定かつ効率的なマッチングを実現します。



拡張版Kemenyルールとdeferred acceptanceアルゴリズムを組み合わせた、ケアワーカーと被介護者の最適マッチングを実現するシステムです。



## 🎯 概要## 概要「ケアワーカーと被介護者のマッチングアルゴリズムの開発」をテーマとした、拡張版Kemenyルールとdeferred acceptanceアルゴリズムを組み合わせたマッチングシステムです。卒業論文「ケアワー### 環境設定



このシステムは、介護分野における人材配置の最適化を目的とした研究プロジェクトです。主観的選好と客観的フィット度を統合した新しいアプローチで、安定かつ効率的なマッチングを実現します。



### 核心技術このシステムは、介護分野における人材配置の最適化を目的とした学術研究プロジェクトです。以下の2つのアルゴリズムを組み合わせて動作します

- **拡張版Kemenyルール**: 個人の選好と客観的適合度を統合

- **Deferred Acceptance**: 被介護者最適な安定マッチング生成

- **制約検証システム**: 厳格なデータ検証とエラーハンドリング

1. **拡張版Kemenyルール**: 個人の主観的選好と客観的フィット度を統合した選好順序の決定## 概要# リポジトリクローン

## 📁 プロジェクト構造

2. **Deferred Acceptance (DA) アルゴリズム**: 被介護者最適な安定マッチングの生成

```

kemeny-extended-aggregator/git clone https://github.com/Krminfinity/kemeny-extended-aggregator.git

├── algorithms/                 # 🔧 核心アルゴリズム

│   ├── extended_kemeny_rule.py     # 拡張版Kemenyルール実装## プロジェクト構造

│   ├── deferred_acceptance.py      # DAアルゴリズム実装

│   ├── care_matching_system.py     # 統合マッチングシステムこのシステムは、被介護者とケアワーカーの間で最適なマッチングを実現するために、以下の2つのアルゴリズムを組み合わせています：cd kemeny-extended-aggregator

│   ├── csv_matching_system.py      # CSV対応システム

│   └── validation.py              # データ検証・制約チェック```

├── docs/                      # 📚 ドキュメント

│   ├── algorithm_flowchart.md     # アルゴリズムフローチャートkemeny-extended-aggregator/

│   └── CSV_INPUT_GUIDE.md         # CSV入力ガイド

└── thesis/                    # 🎓 学術資料├── algorithms/                      # 核心アルゴリズム実装

    ├── ASSUMPTIONS_AND_CONSTRAINTS.md  # 理論的前提・制約条件

    ├── 論文.pdf                       # 研究論文│   ├── extended_kemeny_rule.py          # 拡張版Kemenyルール1. **拡張版Kemenyルール**: 主観的選好と客観的フィット度を統合した選好集約# 仮想環境作成・アクティベート

    └── 論文_発表資料.pptx             # 発表資料

```│   ├── deferred_acceptance.py           # DAアルゴリズム



## 🚀 クイックスタート│   ├── care_matching_system.py          # 統合マッチングシステム2. **Deferred Acceptance (DA) アルゴリズム**: 安定マッチングの生成python -m venv .venv



### 1. セットアップ│   ├── csv_matching_system.py           # CSV対応システム



```bash│   └── validation.py                   # データ検証・制約チェックsource .venv/bin/activate  # macOS/Linux

# リポジトリクローン

git clone https://github.com/Krminfinity/kemeny-extended-aggregator.git├── docs/                           # ドキュメント

cd kemeny-extended-aggregator

│   ├── algorithm_flowchart.md          # アルゴリズムフローチャート## プロジェクト構造# .venv\Scripts\activate  # Windows

# 依存関係インストール

pip install numpy│   └── CSV_INPUT_GUIDE.md              # CSV入力ガイド

```

└── thesis/                         # 学術資料

### 2. 基本実行

    ├── ASSUMPTIONS_AND_CONSTRAINTS.md  # 理論的前提・制約条件

```bash

# 拡張版Kemenyルールのデモ    ├── 論文.pdf                        # 研究論文```# 基本依存関係インストール

python algorithms/extended_kemeny_rule.py

    └── 論文_発表資料.pptx               # 発表資料

# DAアルゴリズムのデモ

python algorithms/deferred_acceptance.py```kemeny-extended-aggregator/pip install numpy pandas



# 統合システムのデモ

python algorithms/care_matching_system.py

```## 主要機能├── algorithms/              # 核心アルゴリズム



## 💡 主要機能



### 拡張版Kemenyルール### 1. 拡張版Kemenyルール (`extended_kemeny_rule.py`)│   ├── extended_kemeny_rule.py      # 拡張版Kemenyルール実装# PowerPoint変換ツール用（オプション）

- 主観的選好と客観的フィット度の重み付き統合

- 拡張された弱効率性・弱耐戦略性を保証- **主観的選好と客観的フィット度の統合**: 重み付きKemeny距離による最適化

- 柔軟な重み設定による調整

- **理論的保証**: 拡張された弱効率性と拡張された弱耐戦略性を満たす│   ├── deferred_acceptance.py       # DAアルゴリズム実装cd powerpoint-to-markdown

### Deferred Acceptance アルゴリズム

- 安定マッチングの生成（ブロッキングペア排除）- **柔軟な重み設定**: `preference_weight`と`fitness_weight`による調整可能

- 被介護者最適な結果の提供

- 容量制約への対応- **厳格な制約対応**: 整数フィット度・単射性・人数制限に対応│   ├── care_matching_system.py      # 統合マッチングシステムpip install -r requirements.txt



### 統合マッチングシステム

- エンドツーエンドのマッチングパイプライン

- 満足度分析と安定性チェック### 2. Deferred Acceptance アルゴリズム (`deferred_acceptance.py`)│   ├── csv_matching_system.py       # CSV対応マッチングシステムcd ..

- JSON形式での構造化出力

- **安定マッチング**: ブロッキングペアが存在しない組み合わせを生成

### CSV対応システム

- 表形式データからの直接処理- **被介護者最適**: 被介護者にとって最良の安定マッチングを提供│   └── validation.py               # データ検証・制約チェック

- 自動化されたワークフロー

- 多種データの統合処理- **容量制約対応**: ケアワーカーの受け入れ可能人数を考慮



### データ検証システム- **詳細ログ**: マッチング過程の完全な履歴記録├── docs/                    # ドキュメント# PDF変換ツール用（オプション）

- **人数制限**: 被介護者・ケアワーカー各100人まで

- **フィット度制約**: 整数値のみ、重複禁止

- **エラーハンドリング**: 詳細な制約違反メッセージ

### 3. 統合マッチングシステム (`care_matching_system.py`)│   ├── algorithm_flowchart.md      # アルゴリズムフローチャートpip install PyPDF2

## 📖 使用方法

- **完全なパイプライン**: データ入力からマッチング結果出力まで

### 基本的なプログラム使用

- **満足度分析**: マッチング品質の定量的評価│   ├── CSV_INPUT_GUIDE.md          # CSV入力ガイド```ルゴリズムの開発」で実装した、拡張版Kemenyルールとdeferred acceptanceアルゴリズムを組み合わせたマッチングシステムです。

```python

from algorithms.care_matching_system import CareMatchingSystem- **安定性チェック**: ブロッキングペアの検出と報告

from algorithms.validation import InputValidator

- **JSON出力**: 結果の構造化された保存│   ├── README_BLACKBOX_TESTS.md    # テスト使用方法

# データ検証

validator = InputValidator()

validator.validate_all_constraints(

    care_recipients, care_workers, ### 4. CSV対応システム (`csv_matching_system.py`)│   └── TEST_REPORT_SUMMARY.md      # テスト結果サマリー## 概要

    preferences, fitness_scores, capacities

)- **表形式データ対応**: CSVファイルからの直接データ読み込み



# マッチング実行- **多種データ統合**: 主観的選好・客観的フィット度・容量データの処理├── thesis/                  # 学術論文関連

system = CareMatchingSystem(preference_weight=1.0, fitness_weight=1.0)

result = system.create_complete_match(- **自動化されたワークフロー**: データ読み込みから結果出力まで自動実行

    care_recipients, care_workers,

    recipient_preferences, worker_preferences,│   ├── 論文.pdf                    # 論文本体このシステムは、被介護者とケアワーカーの間で最適なマッチングを実現するために、以下の2つのアルゴリズムを組み合わせています：

    recipient_fitness, worker_fitness, capacities

)### 5. データ検証システム (`validation.py`)



print("マッチング結果:", result["matches"])- **厳格な制約チェック**: 2025年9月に実装された制約条件の検証│   ├── 発表資料.pptx               # 発表スライド

print("満足度分析:", result["satisfaction_analysis"])

```- **エラーハンドリング**: 制約違反時の詳細なエラーメッセージ



### CSV入力での使用- **型安全性**: 入力データの型と値の整合性保証│   └── 発表資料.md                 # 発表資料マークダウン1. **拡張版Kemenyルール**: 主観的選好と客観的フィット度を統合した選好集約



```bash

# CSV対応システムの実行

python algorithms/csv_matching_system.py## 制約条件（2025年9月実装）├── powerpoint-to-markdown/  # PowerPoint→Markdown変換ツール2. **Deferred Acceptance (DA) アルゴリズム**: 安定マッチングの生成

```



詳細な入力形式については [CSV入力ガイド](docs/CSV_INPUT_GUIDE.md) を参照してください。

### データ制約│   ├── convert_pptx.py             # PowerPoint変換スクリプト

## ⚙️ 技術仕様

- **人数上限**: 被介護者・ケアワーカーそれぞれ最大100人

- **言語**: Python 3.7+

- **依存関係**: numpy- **フィット度制限**: 整数値のみ（実数値は拒否）│   ├── demo.py                     # デモ実行## プロジェクト構造

- **入力形式**: Python辞書, CSV

- **出力形式**: JSON, 構造化テキスト- **単射性**: フィット度の重複禁止（全て異なる値が必要）



## 🔒 制約条件（2025年9月実装）- **完全性**: 全ての選好関係が定義済みであること│   ├── pptx_to_markdown.py         # 変換処理本体



### データ制約

- **人数上限**: 被介護者・ケアワーカー各100人

- **フィット度**: 整数値のみ（実数値拒否）### 計算制約│   ├── README.md                   # 変換ツール説明```

- **単射性**: フィット度の重複禁止

- **計算複雑度**: O(n!)の拡張版Kemenyルール計算

### 計算制約

- **計算複雑度**: O(n!)のKemenyルール計算- **メモリ使用量**: 大規模データでの制限│   ├── requirements.txt            # 依存関係kemeny-extended-aggregator/

- **実行時間**: 現実的な処理時間での完了

- **実行時間**: 現実的な処理時間での完了保証

## 📋 ドキュメント

│   └── setup.py                    # セットアップ設定├── algorithms/              # 核心アルゴリズム

- **[アルゴリズムフローチャート](docs/algorithm_flowchart.md)**: システム処理フローの視覚化

- **[CSV入力ガイド](docs/CSV_INPUT_GUIDE.md)**: データ入力方法の詳細## クイックスタート

- **[前提・制約条件](thesis/ASSUMPTIONS_AND_CONSTRAINTS.md)**: 理論的基盤と制約の詳細

└── pdf-to-markdown/         # PDF→Markdown変換ツール│   ├── extended_kemeny_rule.py      # 拡張版Kemenyルール実装

## 🏆 学術的貢献

### 1. 環境設定

- **研究テーマ**: ケアワーカーと被介護者のマッチングアルゴリズムの開発

- **主要貢献**:     └── pdf_to_markdown.py          # PDF変換スクリプト│   ├── deferred_acceptance.py       # DAアルゴリズム実装

  - 主観的選好と客観的フィット度の統合理論

  - 実用的制約を考慮したマッチングシステム```bash

  - 包括的評価指標による性能検証

# リポジトリクローン```│   ├── care_matching_system.py      # 統合マッチングシステム

## 📄 ライセンス

git clone https://github.com/Krminfinity/kemeny-extended-aggregator.git

学術研究目的で開発されたプロジェクトです。

cd kemeny-extended-aggregator│   ├── csv_matching_system.py       # CSV対応マッチングシステム

## 🤝 貢献



バグ報告や機能提案は、GitHubのIssueからお願いします。

# 仮想環境作成（推奨）## 主な機能│   └── validation.py               # データ検証・制約チェック

---

python -m venv venv

**Author**: 倉持誠 (Makoto Kuramochi) | **Year**: 2025
source venv/bin/activate  # macOS/Linux├── docs/                    # ドキュメント

# venv\Scripts\activate   # Windows

### 核心アルゴリズム (`algorithms/`)│   ├── algorithm_flowchart.md      # アルゴリズムフローチャート

# 依存関係インストール

pip install numpy- **拡張版Kemenyルール**: 重み付きKemeny距離による選好統合│   ├── CSV_INPUT_GUIDE.md          # CSV入力ガイド

```

- **DAアルゴリズム**: 被介護者最適な安定マッチング│   ├── README_BLACKBOX_TESTS.md    # テスト使用方法

### 2. 基本的な使用方法

- **統合システム**: 完全なマッチングパイプライン│   └── TEST_REPORT_SUMMARY.md      # テスト結果サマリー

#### アルゴリズムの個別実行

- **CSV対応システム**: 表形式データ完全対応├── thesis/                  # 卒業論文関連

```bash

# 拡張版Kemenyルールのデモ実行- **データ検証**: 厳密な制約チェック・バリデーション機能│   ├── 卒業論文.pdf                # 卒業論文本体

python algorithms/extended_kemeny_rule.py

│   ├── 卒業論文_発表資料.pptx       # 発表スライド

# DAアルゴリズムのデモ実行

python algorithms/deferred_acceptance.py### ドキュメント (`docs/`)│   └── 卒業論文_発表資料.md         # 発表資料マークダウン



# 統合システムのデモ実行- **アルゴリズムフローチャート**: 処理の流れの可視化├── powerpoint-to-markdown/  # PowerPoint→Markdown変換ツール

python algorithms/care_matching_system.py

```- **CSV入力ガイド**: データ形式の詳細説明│   ├── convert_pptx.py             # PowerPoint変換スクリプト



#### CSV入力でのマッチング実行- **テスト説明書**: 検証手順とテスト結果│   ├── demo.py                     # デモ実行



```bash- **技術ドキュメント**: 実装の詳細説明│   ├── pptx_to_markdown.py         # 変換処理本体

# CSV対応システムの実行

python algorithms/csv_matching_system.py│   ├── README.md                   # 変換ツール説明

```

### 変換ツール│   ├── requirements.txt            # 依存関係

#### データ検証の実行

- **PowerPoint→Markdown変換**: プレゼン資料の文書化│   └── setup.py                    # セットアップ設定

```bash

# バリデーション機能のテスト- **PDF→Markdown変換**: PDF文書のテキスト抽出・変換└── pdf-to-markdown/         # PDF→Markdown変換ツール

python algorithms/validation.py

```    └── pdf_to_markdown.py          # PDF変換スクリプト



### 3. プログラムによる使用## クイックスタート```



```python

from algorithms.extended_kemeny_rule import ExtendedKemenyRule

from algorithms.deferred_acceptance import DeferredAcceptanceAlgorithm### 1. 環境設定## 主な機能

from algorithms.care_matching_system import CareMatchingSystem

from algorithms.validation import InputValidator, ConstraintViolationError```bash



# データ検証# リポジトリクローン### 核心アルゴリズム (`algorithms/`)

validator = InputValidator()

try:git clone https://github.com/Krminfinity/kemeny-extended-aggregator.git- **拡張版Kemenyルール**: 重み付きKemeny距離による選好統合

    validator.validate_all_constraints(

        care_recipients, care_workers, preferences, fitness_scores, capacitiescd kemeny-extended-aggregator- **DAアルゴリズム**: 被介護者最適な安定マッチング

    )

except ConstraintViolationError as e:- **統合システム**: 完全なマッチングパイプライン

    print(f"制約違反: {e}")

    exit(1)# 仮想環境作成・アクティベート- **CSV対応システム**: 表形式データ完全対応



# 統合システムの使用python -m venv .venv- **データ検証**: 厳密な制約チェック・バリデーション機能

system = CareMatchingSystem(preference_weight=1.0, fitness_weight=1.0)

result = system.create_complete_match(source .venv/bin/activate  # macOS/Linux

    care_recipients, care_workers, 

    recipient_preferences, worker_preferences,# .venv\Scripts\activate  # Windows### ドキュメント (`docs/`)

    recipient_fitness, worker_fitness, capacities

)- **アルゴリズムフローチャート**: 処理の流れの可視化



# 結果の表示# 基本依存関係インストール- **CSV入力ガイド**: データ形式の詳細説明

print("マッチング結果:", result["matches"])

print("満足度:", result["satisfaction_analysis"])pip install numpy pandas- **テスト説明書**: 検証手順とテスト結果

```

- **技術ドキュメント**: 実装の詳細説明

## アルゴリズムの特徴

# PowerPoint変換ツール用（オプション）

### 理論的基盤

- **拡張された弱効率性**: 出力されたランキングよりも良いランキングが存在しないcd powerpoint-to-markdown### 変換ツール

- **拡張された弱耐戦略性**: 虚偽申告による利得向上を防止

- **安定性**: DAアルゴリズムによるブロッキングペアの排除pip install -r requirements.txt- **PowerPoint→Markdown変換**: プレゼン資料の文書化



### 実装上の特徴cd ..- **PDF→Markdown変換**: PDF文書のテキスト抽出・変換

- **モジュラー設計**: 各アルゴリズムが独立して使用可能

- **詳細ログ**: 計算過程の完全な記録

- **エラーハンドリング**: 堅牢なエラー処理機能

- **拡張性**: 新しい制約条件や機能の追加が容易# PDF変換ツール用（オプション）## クイックスタート



## ドキュメントpip install PyPDF2



詳細なドキュメントが`docs/`フォルダに用意されています：```### 1. 環境設定



- **[アルゴリズムフローチャート](docs/algorithm_flowchart.md)**: システム全体の処理フローの視覚化```bash

- **[CSV入力ガイド](docs/CSV_INPUT_GUIDE.md)**: CSV形式でのデータ入力方法の詳細説明

### 2. 基本的な使用方法# リポジトリクローン

学術的背景については`thesis/`フォルダを参照：

git clone https://github.com/Krminfinity/kemeny-extended-aggregator.git

- **[前提・制約条件](thesis/ASSUMPTIONS_AND_CONSTRAINTS.md)**: 理論的基盤と実装制約の詳細

#### アルゴリズムの直接実行cd kemeny-extended-aggregator

## 技術仕様

```bash

- **言語**: Python 3.7+

- **主要ライブラリ**: numpy# 拡張版Kemenyルールのデモ# 仮想環境作成・アクティベート

- **アルゴリズム**: 拡張版Kemenyルール, Deferred Acceptance

- **入力形式**: Python辞書, CSVpython algorithms/extended_kemeny_rule.pypython -m venv .venv

- **出力形式**: JSON, 構造化テキスト

- **実行形式**: スタンドアロン, モジュール, CSV一括処理.venv\Scripts\activate  # Windows



## 学術情報# DAアルゴリズムのデモ  # source .venv/bin/activate  # macOS/Linux



このプロジェクトは以下の研究に基づいています：python algorithms/deferred_acceptance.py



- **研究テーマ**: 「ケアワーカーと被介護者のマッチングアルゴリズムの開発」# 依存関係インストール

- **著者**: 倉持誠 (Makoto Kuramochi)

- **年度**: 2025年# 統合システムのデモpip install numpy pandas reportlab openpyxl

- **主要貢献**: 

  1. 主観的選好と客観的フィット度の統合理論python algorithms/care_matching_system.py```

  2. 実用的制約を考慮したマッチングシステム

  3. 包括的な評価指標による性能検証```



## 使用例### 2. 基本的な使用方法



### 基本的なマッチング実行#### CSV入力でのマッチング実行



```python```bash#### アルゴリズムの直接実行

# 簡単な例：3人の被介護者と3人のケアワーカー

care_recipients = [4, 5, 6]# CSV入力システム実行```bash

care_workers = [1, 2, 3]

python algorithms/csv_matching_system.py# 拡張版Kemenyルールのデモ

# 選好（1が最も好ましい）

recipient_prefs = {4: [1, 2, 3], 5: [3, 1, 2], 6: [2, 3, 1]}```python algorithms/extended_kemeny_rule.py

worker_prefs = {1: [4, 5, 6], 2: [5, 4, 6], 3: [6, 4, 5]}



# フィット度（整数、重複なし）

recipient_fitness = {4: [90, 80, 70], 5: [85, 95, 75], 6: [88, 78, 98]}#### 変換ツールの使用# DAアルゴリズムのデモ  

worker_fitness = {1: [92, 87, 83], 2: [89, 91, 85], 3: [86, 84, 96]}

```bashpython algorithms/deferred_acceptance.py

# 容量

capacities = {1: 1, 2: 1, 3: 1}# PowerPoint→Markdown変換



# マッチング実行cd powerpoint-to-markdown# 統合システムのデモ

system = CareMatchingSystem()

result = system.create_complete_match(python convert_pptx.py "path/to/presentation.pptx"python algorithms/care_matching_system.py

    care_recipients, care_workers,

    recipient_prefs, worker_prefs,```

    recipient_fitness, worker_fitness,

    capacities# PDF→Markdown変換  

)

```python pdf_to_markdown.py "path/to/document.pdf"#### CSV入力でのマッチング実行



## ライセンス``````bash



このプロジェクトは学術研究目的で開発されました。商用利用については著者にお問い合わせください。# CSV入力システム実行



## 貢献・フィードバック## アルゴリズムの特徴python algorithms/csv_matching_system.py



バグ報告、機能提案、または学術的な議論については、GitHubのIssueまたは著者まで直接ご連絡ください。```



## 更新履歴### 拡張版Kemenyルール



- **2025年9月**: 厳格な制約条件の実装（人数制限、整数フィット度、単射性）- **主観的選好と客観的フィット度の統合**: 重み付きKemeny距離による最適化#### 変換ツールの使用

- **初期版**: 基本的な拡張版Kemenyルール・DAアルゴリズムの実装
- **理論的保証**: 拡張された弱効率性と拡張された弱耐戦略性を満たす```bash

- **柔軟な重み設定**: preference_weightとfitness_weightによる調整可能# PowerPoint→Markdown変換

cd powerpoint-to-markdown

### Deferred Acceptance (DA) アルゴリズムpython convert_pptx.py "path/to/presentation.pptx"

- **安定マッチング**: ブロッキングペアが存在しない安定な組み合わせ

- **被介護者最適**: 被介護者にとって最良の安定マッチングを生成# PDF→Markdown変換  

- **容量制約対応**: ケアワーカーの受け入れ可能人数を考慮python pdf_to_markdown.py "path/to/document.pdf"

```

### データ検証機能

- **厳密な制約チェック**: 人数上限、フィット度整数制限、単射性検証## アルゴリズムの特徴

- **エラー処理**: 制約違反時の詳細なエラーメッセージ

- **データ整合性**: 入力データの自動検証### 拡張版Kemenyルール

- **主観的選好と客観的フィット度の統合**: 重み付きKemeny距離による最適化

## ドキュメント- **理論的保証**: 拡張された弱効率性と拡張された弱耐戦略性を満たす

- **柔軟な重み設定**: preference_weightとfitness_weightによる調整可能

詳細なドキュメントは `docs/` フォルダに格納されています：

### Deferred Acceptance (DA) アルゴリズム

- **[アルゴリズムフローチャート](docs/algorithm_flowchart.md)**: 処理フローの視覚化- **安定マッチング**: ブロッキングペアが存在しない安定な組み合わせ

- **[CSV入力ガイド](docs/CSV_INPUT_GUIDE.md)**: CSV形式データの作成・使用方法- **被介護者最適**: 被介護者にとって最良の安定マッチングを生成

- **[テスト使用方法](docs/README_BLACKBOX_TESTS.md)**: アルゴリズム検証の詳細手順- **容量制約対応**: ケアワーカーの受け入れ可能人数を考慮

- **[テスト結果サマリー](docs/TEST_REPORT_SUMMARY.md)**: 包括的テスト結果レポート

### データ検証機能

## 学術情報- **厳密な制約チェック**: 人数上限、フィット度整数制限、単射性検証

- **エラー処理**: 制約違反時の詳細なエラーメッセージ

このプロジェクトは以下の研究論文に基づいています：- **データ整合性**: 入力データの自動検証



- **論文**: 「ケアワーカーと被介護者のマッチングアルゴリズムの開発」## ドキュメント

- **著者**: 倉持誠 (Makoto Kuramochi)

- **年度**: 2025年詳細なドキュメントは `docs/` フォルダに格納されています：

- **資料**: `thesis/` フォルダに格納

- **[アルゴリズムフローチャート](docs/algorithm_flowchart.md)**: 処理フローの視覚化

### 主要な貢献- **[CSV入力ガイド](docs/CSV_INPUT_GUIDE.md)**: CSV形式データの作成・使用方法

1. **拡張版Kemenyルール**: 主観的選好と客観的フィット度の重み付き統合- **[テスト使用方法](docs/README_BLACKBOX_TESTS.md)**: アルゴリズム検証の詳細手順

2. **実用的マッチングシステム**: 現実的な制約を考慮した安定マッチング- **[テスト結果サマリー](docs/TEST_REPORT_SUMMARY.md)**: 包括的テスト結果レポート

3. **包括的評価**: 多角的な評価指標による性能検証

## 学術情報

## 技術仕様

このプロジェクトは以下の卒業論文に基づいています：

- **言語**: Python 3.9+

- **主要ライブラリ**: numpy, pandas- **論文**: 「ケアワーカーと被介護者のマッチングアルゴリズムの開発」

- **変換ツール**: python-pptx, PyPDF2- **著者**: 倉持誠 (Makoto Kuramochi)

- **アルゴリズム**: 拡張版Kemenyルール, Deferred Acceptance- **年度**: 2025年

- **入力形式**: Python辞書, CSV, PowerPoint, PDF- **資料**: `thesis/` フォルダに格納

- **出力形式**: JSON, CSV, Markdown

### 主要な貢献

## 制約事項1. **拡張版Kemenyルール**: 主観的選好と客観的フィット度の重み付き統合

2. **実用的マッチングシステム**: 現実的な制約を考慮した安定マッチング

### データ制約3. **包括的評価**: 多角的な評価指標による性能検証

- **人数上限**: 被介護者・ケアワーカーそれぞれ最大50人（計算量考慮）

- **フィット度**: 整数値のみ（実数値は拒否）## 技術仕様

- **単射性**: フィット度の重複は禁止（一意性が必要）

- **言語**: Python 3.9+

### 技術制約- **主要ライブラリ**: numpy, pandas

- **メモリ使用量**: O(n!) の計算複雑度（Kemenyルール）- **変換ツール**: python-pptx, PyPDF2

- **実行時間**: 大規模データでは処理時間が増大- **アルゴリズム**: 拡張版Kemenyルール, Deferred Acceptance

- **数値精度**: 整数演算による高精度計算- **入力形式**: Python辞書, CSV, PowerPoint, PDF

- **出力形式**: JSON, CSV, Markdown

## 使用例

## 制約事項

### プログラムによる使用

```python### データ制約

from algorithms.extended_kemeny_rule import ExtendedKemenyRule- **人数上限**: 被介護者・ケアワーカーそれぞれ最大50人（計算量考慮）

from algorithms.deferred_acceptance import DeferredAcceptanceAlgorithm- **フィット度**: 整数値のみ（実数値は拒否）

from algorithms.validation import validate_input_data- **単射性**: フィット度の重複は禁止（一意性が必要）



# データ検証### 技術制約

is_valid, errors = validate_input_data(care_recipients, care_workers, - **メモリ使用量**: O(n!) の計算複雑度（Kemenyルール）

                                     preferences, fitness_scores)- **実行時間**: 大規模データでは処理時間が増大

- **数値精度**: 整数演算による高精度計算

# 拡張版Kemenyルール

kemeny = ExtendedKemenyRule(preference_weight=1.0, fitness_weight=1.0)## 使用例

ranking, details = kemeny.aggregate_preferences([2,1,0], [0.8,0.9,0.7])

### プログラムによる使用

# DAアルゴリズム```python

da = DeferredAcceptanceAlgorithm()from algorithms.extended_kemeny_rule import ExtendedKemenyRule

matches, details = da.create_match(recipients, caregivers, from algorithms.deferred_acceptance import DeferredAcceptanceAlgorithm

                                  recipient_prefs, caregiver_prefs, capacities)from algorithms.validation import validate_input_data

```

# データ検証

### CSV入力による使用is_valid, errors = validate_input_data(care_recipients, care_workers, 

1. CSV形式のデータファイルを準備                                     preferences, fitness_scores)

2. `python algorithms/csv_matching_system.py` で実行

3. マッチング結果をJSON形式で出力# 拡張版Kemenyルール

kemeny = ExtendedKemenyRule(preference_weight=1.0, fitness_weight=1.0)

### 文書変換の使用ranking, details = kemeny.aggregate_preferences([2,1,0], [0.8,0.9,0.7])

```python

# PowerPoint変換# DAアルゴリズム

from powerpoint_to_markdown.convert_pptx import convert_pptx_to_markdownda = DeferredAcceptanceAlgorithm()

markdown_content = convert_pptx_to_markdown("presentation.pptx")matches, details = da.create_match(recipients, caregivers, 

                                  recipient_prefs, caregiver_prefs, capacities)

# PDF変換```

from pdf_to_markdown import pdf_to_markdown

markdown_content = pdf_to_markdown("document.pdf")### CSV入力による使用

```1. CSV形式のデータファイルを準備
2. `python algorithms/csv_matching_system.py` で実行
3. マッチング結果をJSON形式で出力

### 文書変換の使用
```python
# PowerPoint変換
from powerpoint_to_markdown.convert_pptx import convert_pptx_to_markdown
markdown_content = convert_pptx_to_markdown("presentation.pptx")

# PDF変換
from pdf_to_markdown import pdf_to_markdown
markdown_content = pdf_to_markdown("document.pdf")
```
