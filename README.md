# Kemeny Extended Aggregator

ケアワーカーと被介護者のマッチングアルゴリズムの実装

## 概要

このプロジェクトは、卒業論文「ケアワーカーと被介護者のマッチングアルゴリズムの開発」で提案されたマッチングシステムの実装です。主観的選好と客観的フィット度を統合し、安定マッチングを生成します。

## 主要機能

### 🔧 アルゴリズム
- **拡張版Kemenyルール**: 主観的選好と客観的フィット度を統合
- **Deferred Acceptance (DA)**: 安定マッチングを生成
- **制約検証**: 厳格なデータ検証機能

### 📊 入力方式
- **プログラム内定義**: サンプルデータを使った実行
- **CSV入力**: 外部CSVファイルからのデータ読み込み

## クイックスタート

### 1. 基本実行
```bash
cd algorithms
python care_matching_system.py
```

### 2. CSV入力での実行
```bash
cd algorithms
python csv_matching_system.py
```

### 3. 個別アルゴリズムのテスト
```bash
# 拡張版Kemenyルールのみ
python extended_kemeny_rule.py

# DAアルゴリズムのみ
python deferred_acceptance.py

# 制約検証のテスト
python validation.py
```

## ファイル構成

```
algorithms/
├── care_matching_system.py      # メインシステム
├── csv_matching_system.py       # CSV対応システム
├── extended_kemeny_rule.py      # 拡張版Kemenyルール
├── deferred_acceptance.py       # DAアルゴリズム
└── validation.py                # 制約検証

docs/
├── CSV_INPUT_GUIDE.md          # CSV入力ガイド
└── algorithm_flowchart.md      # アルゴリズムフローチャート

thesis/
├── ASSUMPTIONS_AND_CONSTRAINTS.md  # 制約条件
├── 論文.pdf                    # 卒業論文
└── 論文_発表資料.pptx          # 発表資料
```

## 制約条件（2025年9月更新）

- **参加者数制限**: 被介護者・ケアワーカー各100人まで
- **フィット度**: 整数値のみ（実数不可）
- **単射性**: 同一人物のフィット度は重複なし
- **完全性**: 全ての選好データが必須

## 使用例

### Python内での実行
```python
from care_matching_system import CareMatchingSystem

# システム初期化
system = CareMatchingSystem(preference_weight=1.0, fitness_weight=1.0)

# マッチング実行
results = system.run_complete_matching()

# 結果表示
system.print_complete_results(results)
```

### CSV入力での実行
```python
from csv_matching_system import CSVMatchingSystem

# システム初期化
system = CSVMatchingSystem()

# CSVからマッチング実行
result = system.run_complete_matching_from_csv(
    receiver_subjective_csv="care_receiver_subjective_preferences.csv",
    receiver_objective_csv="care_receiver_objective_fitness.csv",
    worker_subjective_csv="care_worker_subjective_preferences.csv",
    worker_objective_csv="care_worker_objective_fitness.csv",
    worker_capacity_csv="care_worker_capacity.csv"
)
```

## 出力

- **コンソール**: マッチング過程と結果の詳細表示
- **JSON**: 完全な結果データ（`matching_results.json`）
- **満足度分析**: 被介護者・ケアワーカー双方の満足度
- **安定性チェック**: マッチングの安定性評価

## 技術仕様

- **言語**: Python 3.7+
- **依存関係**: NumPy
- **アルゴリズム複雑度**: O(n! × n²)
- **制約**: n ≤ 100（実用的な計算時間を保証）

## 参考文献

論文「ケアワーカーと被介護者のマッチングアルゴリズムの開発」（2025年）

## 作者

倉持誠 (Makoto Kuramochi)

## ライセンス

このプロジェクトは学術研究目的で作成されました。