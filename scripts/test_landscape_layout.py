#!/usr/bin/env python3
"""
横向きPDFレイアウトのテストスクリプト

横向きレイアウトでのテーブル幅やフォントサイズの最適化をテストします。

Author: 倉持誠 (Makoto Kuramochi)
"""

from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import inch


def calculate_landscape_layout():
    """横向きレイアウトの寸法を計算"""
    
    print("=== 横向きPDFレイアウト計算 ===")
    
    # A4縦向きと横向きの寸法
    portrait_width, portrait_height = A4
    landscape_width, landscape_height = landscape(A4)
    
    print(f"縦向きA4: 幅 {portrait_width:.1f} pt ({portrait_width/inch:.2f} inch), 高さ {portrait_height:.1f} pt ({portrait_height/inch:.2f} inch)")
    print(f"横向きA4: 幅 {landscape_width:.1f} pt ({landscape_width/inch:.2f} inch), 高さ {landscape_height:.1f} pt ({landscape_height/inch:.2f} inch)")
    
    # マージンを考慮した利用可能なスペース
    margin = 0.5 * inch
    available_width = landscape_width - (2 * margin)
    available_height = landscape_height - (2 * margin)
    
    print(f"\n利用可能なスペース:")
    print(f"幅: {available_width:.1f} pt ({available_width/inch:.2f} inch)")
    print(f"高さ: {available_height:.1f} pt ({available_height/inch:.2f} inch)")
    
    # テーブル設計の推奨値
    print(f"\n=== テーブル設計推奨値 ===")
    
    # サマリーテーブル (5列)
    summary_cols = 5
    summary_total_width = available_width * 0.8  # 80%使用
    summary_avg_width = summary_total_width / summary_cols
    print(f"サマリーテーブル (5列):")
    print(f"  推奨総幅: {summary_total_width/inch:.2f} inch")
    print(f"  平均列幅: {summary_avg_width/inch:.2f} inch")
    
    # Kemeny入力テーブル (7列)
    kemeny_input_cols = 7
    kemeny_input_total_width = available_width * 0.95  # 95%使用
    kemeny_input_avg_width = kemeny_input_total_width / kemeny_input_cols
    print(f"Kemeny入力テーブル (7列):")
    print(f"  推奨総幅: {kemeny_input_total_width/inch:.2f} inch")
    print(f"  平均列幅: {kemeny_input_avg_width/inch:.2f} inch")
    
    # Kemeny結果テーブル (11列)
    kemeny_result_cols = 11
    kemeny_result_total_width = available_width * 0.95  # 95%使用
    kemeny_result_avg_width = kemeny_result_total_width / kemeny_result_cols
    print(f"Kemeny結果テーブル (11列):")
    print(f"  推奨総幅: {kemeny_result_total_width/inch:.2f} inch")
    print(f"  平均列幅: {kemeny_result_avg_width/inch:.2f} inch")
    
    # DA入力テーブル (6列)
    da_input_cols = 6
    da_input_total_width = available_width * 0.9  # 90%使用
    da_input_avg_width = da_input_total_width / da_input_cols
    print(f"DA入力テーブル (6列):")
    print(f"  推奨総幅: {da_input_total_width/inch:.2f} inch")
    print(f"  平均列幅: {da_input_avg_width/inch:.2f} inch")
    
    # DA結果テーブル (11列)
    da_result_cols = 11
    da_result_total_width = available_width * 0.95  # 95%使用
    da_result_avg_width = da_result_total_width / da_result_cols
    print(f"DA結果テーブル (11列):")
    print(f"  推奨総幅: {da_result_total_width/inch:.2f} inch")
    print(f"  平均列幅: {da_result_avg_width/inch:.2f} inch")
    
    # 推奨フォントサイズ
    print(f"\n=== 推奨フォントサイズ ===")
    print(f"タイトル: 18-20pt")
    print(f"見出し: 14-16pt")
    print(f"テーブルヘッダー: 9-11pt")
    print(f"テーブル内容: 7-9pt")
    print(f"小さなテキスト: 6-8pt")
    
    # 現在の設定と比較
    print(f"\n=== 現在の設定確認 ===")
    current_kemeny_total = 1.5 + 2.2 + 1.2 + 1.2 + 0.7 + 0.7 + 0.9 + 0.9 + 0.7 + 0.7 + 0.8
    current_da_total = 1.2 + 1.8 + 1.0 + 1.0 + 1.0 + 1.4 + 1.4 + 1.0 + 1.0 + 0.7 + 0.8
    
    print(f"現在のKemeny結果テーブル総幅: {current_kemeny_total:.2f} inch")
    print(f"利用可能幅に対する割合: {(current_kemeny_total * inch / available_width) * 100:.1f}%")
    print(f"現在のDA結果テーブル総幅: {current_da_total:.2f} inch")
    print(f"利用可能幅に対する割合: {(current_da_total * inch / available_width) * 100:.1f}%")
    
    if current_kemeny_total * inch > available_width:
        print("⚠️ Kemeny結果テーブルが利用可能幅を超えています")
    else:
        print("✅ Kemeny結果テーブルは適切なサイズです")
        
    if current_da_total * inch > available_width:
        print("⚠️ DA結果テーブルが利用可能幅を超えています")
    else:
        print("✅ DA結果テーブルは適切なサイズです")


if __name__ == "__main__":
    calculate_landscape_layout()