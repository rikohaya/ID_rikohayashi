#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from openpyxl.utils import get_column_letter

wb = Workbook()
ws = wb.active
ws.title = "辛い麺 5000万"

# スタイル定義
header_font = Font(bold=True, size=9)
header_fill = PatternFill(start_color="FFE4B5", end_color="FFE4B5", fill_type="solid")
phase1_fill = PatternFill(start_color="E6F3FF", end_color="E6F3FF", fill_type="solid")
phase2_fill = PatternFill(start_color="FFF0E6", end_color="FFF0E6", fill_type="solid")
phase3_fill = PatternFill(start_color="E6FFE6", end_color="E6FFE6", fill_type="solid")
ad_fill = PatternFill(start_color="F5F5F5", end_color="F5F5F5", fill_type="solid")
thin_border = Border(
    left=Side(style='thin'),
    right=Side(style='thin'),
    top=Side(style='thin'),
    bottom=Side(style='thin')
)

# 列幅設定
widths = [10, 16, 20, 26, 8, 8, 10, 9, 12, 10, 8, 10, 7, 10, 8, 6, 12, 9, 8, 12, 9, 9]
for i, width in enumerate(widths, 1):
    ws.column_dimensions[get_column_letter(i)].width = width

# ヘッダー行
headers = [
    "フェーズ", "目的", "項目", "小項目", "Media", "配信有無", "フォロワー規模",
    "Allocation\nDetail", "Budget(¥)", "KPI", "FW単価", "合計\nFw数", "投稿数",
    "平均\nフォロワー数", "リーチ率", "FQ", "リーチ数", "リーチ単価", "imp率", "IMP", "IMP単価", "CPM"
]

for col, header in enumerate(headers, 1):
    cell = ws.cell(row=2, column=col, value=header)
    cell.font = header_font
    cell.fill = header_fill
    cell.border = thin_border
    cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)

# データ
# [フェーズ, 目的, 項目, 小項目, Media, 配信有無, フォロワー規模, Allocation, Budget, KPI, FW単価, 合計Fw数, 投稿数, 平均FW数, リーチ率, FQ, リーチ数, リーチ単価, imp率, IMP, IMP単価, CPM]

