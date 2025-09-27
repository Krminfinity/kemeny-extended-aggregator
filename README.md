# ケアワーカー・被介護者マッチングシステム (Kemeny Extended Aggregator)

卒業論文「ケアワーカーと被介護者のマッチングアルゴリズムの開発」で実装した、拡張版Kemenyルールとdeferred acceptanceアルゴリズムを組み合わせたマッチングシステムです。

## 🎯 概要

このシステムは、被介護者とケアワーカーの間で最適なマッチングを実現するために、以下の2つのアルゴリズムを組み合わせています：

1. **拡張版Kemenyルール**: 主観的選好と客観的フィット度を統合した選好集約
2. **Deferred Acceptance (DA) アルゴリズム**: 安定マッチングの生成

## 📁 プロジェクト構造

```
kemeny-extended-aggregator/
├── algorithms/              # 🧮 核心アルゴリズム
│   ├── extended_kemeny_rule.py      # 拡張版Kemenyルール実装
│   ├── deferred_acceptance.py       # DAアルゴリズム実装
│   ├── care_matching_system.py      # 統合マッチングシステム
│   └── csv_matching_system.py       # CSV対応マッチングシステム
├── tests/                   # 🧪 テスト・検証
│   ├── test_data_extended_kemeny.py # 拡張版Kemenyルールテスト
│   ├── test_data_da.py              # DAアルゴリズムテスト
│   └── integrated_test_runner.py    # 統合テストランナー
├── data/                    # 📊 入力データ
│   ├── csv_input_handler.py         # CSV入力処理
│   ├── care_receiver_*.csv          # 被介護者データ
│   └── care_worker_*.csv            # ケアワーカーデータ
├── scripts/                 # 🔧 ユーティリティスクリプト
│   ├── generate_test_report.py      # PDFレポート生成
│   ├── generate_excel_report.py     # Excelレポート生成
│   └── run_organized_tests.py       # 整理後テスト実行
├── results/                 # 📈 実行結果・出力
│   ├── integrated_test_results.json # 統合テスト結果
│   ├── *_test_results.csv          # CSV形式テスト結果
│   └── matching_results.json       # マッチング結果
├── reports/                 # 📄 生成レポート
│   ├── test_results_report.pdf     # PDFテストレポート
│   └── detailed_test_results.xlsx  # Excel詳細レポート
├── docs/                    # 📚 ドキュメント
│   ├── README_BLACKBOX_TESTS.md    # テスト使用方法
│   ├── CSV_INPUT_GUIDE.md          # CSV入力ガイド
│   ├── algorithm_flowchart.md      # アルゴリズムフローチャート
│   └── TEST_REPORT_SUMMARY.md      # テスト結果サマリー
├── thesis/                  # 🎓 卒業論文関連
│   ├── 卒業論文.pdf                # 卒業論文本体
│   ├── 卒業論文_発表資料.pptx       # 発表スライド
│   └── 卒業論文_発表資料.md         # 発表資料マークダウン
└── powerpoint-to-markdown/  # 🔄 変換ツール
```

## 🚀 主な機能

### ✨ 核心アルゴリズム (`algorithms/`)
- **拡張版Kemenyルール**: 重み付きKemeny距離による選好統合
- **DAアルゴリズム**: 被介護者最適な安定マッチング
- **統合システム**: 完全なマッチングパイプライン
- **CSV対応システム**: 表形式データ完全対応

### 📊 データ処理 (`data/`)
- **CSV入力処理**: 表形式データの読み込み・検証
- **データ整合性チェック**: 自動的なデータ検証
- **サンプルデータ**: テスト用CSVファイル群
- **多形式サポート**: 主観的選好・客観的フィット度・容量データ

### 🧪 テスト・検証 (`tests/`)
- **包括的テストスイート**: 20個のテストケース（100%成功率）
- **ブラックボックステスト**: アルゴリズム動作の完全検証
- **統合テストランナー**: 一括テスト実行・レポート機能
- **詳細ログ**: 計算過程の完全な記録

### 📈 レポート・分析 (`reports/`, `results/`)
- **PDF/Excelレポート**: 包括的なテスト結果レポート
- **満足度分析**: マッチング品質の定量評価
- **安定性チェック**: ブロッキングペアの検出
- **多形式出力**: JSON, CSV, PDF, Excel対応

## 🏃‍♂️ クイックスタート

### 1. 環境設定
```bash
# リポジトリクローン
git clone https://github.com/Krminfinity/kemeny-extended-aggregator.git
cd kemeny-extended-aggregator

# 仮想環境作成・アクティベート
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # macOS/Linux

# 依存関係インストール
pip install numpy pandas reportlab openpyxl
```

### 2. 基本的な使用方法

