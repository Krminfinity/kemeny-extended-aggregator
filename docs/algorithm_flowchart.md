# ケアワーカー・被介護者マッチングシステム アルゴリズムフローチャート

## 全体システムフロー

```mermaid
flowchart TD
    A[開始] --> B[入力データ読み込み]
    B --> C{制約検証}
    C --> C1[人数制限チェック<br/>被介護者≤100, ケアワーカー≤100]
    C1 --> C2[フィット度整数性チェック<br/>実数値拒否]
    C2 --> C3[フィット度単射性チェック<br/>重複値検出]
    C3 --> C4[選好データ整合性チェック]
    C4 --> C5[容量制約チェック]
    C5 --> D{制約違反?}
    D -->|Yes| ERROR[ConstraintViolationError<br/>システム終了]
    D -->|No| E[制約検証合格]
    E --> F[拡張版Kemenyルールによる選好統合]
    F --> G[DAアルゴリズムによるマッチング]
    G --> H[安定性チェック]
    H --> I[満足度分析]
    I --> J[結果出力・保存]
    J --> K[正常終了]
    
    style A fill:#e1f5fe
    style K fill:#e8f5e8
    style ERROR fill:#ffcdd2
    style E fill:#c8e6c9
    style F fill:#fff3e0
    style G fill:#fce4ec
    style C fill:#ffe0b2
    style C1 fill:#fff9c4
    style C2 fill:#fff9c4
    style C3 fill:#fff9c4
    style C4 fill:#fff9c4
    style C5 fill:#fff9c4
```

## 拡張版Kemenyルール詳細フロー（制約検証統合版）

```mermaid
flowchart TD
    A1[拡張版Kemenyルール開始] --> B1[各エージェントの処理ループ]
    B1 --> C1[主観的選好取得]
    C1 --> D1[客観的フィット度取得]
    D1 --> E1{フィット度制約検証}
    E1 --> E1a[整数性チェック<br/>math.isnan/isinf除外]
    E1a --> E1b[単射性チェック<br/>重複値検出]
    E1b --> E1c{制約違反?}
    E1c -->|Yes| ERROR1[ConstraintViolationError]
    E1c -->|No| F1[フィット度を整数リストに変換]
    F1 --> G1[候補者数n → 全順列生成 n!個]
    G1 --> H1{各順列σについて n!回ループ}
    H1 --> I1[Kemeny距離計算<br/>不一致ペア数をカウント]
    I1 --> J1{フィット度モード?}
    J1 -->|ordinal| J1a[フィット度を順位化<br/>→ Kemeny距離計算]
    J1 -->|gap| J1b[差分ペナルティ計算<br/>フィット度差の合計]
    J1a --> K1[重み付き総合スコア<br/>w1×d_pref + w2×d_fit]
    J1b --> K1
    K1 --> L1[現在最小スコアと比較]
    L1 --> M1{最小更新?}
    M1 -->|Yes| M1a[最適順列更新]
    M1 -->|No| N1[次順列へ]
    M1a --> N1
    N1 --> H1
    H1 --> O1[最適順列を統合選好として出力]
    O1 --> P1{全エージェント完了?}
    P1 -->|No| B1
    P1 -->|Yes| Q1[拡張版Kemenyルール終了]
    
    style A1 fill:#fff3e0
    style Q1 fill:#fff3e0
    style ERROR1 fill:#ffcdd2
    style F1 fill:#c8e6c9
    style K1 fill:#ffecb3
    style E1 fill:#ffe0b2
    style G1 fill:#fff9c4
    style I1 fill:#e3f2fd
    style J1a fill:#f3e5f5
    style J1b fill:#f3e5f5
```

## Kemeny距離計算詳細（O(n²) 最適化版）

```mermaid
flowchart TD
    A2[Kemeny距離計算開始<br/>input: ranking1, ranking2] --> B2[位置辞書構築<br/>pos_map作成]
    B2 --> C2[距離カウンタ初期化<br/>distance = 0]
    C2 --> D2[外側ループ: i = 0 to n-1]
    D2 --> E2[ai = ranking1 の i番目<br/>pi = pos_map での位置]
    E2 --> F2[内側ループ: j = i+1 to n-1]
    F2 --> G2[aj = ranking1 の j番目<br/>pj = pos_map での位置]
    G2 --> H2{ranking1で ai が aj より前<br/>かつ ranking2で pi が pj より後?}
    H2 -->|Yes: 逆転| I2[distance += 1<br/>不一致ペア発見]
    H2 -->|No: 順序一致| J2[一致ペア]
    I2 --> K2[j++]
    J2 --> K2
    K2 --> L2{j < n ?}
    L2 -->|Yes| F2
    L2 -->|No| M2[i++]
    M2 --> N2{i < n-1 ?}
    N2 -->|Yes| D2
    N2 -->|No| O2[return distance<br/>= 不一致ペア数]
    O2 --> P2[Kemeny距離計算終了]
    
    style A2 fill:#e3f2fd
    style P2 fill:#e3f2fd
    style B2 fill:#fff9c4
    style I2 fill:#ffcdd2
    style J2 fill:#c8e6c9
    style O2 fill:#e1f5fe
```