data = [
    # Phase 1: 発売前
    ["Phase1", "辛いもの\nイノベーター", "メガKOLギフティング", "YouTube/IG/X複合 世界観訴求", "YT/IG/X", "無し", "Mega", "", 2500000, "総リーチ数", 5.0, "", 1, 1200000, 0.2, 3, "", "", 0.5, "", "", ""],
    ["", "", "ミドルKOLギフティング", "辛いものイノベーター層", "TT/IG", "無し", "Middle", "", 2000000, "リーチ数", 4.0, "", 4, 150000, 0.25, 3, "", "", 0.5, "", "", ""],
    ["", "", "商品・SPECIAL BOX", "30名分制作・発送", "-", "-", "-", "", 1000000, "発送数", "", "", "", "", "", "", "", "", "", "", "", ""],
    ["", "広告配信", "広告配信", "ティザー・解禁情報拡散", "X", "", "-", "", 2000000, "imp数", "", "", "", "", "", "", "", "", "", 10000000, 0.2, 200],
    ["", "", "広告配信", "ギフティング投稿ブースト", "TT", "", "-", "", 1000000, "imp数", "", "", "", "", "", "", "", "", "", 5000000, 0.2, 200],

    # Phase 2: 発売期
    ["Phase2", "辛いもの/韓国好き\n（発売盛り上げ）", "メガKOL モッパン", "モッパン系コンテンツ", "TT", "有り", "Mega", "", 2500000, "再生数", 4.0, "", 1, 1500000, 0.3, 3, "", "", 0.5, "", "", ""],
    ["", "", "ミドルKOL モッパン", "新発売HOOK+モッパン", "TT", "有り", "Middle", "", 1500000, "再生数", 4.0, "", 2, 200000, 0.3, 3, "", "", 0.5, "", "", ""],
    ["", "", "商品費", "モッパン系用", "-", "-", "-", "", 500000, "-", "", "", "", "", "", "", "", "", "", "", "", ""],
    ["", "辛い麺顧客獲得\nトライブハック①", "メガKOL", "金曜夜の疲れ/理不尽トラブル後\nワンオペ育児後/チートデイ", "TT", "有り", "Mega", "", 4000000, "再生数", 4.0, "", 1, 1200000, 0.3, 3, "", "", 0.5, "", "", ""],
    ["", "", "ミドルKOL（上位）", "各シーン担当×4名", "TT", "有り", "Middle", "", 6000000, "再生数", 4.0, "", 4, 300000, 0.3, 3, "", "", 0.5, "", "", ""],
    ["", "新規顧客獲得\nトライブハック②", "ミドルKOL（上位）", "推し熱愛/生理前爆食/二日酔い\n一人時間/彼氏旦那イライラ/クラス替え", "TT", "有り", "Middle", "", 6000000, "再生数", 4.0, "", 5, 300000, 0.3, 3, "", "", 0.5, "", "", ""],
    ["", "", "商品費", "トライブハック用", "-", "-", "-", "", 500000, "-", "", "", "", "", "", "", "", "", "", "", "", ""],
    ["", "グルメ系", "グルメ系ミドルKOL", "TikTok/Instagram", "TT/IG", "有り", "Middle", "", 2000000, "リーチ数", 4.0, "", 3, 200000, 0.25, 3, "", "", 0.5, "", "", ""],
    ["", "広告配信", "広告配信", "KOL投稿ブースト Spark Ads", "TT", "", "-", "", 5000000, "imp数", "", "", "", "", "", "", "", "", "", 25000000, 0.2, 200],
    ["", "", "広告配信", "トレンド入り狙い・話題拡散", "X", "", "-", "", 2000000, "imp数", "", "", "", "", "", "", "", "", "", 10000000, 0.2, 200],

    # Phase 3: 発売後
    ["Phase3", "SNSトレンド好き\n（UGC醸成）", "ミドルKOL アレンジ", "チーズ/卵/〆ご飯等", "TT", "有り", "Middle", "", 1100000, "再生数", 4.0, "", 2, 180000, 0.25, 3, "", "", 0.5, "", "", ""],
    ["", "", "マイクロKOL アレンジ", "バリエーション展開", "TT", "有り", "Nano", "", 200000, "再生数", 5.0, "", 2, 40000, 0.35, 3, "", "", 0.5, "", "", ""],
    ["", "", "ミドルKOL アレンジ", "アレンジ投稿", "X", "無し", "Middle", "", 200000, "imp数", 2.0, "", 1, 150000, 0.2, 3, "", "", 0.5, "", "", ""],
    ["", "SNS話題HOOK", "ミドルKOL", "○○見ながら訴求", "TT", "有り", "Middle", "", 700000, "再生数", 4.0, "", 1, 180000, 0.25, 3, "", "", 0.5, "", "", ""],
    ["", "", "マイクロKOL", "サブ投稿", "TT", "有り", "Nano", "", 300000, "再生数", 5.0, "", 2, 40000, 0.35, 3, "", "", 0.5, "", "", ""],
    ["", "ミーム系チャレンジ", "ペイドKOL", "チャレンジ火付け役", "TT", "有り", "Middle", "", 2000000, "参加数", 4.0, "", 4, 150000, 0.3, 3, "", "", 0.5, "", "", ""],
    ["", "", "チャレンジ運用費", "ハッシュタグ管理等", "-", "-", "-", "", 700000, "-", "", "", "", "", "", "", "", "", "", "", "", ""],
    ["", "広告配信", "広告配信", "アレンジ・ミーム拡散", "TT", "", "-", "", 2500000, "imp数", "", "", "", "", "", "", "", "", "", 12500000, 0.2, 200],
    ["", "", "広告配信", "Reelsリターゲティング", "IG", "", "-", "", 1500000, "imp数", "", "", "", "", "", "", "", "", "", 6000000, 0.25, 250],

    # 予備費
    ["予備費", "", "追加ブースト対応", "", "-", "-", "-", "", 300000, "-", "", "", "", "", "", "", "", "", "", "", "", ""],
    ["", "", "緊急対応・リスク管理", "", "-", "-", "-", "", 200000, "-", "", "", "", "", "", "", "", "", "", "", "", ""],
]

