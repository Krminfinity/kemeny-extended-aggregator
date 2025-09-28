#!/usr/bin/env python3
"""
マッチングシステムの入力データ検証モジュール

このモジュールは2025年9月に追加された厳格な制約条件を実装し、
入力データが全ての制約を満たすことを保証します。

制約条件:
1. 被介護者数・ケアワーカー数の上限（各100人）
2. フィット度の整数限定
3. フィット度の単射性（重複値なし）

Author: 倉持誠 (Makoto Kuramochi)
"""

from typing import List, Dict, Any, Tuple, Union, Sequence, Mapping
import math


class ConstraintViolationError(Exception):
    """制約違反時に発生する例外"""
    pass


class InputValidator:
    """入力データの制約検証クラス"""
    
    # 計算量を考慮した人数制限
    MAX_CARE_RECIPIENTS = 100
    MAX_CARE_WORKERS = 100
    
    @staticmethod
    def validate_participant_count(care_recipients: List[int], 
                                 care_workers: List[int]) -> None:
        """
        参加者数の制限をチェック
        
        Args:
            care_recipients: 被介護者IDリスト
            care_workers: ケアワーカーIDリスト
            
        Raises:
            ConstraintViolationError: 人数制限違反時
        """
        n_recipients = len(care_recipients)
        n_workers = len(care_workers)
        
        if n_recipients > InputValidator.MAX_CARE_RECIPIENTS:
            raise ConstraintViolationError(
                f"被介護者数が制限を超えています: {n_recipients} > {InputValidator.MAX_CARE_RECIPIENTS}"
            )
        
        if n_workers > InputValidator.MAX_CARE_WORKERS:
            raise ConstraintViolationError(
                f"ケアワーカー数が制限を超えています: {n_workers} > {InputValidator.MAX_CARE_WORKERS}"
            )
        
        if n_recipients == 0:
            raise ConstraintViolationError("被介護者が存在しません")
        
        if n_workers == 0:
            raise ConstraintViolationError("ケアワーカーが存在しません")
    
    @staticmethod
    def validate_fitness_scores_are_integers(fitness_scores: Sequence[Union[int, float]]) -> None:
        """
        フィット度が厳密に整数であることをチェック
        
        Args:
            fitness_scores: フィット度スコアリスト
            
        Raises:
            ConstraintViolationError: 整数制限違反時
        """
        for i, score in enumerate(fitness_scores):
            # 型チェック
            if not isinstance(score, (int, float)):
                raise ConstraintViolationError(
                    f"フィット度[{i}]が数値ではありません: {score} (型: {type(score).__name__})"
                )
            
            # 整数チェック（floatでも整数値ならOK）
            if isinstance(score, float):
                if not score.is_integer():
                    raise ConstraintViolationError(
                        f"フィット度[{i}]が整数ではありません: {score}"
                    )
                if math.isnan(score) or math.isinf(score):
                    raise ConstraintViolationError(
                        f"フィット度[{i}]が無効な値です: {score}"
                    )
            
            # 非負制約
            if score < 0:
                raise ConstraintViolationError(
                    f"フィット度[{i}]が負の値です: {score}"
                )
    
    @staticmethod
    def validate_fitness_uniqueness(fitness_scores: Sequence[Union[int, float]], 
                                  entity_name: str = "エンティティ") -> None:
        """
        フィット度の単射性（一意性）をチェック
        
        Args:
            fitness_scores: フィット度スコアリスト
            entity_name: エンティティ名（エラーメッセージ用）
            
        Raises:
            ConstraintViolationError: 単射性違反時
        """
        # 整数値に変換してチェック
        int_scores = [int(score) for score in fitness_scores]
        
        if len(int_scores) != len(set(int_scores)):
            # 重複値を特定
            seen = set()
            duplicates = set()
            for score in int_scores:
                if score in seen:
                    duplicates.add(score)
                seen.add(score)
            
            raise ConstraintViolationError(
                f"{entity_name}のフィット度に重複があります: {list(duplicates)}"
            )
    
    @staticmethod
    def validate_preference_consistency(participant_ids: List[int],
                                      preference_dict: Dict[int, List[int]],
                                      target_ids: List[int],
                                      participant_type: str) -> None:
        """
        選好の整合性をチェック
        
        Args:
            participant_ids: 参加者IDリスト
            preference_dict: 選好辞書
            target_ids: 選好対象IDリスト
            participant_type: 参加者タイプ（エラーメッセージ用）
            
        Raises:
            ConstraintViolationError: 選好データ不整合時
        """
        for participant_id in participant_ids:
            if participant_id not in preference_dict:
                raise ConstraintViolationError(
                    f"{participant_type}{participant_id}の選好データが存在しません"
                )
            
            prefs = preference_dict[participant_id]
            
            # 選好リストの長さチェック
            if len(prefs) != len(target_ids):
                raise ConstraintViolationError(
                    f"{participant_type}{participant_id}の選好リストの長さが不正です: "
                    f"{len(prefs)} != {len(target_ids)}"
                )
            
            # 選好リストの完全性チェック
            if set(prefs) != set(target_ids):
                missing = set(target_ids) - set(prefs)
                extra = set(prefs) - set(target_ids)
                error_msg = f"{participant_type}{participant_id}の選好リストが不完全です"
                if missing:
                    error_msg += f" (不足: {missing})"
                if extra:
                    error_msg += f" (余分: {extra})"
                raise ConstraintViolationError(error_msg)
    
    @staticmethod
    def validate_fitness_consistency(participant_ids: List[int],
                                   fitness_dict: Mapping[int, Sequence[Union[int, float]]],
                                   target_count: int,
                                   participant_type: str) -> None:
        """
        フィット度データの整合性をチェック
        
        Args:
            participant_ids: 参加者IDリスト
            fitness_dict: フィット度辞書
            target_count: 対象数
            participant_type: 参加者タイプ（エラーメッセージ用）
            
        Raises:
            ConstraintViolationError: フィット度データ不整合時
        """
        for participant_id in participant_ids:
            if participant_id not in fitness_dict:
                raise ConstraintViolationError(
                    f"{participant_type}{participant_id}のフィット度データが存在しません"
                )
            
            fitness_scores = fitness_dict[participant_id]
            
            # フィット度リストの長さチェック
            if len(fitness_scores) != target_count:
                raise ConstraintViolationError(
                    f"{participant_type}{participant_id}のフィット度リストの長さが不正です: "
                    f"{len(fitness_scores)} != {target_count}"
                )
            
            # 各フィット度の制約チェック
            InputValidator.validate_fitness_scores_are_integers(fitness_scores)
            InputValidator.validate_fitness_uniqueness(
                fitness_scores, 
                f"{participant_type}{participant_id}"
            )
    
    @staticmethod
    def validate_capacity_constraints(care_workers: List[int],
                                    capacity_dict: Dict[int, int]) -> None:
        """
        ケアワーカー容量制約をチェック
        
        Args:
            care_workers: ケアワーカーIDリスト
            capacity_dict: 容量辞書
            
        Raises:
            ConstraintViolationError: 容量制約違反時
        """
        for worker_id in care_workers:
            if worker_id not in capacity_dict:
                raise ConstraintViolationError(
                    f"ケアワーカー{worker_id}の容量データが存在しません"
                )
            
            capacity = capacity_dict[worker_id]
            
            if not isinstance(capacity, int):
                raise ConstraintViolationError(
                    f"ケアワーカー{worker_id}の容量が整数ではありません: {capacity}"
                )
            
            if capacity <= 0:
                raise ConstraintViolationError(
                    f"ケアワーカー{worker_id}の容量が正の値ではありません: {capacity}"
                )
    
    @staticmethod
    def validate_complete_input(care_recipients: List[int],
                              care_workers: List[int],
                              recipient_preferences: Dict[int, List[int]],
                              worker_preferences: Dict[int, List[int]],
                              recipient_fitness: Mapping[int, Sequence[Union[int, float]]],
                              worker_fitness: Mapping[int, Sequence[Union[int, float]]],
                              worker_capacities: Dict[int, int]) -> None:
        """
        全ての入力データの制約を一括検証
        
        Args:
            care_recipients: 被介護者IDリスト
            care_workers: ケアワーカーIDリスト
            recipient_preferences: 被介護者選好辞書
            worker_preferences: ケアワーカー選好辞書
            recipient_fitness: 被介護者フィット度辞書
            worker_fitness: ケアワーカーフィット度辞書
            worker_capacities: ケアワーカー容量辞書
            
        Raises:
            ConstraintViolationError: 任意の制約違反時
        """
        print("=== 入力データ制約検証開始 ===")
        
        try:
            # 1. 人数制限チェック
            print("人数制限をチェック中...")
            InputValidator.validate_participant_count(care_recipients, care_workers)
            
            # 2. 選好データ整合性チェック
            print("選好データの整合性をチェック中...")
            InputValidator.validate_preference_consistency(
                care_recipients, recipient_preferences, care_workers, "被介護者"
            )
            InputValidator.validate_preference_consistency(
                care_workers, worker_preferences, care_recipients, "ケアワーカー"
            )
            
            # 3. フィット度データ整合性チェック
            print("フィット度データの整合性をチェック中...")
            InputValidator.validate_fitness_consistency(
                care_recipients, recipient_fitness, len(care_workers), "被介護者"
            )
            InputValidator.validate_fitness_consistency(
                care_workers, worker_fitness, len(care_recipients), "ケアワーカー"
            )
            
            # 4. 容量制約チェック
            print("容量制約をチェック中...")
            InputValidator.validate_capacity_constraints(care_workers, worker_capacities)
            
            print("=== 全ての制約検証に合格しました ===")
            
        except ConstraintViolationError as e:
            print(f"=== 制約違反が検出されました ===")
            raise e


