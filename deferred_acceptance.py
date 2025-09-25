#!/usr/bin/env python3
"""
Deferred Acceptance (DA) アルゴリズムの実装

このモジュールは卒業論文「ケアワーカーと被介護者のマッチングアルゴリズムの開発」で
使用されたDeferred Acceptance (DA) アルゴリズムを実装します。

DAアルゴリズムは安定マッチングを生成する標準的なアルゴリズムで、
この実装では被介護者側最適な安定マッチングを生成します。

Author: 倉持誠 (Makoto Kuramochi)
"""

from typing import List, Dict, Tuple, Optional, Set
import copy


class DeferredAcceptanceAlgorithm:
    """Deferred Acceptance アルゴリズムの実装クラス"""
    
    def __init__(self):
        """DAアルゴリズムの初期化"""
        self.history = []  # マッチング過程の履歴
    
    def create_match(self, 
                    care_recipients: List[int],
                    caregivers: List[int],
                    recipient_preferences: Dict[int, List[int]],
                    caregiver_preferences: Dict[int, List[int]],
                    caregiver_capacities: Dict[int, int]) -> Tuple[Dict[int, int], Dict]:
        """
        DAアルゴリズムを使用してマッチングを生成
        
        Args:
            care_recipients: 被介護者のIDリスト
            caregivers: ケアワーカーのIDリスト
            recipient_preferences: 被介護者の選好辞書 {被介護者ID: [ケアワーカーID順]}
            caregiver_preferences: ケアワーカーの選好辞書 {ケアワーカーID: [被介護者ID順]}
            caregiver_capacities: ケアワーカーのキャパシティ辞書 {ケアワーカーID: 容量}
            
        Returns:
            Tuple[Dict[int, int], Dict]: マッチング結果 {被介護者ID: ケアワーカーID} と詳細情報
        """
        # 初期化
        self.history = []
        unmatched_recipients = set(care_recipients)
        current_proposals = {r: 0 for r in care_recipients}  # 各被介護者の現在の提案先インデックス
        tentative_matches = {c: [] for c in caregivers}  # ケアワーカーの仮マッチリスト
        final_matches = {}  # 最終マッチング結果
        
        step = 1
        
        while unmatched_recipients:
            # 現在のステップの情報を記録
            step_info = {
                'step': step,
                'unmatched_recipients': list(unmatched_recipients),
                'current_proposals': copy.deepcopy(current_proposals),
                'tentative_matches': copy.deepcopy(tentative_matches),
                'actions': []
            }
            
            # ステップ1: 未マッチの被介護者が提案
            proposals_this_round = {}
            for recipient in list(unmatched_recipients):
                if current_proposals[recipient] < len(recipient_preferences[recipient]):
                    target_caregiver = recipient_preferences[recipient][current_proposals[recipient]]
                    proposals_this_round[recipient] = target_caregiver
                    
                    action = f"被介護者{recipient}がケアワーカー{target_caregiver}に提案"
                    step_info['actions'].append(action)
                    
                    current_proposals[recipient] += 1
                else:
                    # 提案先がない場合は未マッチのまま
                    unmatched_recipients.remove(recipient)
                    action = f"被介護者{recipient}は提案先がないため未マッチ確定"
                    step_info['actions'].append(action)
            
            # ステップ2: ケアワーカーが提案を評価
            for recipient, caregiver in proposals_this_round.items():
                # 現在の仮マッチリストに追加
                tentative_matches[caregiver].append(recipient)
                
                # キャパシティを超えている場合は選考
                if len(tentative_matches[caregiver]) > caregiver_capacities[caregiver]:
                    # ケアワーカーの選好に基づいて選考
                    candidates = tentative_matches[caregiver]
                    # 選好順に並べ替え（選好が高い順）
                    candidates_with_pref = []
                    for candidate in candidates:
                        if candidate in caregiver_preferences[caregiver]:
                            pref_order = caregiver_preferences[caregiver].index(candidate)
                            candidates_with_pref.append((pref_order, candidate))
                        else:
                            # 選好リストにない場合は最低優先度
                            candidates_with_pref.append((len(caregiver_preferences[caregiver]), candidate))
                    
                    candidates_with_pref.sort()  # 選好順序でソート
                    
                    # キャパシティ分だけ仮受入
                    accepted = [c for _, c in candidates_with_pref[:caregiver_capacities[caregiver]]]
                    rejected = [c for _, c in candidates_with_pref[caregiver_capacities[caregiver]:]]
                    
                    tentative_matches[caregiver] = accepted
                    
                    # 拒否された被介護者を再び未マッチに
                    for rej in rejected:
                        unmatched_recipients.add(rej)
                        action = f"ケアワーカー{caregiver}が被介護者{rej}を拒否"
                        step_info['actions'].append(action)
                    
                    if accepted:
                        action = f"ケアワーカー{caregiver}が{accepted}を仮受入"
                        step_info['actions'].append(action)
                else:
                    # キャパシティ内なので受入
                    action = f"ケアワーカー{caregiver}が被介護者{recipient}を仮受入"
                    step_info['actions'].append(action)
                
                # 提案した被介護者を一旦マッチ済みに
                if recipient in unmatched_recipients:
                    unmatched_recipients.remove(recipient)
            
            # ステップ履歴に追加
            self.history.append(step_info)
            step += 1
            
            # 無限ループ防止
            if step > 100:
                break
        
        # 最終マッチング結果を生成
        for caregiver, recipients in tentative_matches.items():
            for recipient in recipients:
                final_matches[recipient] = caregiver
        
        # 詳細情報をまとめる
        details = {
            'final_matches': final_matches,
            'history': self.history,
            'unmatched_recipients': [r for r in care_recipients if r not in final_matches],
            'caregiver_utilization': {
                c: len(tentative_matches[c]) for c in caregivers
            }
        }
        
        return final_matches, details
    
    def print_matching_process(self, details: Dict):
        """
        マッチング過程を見やすく出力
        
        Args:
            details: create_matchから返された詳細辞書
        """
        print("=== Deferred Acceptance アルゴリズム実行過程 ===")
        print()
        
        for step_info in details['history']:
            print(f"ステップ {step_info['step']}:")
            print(f"未マッチ被介護者: {step_info['unmatched_recipients']}")
            
            for action in step_info['actions']:
                print(f"  - {action}")
            
            print(f"仮マッチ状況: {step_info['tentative_matches']}")
            print()
        
        print("=== 最終結果 ===")
        print(f"マッチング: {details['final_matches']}")
        print(f"未マッチ被介護者: {details['unmatched_recipients']}")
        print(f"ケアワーカー利用率: {details['caregiver_utilization']}")
    
    def is_stable_matching(self, 
                          matches: Dict[int, int],
                          recipient_preferences: Dict[int, List[int]],
                          caregiver_preferences: Dict[int, List[int]],
                          caregiver_capacities: Dict[int, int]) -> Tuple[bool, List]:
        """
        マッチングが安定かどうかを判定
        
        Args:
            matches: マッチング結果
            recipient_preferences: 被介護者の選好
            caregiver_preferences: ケアワーカーの選好
            caregiver_capacities: ケアワーカーのキャパシティ
            
        Returns:
            Tuple[bool, List]: 安定性の判定結果とブロッキングペアのリスト
        """
        blocking_pairs = []
        
        # 各ケアワーカーの現在のマッチを取得
        caregiver_matches = {}
        for caregiver_id in caregiver_preferences.keys():
            caregiver_matches[caregiver_id] = [r for r, c in matches.items() if c == caregiver_id]
        
        # 全ての被介護者-ケアワーカーペアをチェック
        for recipient, current_match in matches.items():
            for caregiver in recipient_preferences[recipient]:
                if caregiver == current_match:
                    break  # 現在のマッチ以上の選好はチェック済み
                
                # この被介護者がこのケアワーカーを現在のマッチより好む場合
                current_matches = caregiver_matches[caregiver]
                
                # ケアワーカーに余裕がある場合
                if len(current_matches) < caregiver_capacities[caregiver]:
                    blocking_pairs.append((recipient, caregiver))
                    continue
                
                # ケアワーカーがこの被介護者を現在のマッチの誰かより好む場合
                worst_current = None
                worst_pref_order = -1
                
                for current_recipient in current_matches:
                    if current_recipient in caregiver_preferences[caregiver]:
                        pref_order = caregiver_preferences[caregiver].index(current_recipient)
                        if pref_order > worst_pref_order:
                            worst_pref_order = pref_order
                            worst_current = current_recipient
                
                if (recipient in caregiver_preferences[caregiver] and
                    worst_current is not None and
                    caregiver_preferences[caregiver].index(recipient) < worst_pref_order):
                    blocking_pairs.append((recipient, caregiver))
        
        return len(blocking_pairs) == 0, blocking_pairs


