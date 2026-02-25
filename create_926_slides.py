#!/usr/bin/env python3
"""推し活とグッズ購買に関するアンケート(926) スライド生成スクリプト"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION, XL_LABEL_POSITION
from pptx.chart.data import CategoryChartData
import math

# ── カラーパレット ──
BG_COLOR = RGBColor(0xF8, 0xF5, 0xF0)       # 温かみのあるベージュ背景
TITLE_COLOR = RGBColor(0x2D, 0x2D, 0x2D)     # ダークグレー
ACCENT_1 = RGBColor(0xE8, 0x6B, 0x6B)        # コーラルピンク
ACCENT_2 = RGBColor(0x7E, 0xB8, 0xDA)        # スカイブルー
ACCENT_3 = RGBColor(0x9B, 0xC4, 0x8E)        # セージグリーン
ACCENT_4 = RGBColor(0xF0, 0xB8, 0x6E)        # ゴールド
ACCENT_5 = RGBColor(0xBB, 0x8F, 0xCE)        # ラベンダー
ACCENT_6 = RGBColor(0xE8, 0x9E, 0xB0)        # ローズ
TEXT_DARK = RGBColor(0x3A, 0x3A, 0x3A)
TEXT_LIGHT = RGBColor(0x6B, 0x6B, 0x6B)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT_GRAY = RGBColor(0xE0, 0xE0, 0xE0)

CHART_COLORS = [
    RGBColor(0xE8, 0x6B, 0x6B),  # コーラルピンク
    RGBColor(0x7E, 0xB8, 0xDA),  # スカイブルー
    RGBColor(0x9B, 0xC4, 0x8E),  # セージグリーン
    RGBColor(0xF0, 0xB8, 0x6E),  # ゴールド
    RGBColor(0xBB, 0x8F, 0xCE),  # ラベンダー
    RGBColor(0xE8, 0x9E, 0xB0),  # ローズ
    RGBColor(0x8E, 0xC4, 0xC4),  # ティール
    RGBColor(0xD4, 0xA0, 0x7A),  # キャメル
    RGBColor(0xA8, 0xA8, 0xD8),  # パープル
    RGBColor(0xC4, 0xD4, 0x8E),  # ライムグリーン
    RGBColor(0xE0, 0x80, 0x80),  # サーモン
]


def set_slide_bg(slide, color):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_rounded_rect(slide, left, top, width, height, fill_color, shadow=False):
    from pptx.oxml.ns import qn
    shape = slide.shapes.add_shape(
        5,  # MSO_SHAPE.ROUNDED_RECTANGLE
        left, top, width, height
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    shape.line.fill.background()
    # 角丸を調整
    sp = shape._element
    prstGeom = sp.find(qn('a:prstGeom'), sp.nsmap if hasattr(sp, 'nsmap') else
                       {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'})
    if prstGeom is None:
        for child in sp:
            if 'prstGeom' in child.tag:
                prstGeom = child
                break
    return shape


def add_text_box(slide, left, top, width, height, text, font_size=12,
                 font_color=TEXT_DARK, bold=False, alignment=PP_ALIGN.LEFT,
                 font_name="Yu Gothic"):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.color.rgb = font_color
    p.font.bold = bold
    p.font.name = font_name
    p.alignment = alignment
    return txBox


def create_horizontal_bar_chart(slide, left, top, width, height,
                                 categories, values, title, chart_colors=None,
                                 show_percent=True):
    """水平バーチャートを図形で描画"""
    # タイトル
    add_text_box(slide, left, top, width, Inches(0.4), title,
                 font_size=11, bold=True, font_color=TITLE_COLOR)

    bar_area_top = top + Inches(0.45)
    n = len(categories)
    bar_height = min(Inches(0.32), (height - Inches(0.5)) / n)
    gap = Inches(0.04)
    label_width = Inches(2.8)
    bar_max_width = width - label_width - Inches(0.6)
    max_val = max(values) if max(values) > 0 else 1

    colors = chart_colors or CHART_COLORS

    for i, (cat, val) in enumerate(zip(categories, values)):
        y = bar_area_top + i * (bar_height + gap)

        # ラベル
        add_text_box(slide, left, y, label_width, bar_height,
                     cat, font_size=8, font_color=TEXT_DARK,
                     alignment=PP_ALIGN.RIGHT)

        # バー
        bar_w = int(bar_max_width * (val / max_val)) if val > 0 else Inches(0.05)
        bar = slide.shapes.add_shape(
            1,  # RECTANGLE
            left + label_width + Inches(0.08), y + Inches(0.02),
            bar_w, bar_height - Inches(0.04)
        )
        bar.fill.solid()
        bar.fill.fore_color.rgb = colors[i % len(colors)]
        bar.line.fill.background()

        # 値ラベル
        label_text = f"{val:.1f}%" if show_percent else f"{val}"
        add_text_box(slide, left + label_width + Inches(0.12) + bar_w, y,
                     Inches(0.6), bar_height,
                     label_text, font_size=8, font_color=TEXT_LIGHT)


def create_pie_shapes(slide, left, top, size, categories, values, colors=None):
    """パイチャートをpptxのチャート機能で描画"""
    chart_data = CategoryChartData()
    chart_data.categories = categories
    chart_data.add_series('', tuple(values))

    chart_frame = slide.shapes.add_chart(
        XL_CHART_TYPE.PIE, left, top, size, size, chart_data
    )
    chart = chart_frame.chart
    chart.has_legend = True
    chart.legend.position = XL_LEGEND_POSITION.BOTTOM
    chart.legend.include_in_layout = False
    chart.legend.font.size = Pt(8)
    chart.legend.font.name = "Yu Gothic"

    plot = chart.plots[0]
    plot.has_data_labels = True
    data_labels = plot.data_labels
    data_labels.number_format = '0.0"%"'
    data_labels.font.size = Pt(9)
    data_labels.font.name = "Yu Gothic"
    data_labels.font.bold = True

    # 色設定
    palette = colors or CHART_COLORS
    series = chart.series[0]
    for i in range(len(categories)):
        point = series.points[i]
        point.format.fill.solid()
        point.format.fill.fore_color.rgb = palette[i % len(palette)]

    return chart_frame


def create_bar_chart_native(slide, left, top, width, height,
                            categories, values, title_text, colors=None):
    """ネイティブバーチャート"""
    chart_data = CategoryChartData()
    chart_data.categories = categories
    chart_data.add_series('', tuple(values))

    chart_frame = slide.shapes.add_chart(
        XL_CHART_TYPE.BAR_CLUSTERED, left, top, width, height, chart_data
    )
    chart = chart_frame.chart
    chart.has_legend = False
    chart.has_title = True
    chart.chart_title.text_frame.paragraphs[0].text = title_text
    chart.chart_title.text_frame.paragraphs[0].font.size = Pt(11)
    chart.chart_title.text_frame.paragraphs[0].font.name = "Yu Gothic"
    chart.chart_title.text_frame.paragraphs[0].font.bold = True

    plot = chart.plots[0]
    plot.has_data_labels = True
    plot.data_labels.number_format = '0.0"%"'
    plot.data_labels.font.size = Pt(8)
    plot.data_labels.font.name = "Yu Gothic"
    plot.gap_width = 80

    palette = colors or CHART_COLORS
    series = chart.series[0]
    for i in range(len(categories)):
        point = series.points[i]
        point.format.fill.solid()
        point.format.fill.fore_color.rgb = palette[i % len(palette)]

    # Y軸（カテゴリ軸）
    cat_axis = chart.category_axis
    cat_axis.tick_labels.font.size = Pt(8)
    cat_axis.tick_labels.font.name = "Yu Gothic"
    cat_axis.has_major_gridlines = False

    # X軸（値軸）
    val_axis = chart.value_axis
    val_axis.has_major_gridlines = True
    val_axis.major_gridlines.format.line.color.rgb = LIGHT_GRAY
    val_axis.tick_labels.font.size = Pt(8)

    return chart_frame


# ── スライド生成 ──
prs = Presentation()
prs.slide_width = Inches(13.33)
prs.slide_height = Inches(7.5)

# ===========================================
# SLIDE 1: 表紙
# ===========================================
slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank
set_slide_bg(slide, BG_COLOR)

# 上部アクセントライン
line_shape = slide.shapes.add_shape(1, Inches(0), Inches(0), prs.slide_width, Inches(0.08))
line_shape.fill.solid()
line_shape.fill.fore_color.rgb = ACCENT_1
line_shape.line.fill.background()

# メインタイトルエリア
add_text_box(slide, Inches(1.5), Inches(2.0), Inches(10), Inches(1.2),
             "推し活とグッズ購買に関するアンケート",
             font_size=36, bold=True, font_color=TITLE_COLOR,
             alignment=PP_ALIGN.CENTER)

add_text_box(slide, Inches(1.5), Inches(3.3), Inches(10), Inches(0.6),
             "調査結果レポート",
             font_size=20, font_color=ACCENT_1,
             alignment=PP_ALIGN.CENTER)

# サーベイ情報
info_texts = [
    "調査期間：2026年2月18日〜2月19日",
    "対象：全国 15〜30歳 女性",
    "サンプル数：n=1,000",
]
for i, txt in enumerate(info_texts):
    add_text_box(slide, Inches(3.5), Inches(4.5 + i * 0.4), Inches(6), Inches(0.4),
                 txt, font_size=14, font_color=TEXT_LIGHT,
                 alignment=PP_ALIGN.CENTER)

# 下部アクセントライン
line_shape2 = slide.shapes.add_shape(1, Inches(0), Inches(7.42), prs.slide_width, Inches(0.08))
line_shape2.fill.solid()
line_shape2.fill.fore_color.rgb = ACCENT_1
line_shape2.line.fill.background()


# ===========================================
# SLIDE 2: 回答者プロフィール
# ===========================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide, BG_COLOR)

# ヘッダー
header_bg = slide.shapes.add_shape(1, Inches(0), Inches(0), prs.slide_width, Inches(0.9))
header_bg.fill.solid()
header_bg.fill.fore_color.rgb = ACCENT_1
header_bg.line.fill.background()
add_text_box(slide, Inches(0.5), Inches(0.15), Inches(10), Inches(0.6),
             "回答者プロフィール", font_size=24, bold=True, font_color=WHITE,
             alignment=PP_ALIGN.LEFT)

# 年代パイチャート
age_cats = ["10代", "20代", "30代"]
age_vals = [18.5, 69.9, 11.6]
create_pie_shapes(slide, Inches(0.5), Inches(1.2), Inches(4.0),
                  age_cats, age_vals, [ACCENT_1, ACCENT_2, ACCENT_3])
add_text_box(slide, Inches(0.5), Inches(1.0), Inches(4.0), Inches(0.3),
             "年代構成（n=1,000）", font_size=12, bold=True, font_color=TITLE_COLOR,
             alignment=PP_ALIGN.CENTER)

# 婚姻状況
marital_cats = ["未婚", "既婚"]
marital_vals = [81.7, 18.3]
create_pie_shapes(slide, Inches(4.8), Inches(1.2), Inches(3.5),
                  marital_cats, marital_vals, [ACCENT_2, ACCENT_4])
add_text_box(slide, Inches(4.8), Inches(1.0), Inches(3.5), Inches(0.3),
             "婚姻状況（n=1,000）", font_size=12, bold=True, font_color=TITLE_COLOR,
             alignment=PP_ALIGN.CENTER)

# 職業（上位のみ）
job_cats = ["会社員(正社員)", "学生", "パート・アルバイト", "無職", "会社員(契約等)", "専業主婦", "その他"]
job_vals = [27.9, 26.9, 16.6, 10.1, 4.5, 4.2, 9.8]
create_bar_chart_native(slide, Inches(8.5), Inches(1.0), Inches(4.5), Inches(3.0),
                        job_cats, job_vals, "職業構成（n=1,000）")

# 子供有無
child_cats = ["子供あり", "子供なし"]
child_vals = [11.2, 88.8]
create_pie_shapes(slide, Inches(0.5), Inches(4.5), Inches(3.5),
                  child_cats, child_vals, [ACCENT_4, ACCENT_3])
add_text_box(slide, Inches(0.5), Inches(4.3), Inches(3.5), Inches(0.3),
             "子供の有無（n=1,000）", font_size=12, bold=True, font_color=TITLE_COLOR,
             alignment=PP_ALIGN.CENTER)

# 世帯年収
income_cats = ["〜100万", "100〜300万", "300〜500万", "500〜700万", "700〜1000万", "1000万〜"]
income_vals = [16.9, 18.9, 20.9, 15.7, 14.0, 13.6]
create_bar_chart_native(slide, Inches(4.3), Inches(4.3), Inches(4.5), Inches(3.0),
                        income_cats, income_vals, "世帯年収（n=1,000）")

# 居住エリアTOP5
area_cats = ["東京都", "大阪府", "神奈川県", "兵庫県", "埼玉県"]
area_vals = [14.4, 9.8, 7.5, 6.2, 5.9]
create_bar_chart_native(slide, Inches(8.8), Inches(4.3), Inches(4.3), Inches(3.0),
                        area_cats, area_vals, "居住地TOP5（n=1,000）")


# ===========================================
# SLIDE 3: Q1 推しの有無
# ===========================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide, BG_COLOR)

header_bg = slide.shapes.add_shape(1, Inches(0), Inches(0), prs.slide_width, Inches(0.9))
header_bg.fill.solid()
header_bg.fill.fore_color.rgb = ACCENT_2
header_bg.line.fill.background()
add_text_box(slide, Inches(0.5), Inches(0.15), Inches(12), Inches(0.6),
             "Q1. 推し（アイドル／俳優／アーティスト等）はいますか？",
             font_size=22, bold=True, font_color=WHITE)

add_text_box(slide, Inches(10.5), Inches(0.2), Inches(2.5), Inches(0.4),
             "n=1,000 / SA", font_size=12, font_color=WHITE, alignment=PP_ALIGN.RIGHT)

# パイチャート
q1_cats = ["現在いる", "過去にいた", "いない"]
q1_vals = [56.1, 12.4, 31.5]
create_pie_shapes(slide, Inches(1.0), Inches(1.5), Inches(5.0),
                  q1_cats, q1_vals, [ACCENT_1, ACCENT_4, LIGHT_GRAY])

# Key Findings
card = add_rounded_rect(slide, Inches(7.0), Inches(1.5), Inches(5.5), Inches(4.5), WHITE)
add_text_box(slide, Inches(7.3), Inches(1.7), Inches(5.0), Inches(0.4),
             "KEY FINDINGS", font_size=14, bold=True, font_color=ACCENT_2)

findings = [
    "推しが「現在いる」と回答した人は 56.1%で過半数超",
    "「過去にいた」12.4%を含めると、約7割（68.5%）が推し活経験者",
    "15〜30歳女性の推し活参加率は非常に高い",
    "→ この層はグッズ購買のコアターゲットとなりうる"
]
for i, f in enumerate(findings):
    marker = "●" if i < 3 else ""
    add_text_box(slide, Inches(7.5), Inches(2.3 + i * 0.7), Inches(4.8), Inches(0.6),
                 f"{marker} {f}" if marker else f, font_size=12, font_color=TEXT_DARK)

# 強調数値
add_text_box(slide, Inches(1.0), Inches(6.0), Inches(3.5), Inches(0.8),
             "推し活経験率  68.5%", font_size=22, bold=True,
             font_color=ACCENT_1, alignment=PP_ALIGN.CENTER)


# ===========================================
# SLIDE 4: Q2 グッズ購入頻度
# ===========================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide, BG_COLOR)

header_bg = slide.shapes.add_shape(1, Inches(0), Inches(0), prs.slide_width, Inches(0.9))
header_bg.fill.solid()
header_bg.fill.fore_color.rgb = ACCENT_3
header_bg.line.fill.background()
add_text_box(slide, Inches(0.5), Inches(0.15), Inches(12), Inches(0.6),
             "Q2. 推し関連グッズをどれくらいの頻度で購入しますか？",
             font_size=22, bold=True, font_color=WHITE)
add_text_box(slide, Inches(10.5), Inches(0.2), Inches(2.5), Inches(0.4),
             "n=685 / SA", font_size=12, font_color=WHITE, alignment=PP_ALIGN.RIGHT)

# バーチャート
q2_cats = ["月1回以上", "2〜3か月に1回", "半年に1回", "年1回程度", "ほとんど買わない"]
q2_vals = [22.63, 28.47, 14.89, 8.61, 25.40]
create_bar_chart_native(slide, Inches(0.8), Inches(1.3), Inches(6.5), Inches(5.5),
                        q2_cats, q2_vals, "購入頻度")

# Key Findings
card = add_rounded_rect(slide, Inches(7.8), Inches(1.5), Inches(5.0), Inches(5.0), WHITE)
add_text_box(slide, Inches(8.1), Inches(1.7), Inches(4.5), Inches(0.4),
             "KEY FINDINGS", font_size=14, bold=True, font_color=ACCENT_3)

findings2 = [
    "「月1回以上」22.6% + 「2〜3か月に1回」28.5%\n→ ヘビーバイヤー層が約51%",
    "「半年に1回」14.9% はライトバイヤー層",
    "「ほとんど買わない」25.4% も\n推し活経験者であり潜在顧客",
    "→ 購入頻度の二極化が見られる\n  （月1回以上 vs ほとんど買わない）"
]
for i, f in enumerate(findings2):
    add_text_box(slide, Inches(8.3), Inches(2.3 + i * 1.1), Inches(4.3), Inches(1.0),
                 f"● {f}", font_size=11, font_color=TEXT_DARK)


# ===========================================
# SLIDE 5: Q3 グッズ購入時の重視ポイント
# ===========================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide, BG_COLOR)

header_bg = slide.shapes.add_shape(1, Inches(0), Inches(0), prs.slide_width, Inches(0.9))
header_bg.fill.solid()
header_bg.fill.fore_color.rgb = ACCENT_4
header_bg.line.fill.background()
add_text_box(slide, Inches(0.5), Inches(0.15), Inches(12), Inches(0.6),
             "Q3. グッズ購入時に重視するポイント（最大3つ）",
             font_size=22, bold=True, font_color=WHITE)
add_text_box(slide, Inches(10.5), Inches(0.2), Inches(2.5), Inches(0.4),
             "n=685 / MA", font_size=12, font_color=WHITE, alignment=PP_ALIGN.RIGHT)

q3_cats = [
    "推しのビジュアル", "デザイン（グッズの見た目）",
    "実用性（普段使い）", "価格の納得感",
    "サイズ感", "希少性（限定）",
    "展示性（飾りやすい）", "加工しやすさ"
]
q3_vals = [54.01, 47.30, 35.62, 23.21, 20.73, 12.12, 9.49, 3.21]

create_bar_chart_native(slide, Inches(0.5), Inches(1.2), Inches(7.5), Inches(5.8),
                        q3_cats, q3_vals, "重視ポイント（%）")

# Insight
card = add_rounded_rect(slide, Inches(8.3), Inches(1.3), Inches(4.7), Inches(5.5), WHITE)
add_text_box(slide, Inches(8.5), Inches(1.5), Inches(4.3), Inches(0.4),
             "INSIGHT", font_size=14, bold=True, font_color=ACCENT_4)

insights = [
    "TOP1「推しのビジュアル」54.0%\n→ 表情・衣装・写真の品質が最重要",
    "TOP2「デザイン」47.3%\n→ 推し関係なくグッズ自体のデザイン性",
    "TOP3「実用性」35.6%\n→ 普段使いできることへのニーズ",
    "「価格の納得感」23.2%\n→ 4人に1人が価格を重視",
    "→ ビジュアル品質 × 実用性 × デザイン性\n  この3要素が購買の鍵"
]
for i, ins in enumerate(insights):
    color = ACCENT_1 if i == 4 else TEXT_DARK
    add_text_box(slide, Inches(8.6), Inches(2.1 + i * 1.0), Inches(4.2), Inches(0.9),
                 f"{'→' if i == 4 else '●'} {ins}", font_size=10, font_color=color,
                 bold=(i == 4))


# ===========================================
# SLIDE 6: Q4 「これなら買ってしまう」グッズ
# ===========================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide, BG_COLOR)

header_bg = slide.shapes.add_shape(1, Inches(0), Inches(0), prs.slide_width, Inches(0.9))
header_bg.fill.solid()
header_bg.fill.fore_color.rgb = ACCENT_5
header_bg.line.fill.background()
add_text_box(slide, Inches(0.5), Inches(0.15), Inches(12), Inches(0.6),
             'Q4.「これなら買ってしまう」グッズはどれですか？（最大3つ）',
             font_size=22, bold=True, font_color=WHITE)
add_text_box(slide, Inches(10.5), Inches(0.2), Inches(2.5), Inches(0.4),
             "n=685 / MA", font_size=12, font_color=WHITE, alignment=PP_ALIGN.RIGHT)

q4_cats = [
    "キーホルダー／チャーム", "アクリルスタンド", "トレカ（フォトカード）",
    "ポーチ／小物入れ", "生写真", "ステッカー",
    "アパレル（Tシャツ等）", "缶バッジ",
    "タンブラー／ボトル", "限定ボイス／デジタル特典"
]
q4_vals = [50.66, 47.74, 39.42, 33.87, 26.86, 25.11, 22.34, 20.58, 17.96, 12.12]

create_bar_chart_native(slide, Inches(0.5), Inches(1.2), Inches(7.5), Inches(5.8),
                        q4_cats, q4_vals, "購入意向グッズランキング（%）")

# Insight
card = add_rounded_rect(slide, Inches(8.3), Inches(1.3), Inches(4.7), Inches(5.5), WHITE)
add_text_box(slide, Inches(8.5), Inches(1.5), Inches(4.3), Inches(0.4),
             "INSIGHT", font_size=14, bold=True, font_color=ACCENT_5)

insights4 = [
    "TOP1「キーホルダー／チャーム」50.7%\n→ 手軽さ・持ち運びやすさが人気",
    "TOP2「アクリルスタンド」47.7%\n→ 飾る＆持ち運ぶ両用途で高人気",
    "TOP3「トレカ」39.4%\n→ コレクション性が高い定番アイテム",
    "「ポーチ／小物入れ」33.9%\n→ 実用性グッズの代表格",
    "→ 実用性＋コレクション性の\n  両方を兼ね備えたグッズが強い"
]
for i, ins in enumerate(insights4):
    color = ACCENT_1 if i == 4 else TEXT_DARK
    add_text_box(slide, Inches(8.6), Inches(2.1 + i * 1.0), Inches(4.2), Inches(0.9),
                 f"{'→' if i == 4 else '●'} {ins}", font_size=10, font_color=color,
                 bold=(i == 4))


# ===========================================
# SLIDE 7: Q5 コラボで嬉しいポイント
# ===========================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide, BG_COLOR)

header_bg = slide.shapes.add_shape(1, Inches(0), Inches(0), prs.slide_width, Inches(0.9))
header_bg.fill.solid()
header_bg.fill.fore_color.rgb = ACCENT_6
header_bg.line.fill.background()
add_text_box(slide, Inches(0.5), Inches(0.15), Inches(12), Inches(0.6),
             "Q5. 推し×企業コラボで「うれしい＆買いたい」と感じるポイント（3つ）",
             font_size=20, bold=True, font_color=WHITE)
add_text_box(slide, Inches(10.5), Inches(0.2), Inches(2.5), Inches(0.4),
             "n=685 / MA", font_size=12, font_color=WHITE, alignment=PP_ALIGN.RIGHT)

q5_cats = [
    '推しが"確定"で手に入る', "日常生活で使えるアイテム",
    "価格に納得感がある", "撮り下ろし新ビジュアル",
    "推しが関わっている（監修等）", "限定仕様である",
    "世界観やコンセプト", "ペア／ユニットのセット",
    "長く使えるクオリティ"
]
q5_vals = [48.91, 46.42, 41.46, 40.88, 35.33, 25.69, 21.75, 20.00, 19.27]

create_bar_chart_native(slide, Inches(0.5), Inches(1.2), Inches(7.5), Inches(5.8),
                        q5_cats, q5_vals, "コラボグッズの魅力ポイント（%）")

# Insight
card = add_rounded_rect(slide, Inches(8.3), Inches(1.3), Inches(4.7), Inches(5.8), WHITE)
add_text_box(slide, Inches(8.5), Inches(1.5), Inches(4.3), Inches(0.4),
             "INSIGHT", font_size=14, bold=True, font_color=ACCENT_6)

insights5 = [
    'TOP1「推し確定で手に入る」48.9%\n→ ランダム排除が最大の購買動機',
    "TOP2「日常使いできる」46.4%\n→ 飾るだけでなく使えることが重要",
    "TOP3「価格の納得感」41.5%\n→ コスパ意識は高い",
    "TOP4「撮り下ろし新ビジュアル」40.9%\n→ 限定感のある新規素材が欲しい",
    "TOP5「推しの関与」35.3%\n→ 監修・コメントなどの本人参加",
    "→ 確定入手 × 実用性 × 適正価格\n  この3条件がコラボ成功の鍵"
]
for i, ins in enumerate(insights5):
    color = ACCENT_1 if i == 5 else TEXT_DARK
    add_text_box(slide, Inches(8.6), Inches(2.1 + i * 0.9), Inches(4.2), Inches(0.85),
                 f"{'→' if i == 5 else '●'} {ins}", font_size=10, font_color=color,
                 bold=(i == 5))


# ===========================================
# SLIDE 8: Q6 M!LKファン認知度
# ===========================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide, BG_COLOR)

header_bg = slide.shapes.add_shape(1, Inches(0), Inches(0), prs.slide_width, Inches(0.9))
header_bg.fill.solid()
header_bg.fill.fore_color.rgb = ACCENT_1
header_bg.line.fill.background()
add_text_box(slide, Inches(0.5), Inches(0.15), Inches(12), Inches(0.6),
             "Q6. M!LKのファンですか？",
             font_size=22, bold=True, font_color=WHITE)
add_text_box(slide, Inches(10.5), Inches(0.2), Inches(2.5), Inches(0.4),
             "n=1,000 / SA", font_size=12, font_color=WHITE, alignment=PP_ALIGN.RIGHT)

q6_cats = ["はい（ファン）", "どちらかというとファン", "知っているがファンではない", "知らない"]
q6_vals = [8.2, 12.1, 50.6, 29.1]

create_pie_shapes(slide, Inches(1.0), Inches(1.5), Inches(5.5),
                  q6_cats, q6_vals, [ACCENT_1, ACCENT_6, ACCENT_2, LIGHT_GRAY])

# Key Findings
card = add_rounded_rect(slide, Inches(7.0), Inches(1.5), Inches(5.8), Inches(5.2), WHITE)
add_text_box(slide, Inches(7.3), Inches(1.7), Inches(5.3), Inches(0.4),
             "KEY FINDINGS", font_size=14, bold=True, font_color=ACCENT_1)

findings6 = [
    "M!LKの認知率は 70.9%（知らない29.1%を除く）",
    "ファン層（ファン＋どちらかというとファン）は 20.3%",
    "「知っているがファンではない」が最多の 50.6%\n→ 認知はあるがファン化に至っていない層が大きい",
    "→ 認知→ファン転換の施策が重要\n  コラボ・SNS施策で接触機会を増やすことで\n  この50.6%の取り込みが成長の鍵",
]
for i, f in enumerate(findings6):
    add_text_box(slide, Inches(7.5), Inches(2.3 + i * 1.1), Inches(5.1), Inches(1.0),
                 f"● {f}", font_size=11, font_color=TEXT_DARK)

# 強調カード
card2 = add_rounded_rect(slide, Inches(1.0), Inches(5.8), Inches(5.5), Inches(1.2), ACCENT_1)
add_text_box(slide, Inches(1.3), Inches(5.9), Inches(5.0), Inches(0.5),
             "認知率 70.9%  /  ファン率 20.3%", font_size=20, bold=True,
             font_color=WHITE, alignment=PP_ALIGN.CENTER)
add_text_box(slide, Inches(1.3), Inches(6.4), Inches(5.0), Inches(0.4),
             "認知→ファン転換が最大の成長機会", font_size=13,
             font_color=WHITE, alignment=PP_ALIGN.CENTER)


# ===========================================
# SLIDE 9: サマリー＆示唆
# ===========================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide, BG_COLOR)

header_bg = slide.shapes.add_shape(1, Inches(0), Inches(0), prs.slide_width, Inches(0.9))
header_bg.fill.solid()
header_bg.fill.fore_color.rgb = TITLE_COLOR
header_bg.line.fill.background()
add_text_box(slide, Inches(0.5), Inches(0.15), Inches(12), Inches(0.6),
             "Summary & Implications", font_size=24, bold=True, font_color=WHITE)

# カード1: 推し活市場
card1 = add_rounded_rect(slide, Inches(0.5), Inches(1.3), Inches(3.8), Inches(5.8), WHITE)
accent_line1 = slide.shapes.add_shape(1, Inches(0.5), Inches(1.3), Inches(3.8), Inches(0.06))
accent_line1.fill.solid()
accent_line1.fill.fore_color.rgb = ACCENT_1
accent_line1.line.fill.background()

add_text_box(slide, Inches(0.8), Inches(1.6), Inches(3.2), Inches(0.4),
             "1. 推し活市場の規模感", font_size=14, bold=True, font_color=ACCENT_1)
summary1 = [
    "● 15〜30歳女性の68.5%が推し活経験者",
    "● うち51%が3か月に1回以上グッズを購入",
    "● 活発な購買層が大きく存在する市場",
]
for i, s in enumerate(summary1):
    add_text_box(slide, Inches(0.8), Inches(2.2 + i * 0.55), Inches(3.2), Inches(0.5),
                 s, font_size=10, font_color=TEXT_DARK)

# カード2: グッズ開発の方向性
card2 = add_rounded_rect(slide, Inches(4.6), Inches(1.3), Inches(3.8), Inches(5.8), WHITE)
accent_line2 = slide.shapes.add_shape(1, Inches(4.6), Inches(1.3), Inches(3.8), Inches(0.06))
accent_line2.fill.solid()
accent_line2.fill.fore_color.rgb = ACCENT_2
accent_line2.line.fill.background()

add_text_box(slide, Inches(4.9), Inches(1.6), Inches(3.2), Inches(0.4),
             "2. グッズ開発の方向性", font_size=14, bold=True, font_color=ACCENT_2)
summary2 = [
    "● ビジュアル品質が最重要（54%）",
    "● デザイン性＋実用性の両立が鍵",
    "● 人気TOP3：キーホルダー、\n  アクスタ、トレカ",
    "● 「普段使い」できる実用グッズに\n  強いニーズあり",
]
for i, s in enumerate(summary2):
    add_text_box(slide, Inches(4.9), Inches(2.2 + i * 0.7), Inches(3.2), Inches(0.65),
                 s, font_size=10, font_color=TEXT_DARK)

# カード3: コラボ成功の鍵
card3 = add_rounded_rect(slide, Inches(8.7), Inches(1.3), Inches(4.2), Inches(5.8), WHITE)
accent_line3 = slide.shapes.add_shape(1, Inches(8.7), Inches(1.3), Inches(4.2), Inches(0.06))
accent_line3.fill.solid()
accent_line3.fill.fore_color.rgb = ACCENT_3
accent_line3.line.fill.background()

add_text_box(slide, Inches(9.0), Inches(1.6), Inches(3.6), Inches(0.4),
             "3. コラボ施策への示唆", font_size=14, bold=True, font_color=ACCENT_3)
summary3 = [
    "● 「推し確定入手」が最重要（48.9%）\n  → ランダム排除で購買率向上",
    "● 日常使いアイテム×新ビジュアル\n  → 実用性と限定感の両立",
    "● 価格納得感が41.5%で3位\n  → 適正価格設定が重要",
    "● M!LK認知率70.9%に対しファン率20.3%\n  → 認知層のファン転換が成長のカギ",
    "● 「推しの関与」35.3%\n  → 監修・コメント等の本人参加で\n    ファンの心を掴む",
]
for i, s in enumerate(summary3):
    add_text_box(slide, Inches(9.0), Inches(2.2 + i * 0.95), Inches(3.6), Inches(0.9),
                 s, font_size=10, font_color=TEXT_DARK)


# ── 保存 ──
output_path = "/Users/rikohayashi/Downloads/926_推し活グッズ購買アンケート_結果レポート.pptx"
prs.save(output_path)
print(f"Saved: {output_path}")
