"""
CSV入力処理モジュール
被介護者とケアワーカーのランキングとレイティングデータをCSVファイルから読み込む
"""

import csv
from typing import Dict, List, Tuple, Optional
import os

class CSVInputHandler:
    """CSV形式のデータ入力を処理するクラス"""
    
    def __init__(self):
        self.care_receivers_data = {}
        self.care_workers_data = {}
        
    def load_care_receivers_data(self, subjective_csv: str, objective_csv: str) -> Dict:
        """
        被介護者の主観的選好と客観的フィット度をCSVから読み込む
        
        Args:
            subjective_csv: 主観的選好CSVファイルのパス
            objective_csv: 客観的フィット度CSVファイルのパス
            
        Returns:
            被介護者データの辞書
        """
        print(f"被介護者データを読み込み中...")
        print(f"主観的選好: {subjective_csv}")
        print(f"客観的フィット度: {objective_csv}")
        
        # 主観的選好の読み込み
        subjective_prefs = self._load_preferences_csv(subjective_csv, "被介護者", "ケアワーカー")
        
        # 客観的フィット度の読み込み
        objective_ratings = self._load_ratings_csv(objective_csv, "被介護者", "ケアワーカー")
        
        # データ統合
        care_receivers_data = {}
        for receiver_id in subjective_prefs.keys():
            care_receivers_data[receiver_id] = {
                'subjective_preferences': subjective_prefs.get(receiver_id, {}),
                'objective_fitness': objective_ratings.get(receiver_id, {})
            }
            
        self.care_receivers_data = care_receivers_data
        print(f"被介護者 {len(care_receivers_data)} 人のデータを読み込みました")
        return care_receivers_data
    
    def load_care_workers_data(self, subjective_csv: str, objective_csv: str, capacity_csv: Optional[str] = None) -> Dict:
        """
        ケアワーカーの主観的選好と客観的フィット度をCSVから読み込む
        
        Args:
            subjective_csv: 主観的選好CSVファイルのパス
            objective_csv: 客観的フィット度CSVファイルのパス
            capacity_csv: 容量情報CSVファイルのパス（オプション）
            
        Returns:
            ケアワーカーデータの辞書
        """
        print(f"ケアワーカーデータを読み込み中...")
        print(f"主観的選好: {subjective_csv}")
        print(f"客観的フィット度: {objective_csv}")
        
        # 主観的選好の読み込み
        subjective_prefs = self._load_preferences_csv(subjective_csv, "ケアワーカー", "被介護者")
        
        # 客観的フィット度の読み込み
        objective_ratings = self._load_ratings_csv(objective_csv, "ケアワーカー", "被介護者")
        
        # 容量情報の読み込み
        capacities = {}
        if capacity_csv and os.path.exists(capacity_csv):
            capacities = self._load_capacity_csv(capacity_csv)
        
        # データ統合
        care_workers_data = {}
        for worker_id in subjective_prefs.keys():
            care_workers_data[worker_id] = {
                'subjective_preferences': subjective_prefs.get(worker_id, {}),
                'objective_fitness': objective_ratings.get(worker_id, {}),
                'capacity': capacities.get(worker_id, 1)  # デフォルト容量は1
            }
            
        self.care_workers_data = care_workers_data
        print(f"ケアワーカー {len(care_workers_data)} 人のデータを読み込みました")
        return care_workers_data
    
    def _load_preferences_csv(self, csv_file: str, row_entity: str, col_entity: str) -> Dict[int, Dict[int, int]]:
        """
        選好ランキングCSVを読み込む
        
        CSV形式:
        行: エージェント（被介護者 or ケアワーカー）
        列: 対象（ケアワーカー or 被介護者）
        値: ランキング（1が最も好ましい）
        """
        preferences = {}
        
        try:
            with open(csv_file, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                header = next(reader)  # ヘッダー行を読み取り
                col_ids = [int(col) for col in header[1:]]  # 最初の列はID列なのでスキップ
                
                row_count = 0
                for row in reader:
                    row_id = int(row[0])
                    preferences[row_id] = {}
                    
                    for i, ranking_str in enumerate(row[1:]):
                        if ranking_str.strip() and ranking_str.strip() != '':
                            col_id = col_ids[i]
                            ranking = int(float(ranking_str))  # 浮動小数点数も処理
                            preferences[row_id][col_id] = ranking
                    
                    row_count += 1
                
                print(f"  {row_count} 人の{row_entity}選好を読み込み")
            
        except Exception as e:
            print(f"エラー: {csv_file} の読み込みに失敗しました: {e}")
            raise
        
        return preferences
    
    def _load_ratings_csv(self, csv_file: str, row_entity: str, col_entity: str) -> Dict[int, Dict[int, float]]:
        """
        レイティング（客観的フィット度）CSVを読み込む
        
        CSV形式:
        行: エージェント（被介護者 or ケアワーカー）
        列: 対象（ケアワーカー or 被介護者）
        値: レイティング（高いほど適合度が高い）
        """
        ratings = {}
        
        try:
            with open(csv_file, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                header = next(reader)  # ヘッダー行を読み取り
                col_ids = [int(col) for col in header[1:]]  # 最初の列はID列なのでスキップ
                
                row_count = 0
                for row in reader:
                    row_id = int(row[0])
                    ratings[row_id] = {}
                    
                    for i, rating_str in enumerate(row[1:]):
                        if rating_str.strip() and rating_str.strip() != '':
                            col_id = col_ids[i]
                            rating = float(rating_str)
                            ratings[row_id][col_id] = rating
                    
                    row_count += 1
                
                print(f"  {row_count} 人の{row_entity}レイティングを読み込み")
            
        except Exception as e:
            print(f"エラー: {csv_file} の読み込みに失敗しました: {e}")
            raise
        
        return ratings
    
    def _load_capacity_csv(self, csv_file: str) -> Dict[int, int]:
        """
        ケアワーカーの容量情報CSVを読み込む
        
        CSV形式:
        ケアワーカーID, 容量
        """
        capacities = {}
        
        try:
            with open(csv_file, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                header = next(reader)  # ヘッダー行をスキップ
                
                for row in reader:
                    worker_id = int(row[0])  # 最初の列をワーカーID
                    capacity = int(row[1])   # 2番目の列を容量
                    capacities[worker_id] = capacity
            
            print(f"  {len(capacities)} 人のケアワーカー容量を読み込み")
            
        except Exception as e:
            print(f"エラー: {csv_file} の読み込みに失敗しました: {e}")
            raise
        
        return capacities
    
    def create_sample_csv_files(self):
        """
        サンプルCSVファイルを作成する
        """
        print("サンプルCSVファイルを作成中...")
        
        # 被介護者の主観的選好サンプル
        with open("care_receiver_subjective_preferences.csv", 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['被介護者ID', '1', '2', '3'])  # ヘッダー: ケアワーカーID
            writer.writerow([4, 1, 2, 3])  # 被介護者4の選好
            writer.writerow([5, 3, 1, 2])  # 被介護者5の選好
            writer.writerow([6, 2, 3, 1])  # 被介護者6の選好
            writer.writerow([7, 3, 1, 2])  # 被介護者7の選好
        
        # 被介護者の客観的フィット度サンプル
        with open("care_receiver_objective_fitness.csv", 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['被介護者ID', '1', '2', '3'])  # ヘッダー: ケアワーカーID
            writer.writerow([4, 0.9, 0.8, 0.7])  # 被介護者4のフィット度
            writer.writerow([5, 0.6, 0.9, 0.8])  # 被介護者5のフィット度
            writer.writerow([6, 0.7, 0.5, 0.9])  # 被介護者6のフィット度
            writer.writerow([7, 0.8, 0.7, 0.6])  # 被介護者7のフィット度
        
        # ケアワーカーの主観的選好サンプル
        with open("care_worker_subjective_preferences.csv", 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['ケアワーカーID', '4', '5', '6', '7'])  # ヘッダー: 被介護者ID
            writer.writerow([1, 2, 3, 1, 4])  # ケアワーカー1の選好
            writer.writerow([2, 1, 2, 4, 3])  # ケアワーカー2の選好
            writer.writerow([3, 4, 1, 2, 3])  # ケアワーカー3の選好
        
        # ケアワーカーの客観的フィット度サンプル
        with open("care_worker_objective_fitness.csv", 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['ケアワーカーID', '4', '5', '6', '7'])  # ヘッダー: 被介護者ID
            writer.writerow([1, 0.9, 0.6, 0.7, 0.8])  # ケアワーカー1のフィット度
            writer.writerow([2, 0.8, 0.9, 0.5, 0.7])  # ケアワーカー2のフィット度
            writer.writerow([3, 0.7, 0.8, 0.9, 0.6])  # ケアワーカー3のフィット度
        
        # ケアワーカー容量サンプル
        with open("care_worker_capacity.csv", 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['ケアワーカーID', '容量'])  # ヘッダー
            writer.writerow([1, 1])  # ケアワーカー1の容量
            writer.writerow([2, 1])  # ケアワーカー2の容量
            writer.writerow([3, 1])  # ケアワーカー3の容量
        
        print("以下のサンプルCSVファイルを作成しました:")
        print("  - care_receiver_subjective_preferences.csv")
        print("  - care_receiver_objective_fitness.csv")
        print("  - care_worker_subjective_preferences.csv") 
        print("  - care_worker_objective_fitness.csv")
        print("  - care_worker_capacity.csv")
    
    def validate_data_consistency(self) -> bool:
        """
        読み込んだデータの整合性をチェック
        """
        print("\nデータ整合性チェック中...")
        
        # 被介護者IDの取得
        receiver_ids = set(self.care_receivers_data.keys())
        
        # ケアワーカーIDの取得  
        worker_ids = set(self.care_workers_data.keys())
        
        # 被介護者データの整合性チェック
        for receiver_id, data in self.care_receivers_data.items():
            subjective_targets = set(data['subjective_preferences'].keys())
            objective_targets = set(data['objective_fitness'].keys())
            
            if subjective_targets != worker_ids:
                print(f"警告: 被介護者{receiver_id}の主観的選好に不整合があります")
                print(f"  期待: {worker_ids}, 実際: {subjective_targets}")
                
            if objective_targets != worker_ids:
                print(f"警告: 被介護者{receiver_id}の客観的フィット度に不整合があります")
                print(f"  期待: {worker_ids}, 実際: {objective_targets}")
        
        # ケアワーカーデータの整合性チェック
        for worker_id, data in self.care_workers_data.items():
            subjective_targets = set(data['subjective_preferences'].keys())
            objective_targets = set(data['objective_fitness'].keys())
            
            if subjective_targets != receiver_ids:
                print(f"警告: ケアワーカー{worker_id}の主観的選好に不整合があります")
                print(f"  期待: {receiver_ids}, 実際: {subjective_targets}")
                
            if objective_targets != receiver_ids:
                print(f"警告: ケアワーカー{worker_id}の客観的フィット度に不整合があります")
                print(f"  期待: {receiver_ids}, 実際: {objective_targets}")
        
        print("データ整合性チェック完了")
        return True

def demo_csv_input():
    """CSV入力機能のデモンストレーション"""
    print("=== CSV入力機能デモ ===")
    
    handler = CSVInputHandler()
    
    # サンプルCSVファイルの作成
    handler.create_sample_csv_files()
    
    print("\n" + "="*50)
    
    # 被介護者データの読み込み
    care_receivers = handler.load_care_receivers_data(
        "care_receiver_subjective_preferences.csv",
        "care_receiver_objective_fitness.csv"
    )
    
    print("\n" + "="*50)
    
    # ケアワーカーデータの読み込み
    care_workers = handler.load_care_workers_data(
        "care_worker_subjective_preferences.csv",
        "care_worker_objective_fitness.csv", 
        "care_worker_capacity.csv"
    )
    
    print("\n" + "="*50)
    
    # データ整合性チェック
    handler.validate_data_consistency()
    
    print("\n=== 読み込み結果サンプル ===")
    print("被介護者4のデータ:")
    print(f"  主観的選好: {care_receivers[4]['subjective_preferences']}")
    print(f"  客観的フィット度: {care_receivers[4]['objective_fitness']}")
    
    print("\nケアワーカー1のデータ:")
    print(f"  主観的選好: {care_workers[1]['subjective_preferences']}")
    print(f"  客観的フィット度: {care_workers[1]['objective_fitness']}")
    print(f"  容量: {care_workers[1]['capacity']}")

if __name__ == "__main__":
    demo_csv_input()