def demo_validation():
    """バリデーション機能のデモ"""
    print("=== 入力データ制約検証デモ ===\n")
    
    # 正常なデータの例
    print("1. 正常なデータのテスト:")
    try:
        care_recipients = [1, 2, 3]
        care_workers = [101, 102]
        
        recipient_preferences = {
            1: [101, 102],
            2: [102, 101], 
            3: [101, 102]
        }
        
        worker_preferences = {
            101: [1, 2, 3],
            102: [3, 1, 2]
        }
        
        # 整数フィット度（単射性あり）
        recipient_fitness = {
            1: [5, 3],  # ケアワーカー101に5、102に3
            2: [7, 1],  # ケアワーカー101に7、102に1
            3: [2, 4]   # ケアワーカー101に2、102に4
        }
        
        worker_fitness = {
            101: [8, 6, 9],  # 被介護者1に8、2に6、3に9
            102: [1, 3, 2]   # 被介護者1に1、2に3、3に2
        }
        
        worker_capacities = {101: 2, 102: 1}
        
        InputValidator.validate_complete_input(
            care_recipients, care_workers,
            recipient_preferences, worker_preferences,
            recipient_fitness, worker_fitness,
            worker_capacities
        )
        print("✓ 正常なデータの検証に成功しました\n")
        
    except ConstraintViolationError as e:
        print(f"✗ 予期しないエラー: {e}\n")
    
    # 制約違反の例
    print("2. 制約違反のテスト:")
    
    # 実数フィット度のテスト
    print("a) 実数フィット度の検出:")
    try:
        invalid_fitness = [5.5, 3, 7]  # 5.5は実数
        InputValidator.validate_fitness_scores_are_integers(invalid_fitness)
        print("✗ 実数フィット度が検出されませんでした")
    except ConstraintViolationError as e:
        print(f"✓ 正しく検出: {e}")
    
    # フィット度重複のテスト
    print("\nb) フィット度重複の検出:")
    try:
        duplicate_fitness = [5, 3, 5]  # 5が重複
        InputValidator.validate_fitness_uniqueness(duplicate_fitness, "テストエンティティ")
        print("✗ フィット度重複が検出されませんでした")
    except ConstraintViolationError as e:
        print(f"✓ 正しく検出: {e}")
    
    # 人数制限のテスト
    print("\nc) 人数制限の検出:")
    try:
        too_many_recipients = list(range(InputValidator.MAX_CARE_RECIPIENTS + 1))
        too_many_workers = [1, 2, 3]
        InputValidator.validate_participant_count(too_many_recipients, too_many_workers)
        print("✗ 人数制限違反が検出されませんでした")
    except ConstraintViolationError as e:
        print(f"✓ 正しく検出: {e}")
    
    print("\n=== デモ完了 ===")


if __name__ == "__main__":
    demo_validation()