## DAアルゴリズム詳細フロー（被介護者提案型）

```mermaid
flowchart TD
    A3[DAアルゴリズム開始] --> B3[データ構造初期化]
    B3 --> C3[unmatched_recipients設定<br/>current_proposals初期化<br/>tentative_matches初期化]
    C3 --> D3[step = 1, history = 空リスト]
    D3 --> E3{unmatched_recipients が空?}
    E3 -->|Yes| FINAL[マッチング完了]
    E3 -->|No| F3[ステップ step 開始]
    F3 --> G3[proposals_this_round = 空辞書]
    G3 --> H3{各 recipient について}
    H3 --> I3{提案先が残っている?}
    I3 -->|No| I3a[recipient を unmatched から削除<br/>提案先なし]
    I3 -->|Yes| J3[次の希望先に提案<br/>提案カウンタ更新]
    I3a --> K3[次の recipient へ]
    J3 --> K3
    K3 --> H3
    H3 --> L3{各提案について}
    L3 --> M3[tentative_matchesに追加]
    M3 --> N3{容量超過?}
    N3 -->|No| N3a[容量内受入<br/>recipient を unmatched から削除]
    N3 -->|Yes| O3[容量超過: 選考開始]
    O3 --> P3[候補者を選好順序でソート]
    P3 --> Q3[容量分のみ受入<br/>残りは拒否]
    Q3 --> R3{拒否された各recipientについて}
    R3 --> S3[unmatchedに戻す]
    S3 --> R3
    R3 --> T3[受入確定<br/>拒否者は再未マッチ化]
    N3a --> U3[次の proposal へ]
    T3 --> U3
    U3 --> L3
    L3 --> V3[step更新, 履歴記録]
    V3 --> W3{step > 100? 無限ループ防止}
    W3 -->|Yes| ERROR3[アルゴリズム異常終了]
    W3 -->|No| E3
    FINAL --> X3[final_matches作成]
    X3 --> Y3[安定性チェック実行]
    Y3 --> Z3[DAアルゴリズム終了]
    
    style A3 fill:#fce4ec
    style Z3 fill:#fce4ec
    style ERROR3 fill:#ffcdd2
    style N3a fill:#c8e6c9
    style T3 fill:#c8e6c9
    style O3 fill:#ffecb3
    style FINAL fill:#e8f5e8
    style C3 fill:#fff9c4
    style X3 fill:#e1f5fe
```

## 安定性チェックフロー（ブロッキングペア検出）

```mermaid
flowchart TD
    A4[安定性チェック開始<br/>input: matches, preferences, capacities] --> B4[blocking_pairs = 空リスト<br/>caregiver_matches = 逆マッチング辞書構築]
    B4 --> C4{各マッチペアについて}
    C4 --> D4[recipient_prefs = 被介護者の選好リスト]
    D4 --> E4{各ケアワーカーについて}
    E4 --> F4{現在のマッチ相手?}
    F4 -->|Yes| F4a[現在のマッチ到達<br/>これ以降は現在より劣る<br/>→ 次の recipient]
    F4 -->|No| G4[recipientがcaregiverを現在より好む]
    G4 --> H4[current_matches取得]
    H4 --> I4{ケアワーカーに余裕あり?}
    I4 -->|Yes| J4[ケアワーカーに余裕あり<br/>ブロッキングペア追加]
    I4 -->|No| K4[ケアワーカーの現在マッチを分析]
    K4 --> L4[worst_current = None<br/>worst_pref_order = -1]
    L4 --> M4{現在マッチの各recipientについて}
    M4 --> N4[選好順序を取得]
    N4 --> O4{より悪い順序?}
    O4 -->|Yes| P4[worst更新]
    O4 -->|No| Q4[次のcurrent_recipient]
    P4 --> Q4
    Q4 --> M4
    M4 --> R4[recipientの順序を取得]
    R4 --> S4{recipientの方が好ましい?}
    S4 -->|Yes| T4[ケアワーカーがrecipientを<br/>worst_currentより好む<br/>ブロッキングペア追加]
    S4 -->|No| U4[ブロッキングペアなし]
    J4 --> V4[次のcaregiver]
    T4 --> V4
    U4 --> V4
    V4 --> E4
    E4 --> F4a
    F4a --> W4[次のrecipient]
    W4 --> C4
    C4 --> X4{ブロッキングペアなし?}
    X4 -->|Yes| Y4[return True<br/>マッチング安定]
    X4 -->|No| Z4[return False<br/>マッチング不安定]
    Y4 --> END4[安定性チェック終了]
    Z4 --> END4
    
    style A4 fill:#f3e5f5
    style END4 fill:#f3e5f5
    style Y4 fill:#c8e6c9
    style Z4 fill:#ffcdd2
    style J4 fill:#ff8a80
    style T4 fill:#ff8a80
    style U4 fill:#c8e6c9
    style F4a fill:#c8e6c9
    style B4 fill:#fff9c4
```