# データ入力
start_row = 3
for row_idx, row_data in enumerate(data):
    current_row = start_row + row_idx

    # フェーズに応じた色分け
    if row_data[0] == "Phase1" or (row_idx < 5):
        fill = phase1_fill
    elif row_data[0] == "Phase2" or (5 <= row_idx < 15):
        fill = phase2_fill
    elif row_data[0] == "Phase3" or (15 <= row_idx < 25):
        fill = phase3_fill
    else:
        fill = None

    # 広告配信行は別色
    if "広告配信" in str(row_data[1]) or "広告配信" in str(row_data[2]):
        fill = ad_fill

    for col_idx, value in enumerate(row_data):
        cell = ws.cell(row=current_row, column=col_idx + 1, value=value)
        cell.border = thin_border
        cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
        cell.font = Font(size=9)
        if fill:
            cell.fill = fill

        # 数値フォーマット
        if col_idx == 8 and isinstance(value, (int, float)) and value > 0:  # Budget
            cell.number_format = '#,##0'
        if col_idx == 13 and isinstance(value, (int, float)) and value > 0:  # 平均FW数
            cell.number_format = '#,##0'
        if col_idx in [14, 18] and isinstance(value, (int, float)):  # リーチ率、imp率
            cell.number_format = '0%'
        if col_idx == 19 and isinstance(value, (int, float)) and value > 0:  # IMP
            cell.number_format = '#,##0'

# Allocation Detail の数式を設定
total_row = start_row + len(data)
for row_idx in range(len(data)):
    current_row = start_row + row_idx
    budget_value = ws.cell(row=current_row, column=9).value
    if isinstance(budget_value, (int, float)) and budget_value > 0:
        ws.cell(row=current_row, column=8, value=f"=I{current_row}/$I${total_row}")
        ws.cell(row=current_row, column=8).number_format = '0%'
        ws.cell(row=current_row, column=8).alignment = Alignment(horizontal='center', vertical='center')

# 合計Fw数の計算（Budget / FW単価）
for row_idx in range(len(data)):
    current_row = start_row + row_idx
    fw_unit = ws.cell(row=current_row, column=11).value
    if isinstance(fw_unit, (int, float)) and fw_unit > 0:
        ws.cell(row=current_row, column=12, value=f"=I{current_row}/K{current_row}")
        ws.cell(row=current_row, column=12).number_format = '#,##0'

# リーチ数の計算（投稿数 × 平均FW数 × リーチ率 × FQ）
for row_idx in range(len(data)):
    current_row = start_row + row_idx
    posts = ws.cell(row=current_row, column=13).value
    avg_fw = ws.cell(row=current_row, column=14).value
    if isinstance(posts, (int, float)) and posts > 0 and isinstance(avg_fw, (int, float)) and avg_fw > 0:
        ws.cell(row=current_row, column=17, value=f"=M{current_row}*N{current_row}*O{current_row}*P{current_row}")
        ws.cell(row=current_row, column=17).number_format = '#,##0'
        # リーチ単価
        ws.cell(row=current_row, column=18, value=f"=IF(Q{current_row}>0,I{current_row}/Q{current_row},\"\")")
        ws.cell(row=current_row, column=18).number_format = '#,##0.0'
        # IMP（リーチ数 × imp率）- 広告以外
        if "広告" not in str(data[row_idx][2]):
            ws.cell(row=current_row, column=20, value=f"=Q{current_row}/S{current_row}")
            ws.cell(row=current_row, column=20).number_format = '#,##0'
            # IMP単価
            ws.cell(row=current_row, column=21, value=f"=IF(T{current_row}>0,I{current_row}/T{current_row},\"\")")
            ws.cell(row=current_row, column=21).number_format = '#,##0.0'
            # CPM
            ws.cell(row=current_row, column=22, value=f"=IF(T{current_row}>0,I{current_row}/T{current_row}*1000,\"\")")
            ws.cell(row=current_row, column=22).number_format = '#,##0'