def demo_da_algorithm():
    """DAアルゴリズムのデモ実行"""
    print("=== Deferred Acceptance アルゴリズム デモ ===")
    print()
    
    # 論文の例に基づいた設定
    care_recipients = [4, 5, 6, 7]  # 被介護者4,5,6,7
    caregivers = [1, 2, 3]  # ケアワーカー1,2,3
    
    # 拡張版Kemenyルールで生成された選好（例）
    recipient_preferences = {
        4: [1, 3, 2],  # 被介護者4の選好: ケアワーカー1>3>2
        5: [2, 1, 3],  # 被介護者5の選好: ケアワーカー2>1>3
        6: [2, 1, 3],  # 被介護者6の選好: ケアワーカー2>1>3 (論文の213)
        7: [3, 1, 2],  # 被介護者7の選好: ケアワーカー3>1>2
    }
    
    caregiver_preferences = {
        1: [4, 7, 5, 6],  # ケアワーカー1の選好
        2: [6, 5, 4, 7],  # ケアワーカー2の選好
        3: [7, 4, 5, 6],  # ケアワーカー3の選好
    }
    
    caregiver_capacities = {
        1: 1,  # ケアワーカー1のキャパシティ
        2: 1,  # ケアワーカー2のキャパシティ
        3: 2,  # ケアワーカー3のキャパシティ
    }
    
    print("設定:")
    print(f"被介護者: {care_recipients}")
    print(f"ケアワーカー: {caregivers}")
    print(f"キャパシティ: {caregiver_capacities}")
    print()
    print("被介護者の選好:")
    for recipient, prefs in recipient_preferences.items():
        print(f"  被介護者{recipient}: {prefs}")
    print()
    print("ケアワーカーの選好:")
    for caregiver, prefs in caregiver_preferences.items():
        print(f"  ケアワーカー{caregiver}: {prefs}")
    print()
    
    # DAアルゴリズムを実行
    da = DeferredAcceptanceAlgorithm()
    matches, details = da.create_match(
        care_recipients, caregivers, recipient_preferences, 
        caregiver_preferences, caregiver_capacities
    )
    
    # 結果表示
    da.print_matching_process(details)
    
    # 安定性チェック
    is_stable, blocking_pairs = da.is_stable_matching(
        matches, recipient_preferences, caregiver_preferences, caregiver_capacities
    )
    
    print()
    print("=== 安定性チェック ===")
    print(f"マッチングは安定: {is_stable}")
    if not is_stable:
        print(f"ブロッキングペア: {blocking_pairs}")


if __name__ == "__main__":
    demo_da_algorithm()