## 満足度計算フロー

```mermaid
flowchart TD
    A5[満足度計算開始] --> B5{各被介護者について}
    B5 --> C5[マッチした相手取得]
    C5 --> D5[選好リストでの順位確認]
    D5 --> E5[満足度 = 1 ÷ 順位]
    E5 --> F5[次の被介護者へ]
    F5 --> B5
    B5 --> G5{各ケアワーカーについて}
    G5 --> H5[マッチした被介護者リスト取得]
    H5 --> I5{各マッチ相手について}
    I5 --> J5[選好リストでの順位確認]
    J5 --> K5[個別満足度 = 1 ÷ 順位]
    K5 --> L5[次のマッチ相手へ]
    L5 --> I5
    I5 --> M5[平均満足度計算]
    M5 --> N5[次のケアワーカーへ]
    N5 --> G5
    G5 --> O5[全体平均満足度計算]
    O5 --> P5[満足度計算終了]
    
    style A5 fill:#e8f5e8
    style P5 fill:#e8f5e8
    style E5 fill:#dcedc8
    style K5 fill:#dcedc8
```

## 制約検証フロー（2025年9月追加）

```mermaid
flowchart TD
    V1[制約検証開始] --> V2[人数制限チェック]
    V2 --> V2a{被介護者数 ≤ 100?}
    V2a -->|No| VERR1[被介護者数制限違反]
    V2a -->|Yes| V2b{ケアワーカー数 ≤ 100?}
    V2b -->|No| VERR2[ケアワーカー数制限違反]
    V2b -->|Yes| V3[フィット度整数性チェック]
    V3 --> V3a{各フィット度について}
    V3a --> V3b{isinstance int or float?}
    V3b -->|No| VERR3[数値でない]
    V3b -->|Yes| V3c{is_integer?}
    V3c -->|No| VERR4[整数でない]
    V3c -->|Yes| V3d{not isnan and not isinf?}
    V3d -->|No| VERR5[無効な値]
    V3d -->|Yes| V3e{≥ 0?}
    V3e -->|No| VERR6[負の値]
    V3e -->|Yes| V3f[次のフィット度]
    V3f --> V3a
    V3a --> V4[単射性チェック]
    V4 --> V4a{len set == len list?}
    V4a -->|No| VERR7[重複値あり]
    V4a -->|Yes| V5[選好整合性チェック]
    V5 --> V5a{各参加者について}
    V5a --> V5b{選好データ存在?}
    V5b -->|No| VERR8[選好データなし]
    V5b -->|Yes| V5c{選好リスト長さ正しい?}
    V5c -->|No| VERR9[長さ不正]
    V5c -->|Yes| V5d{選好リスト完全?}
    V5d -->|No| VERR10[不完全リスト]
    V5d -->|Yes| V5e[次の参加者]
    V5e --> V5a
    V5a --> V6[容量制約チェック]
    V6 --> V6a{各ケアワーカーについて}
    V6a --> V6b{容量データ存在?}
    V6b -->|No| VERR11[容量データなし]
    V6b -->|Yes| V6c{容量 > 0?}
    V6c -->|No| VERR12[無効な容量]
    V6c -->|Yes| V6d[次のケアワーカー]
    V6d --> V6a
    V6a --> V7[全制約検証合格]
    
    VERR1 --> VERR_END[制約違反終了]
    VERR2 --> VERR_END
    VERR3 --> VERR_END
    VERR4 --> VERR_END
    VERR5 --> VERR_END
    VERR6 --> VERR_END
    VERR7 --> VERR_END
    VERR8 --> VERR_END
    VERR9 --> VERR_END
    VERR10 --> VERR_END
    VERR11 --> VERR_END
    VERR12 --> VERR_END
    
    style V1 fill:#ffe0b2
    style V7 fill:#c8e6c9
    style VERR_END fill:#ffcdd2
    style VERR1 fill:#ffcdd2
    style VERR2 fill:#ffcdd2
    style VERR3 fill:#ffcdd2
    style VERR4 fill:#ffcdd2
    style VERR5 fill:#ffcdd2
    style VERR6 fill:#ffcdd2
    style VERR7 fill:#ffcdd2
    style VERR8 fill:#ffcdd2
    style VERR9 fill:#ffcdd2
    style VERR10 fill:#ffcdd2
    style VERR11 fill:#ffcdd2
    style VERR12 fill:#ffcdd2
```