# 広告行のIMP単価とCPM計算
for row_idx in range(len(data)):
    current_row = start_row + row_idx
    if "広告" in str(data[row_idx][2]):
        imp_val = ws.cell(row=current_row, column=20).value
        if isinstance(imp_val, (int, float)) and imp_val > 0:
            # IMP単価
            ws.cell(row=current_row, column=21, value=f"=I{current_row}/T{current_row}")
            ws.cell(row=current_row, column=21).number_format = '0.00'
            # CPM
            ws.cell(row=current_row, column=22, value=f"=I{current_row}/T{current_row}*1000")
            ws.cell(row=current_row, column=22).number_format = '#,##0'

# 合計行
ws.cell(row=total_row, column=7, value="合計").font = Font(bold=True, size=9)
ws.cell(row=total_row, column=8, value=f"=SUM(H{start_row}:H{total_row-1})")
ws.cell(row=total_row, column=8).number_format = '0%'
ws.cell(row=total_row, column=9, value=f"=SUM(I{start_row}:I{total_row-1})")
ws.cell(row=total_row, column=9).number_format = '#,##0'
ws.cell(row=total_row, column=9).font = Font(bold=True, size=9)
ws.cell(row=total_row, column=13, value=f"=SUM(M{start_row}:M{total_row-1})")
ws.cell(row=total_row, column=13).font = Font(bold=True, size=9)
ws.cell(row=total_row, column=17, value=f"=SUM(Q{start_row}:Q{total_row-1})")
ws.cell(row=total_row, column=17).number_format = '#,##0'
ws.cell(row=total_row, column=17).font = Font(bold=True, size=9)
ws.cell(row=total_row, column=20, value=f"=SUM(T{start_row}:T{total_row-1})")
ws.cell(row=total_row, column=20).number_format = '#,##0'
ws.cell(row=total_row, column=20).font = Font(bold=True, size=9)

for col in range(1, 23):
    ws.cell(row=total_row, column=col).border = thin_border

# 下部にサマリーテーブル追加
summary_start = total_row + 3

ws.cell(row=summary_start, column=2, value="月").font = Font(bold=True, size=9)
ws.cell(row=summary_start, column=3, value="フェーズ").font = Font(bold=True, size=9)
ws.cell(row=summary_start, column=4, value="費用").font = Font(bold=True, size=9)

summary_data = [
    ["発売前", "Phase1: 話題化", f"=SUM(I{start_row}:I{start_row+4})"],
    ["発売期", "Phase2: 盛り上げ", f"=SUM(I{start_row+5}:I{start_row+14})"],
    ["発売後", "Phase3: UGC醸成", f"=SUM(I{start_row+15}:I{start_row+23})"],
    ["", "予備費", f"=SUM(I{start_row+24}:I{start_row+25})"],
    ["合計", "", f"=I{total_row}"],
]

for idx, (month, phase, cost) in enumerate(summary_data):
    row = summary_start + 1 + idx
    ws.cell(row=row, column=2, value=month).font = Font(size=9)
    ws.cell(row=row, column=3, value=phase).font = Font(size=9)
    ws.cell(row=row, column=4, value=cost).font = Font(size=9)
    ws.cell(row=row, column=4).number_format = '#,##0'
    if idx == len(summary_data) - 1:
        ws.cell(row=row, column=4).font = Font(bold=True, size=9)

# ファイル保存
output_path = "/Users/rikohayashi/Downloads/AP/辛い麺_メディアプラン_5000万_v3.xlsx"
wb.save(output_path)
print(f"Excel file created: {output_path}")