#### アルゴリズムの直接実行
```bash
# 拡張版Kemenyルールのデモ
python algorithms/extended_kemeny_rule.py

# DAアルゴリズムのデモ  
python algorithms/deferred_acceptance.py

# 統合システムのデモ
python algorithms/care_matching_system.py
```

#### CSV入力でのマッチング実行
```bash
# CSV入力システム実行
python algorithms/csv_matching_system.py
```

#### テスト実行
```bash
# 全テスト実行
python tests/integrated_test_runner.py

# 特定アルゴリズムのテスト
python tests/integrated_test_runner.py --kemeny
python tests/integrated_test_runner.py --da

# 特定テストケース実行
python tests/integrated_test_runner.py --test kemeny basic_3_candidates
```

#### レポート生成
```bash
# PDFレポート生成
python scripts/generate_test_report.py

# Excelレポート生成
python scripts/generate_excel_report.py
```

## 📊 テスト結果

### 🏆 テスト結果サマリー

| アルゴリズム | テスト数 | 成功 | 失敗 | 成功率 |
|-------------|---------|------|------|--------|
| **拡張版Kemenyルール** | 10 | 10 | 0 | **100.0%** |
| **DAアルゴリズム** | 10 | 10 | 0 | **100.0%** |
| **全体** | **20** | **20** | **0** | **🎉 100.0%** |

### 📋 テストケース概要

#### 拡張版Kemenyルール (10ケース)
- 基本的なケース・完全一致・完全不一致
- 重み付け設定（選好重視・フィット度重視）
- エッジケース（同点・極端差・単一考慮など）

#### DAアルゴリズム (10ケース)  
- 論文例・バランス・容量不足・大容量
- 特殊ケース（同一選好・循環選好・空選好など）
- スケーラビリティ（大規模ケース）

## 📖 ドキュメント

詳細なドキュメントは `docs/` フォルダに格納されています：

- 📚 **[テスト使用方法](docs/README_BLACKBOX_TESTS.md)**: ブラックボックステストの詳細手順
- 📊 **[CSV入力ガイド](docs/CSV_INPUT_GUIDE.md)**: CSV形式データの作成・使用方法
- 🔄 **[アルゴリズムフローチャート](docs/algorithm_flowchart.md)**: 処理フローの視覚化
- 📈 **[テスト結果サマリー](docs/TEST_REPORT_SUMMARY.md)**: 包括的テスト結果レポート

## 🎓 学術情報

このプロジェクトは以下の卒業論文に基づいています：

- **論文**: 「ケアワーカーと被介護者のマッチングアルゴリズムの開発」
- **著者**: 倉持誠 (Makoto Kuramochi)
- **年度**: 2025年
- **資料**: `thesis/` フォルダに格納

### 主要な貢献
1. **拡張版Kemenyルール**: 主観的選好と客観的フィット度の重み付き統合
2. **実用的マッチングシステム**: 現実的な制約を考慮した安定マッチング
3. **包括的評価**: 多角的な評価指標による性能検証

## 🛠️ 技術仕様

- **言語**: Python 3.13+
- **主要ライブラリ**: numpy, pandas, reportlab, openpyxl
- **アルゴリズム**: 拡張版Kemenyルール, Deferred Acceptance
- **入力形式**: Python辞書, CSV
- **出力形式**: JSON, CSV, PDF, Excel

## 📊 出力形式

### マッチング結果
- **JSON**: 詳細な計算過程を含む完全な結果
- **CSV**: 表形式での結果出力

### テスト結果
- **PDF**: 印刷に適した統合レポート
- **Excel**: データ分析に適した多シート詳細レポート
- **CSV**: データ処理用軽量ファイル

## 🤝 使用例

### プログラムによる使用
```python
from algorithms.extended_kemeny_rule import ExtendedKemenyRule
from algorithms.deferred_acceptance import DeferredAcceptanceAlgorithm

# 拡張版Kemenyルール
kemeny = ExtendedKemenyRule(preference_weight=1.0, fitness_weight=1.0)
ranking, details = kemeny.aggregate_preferences([2,1,0], [0.8,0.9,0.7])

# DAアルゴリズム
da = DeferredAcceptanceAlgorithm()
matches, details = da.create_match(recipients, caregivers, 
                                  recipient_prefs, caregiver_prefs, capacities)
```

### CSV入力による使用
1. `data/` フォルダのサンプルCSVを参考にデータ作成
2. `python algorithms/csv_matching_system.py` で実行
3. `results/` フォルダで結果確認

## 📄 ライセンス

このプロジェクトは学術研究目的で作成されました。商用利用の場合は著者にお問い合わせください。

## 👤 著者

**倉持誠 (Makoto Kuramochi)**
- 卒業論文「ケアワーカーと被介護者のマッチングアルゴリズムの開発」
- GitHub: [@Krminfinity](https://github.com/Krminfinity)

---

**最終更新**: 2025年9月27日