## データ構造関係図

```mermaid
classDiagram
    class CareReceiver {
        +int id
        +dict subjective_preferences
        +dict objective_fitness
        +list integrated_preferences
    }
    
    class CareWorker {
        +int id
        +int capacity
        +dict subjective_preferences
        +dict objective_fitness
        +list integrated_preferences
    }
    
    class MatchingSystem {
        +list care_receivers
        +list care_workers
        +dict matching_result
        +aggregate_preferences()
        +run_da_algorithm()
        +check_stability()
        +calculate_satisfaction()
    }
    
    class ExtendedKemenyRule {
        +float w_subjective
        +float w_objective
        +aggregate_preferences()
        +kemeny_distance()
        +generate_permutations()
    }
    
    class DeferredAcceptance {
        +create_match()
        +is_stable_matching()
    }
    
    MatchingSystem --> CareReceiver
    MatchingSystem --> CareWorker
    MatchingSystem --> ExtendedKemenyRule
    MatchingSystem --> DeferredAcceptance
```

## 時間複雑度分析（制約検証統合版）

```mermaid
graph LR
    A[制約検証] --> A1["O(n)"]
    B[拡張版Kemenyルール] --> B1["O(n! × n²)"]
    C[DAアルゴリズム] --> C1["O(n²)"]
    D[安定性チェック] --> D1["O(n²)"]
    E[満足度計算] --> E1["O(n)"]
    
    A1 --> F[支配的複雑度]
    B1 --> F
    C1 --> F
    D1 --> F
    E1 --> F
    
    F --> G["全体: O(n! × n²)"]
    
    A --> H[人数制限により n ≤ 100]
    H --> I[実用的な計算時間を保証]
    
    style A fill:#ffe0b2
    style B fill:#fff3e0
    style C fill:#fce4ec
    style D fill:#f3e5f5
    style E fill:#e8f5e8
    style G fill:#ffcdd2
    style H fill:#fff9c4
    style I fill:#c8e6c9
```

## データ構造関係図（制約対応版）

```mermaid
classDiagram
    class InputValidator {
        +MAX_CARE_RECIPIENTS: int = 100
        +MAX_CARE_WORKERS: int = 100
        +validate_participant_count()
        +validate_fitness_scores_are_integers()
        +validate_fitness_uniqueness()
        +validate_complete_input()
    }
    
    class CareReceiver {
        +int id
        +dict subjective_preferences
        +List~int~ objective_fitness
        +list integrated_preferences
    }
    
    class CareWorker {
        +int id
        +int capacity
        +dict subjective_preferences  
        +List~int~ objective_fitness
        +list integrated_preferences
    }
    
    class MatchingSystem {
        +list care_receivers
        +list care_workers
        +dict matching_result
        +aggregate_preferences()
        +run_da_algorithm()
        +check_stability()
        +calculate_satisfaction()
    }
    
    class ExtendedKemenyRule {
        +float w_subjective
        +float w_objective
        +aggregate_preferences()
        +kemeny_distance()
        +generate_permutations()
    }
    
    class DeferredAcceptance {
        +create_match()
        +is_stable_matching()
    }
    
    class ConstraintViolationError {
        <<exception>>
    }
    
    InputValidator --> ConstraintViolationError : raises
    MatchingSystem --> InputValidator : uses
    MatchingSystem --> CareReceiver
    MatchingSystem --> CareWorker
    MatchingSystem --> ExtendedKemenyRule
    MatchingSystem --> DeferredAcceptance
    ExtendedKemenyRule --> InputValidator : uses
    ExtendedKemenyRule --> ConstraintViolationError : raises
```