# ケアワーカー・被介護者マッチングシステム (Kemeny Extended Aggregator)

卒業論文「ケアワーカーと被介護者のマッチングアルゴリズムの開発」で実装した、拡張版Kemenyルールとdeferred acceptanceアルゴリズムを組み合わせたマッチングシステムです。

## 🎯 概要

このシステムは、被介護者とケアワーカーの間で最適なマッチングを実現するために、以下の2つのアルゴリズムを組み合わせています：

1. **拡張版Kemenyルール**: 主観的選好と客観的フィット度を統合した選好集約
2. **Deferred Acceptance (DA) アルゴリズム**: 安定マッチングの生成

## 🚀 主な機能

### ✨ 核心アルゴリズム
- **拡張版Kemenyルール** (`extended_kemeny_rule.py`): 重み付きKemeny距離による選好統合
- **DAアルゴリズム** (`deferred_acceptance.py`): 被介護者最適な安定マッチング
- **統合システム** (`care_matching_system.py`): 完全なマッチングパイプライン

### 📊 CSV入力機能
- **CSV入力処理** (`csv_input_handler.py`): 表形式データの読み込み
- **CSV対応システム** (`csv_matching_system.py`): CSV入力完全対応
- **データ整合性チェック**: 自動的なデータ検証
- **サンプルファイル生成**: テスト用CSVの自動作成

### 📈 分析・可視化
- **満足度分析**: マッチング品質の定量評価
- **安定性チェック**: ブロッキングペアの検出
- **フローチャート** (`algorithm_flowchart.md`): アルゴリズムの視覚化
- **詳細ログ**: 計算過程の完全な記録

## 📋 必要なファイル

### CSV入力ファイル (5つのファイルが必要)

1. `care_receiver_subjective_preferences.csv` - 被介護者の主観的選好
2. `care_receiver_objective_fitness.csv` - 被介護者の客観的フィット度  
3. `care_worker_subjective_preferences.csv` - ケアワーカーの主観的選好
4. `care_worker_objective_fitness.csv` - ケアワーカーの客観的フィット度
5. `care_worker_capacity.csv` - ケアワーカーの容量情報

詳細な形式については [`CSV_INPUT_GUIDE.md`](CSV_INPUT_GUIDE.md) をご覧ください。

## 🏃‍♂️ クイックスタート

### 1. 基本システムの実行
```bash
python care_matching_system.py
```

### 2. CSV入力システムの実行
```bash
python csv_matching_system.py
```

### 3. サンプルデータでのテスト
```python
from csv_matching_system import demo_csv_matching
demo_csv_matching()  # サンプルCSVファイルを生成して実行
```

### 4. カスタムデータでの実行
```python
from csv_matching_system import CSVMatchingSystem

system = CSVMatchingSystem()
result = system.run_complete_matching_from_csv(
    "your_receiver_subjective.csv",
    "your_receiver_objective.csv", 
    "your_worker_subjective.csv",
    "your_worker_objective.csv",
    "your_worker_capacity.csv",
    w_subjective=1.0,  # 主観的選好の重み
    w_objective=1.0    # 客観的フィット度の重み
)
```

## 📚 ドキュメント

- [`CSV_INPUT_GUIDE.md`](CSV_INPUT_GUIDE.md) - CSV入力機能の詳細ガイド
- [`algorithm_flowchart.md`](algorithm_flowchart.md) - アルゴリズムフローチャート
- [`卒業論文_発表資料.md`](卒業論文_発表資料.md) - 研究発表資料

## 🔬 アルゴリズムの詳細

### 拡張版Kemenyルール
- 主観的選好 (ランキング) と客観的フィット度 (レイティング) を統合
- 重み付きKemeny距離による最適順列の選択
- 全順列探索による厳密解の計算

### DAアルゴリズム
- 被介護者側最適な安定マッチング
- 容量制約対応
- ブロッキングペアの排除

## 📊 出力結果

- **マッチング結果**: 最終的なペアリング
- **満足度分析**: 各エージェントの満足度
- **安定性評価**: マッチングの安定性
- **統計情報**: マッチング率、利用率など
- **JSON出力**: 全結果データの保存

## 🔧 その他のツール

### 📁 powerpoint-to-markdown/
PowerPointファイル（.pptx）をMarkdown形式に変換するユーティリティ

```bash
cd powerpoint-to-markdown/
python setup.py
python convert_pptx.py your_presentation.pptx
```

## 👨‍💻 作者

倉持誠 (Makoto Kuramochi)  
卒業論文: 「ケアワーカーと被介護者のマッチングアルゴリズムの開発」

## 📄 ライセンス

This project is licensed under the MIT License.

## 🤝 貢献

プルリクエストやイシューの報告を歓迎します。

---

*このシステムは学術研究目的で開発されましたが、実際のケアマッチングシステムへの応用も可能です。*