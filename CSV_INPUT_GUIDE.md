# CSV入力機能 使用ガイド

## 概要

このシステムでは、被介護者とケアワーカーのランキング（選好順序）とレイティング（客観的フィット度）をCSV形式で入力できます。

## 必要なCSVファイル

### 1. 被介護者の主観的選好 (`care_receiver_subjective_preferences.csv`)

**形式**: 各被介護者が各ケアワーカーに対してつけるランキング（1が最も好ましい）

```csv
被介護者ID,1,2,3
4,1,2,3
5,3,1,2
6,2,3,1
7,3,1,2
```

- **行**: 被介護者ID
- **列**: ケアワーカーID  
- **値**: ランキング（1=最も好ましい、2=2番目、など）

### 2. 被介護者の客観的フィット度 (`care_receiver_objective_fitness.csv`)

**形式**: 各被介護者と各ケアワーカーの客観的な適合度（0.0-1.0、高いほど適合）

```csv
被介護者ID,1,2,3
4,0.9,0.8,0.7
5,0.6,0.9,0.8
6,0.7,0.5,0.9
7,0.8,0.7,0.6
```

- **行**: 被介護者ID
- **列**: ケアワーカーID
- **値**: フィット度（0.0-1.0の範囲）

### 3. ケアワーカーの主観的選好 (`care_worker_subjective_preferences.csv`)

**形式**: 各ケアワーカーが各被介護者に対してつけるランキング（1が最も好ましい）

```csv
ケアワーカーID,4,5,6,7
1,2,3,1,4
2,1,2,4,3
3,4,1,2,3
```

- **行**: ケアワーカーID
- **列**: 被介護者ID
- **値**: ランキング（1=最も好ましい、2=2番目、など）

### 4. ケアワーカーの客観的フィット度 (`care_worker_objective_fitness.csv`)

**形式**: 各ケアワーカーと各被介護者の客観的な適合度（0.0-1.0、高いほど適合）

```csv
ケアワーカーID,4,5,6,7
1,0.9,0.6,0.7,0.8
2,0.8,0.9,0.5,0.7
3,0.7,0.8,0.9,0.6
```

- **行**: ケアワーカーID
- **列**: 被介護者ID
- **値**: フィット度（0.0-1.0の範囲）

### 5. ケアワーカーの容量情報 (`care_worker_capacity.csv`) [オプション]

**形式**: 各ケアワーカーが対応できる被介護者の数

```csv
ケアワーカーID,容量
1,1
2,1
3,1
```

- **行**: 各ケアワーカー
- **列1**: ケアワーカーID
- **列2**: 容量（対応可能な被介護者数）

## 使用方法

### 1. CSVファイルの準備

上記の形式に従って5つのCSVファイルを準備します。

### 2. プログラムでの読み込み

```python
from csv_matching_system import CSVMatchingSystem

# システムのインスタンス作成
system = CSVMatchingSystem()

# CSVファイルからデータを読み込んでマッチング実行
result = system.run_complete_matching_from_csv(
    receiver_subjective_csv="care_receiver_subjective_preferences.csv",
    receiver_objective_csv="care_receiver_objective_fitness.csv", 
    worker_subjective_csv="care_worker_subjective_preferences.csv",
    worker_objective_csv="care_worker_objective_fitness.csv",
    worker_capacity_csv="care_worker_capacity.csv",  # オプション
    w_subjective=1.0,  # 主観的選好の重み
    w_objective=1.0    # 客観的フィット度の重み
)
```

### 3. サンプルファイルの自動生成

```python
from csv_input_handler import CSVInputHandler

handler = CSVInputHandler()
handler.create_sample_csv_files()  # サンプルCSVファイルを自動生成
```

## 重要な注意点

### データの整合性
- **被介護者ID**: 全CSVファイルで一貫している必要があります
- **ケアワーカーID**: 全CSVファイルで一貫している必要があります
- **欠損値**: 空白セルやNaN値は自動的にスキップされます

### ランキングの形式
- **1から始まる連続した整数**: ランキングは1が最も好ましく、2、3...と続きます
- **同順位は不可**: 同じエージェントが同じランキング値を複数回使用することはできません

### フィット度の形式
- **0.0-1.0の範囲**: 客観的フィット度は0.0（全く適合しない）から1.0（完全に適合）の範囲
- **浮動小数点数**: 小数点以下の値も使用可能

## 出力結果

マッチング実行後、以下の情報が出力されます：

### コンソール出力
- データ読み込み状況
- 選好統合結果
- マッチング結果
- 満足度分析
- 安定性チェック結果

### JSONファイル出力
結果は`csv_matching_results.json`ファイルに保存され、以下が含まれます：
- 入力データ
- 統合された選好
- マッチング結果
- メタデータ（統計情報）

## 使用例

```python
# 1. サンプルファイル生成
from csv_matching_system import demo_csv_matching
demo_csv_matching()

# 2. 個別実行
system = CSVMatchingSystem()
system.load_data_from_csv(
    "care_receiver_subjective_preferences.csv",
    "care_receiver_objective_fitness.csv", 
    "care_worker_subjective_preferences.csv",
    "care_worker_objective_fitness.csv",
    "care_worker_capacity.csv"
)
system.aggregate_preferences(w_subjective=1.5, w_objective=0.5)  # 重み調整
system.run_matching()
system.analyze_results()
system.save_results("my_results.json")
```

## エラー対処

### よくあるエラー
1. **ファイルが見つからない**: ファイルパスを確認してください
2. **データ形式エラー**: CSVの形式が正しいか確認してください
3. **ID不整合**: 被介護者IDとケアワーカーIDが全ファイルで一致するか確認してください

### デバッグ方法
1. `validate_data_consistency()`メソッドでデータ整合性をチェック
2. 小さなサンプルデータで動作確認
3. エラーメッセージを確認してファイル形式を修正