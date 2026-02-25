#!/usr/bin/env python3
"""
シャトレーゼ インドネシア市場分析レポート → PowerPoint スライド生成
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
import os

# ==============================================================================
# カラー定義
# ==============================================================================
RED = RGBColor(0xC4, 0x1E, 0x3A)       # シャトレーゼ赤
DARK_RED = RGBColor(0x9B, 0x17, 0x2E)   # 濃い赤
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
BLACK = RGBColor(0x33, 0x33, 0x33)       # ダークグレー
GRAY = RGBColor(0x66, 0x66, 0x66)
LIGHT_GRAY = RGBColor(0xF5, 0xF5, 0xF5)
LIGHT_RED = RGBColor(0xFD, 0xE8, 0xEB)  # 薄い赤背景
BLUE = RGBColor(0x1A, 0x73, 0xE8)
GREEN = RGBColor(0x0D, 0x87, 0x2A)
ORANGE = RGBColor(0xE8, 0x6C, 0x00)

# フォント候補
FONT_JP = "Yu Gothic"
FONT_FALLBACK = "Meiryo"

SLIDE_WIDTH = Inches(13.333)
SLIDE_HEIGHT = Inches(7.5)


def set_slide_bg(slide, color=WHITE):
    """スライド背景を設定"""
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_top_bar(slide, height=Inches(0.08)):
    """上部に赤いバーを追加"""
    shape = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 0, 0, SLIDE_WIDTH, height
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = RED
    shape.line.fill.background()


def add_bottom_bar(slide):
    """下部にフッターバーを追加"""
    bar_h = Inches(0.35)
    shape = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 0, SLIDE_HEIGHT - bar_h, SLIDE_WIDTH, bar_h
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = RED
    shape.line.fill.background()

    tf = shape.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    run = p.add_run()
    run.text = "Confidential | Chateraise Indonesia Market Analysis 2026"
    run.font.size = Pt(9)
    run.font.color.rgb = WHITE
    run.font.name = FONT_JP


def add_slide_number(slide, num, total=31):
    """スライド番号を追加"""
    left = SLIDE_WIDTH - Inches(0.8)
    top = SLIDE_HEIGHT - Inches(0.7)
    txBox = slide.shapes.add_textbox(left, top, Inches(0.7), Inches(0.3))
    tf = txBox.text_frame
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.RIGHT
    run = p.add_run()
    run.text = f"{num} / {total}"
    run.font.size = Pt(9)
    run.font.color.rgb = GRAY
    run.font.name = FONT_JP


def add_section_title(slide, title, subtitle=""):
    """セクションタイトル（ページ上部）"""
    add_top_bar(slide)

    txBox = slide.shapes.add_textbox(Inches(0.7), Inches(0.25), Inches(11), Inches(0.6))
    tf = txBox.text_frame
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = title
    run.font.size = Pt(28)
    run.font.bold = True
    run.font.color.rgb = BLACK
    run.font.name = FONT_JP

    if subtitle:
        txBox2 = slide.shapes.add_textbox(Inches(0.7), Inches(0.85), Inches(11), Inches(0.4))
        tf2 = txBox2.text_frame
        p2 = tf2.paragraphs[0]
        run2 = p2.add_run()
        run2.text = subtitle
        run2.font.size = Pt(14)
        run2.font.color.rgb = GRAY
        run2.font.name = FONT_JP


def add_body_text(slide, text, left=0.7, top=1.4, width=11.5, size=14, color=BLACK, bold=False):
    """本文テキストを追加"""
    txBox = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(5))
    tf = txBox.text_frame
    tf.word_wrap = True
    for i, line in enumerate(text.split("\n")):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        run = p.add_run()
        run.text = line
        run.font.size = Pt(size)
        run.font.color.rgb = color
        run.font.bold = bold
        run.font.name = FONT_JP
        p.space_after = Pt(6)
    return txBox


def add_bullet_list(slide, items, left=0.7, top=1.4, width=11.5, size=14):
    """箇条書きリスト"""
    txBox = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(5))
    tf = txBox.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        run = p.add_run()
        run.text = f"  {item}"
        run.font.size = Pt(size)
        run.font.color.rgb = BLACK
        run.font.name = FONT_JP
        p.space_after = Pt(8)
        p.bullet = True
    return txBox


def add_table(slide, data, left=0.7, top=1.5, width=11.5, row_height=0.4, font_size=11, header_color=RED):
    """テーブルを追加。data = [[header...], [row1...], ...]"""
    rows = len(data)
    cols = len(data[0])
    tbl_width = Inches(width)
    col_w = tbl_width // cols

    table_shape = slide.shapes.add_table(
        rows, cols, Inches(left), Inches(top), tbl_width, Inches(row_height * rows)
    )
    table = table_shape.table

    for ci in range(cols):
        table.columns[ci].width = col_w

    for ri, row_data in enumerate(data):
        for ci, cell_text in enumerate(row_data):
            cell = table.cell(ri, ci)
            cell.text = str(cell_text)
            for paragraph in cell.text_frame.paragraphs:
                paragraph.font.size = Pt(font_size)
                paragraph.font.name = FONT_JP
                if ri == 0:
                    paragraph.font.color.rgb = WHITE
                    paragraph.font.bold = True
                else:
                    paragraph.font.color.rgb = BLACK
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE

            if ri == 0:
                cell.fill.solid()
                cell.fill.fore_color.rgb = header_color
            elif ri % 2 == 0:
                cell.fill.solid()
                cell.fill.fore_color.rgb = LIGHT_GRAY
            else:
                cell.fill.solid()
                cell.fill.fore_color.rgb = WHITE

    return table_shape


def add_card(slide, title, text, left, top, width, height, bg_color=LIGHT_RED, title_color=RED):
    """カード型の情報ブロック"""
    shape = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height)
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    shape.line.fill.background()

    tf = shape.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.15)
    tf.margin_right = Inches(0.15)
    tf.margin_top = Inches(0.1)

    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = title
    run.font.size = Pt(14)
    run.font.bold = True
    run.font.color.rgb = title_color
    run.font.name = FONT_JP
    p.space_after = Pt(6)

    for line in text.split("\n"):
        p2 = tf.add_paragraph()
        run2 = p2.add_run()
        run2.text = line
        run2.font.size = Pt(11)
        run2.font.color.rgb = BLACK
        run2.font.name = FONT_JP
        p2.space_after = Pt(3)


def add_swot_quadrant(slide, title, items, left, top, width, height, bg_color, title_color):
    """SWOT用の象限"""
    shape = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height)
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    shape.line.fill.background()

    tf = shape.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.15)
    tf.margin_right = Inches(0.15)
    tf.margin_top = Inches(0.1)

    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = title
    run.font.size = Pt(16)
    run.font.bold = True
    run.font.color.rgb = title_color
    run.font.name = FONT_JP
    p.space_after = Pt(8)

    for item in items:
        p2 = tf.add_paragraph()
        run2 = p2.add_run()
        run2.text = f"  {item}"
        run2.font.size = Pt(10)
        run2.font.color.rgb = BLACK
        run2.font.name = FONT_JP
        p2.space_after = Pt(3)
        p2.bullet = True


# ==============================================================================
# スライド作成
# ==============================================================================

def create_presentation():
    prs = Presentation()
    prs.slide_width = SLIDE_WIDTH
    prs.slide_height = SLIDE_HEIGHT
    blank_layout = prs.slide_layouts[6]  # Blank layout
    total_slides = 31

    # =========================================================================
    # Slide 1: タイトル
    # =========================================================================
    slide = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide, WHITE)

    # 上部の大きな赤帯
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SLIDE_WIDTH, Inches(3.2))
    shape.fill.solid()
    shape.fill.fore_color.rgb = RED
    shape.line.fill.background()

    # タイトル
    txBox = slide.shapes.add_textbox(Inches(0.8), Inches(0.8), Inches(11), Inches(1.2))
    tf = txBox.text_frame
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = "シャトレーゼ"
    run.font.size = Pt(48)
    run.font.bold = True
    run.font.color.rgb = WHITE
    run.font.name = FONT_JP

    p2 = tf.add_paragraph()
    run2 = p2.add_run()
    run2.text = "インドネシア市場分析レポート"
    run2.font.size = Pt(36)
    run2.font.color.rgb = WHITE
    run2.font.name = FONT_JP

    # サブタイトル
    txBox2 = slide.shapes.add_textbox(Inches(0.8), Inches(3.6), Inches(11), Inches(1.5))
    tf2 = txBox2.text_frame
    tf2.word_wrap = True
    items = [
        "市場分析 → プレイヤー分析 → 顧客分析 → CEP分析 → 口コミ分析 → 統合戦略",
        "",
        "分析フレームワーク：市場 → プレイヤー（競合/自社） → 顧客",
        "作成日：2026年2月5日"
    ]
    for i, item in enumerate(items):
        if i == 0:
            p = tf2.paragraphs[0]
        else:
            p = tf2.add_paragraph()
        run = p.add_run()
        run.text = item
        run.font.size = Pt(16) if i == 0 else Pt(13)
        run.font.color.rgb = GRAY if i > 0 else BLACK
        run.font.name = FONT_JP
        p.space_after = Pt(4)

    # 下部赤バー
    add_bottom_bar(slide)

    # =========================================================================
    # Slide 2: 目次
    # =========================================================================
    slide = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide, WHITE)
    add_section_title(slide, "目次", "Report Structure")
    add_top_bar(slide)

    toc_items = [
        ("01", "市場分析", "カテゴリ市場規模・成長ドライバー・消費者トレンド"),
        ("02", "プレイヤー分析", "主要7社の競合マップ・各社詳細・訴求比較"),
        ("03", "シャトレーゼ現状", "基本情報・成功要因・SNSプレゼンス"),
        ("04", "顧客分析", "ターゲット像・ニーズ・消費者行動・SNS利用"),
        ("05", "SWOT分析", "強み・弱み・機会・脅威"),
        ("06", "CEP分析", "12のCEP特定・言及率分析・メンタルアドバンテージ"),
        ("07", "口コミ分析", "TikTok 243件の頻出ワード・インサイト"),
        ("08", "統合戦略提言", "押し出すべき商品・訴求・アクションプラン"),
    ]

    for i, (num, title, desc) in enumerate(toc_items):
        y = 1.4 + i * 0.7
        # 番号
        txBox = slide.shapes.add_textbox(Inches(0.7), Inches(y), Inches(0.8), Inches(0.5))
        tf = txBox.text_frame
        p = tf.paragraphs[0]
        run = p.add_run()
        run.text = num
        run.font.size = Pt(24)
        run.font.bold = True
        run.font.color.rgb = RED
        run.font.name = FONT_JP

        # タイトル
        txBox2 = slide.shapes.add_textbox(Inches(1.5), Inches(y), Inches(3), Inches(0.5))
        tf2 = txBox2.text_frame
        p2 = tf2.paragraphs[0]
        run2 = p2.add_run()
        run2.text = title
        run2.font.size = Pt(18)
        run2.font.bold = True
        run2.font.color.rgb = BLACK
        run2.font.name = FONT_JP

        # 説明
        txBox3 = slide.shapes.add_textbox(Inches(4.5), Inches(y + 0.03), Inches(7), Inches(0.5))
        tf3 = txBox3.text_frame
        p3 = tf3.paragraphs[0]
        run3 = p3.add_run()
        run3.text = desc
        run3.font.size = Pt(13)
        run3.font.color.rgb = GRAY
        run3.font.name = FONT_JP

    add_bottom_bar(slide)
    add_slide_number(slide, 2, total_slides)

    # =========================================================================
    # Slide 3: エグゼクティブサマリー
    # =========================================================================
    slide = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide, WHITE)
    add_section_title(slide, "エグゼクティブサマリー", "Executive Summary")

    summary_items = [
        ("市場機会", "インドネシア菓子・ベーカリー市場はUSD 23.8億（CAGR 3.25%）。\n2億7,000万人の人口と拡大する中間層が成長を牽引。"),
        ("競合環境", "ローカル老舗（Holland Bakery 470店）、プレミアム（The Harvest）、\n韓国系（TLJ/PB）が存在。「日本品質」は競合不可侵の領域。"),
        ("戦略提言", "「Mochi × 甘さ控えめ × 日本品質」を軸に展開。\nハラル認証の取得・訴求を急ぎ、2億人のムスリム市場にアクセス。"),
    ]

    for i, (title, text) in enumerate(summary_items):
        add_card(slide, title, text, 0.7, 1.4 + i * 1.7, 11.5, 1.4)

    add_bottom_bar(slide)
    add_slide_number(slide, 3, total_slides)

    # =========================================================================
    # Slide 4: 市場規模
    # =========================================================================
    slide = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide, WHITE)
    add_section_title(slide, "市場規模", "Market Size — 菓子・ベーカリー")

    data = [
        ["指標", "数値", "備考"],
        ["菓子市場規模（2024年）", "USD 23.8億（約3,600億円）", ""],
        ["予測市場規模（2033年）", "USD 32.7億", "CAGR 3.25%"],
        ["ベーカリー市場規模（2025年）", "USD 547億", "CAGR 5.70%"],
        ["ASEAN市場シェア", "27.89%", "ASEAN最大市場"],
        ["チョコレート菓子シェア", "市場の50%以上", "最大カテゴリ"],
        ["人口", "約2億7,000万人", "ASEAN最大"],
        ["中間層比率", "人口の約66%", "総家計支出の81.49%"],
    ]
    add_table(slide, data, left=0.7, top=1.4, width=11.5, row_height=0.45, font_size=12)

    add_bottom_bar(slide)
    add_slide_number(slide, 4, total_slides)

    # =========================================================================
    # Slide 5: 市場成長ドライバー
    # =========================================================================
    slide = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide, WHITE)
    add_section_title(slide, "市場成長ドライバー", "Growth Drivers")

    drivers = [
        ("中間層の拡大", "可処分所得の増加により、プレミアムスイーツ需要が拡大"),
        ("都市化の加速", "便利な食品・テイクアウト需要が増加"),
        ("食文化の西洋化", "カフェ文化・ベーカリー需要の浸透"),
        ("SNS・韓流の影響", "TikTok/Instagramでのスイーツブーム拡散"),
        ("ギフト文化", "ラマダン・クリスマス・旧正月の贈答需要"),
    ]

    for i, (title, desc) in enumerate(drivers):
        y = 1.4 + i * 1.05
        # 番号丸
        shape = slide.shapes.add_shape(
            MSO_SHAPE.OVAL, Inches(0.7), Inches(y), Inches(0.5), Inches(0.5)
        )
        shape.fill.solid()
        shape.fill.fore_color.rgb = RED
        shape.line.fill.background()
        tf = shape.text_frame
        tf.word_wrap = False
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        run = p.add_run()
        run.text = str(i + 1)
        run.font.size = Pt(18)
        run.font.bold = True
        run.font.color.rgb = WHITE
        run.font.name = FONT_JP

        # タイトル
        txBox = slide.shapes.add_textbox(Inches(1.4), Inches(y - 0.05), Inches(10), Inches(0.35))
        tf2 = txBox.text_frame
        p2 = tf2.paragraphs[0]
        run2 = p2.add_run()
        run2.text = title
        run2.font.size = Pt(18)
        run2.font.bold = True
        run2.font.color.rgb = BLACK
        run2.font.name = FONT_JP

        # 説明
        txBox2 = slide.shapes.add_textbox(Inches(1.4), Inches(y + 0.35), Inches(10), Inches(0.35))
        tf3 = txBox2.text_frame
        p3 = tf3.paragraphs[0]
        run3 = p3.add_run()
        run3.text = desc
        run3.font.size = Pt(13)
        run3.font.color.rgb = GRAY
        run3.font.name = FONT_JP

    add_bottom_bar(slide)
    add_slide_number(slide, 5, total_slides)

    # =========================================================================
    # Slide 6: 消費者トレンド
    # =========================================================================
    slide = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide, WHITE)
    add_section_title(slide, "消費者トレンドの変化", "Consumer Trends")

    trends = [
        ("健康志向", "低糖・グルテンフリー需要の増加\nヘルスコンシャス層が拡大中"),
        ("プレミアム志向", "プレミアム・グルメスイーツへの\n支出意欲が高まっている"),
        ("オンライン購買", "EC/デリバリー経由の購買が急成長\nCAGR 11.49%"),
        ("コンビニエンス", "シングルサーブ、ポーション\nコントロール商品の需要増"),
    ]

    for i, (title, desc) in enumerate(trends):
        col = i % 2
        row = i // 2
        x = 0.7 + col * 6.0
        y = 1.4 + row * 2.5
        add_card(slide, title, desc, x, y, 5.5, 2.0)

    # リスク注記
    add_body_text(slide, "注意: 41%の消費者が支出に慎重（節約志向）。インフレ圧力による原材料コスト上昇リスクあり。",
                  left=0.7, top=6.5, width=11.5, size=11, color=GRAY)

    add_bottom_bar(slide)
    add_slide_number(slide, 6, total_slides)

    # =========================================================================
    # Slide 7: 主要プレイヤー一覧
    # =========================================================================
    slide = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide, WHITE)
    add_section_title(slide, "主要プレイヤー一覧", "Key Players")

    data = [
        ["ブランド", "出自", "店舗数", "特徴", "動向"],
        ["シャトレーゼ", "日本", "約40→450目標", "日本品質・手頃な価格", "急増"],
        ["Holland Bakery", "インドネシア", "470店舗以上", "老舗ローカル、幅広い品揃え", "維持"],
        ["The Harvest", "インドネシア", "130店舗以上", "高級洋菓子、幅広い認知", "維持"],
        ["Tous les Jours", "韓国", "52店舗以上", "韓流人気、ハラル認証", "増加"],
        ["Paris Baguette", "韓国", "急成長中", "K-POPブーム・若者人気", "急増"],
        ["Mako", "シンガポール", "約30店舗", "日本風パン・スイーツ", "維持"],
        ["Dapur Cokelat", "インドネシア", "36店舗", "チョコレート特化", "維持"],
    ]
    add_table(slide, data, left=0.5, top=1.4, width=12.0, row_height=0.45, font_size=11)

    add_bottom_bar(slide)
    add_slide_number(slide, 7, total_slides)

    # =========================================================================
    # Slide 8: ポジショニングマップ
    # =========================================================================
    slide = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide, WHITE)
    add_section_title(slide, "ポジショニングマップ", "Positioning Map — 価格 × ブランド感")

    # 軸の描画
    cx, cy = Inches(6.5), Inches(4.0)
    axis_len = Inches(4.5)

    # 縦軸
    slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, cx - Inches(0.01), cy - axis_len, Inches(0.02), axis_len * 2)
    # 横軸
    slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, cx - axis_len, cy - Inches(0.01), axis_len * 2, Inches(0.02))

    # ラベル
    labels = [
        ("高価格", cx - Inches(0.5), cy - axis_len - Inches(0.3)),
        ("低価格", cx - Inches(0.5), cy + axis_len + Inches(0.05)),
        ("ローカル感", cx - axis_len - Inches(1.2), cy - Inches(0.15)),
        ("海外ブランド感", cx + axis_len + Inches(0.1), cy - Inches(0.15)),
    ]
    for text, lx, ly in labels:
        txBox = slide.shapes.add_textbox(lx, ly, Inches(1.5), Inches(0.3))
        tf = txBox.text_frame
        p = tf.paragraphs[0]
        run = p.add_run()
        run.text = text
        run.font.size = Pt(11)
        run.font.bold = True
        run.font.color.rgb = GRAY
        run.font.name = FONT_JP

    # プレイヤー配置
    players = [
        ("The Harvest", cx + Inches(0.3), cy - Inches(3.0), DARK_RED),
        ("Paris Baguette", cx + Inches(2.5), cy - Inches(1.5), GRAY),
        ("Tous les Jours", cx + Inches(2.0), cy - Inches(0.8), GRAY),
        ("Holland Bakery", cx - Inches(3.0), cy + Inches(1.5), GRAY),
        ("Dapur Cokelat", cx + Inches(1.0), cy + Inches(1.5), GRAY),
        ("★ シャトレーゼ", cx + Inches(2.0), cy + Inches(2.5), RED),
    ]
    for name, px, py, color in players:
        shape = slide.shapes.add_shape(
            MSO_SHAPE.OVAL, px, py, Inches(0.2), Inches(0.2)
        )
        shape.fill.solid()
        shape.fill.fore_color.rgb = color
        shape.line.fill.background()

        txBox = slide.shapes.add_textbox(px + Inches(0.25), py - Inches(0.05), Inches(2), Inches(0.3))
        tf = txBox.text_frame
        p = tf.paragraphs[0]
        run = p.add_run()
        run.text = name
        run.font.size = Pt(12)
        run.font.bold = True
        run.font.color.rgb = color
        run.font.name = FONT_JP

    # 注釈
    add_body_text(slide, "シャトレーゼの目指すポジション: 海外ブランド感 × 低価格（日本品質 × 手頃な価格）",
                  left=0.7, top=6.7, width=11, size=11, color=GRAY)

    add_bottom_bar(slide)
    add_slide_number(slide, 8, total_slides)

    # =========================================================================
    # Slide 9-12: 競合詳細（4社分）
    # =========================================================================
    competitors = [
        {
            "name": "Holland Bakery",
            "subtitle": "インドネシア老舗 — 圧倒的店舗網",
            "slide_num": 9,
            "data": [
                ["項目", "内容"],
                ["タグライン", "「Teratas dalam kualitas」（品質でNo.1）"],
                ["ポジショニング", "ローカル老舗だが西洋風イメージ"],
                ["強み", "1978年創業の信頼、全国546店舗"],
                ["価格帯", "中〜低価格（庶民派）"],
                ["訴求", "健康的・栄養価が高い・手頃な価格"],
            ],
            "sns": "TikTok約7万フォロワー / 祝日連動プロモ / #hollandbakery 1,870万投稿",
        },
        {
            "name": "The Harvest",
            "subtitle": "ローカルプレミアム — 値引きしないブランド",
            "slide_num": 10,
            "data": [
                ["項目", "内容"],
                ["コンセプト", "「Fashionably Delicious」"],
                ["ポジショニング", "欧州品質のプレミアムケーキ"],
                ["強み", "フォーシーズンズ出身シェフ創業・欧州直輸入原材料"],
                ["価格帯", "高価格（プレミアム）"],
                ["訴求", "ギフト需要、特別な日の演出"],
            ],
            "sns": "インフルエンサー/セレブコラボ / 基本ディスカウントなし / バイラル商品の迅速メニュー化",
        },
        {
            "name": "Tous les Jours",
            "subtitle": "韓国系 — K-POP人気×ハラル認証",
            "slide_num": 11,
            "data": [
                ["項目", "内容"],
                ["コンセプト", "「The 1st South Korean Bakery & Cafe in Indonesia」"],
                ["ポジショニング", "韓国体験の提供、フレンチ×アジアン融合"],
                ["強み", "K-POP人気との連動、ハラル認証取得（2020年）"],
                ["価格帯", "中〜高価格"],
                ["訴求", "韓流ファン層への訴求、ハラル対応の安心感"],
            ],
            "sns": "Instagram 30.7万フォロワー（競合最大）/ OVO連携20%キャッシュバック / 季節キャンペーン",
        },
        {
            "name": "Paris Baguette",
            "subtitle": "韓国系・新規参入 — グローバル展開",
            "slide_num": 12,
            "data": [
                ["項目", "内容"],
                ["コンセプト", "「Premium Fast-Casual Bakery-Café」"],
                ["ポジショニング", "グローバルブランド、トレンド感"],
                ["強み", "世界4,000店舗のスケール・毎日焼き上げ"],
                ["価格帯", "中〜高価格"],
                ["訴求", "ビジネス層ターゲット、インドネシア限定メニュー"],
            ],
            "sns": "グランドオープンイベント話題化 / KOL活用 / 銀行・モール連携プロモーション",
        },
    ]

    for comp in competitors:
        slide = prs.slides.add_slide(blank_layout)
        set_slide_bg(slide, WHITE)
        add_section_title(slide, comp["name"], comp["subtitle"])
        add_table(slide, comp["data"], left=0.7, top=1.4, width=11.5, row_height=0.5, font_size=12)

        # SNS情報
        add_card(slide, "SNSマーケティング施策", comp["sns"], 0.7, 5.0, 11.5, 1.0)

        add_bottom_bar(slide)
        add_slide_number(slide, comp["slide_num"], total_slides)

    # =========================================================================
    # Slide 13: 競合訴求比較
    # =========================================================================
    slide = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide, WHITE)
    add_section_title(slide, "競合訴求比較", "Competitive Messaging Comparison")

    data = [
        ["ブランド", "主な訴求", "ターゲット", "差別化ポイント"],
        ["Holland Bakery", "ローカル老舗×西洋風品質", "幅広い層", "圧倒的店舗網、庶民派価格"],
        ["The Harvest", "プレミアム欧州品質", "富裕層・ギフト需要", "値引きしないブランド戦略"],
        ["Tous les Jours", "韓国×ハラル認証", "K-POP好き・若者", "ハラル認証、30万フォロワー"],
        ["Paris Baguette", "トレンド×利便性", "ビジネス層・若者", "グランドオープンの話題化"],
        ["Dapur Cokelat", "チョコレート専門", "中間層", "ニッチポジション"],
    ]
    add_table(slide, data, left=0.5, top=1.4, width=12.0, row_height=0.55, font_size=12)

    # シャトレーゼの差別化
    add_card(slide, "シャトレーゼの差別化ポジション",
             "「日本品質 × 手頃な価格 × 甘さ控えめ」— 競合が参入できない独自領域",
             0.7, 5.2, 11.5, 0.8, bg_color=LIGHT_RED)

    add_bottom_bar(slide)
    add_slide_number(slide, 13, total_slides)

    # =========================================================================
    # Slide 14: シャトレーゼ現状
    # =========================================================================
    slide = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide, WHITE)
    add_section_title(slide, "シャトレーゼ現状分析", "Chateraise — Current Status")

    data = [
        ["項目", "内容"],
        ["参入時期", "2017年"],
        ["合弁パートナー", "Gobelグループ（PT Chateraise Gobel Indonesia）"],
        ["現在店舗数", "約40店舗"],
        ["目標店舗数", "450店舗（2025年度末）"],
        ["工場", "ボゴール工場（2022年稼働）"],
        ["新工場", "ブカシ新工場（2026年稼働予定、現工場の9倍規模）"],
        ["現在の訴求", "「#DirectlyFromJapan」（日本直輸入）"],
    ]
    add_table(slide, data, left=0.7, top=1.4, width=7.0, row_height=0.5, font_size=12)

    # SNSプレゼンス
    add_card(slide, "SNSプレゼンス",
             "Instagram: @chateraise.id\nTikTok: @chateraise\nYouTube: 運用中",
             8.3, 1.4, 4.0, 2.0)

    add_card(slide, "Key Metric",
             "40店舗 → 450店舗\n約11倍の拡大計画",
             8.3, 3.8, 4.0, 1.5, bg_color=LIGHT_RED, title_color=RED)

    add_bottom_bar(slide)
    add_slide_number(slide, 14, total_slides)

    # =========================================================================
    # Slide 15: シャトレーゼ成功要因
    # =========================================================================
    slide = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide, WHITE)
    add_section_title(slide, "シャトレーゼ 5つの強み", "Key Success Factors")

    factors = [
        ("日本ブランドへの信頼", "品質・安全性で高い評価。「日本製」は競合が真似できない。"),
        ("甘さ控えめ", "健康志向の若者・中間層に刺さる差別化要素。"),
        ("ハイイメージ × ローコスト", "同等品質を競合より安く提供する価格戦略。"),
        ("現地生産による価格競争力", "Rp 25,000 → Rp 15,000以下への引き下げが可能。"),
        ("カカオ農家支援", "サステナビリティ訴求で原料調達安定化も実現。"),
    ]

    for i, (title, desc) in enumerate(factors):
        col = i % 3
        row = i // 3
        x = 0.5 + col * 4.2
        y = 1.4 + row * 2.8
        add_card(slide, f"{i+1}. {title}", desc, x, y, 3.8, 2.2)

    add_bottom_bar(slide)
    add_slide_number(slide, 15, total_slides)

    # =========================================================================
    # Slide 16: ターゲット顧客
    # =========================================================================
    slide = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide, WHITE)
    add_section_title(slide, "ターゲット顧客セグメント", "Target Customer Segments")

    segments = [
        ("メインターゲット", "都市部在住の20-40代、中間層", RED),
        ("サブターゲット1", "日本文化に好意的な層", DARK_RED),
        ("サブターゲット2", "健康志向の若者（甘さ控えめ需要）", DARK_RED),
        ("サブターゲット3", "ギフト購入層（ラマダン、記念日）", DARK_RED),
    ]

    for i, (seg, desc, color) in enumerate(segments):
        x = 0.5 + i * 3.1
        # カード
        shape = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(1.5), Inches(2.8), Inches(3.5)
        )
        if i == 0:
            shape.fill.solid()
            shape.fill.fore_color.rgb = RED
            text_color = WHITE
        else:
            shape.fill.solid()
            shape.fill.fore_color.rgb = LIGHT_RED
            text_color = BLACK
        shape.line.fill.background()

        tf = shape.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.15)
        tf.margin_right = Inches(0.15)
        tf.margin_top = Inches(0.3)

        p = tf.paragraphs[0]
        run = p.add_run()
        run.text = seg
        run.font.size = Pt(16)
        run.font.bold = True
        run.font.color.rgb = text_color
        run.font.name = FONT_JP
        p.space_after = Pt(12)

        p2 = tf.add_paragraph()
        run2 = p2.add_run()
        run2.text = desc
        run2.font.size = Pt(13)
        run2.font.color.rgb = text_color if i == 0 else GRAY
        run2.font.name = FONT_JP

    add_bottom_bar(slide)
    add_slide_number(slide, 16, total_slides)

    # =========================================================================
    # Slide 17: 顧客ニーズ
    # =========================================================================
    slide = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide, WHITE)
    add_section_title(slide, "顧客ニーズ 7カテゴリ", "Customer Needs")

    data = [
        ["ニーズカテゴリ", "詳細"],
        ["品質・安全性", "日本製・海外ブランドへの信頼感、原材料の安心感"],
        ["味の好み", "甘すぎないスイーツ、多様なフレーバー体験"],
        ["価格", "手頃な価格でプレミアム感を得たい（コスパ重視）"],
        ["利便性", "モール内立地、オンライン購入・デリバリー対応"],
        ["体験価値", "SNS映え、ギフト需要、特別な日の演出"],
        ["健康志向", "低糖、グルテンフリー、添加物への配慮"],
        ["宗教対応", "ハラル認証への期待（ムスリム人口2億人超）"],
    ]
    add_table(slide, data, left=0.7, top=1.4, width=11.5, row_height=0.55, font_size=12)

    add_bottom_bar(slide)
    add_slide_number(slide, 17, total_slides)

    # =========================================================================
    # Slide 18: 消費者行動の変化
    # =========================================================================
    slide = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide, WHITE)
    add_section_title(slide, "消費者行動の変化（2024年）", "Consumer Behavior Shifts")

    behaviors = [
        ("41%", "が支出に慎重\n（節約志向の高まり）"),
        ("58%", "が特別な日には\n支出を惜しまない"),
        ("64%", "が自宅での体験を好む\n（外食→中食シフト）"),
        ("57%", "が使いやすい商品\nフォーマットを選好"),
    ]

    for i, (pct, desc) in enumerate(behaviors):
        x = 0.5 + i * 3.1
        shape = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(1.5), Inches(2.8), Inches(3.5)
        )
        shape.fill.solid()
        shape.fill.fore_color.rgb = WHITE
        shape.line.color.rgb = RED
        shape.line.width = Pt(2)

        tf = shape.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.2)
        tf.margin_right = Inches(0.2)
        tf.margin_top = Inches(0.4)

        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        run = p.add_run()
        run.text = pct
        run.font.size = Pt(42)
        run.font.bold = True
        run.font.color.rgb = RED
        run.font.name = FONT_JP
        p.space_after = Pt(12)

        p2 = tf.add_paragraph()
        p2.alignment = PP_ALIGN.CENTER
        run2 = p2.add_run()
        run2.text = desc
        run2.font.size = Pt(13)
        run2.font.color.rgb = BLACK
        run2.font.name = FONT_JP

    add_bottom_bar(slide)
    add_slide_number(slide, 18, total_slides)

    # =========================================================================
    # Slide 19: SNS利用状況
    # =========================================================================
    slide = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide, WHITE)
    add_section_title(slide, "SNS利用状況", "Social Media Landscape in Indonesia")

    data = [
        ["プラットフォーム", "利用率", "特徴"],
        ["WhatsApp", "91.7%", "コミュニケーション中心"],
        ["Instagram", "84.6%", "ブランド構築・ビジュアル訴求"],
        ["Facebook", "83.0%", "幅広い年齢層"],
        ["TikTok", "77.4%", "バイラル狙い・若年層リーチ"],
    ]
    add_table(slide, data, left=0.7, top=1.4, width=7.0, row_height=0.55, font_size=13)

    # 右側にキーデータ
    add_card(slide, "Key Data",
             "1日あたりSNS利用時間: 3時間8分\n月間TikTok利用時間: 平均30.8時間",
             8.3, 1.4, 4.0, 1.8)

    add_card(slide, "人気コンテンツ TOP3",
             "1. エンターテインメント（76%）\n2. 商品レビュー（67%）\n3. グルメ（63%）",
             8.3, 3.6, 4.0, 2.0)

    add_bottom_bar(slide)
    add_slide_number(slide, 19, total_slides)

    # =========================================================================
    # Slide 20: SWOT分析
    # =========================================================================
    slide = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide, WHITE)
    add_section_title(slide, "SWOT分析", "SWOT Analysis — シャトレーゼ")

    s_items = [
        "「日本直輸入」「日本品質」のブランド力",
        "甘さ控えめで健康志向層に訴求",
        "Gobelグループとの強力なパートナーシップ",
        "現地工場による価格競争力",
        "カカオ農家支援によるサステナビリティ訴求",
    ]
    w_items = [
        "店舗数は競合に劣る（約40 vs HB 470）",
        "ハラル認証の取得状況が不明確",
        "SNSフォロワー数で韓国系に劣る",
    ]
    o_items = [
        "2億7,000万人市場へのアクセス拡大",
        "新工場稼働（2026年）による価格競争力強化",
        "「日本品質×手頃な価格」のブルーオーシャン",
        "健康志向トレンドとの親和性",
        "オンライン・デリバリーチャネルの成長",
        "ラマダン等のギフトシーズン需要",
    ]
    t_items = [
        "韓国系ベーカリーの積極展開",
        "消費者の節約志向の高まり",
        "Holland Bakeryの圧倒的店舗網",
        "ハラル認証の重要性増大",
        "原材料コスト上昇リスク",
    ]

    add_swot_quadrant(slide, "Strengths（強み）", s_items,
                      0.5, 1.3, 5.8, 2.8, LIGHT_RED, RED)
    add_swot_quadrant(slide, "Weaknesses（弱み）", w_items,
                      6.6, 1.3, 5.8, 2.8, RGBColor(0xFD, 0xF0, 0xE0), ORANGE)
    add_swot_quadrant(slide, "Opportunities（機会）", o_items,
                      0.5, 4.3, 5.8, 2.8, RGBColor(0xE8, 0xF5, 0xE9), GREEN)
    add_swot_quadrant(slide, "Threats（脅威）", t_items,
                      6.6, 4.3, 5.8, 2.8, RGBColor(0xE3, 0xF2, 0xFD), BLUE)

    add_bottom_bar(slide)
    add_slide_number(slide, 20, total_slides)

    # =========================================================================
    # Slide 21: CEP分析概要
    # =========================================================================
    slide = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide, WHITE)
    add_section_title(slide, "CEP分析概要 — 12のカテゴリーエントリーポイント", "Category Entry Point Analysis")

    data = [
        ["#", "CEP", "説明", "間口"],
        ["①", "プロモーション・割引時", "40%OFF、Buy1Get1等の割引キャンペーン時", "大"],
        ["②", "記念日・祝日", "独立記念日、National Customer Day、旧正月等", "大"],
        ["③", "ラマダン・イフタール", "断食明けの食事、ラマダン期間のギフト", "大"],
        ["④", "日常のパン購入", "朝食用、日常の軽食としてのパン購入", "大"],
        ["⑤", "朝食・モーニング", "朝の食事シーン、出勤前の軽食", "中"],
        ["⑥", "ギフト・手土産", "お祝い、お見舞い、訪問時の手土産", "中"],
        ["⑦", "デザート・スイーツタイム", "午後のおやつ、食後のデザート", "中"],
        ["⑧", "トレンド商品体験", "バイラル商品（抹茶、ドバイチョコ等）", "中"],
        ["⑨", "韓国文化体験", "K-POP、韓国ドラマからの影響", "小〜中"],
        ["⑩", "プレミアム・贅沢体験", "自分へのご褒美、特別な日の贅沢", "小"],
        ["⑪", "日本品質・日本ブランド", "#DirectlyFromJapan、日本式の丁寧さ", "小〜中"],
        ["⑫", "甘さ控えめ・ヘルシー志向", "甘すぎないスイーツ、健康を意識した選択", "小〜中"],
    ]
    add_table(slide, data, left=0.3, top=1.3, width=12.5, row_height=0.38, font_size=10)

    add_bottom_bar(slide)
    add_slide_number(slide, 21, total_slides)

    # =========================================================================
    # Slide 22: CEP言及率テーブル
    # =========================================================================
    slide = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide, WHITE)
    add_section_title(slide, "CEP言及率 — 5社比較", "CEP Mention Rate by Brand")

    data = [
        ["CEP", "シャトレーゼ", "TLJ", "PB", "HB", "Harvest", "間口"],
        ["① プロモーション", "13.8%", "26.8%", "22.8%", "29.3%", "7.3%", "615"],
        ["② 記念日・祝日", "14.4%", "24.8%", "23.2%", "28.0%", "9.6%", "625"],
        ["③ ラマダン", "8.2%", "24.7%", "27.8%", "33.0%", "6.2%", "485"],
        ["④ 日常パン", "16.0%", "24.4%", "21.8%", "31.9%", "5.9%", "595"],
        ["⑤ 朝食", "15.7%", "19.1%", "28.1%", "31.5%", "5.6%", "445"],
        ["⑥ ギフト", "15.4%", "21.2%", "20.2%", "25.0%", "18.3%", "520"],
        ["⑦ デザート", "19.3%", "22.8%", "21.1%", "16.7%", "20.2%", "570"],
        ["⑧ トレンド", "11.9%", "28.7%", "27.7%", "13.9%", "17.8%", "505"],
        ["⑨ 韓国文化", "3.9%", "46.1%", "42.1%", "5.3%", "2.6%", "380"],
        ["⑩ プレミアム", "16.1%", "20.4%", "23.7%", "11.8%", "28.0%", "465"],
        ["⑪ 日本品質", "36.2%", "13.0%", "14.5%", "20.3%", "15.9%", "345"],
        ["⑫ 甘さ控えめ", "27.5%", "20.3%", "18.8%", "14.5%", "18.8%", "345"],
        ["平均", "16.0%", "24.5%", "24.2%", "22.9%", "12.4%", "5880"],
    ]
    add_table(slide, data, left=0.3, top=1.3, width=12.5, row_height=0.35, font_size=9)

    add_bottom_bar(slide)
    add_slide_number(slide, 22, total_slides)

    # =========================================================================
    # Slide 23: メンタルアドバンテージ
    # =========================================================================
    slide = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide, WHITE)
    add_section_title(slide, "メンタルアドバンテージ分析", "Mental Advantage / Disadvantage")

    # MA/MDサマリー
    add_card(slide, "シャトレーゼのMA（メンタルアドバンテージ）: 3個",
             "⑪ 日本品質 (+24)  — 圧倒的1位、競合不可侵\n⑫ 甘さ控えめ (+14) — 健康志向層の独自領域\n⑦ デザート (+10)   — The Harvestと並ぶ強み",
             0.7, 1.4, 11.5, 2.0, bg_color=LIGHT_RED)

    add_card(slide, "シャトレーゼのMD（メンタルディスアドバンテージ）: 2個",
             "⑨ 韓国文化 (-13) — TLJ/PBが独占。正面衝突は避ける\n③ ラマダン (-9)    — ハラル認証取得で改善可能",
             0.7, 3.8, 11.5, 1.6, bg_color=RGBColor(0xFD, 0xF0, 0xE0))

    # 競合比較
    data = [
        ["指標", "シャトレーゼ", "TLJ", "PB", "HB", "Harvest"],
        ["CEPリンク総数", "940", "1440", "1425", "1345", "730"],
        ["平均言及率", "16.0%", "24.5%", "24.2%", "22.9%", "12.4%"],
        ["MA数", "3", "3", "4", "5", "3"],
        ["MD数", "2", "3", "3", "4", "5"],
    ]
    add_table(slide, data, left=0.7, top=5.6, width=11.5, row_height=0.35, font_size=10)

    add_bottom_bar(slide)
    add_slide_number(slide, 23, total_slides)

    # =========================================================================
    # Slide 24: ブルーオーシャンCEP
    # =========================================================================
    slide = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide, WHITE)
    add_section_title(slide, "ブルーオーシャンCEP", "Blue Ocean — 競合が入れない領域")

    # 日本品質カード
    shape = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), Inches(1.4), Inches(5.8), Inches(4.8)
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = LIGHT_RED
    shape.line.color.rgb = RED
    shape.line.width = Pt(2)

    tf = shape.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.25)
    tf.margin_right = Inches(0.25)
    tf.margin_top = Inches(0.25)

    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = "CEP⑪ 日本品質・日本ブランド"
    run.font.size = Pt(20)
    run.font.bold = True
    run.font.color.rgb = RED
    run.font.name = FONT_JP
    p.space_after = Pt(16)

    lines = [
        ("言及率: 36.2%", True, Pt(28), RED),
        ("市場1位  |  2位 HB 20.3%に+15.9pt差", False, Pt(14), BLACK),
        ("MA: +24ポイント（圧倒的）", True, Pt(16), RED),
        ("", False, Pt(8), BLACK),
        ("競合が真似できない領域", True, Pt(14), BLACK),
        ("韓国系はK-POP、HBはローカルで勝負", False, Pt(12), GRAY),
        ("「日本品質×手頃価格」はシャトレーゼだけが占有", False, Pt(12), GRAY),
    ]
    for text, bold, size, color in lines:
        p2 = tf.add_paragraph()
        run2 = p2.add_run()
        run2.text = text
        run2.font.size = size
        run2.font.bold = bold
        run2.font.color.rgb = color
        run2.font.name = FONT_JP
        p2.space_after = Pt(4)

    # 甘さ控えめカード
    shape2 = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.6), Inches(1.4), Inches(5.8), Inches(4.8)
    )
    shape2.fill.solid()
    shape2.fill.fore_color.rgb = RGBColor(0xE8, 0xF5, 0xE9)
    shape2.line.color.rgb = GREEN
    shape2.line.width = Pt(2)

    tf2 = shape2.text_frame
    tf2.word_wrap = True
    tf2.margin_left = Inches(0.25)
    tf2.margin_right = Inches(0.25)
    tf2.margin_top = Inches(0.25)

    p = tf2.paragraphs[0]
    run = p.add_run()
    run.text = "CEP⑫ 甘さ控えめ・ヘルシー志向"
    run.font.size = Pt(20)
    run.font.bold = True
    run.font.color.rgb = GREEN
    run.font.name = FONT_JP
    p.space_after = Pt(16)

    lines2 = [
        ("言及率: 27.5%", True, Pt(28), GREEN),
        ("市場1位  |  2位 TLJ 20.3%に+7.2pt差", False, Pt(14), BLACK),
        ("MA: +14ポイント", True, Pt(16), GREEN),
        ("", False, Pt(8), BLACK),
        ("インドネシアの隠れたニーズ", True, Pt(14), BLACK),
        ("「甘すぎる」がペインポイント", False, Pt(12), GRAY),
        ("健康志向の若者・中間層に刺さる差別化要素", False, Pt(12), GRAY),
    ]
    for text, bold, size, color in lines2:
        p2 = tf2.add_paragraph()
        run2 = p2.add_run()
        run2.text = text
        run2.font.size = size
        run2.font.bold = bold
        run2.font.color.rgb = color
        run2.font.name = FONT_JP
        p2.space_after = Pt(4)

    add_bottom_bar(slide)
    add_slide_number(slide, 24, total_slides)

    # =========================================================================
    # Slide 25: CEP戦略提言
    # =========================================================================
    slide = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide, WHITE)
    add_section_title(slide, "CEP戦略提言", "CEP Strategy Recommendations")

    # 短期
    add_card(slide, "短期（〜6ヶ月）: CEP⑦ デザート強化",
             "訴求: 「甘さ控えめ、日本品質のデザート」\nSNS: #LessSweet #JapaneseQuality のUGC促進\n狙う競合: The Harvest（同じデザート強み、しかし高価格）",
             0.5, 1.4, 11.8, 1.4, bg_color=LIGHT_RED)

    # 中期
    add_card(slide, "中期（6ヶ月〜1年）: CEP④ 日常パン参入",
             "前提: 新工場稼働による価格競争力確保（Rp 15,000以下）\n訴求: 「毎日食べられる日本のパン」\n注意: HBの+17は強力。「品質重視層」を狙う",
             0.5, 3.1, 11.8, 1.4, bg_color=RGBColor(0xFD, 0xF0, 0xE0))

    # 長期
    add_card(slide, "長期（1年〜）: CEP③ ラマダン MD解消",
             "必須条件: ハラル認証の取得・明確な訴求\n訴求: 「ハラル認証取得、日本品質のイフタールスイーツ」\n商品: ラマダン限定ギフトボックス、イフタール向けセット",
             0.5, 4.8, 11.8, 1.4, bg_color=RGBColor(0xE3, 0xF2, 0xFD))

    # 回避
    add_body_text(slide, "回避: CEP⑨韓国文化（TLJ/PBが独占）、CEP⑩プレミアム（Harvestが支配）",
                  left=0.7, top=6.5, size=12, color=GRAY)

    add_bottom_bar(slide)
    add_slide_number(slide, 25, total_slides)

    # =========================================================================
    # Slide 26: TikTok口コミ分析
    # =========================================================================
    slide = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide, WHITE)
    add_section_title(slide, "TikTok口コミ分析", "TikTok Word-of-Mouth Analysis — 243 posts")

    data = [
        ["順位", "ワード", "出現数", "備考"],
        ["1", "chateraise", "177", "ブランド名"],
        ["2", "mochi", "89", "最も言及される商品"],
        ["3", "enak（おいしい）", "88", "圧倒的な評価ワード"],
        ["4", "beli（買う）", "40", "購買意欲"],
        ["5", "cake", "39", "ケーキ全般"],
        ["6", "cream", "36", "クリーム系商品"],
        ["7", "matcha", "34", "抹茶フレーバー人気"],
        ["8", "halal", "33", "ハラル認証への関心"],
        ["9", "promo", "33", "プロモーション・割引"],
        ["10", "manis（甘い）", "30", "甘さへの言及"],
    ]
    add_table(slide, data, left=0.5, top=1.3, width=7.5, row_height=0.43, font_size=11)

    # 右側カテゴリ
    add_card(slide, "商品カテゴリ TOP3",
             "1. mochi（89回）\n2. cake（39回）\n3. cream（36回）",
             8.5, 1.3, 4.0, 1.8)

    add_card(slide, "評価ワード",
             "enak（88回）= おいしい\nmanis（30回）= 甘い\nlembut（18回）= やわらかい",
             8.5, 3.4, 4.0, 1.8)

    add_card(slide, "注目キーワード",
             "halal（33回）→ 認証への高い関心\njepang（17回）→ 日本ブランド認知",
             8.5, 5.5, 4.0, 1.3)

    add_bottom_bar(slide)
    add_slide_number(slide, 26, total_slides)

    # =========================================================================
    # Slide 27: 口コミインサイト
    # =========================================================================
    slide = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide, WHITE)
    add_section_title(slide, "口コミインサイト — 5つの発見", "Key Insights from TikTok Analysis")

    insights = [
        ("Mochi が圧倒的人気商品", "89回言及で全商品中1位。chocolate mochi viralで400万再生級。"),
        ("「enak」が最多の評価ワード", "88回の「おいしい」評価。ポジティブな口コミが圧倒的。"),
        ("Halal への関心が高い", "33回の言及。質問・懸念として頻出。認証の明確化が必要。"),
        ("Matcha が人気フレーバー", "34回言及。「日本＝抹茶」の強い連想が存在。"),
        ("プロモへの反応が強い", "promo/diskon 合計45回。価格感度の高い市場。"),
    ]

    for i, (title, desc) in enumerate(insights):
        y = 1.3 + i * 1.1
        # 番号
        shape = slide.shapes.add_shape(
            MSO_SHAPE.OVAL, Inches(0.7), Inches(y), Inches(0.45), Inches(0.45)
        )
        shape.fill.solid()
        shape.fill.fore_color.rgb = RED
        shape.line.fill.background()
        tf = shape.text_frame
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        run = p.add_run()
        run.text = str(i + 1)
        run.font.size = Pt(16)
        run.font.bold = True
        run.font.color.rgb = WHITE
        run.font.name = FONT_JP

        # テキスト
        txBox = slide.shapes.add_textbox(Inches(1.4), Inches(y - 0.05), Inches(10.5), Inches(0.3))
        tf2 = txBox.text_frame
        p2 = tf2.paragraphs[0]
        run2 = p2.add_run()
        run2.text = title
        run2.font.size = Pt(16)
        run2.font.bold = True
        run2.font.color.rgb = BLACK
        run2.font.name = FONT_JP

        txBox2 = slide.shapes.add_textbox(Inches(1.4), Inches(y + 0.33), Inches(10.5), Inches(0.3))
        tf3 = txBox2.text_frame
        p3 = tf3.paragraphs[0]
        run3 = p3.add_run()
        run3.text = desc
        run3.font.size = Pt(12)
        run3.font.color.rgb = GRAY
        run3.font.name = FONT_JP

    add_bottom_bar(slide)
    add_slide_number(slide, 27, total_slides)

    # =========================================================================
    # Slide 28: 統合戦略 — 押し出すべき商品
    # =========================================================================
    slide = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide, WHITE)
    add_section_title(slide, "統合戦略：押し出すべき商品", "Integrated Strategy — Priority Products")

    products = [
        {
            "title": "最優先: Mochi",
            "desc": "口コミ言及数89回（全商品1位）\nバイラル実績: 400万再生級\n差別化: 日本式の本格mochi = 競合不可侵",
            "items": "Nama Chocolate Mochi / Matcha Mochi / Warabi Mochi",
            "color": RED,
        },
        {
            "title": "2位: Matcha系商品",
            "desc": "フレーバー中1位（34回言及）\n「日本＝抹茶」の強い連想\n韓国系は抹茶で勝負できない",
            "items": "Matcha Ice Cream / Matcha Cake / Matcha Roll Cake",
            "color": GREEN,
        },
        {
            "title": "3位: Cream Puff / Eclair",
            "desc": "「eclair enak banget」の評価多数\nRp 15,000以下で提供可能\nCEP④「日常パン」への参入商品",
            "items": "Cream Puff / Eclair / Custard商品",
            "color": BLUE,
        },
    ]

    for i, prod in enumerate(products):
        x = 0.3 + i * 4.2
        shape = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(1.4), Inches(3.9), Inches(5.0)
        )
        shape.fill.solid()
        shape.fill.fore_color.rgb = WHITE
        shape.line.color.rgb = prod["color"]
        shape.line.width = Pt(2)

        tf = shape.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.2)
        tf.margin_right = Inches(0.2)
        tf.margin_top = Inches(0.25)

        p = tf.paragraphs[0]
        run = p.add_run()
        run.text = prod["title"]
        run.font.size = Pt(18)
        run.font.bold = True
        run.font.color.rgb = prod["color"]
        run.font.name = FONT_JP
        p.space_after = Pt(12)

        for line in prod["desc"].split("\n"):
            p2 = tf.add_paragraph()
            run2 = p2.add_run()
            run2.text = line
            run2.font.size = Pt(12)
            run2.font.color.rgb = BLACK
            run2.font.name = FONT_JP
            p2.space_after = Pt(4)

        p3 = tf.add_paragraph()
        p3.space_before = Pt(12)
        run3 = p3.add_run()
        run3.text = "具体的アイテム:"
        run3.font.size = Pt(11)
        run3.font.bold = True
        run3.font.color.rgb = GRAY
        run3.font.name = FONT_JP

        p4 = tf.add_paragraph()
        run4 = p4.add_run()
        run4.text = prod["items"]
        run4.font.size = Pt(11)
        run4.font.color.rgb = GRAY
        run4.font.name = FONT_JP

    add_bottom_bar(slide)
    add_slide_number(slide, 28, total_slides)

    # =========================================================================
    # Slide 29: 統合戦略 — 押し出すべき訴求
    # =========================================================================
    slide = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide, WHITE)
    add_section_title(slide, "統合戦略：押し出すべき訴求", "Integrated Strategy — Key Messages")

    messages = [
        {
            "title": "最優先訴求: 「甘さ控えめ」",
            "ma": "MA +14（市場1位）",
            "data": "manis（30回言及）/ ヘルスコンシャス層の増加",
            "msg_jp": "「甘さ控えめ、だから毎日食べられる」",
            "msg_id": "\"Tidak Terlalu Manis, Bisa Dinikmati Setiap Hari\"",
            "hashtag": "#LessSweet #GuiltyFree",
        },
        {
            "title": "2位訴求: 「日本品質」",
            "ma": "MA +24（市場1位、圧倒的）",
            "data": "jepang（17回言及）/ 競合不可侵",
            "msg_jp": "「日本から届く、毎日のご褒美」",
            "msg_id": "\"Kualitas Jepang, Harga Terjangkau\"",
            "hashtag": "#DirectlyFromJapan",
        },
        {
            "title": "要対応訴求: 「ハラル」",
            "ma": "ラマダンCEPで-9 MD",
            "data": "halal（33回言及）/ ムスリム人口2億人超",
            "msg_jp": "ハラル認証取得 → 全面訴求",
            "msg_id": "\"Halal Certified\"",
            "hashtag": "認証取得が最優先アクション",
        },
    ]

    for i, msg in enumerate(messages):
        y = 1.3 + i * 1.8
        colors = [RED, BLUE, ORANGE]
        bg_colors = [LIGHT_RED, RGBColor(0xE3, 0xF2, 0xFD), RGBColor(0xFD, 0xF0, 0xE0)]

        shape = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), Inches(y), Inches(12.0), Inches(1.55)
        )
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg_colors[i]
        shape.line.fill.background()

        tf = shape.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.2)
        tf.margin_right = Inches(0.2)
        tf.margin_top = Inches(0.1)

        p = tf.paragraphs[0]
        run = p.add_run()
        run.text = f"{msg['title']}    |    {msg['ma']}    |    {msg['data']}"
        run.font.size = Pt(13)
        run.font.bold = True
        run.font.color.rgb = colors[i]
        run.font.name = FONT_JP
        p.space_after = Pt(6)

        p2 = tf.add_paragraph()
        run2 = p2.add_run()
        run2.text = f"JP: {msg['msg_jp']}    |    ID: {msg['msg_id']}    |    {msg['hashtag']}"
        run2.font.size = Pt(12)
        run2.font.color.rgb = BLACK
        run2.font.name = FONT_JP

    add_bottom_bar(slide)
    add_slide_number(slide, 29, total_slides)

    # =========================================================================
    # Slide 30: アクションプラン
    # =========================================================================
    slide = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide, WHITE)
    add_section_title(slide, "アクションプラン", "Action Plan — Short / Mid / Long Term")

    # 短期
    add_card(slide, "短期（〜6ヶ月）",
             "1. ハラル認証の取得・訴求強化\n2. Rp 15,000以下の商品ラインナップ拡充\n3. Instagram・TikTokフォロワー拡大施策\n4. ラマダン向けギフト商品の開発・プロモーション",
             0.5, 1.3, 3.8, 3.5, bg_color=LIGHT_RED, title_color=RED)

    # 中期
    add_card(slide, "中期（6ヶ月〜1年）",
             "5. デリバリー対応の強化（Grab、GoFood）\n6. 「甘さ控えめ」のUGC促進キャンペーン\n7. 決済アプリ連携プロモーション\n8. 地方都市への出店加速",
             4.6, 1.3, 3.8, 3.5, bg_color=RGBColor(0xFD, 0xF0, 0xE0), title_color=ORANGE)

    # 長期
    add_card(slide, "長期（1年〜）",
             "9. ブカシ新工場稼働に合わせた大規模プロモ\n10. カカオ農家支援ストーリーのブランディング\n11. 450店舗体制に向けたFC展開検討",
             8.7, 1.3, 3.8, 3.5, bg_color=RGBColor(0xE3, 0xF2, 0xFD), title_color=BLUE)

    # CEPベースKPI
    data = [
        ["フェーズ", "期間", "重点CEP", "KPI"],
        ["短期", "〜6ヶ月", "⑪⑫（独自CEP強化）", "言及率: ⑪→40%、⑫→30%"],
        ["中期", "6ヶ月〜1年", "⑦④⑤（参入・拡大）", "平均言及率: 16%→20%"],
        ["長期", "1年〜", "③（ハラル対応）", "ラマダンCEP: 8%→15%"],
    ]
    add_table(slide, data, left=0.5, top=5.2, width=12.0, row_height=0.4, font_size=11)

    add_bottom_bar(slide)
    add_slide_number(slide, 30, total_slides)

    # =========================================================================
    # Slide 31: 結論
    # =========================================================================
    slide = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide, WHITE)

    # 上部の大きな赤帯
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SLIDE_WIDTH, Inches(2.5))
    shape.fill.solid()
    shape.fill.fore_color.rgb = RED
    shape.line.fill.background()

    txBox = slide.shapes.add_textbox(Inches(0.8), Inches(0.6), Inches(11), Inches(1.5))
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = "結論"
    run.font.size = Pt(36)
    run.font.bold = True
    run.font.color.rgb = WHITE
    run.font.name = FONT_JP
    p.space_after = Pt(8)

    p2 = tf.add_paragraph()
    run2 = p2.add_run()
    run2.text = "「総合力では負けているが、独自の土俵では圧勝している」"
    run2.font.size = Pt(20)
    run2.font.color.rgb = WHITE
    run2.font.name = FONT_JP

    # 核心メッセージ
    core_msg = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(3.0), Inches(11.5), Inches(2.0)
    )
    core_msg.fill.solid()
    core_msg.fill.fore_color.rgb = LIGHT_RED
    core_msg.line.color.rgb = RED
    core_msg.line.width = Pt(2)

    tf3 = core_msg.text_frame
    tf3.word_wrap = True
    tf3.margin_left = Inches(0.3)
    tf3.margin_top = Inches(0.2)

    p3 = tf3.paragraphs[0]
    run3 = p3.add_run()
    run3.text = "Mochi × 甘さ控えめ × 日本品質"
    run3.font.size = Pt(28)
    run3.font.bold = True
    run3.font.color.rgb = RED
    run3.font.name = FONT_JP
    p3.space_after = Pt(8)

    p4 = tf3.add_paragraph()
    run4 = p4.add_run()
    run4.text = "を軸に展開し、ハラル対応を急ぐ。これが CEP分析・口コミ分析・市場分析の3つを統合した最適解。"
    run4.font.size = Pt(16)
    run4.font.color.rgb = BLACK
    run4.font.name = FONT_JP

    # 3つの柱
    pillars = [
        ("独自CEPで勝つ", "日本品質(MA+24)\n甘さ控えめ(MA+14)"),
        ("Mochiを主力に", "口コミ89回\nバイラル実績あり"),
        ("ハラル対応を急ぐ", "口コミ33回の懸念\n2億人市場へのキー"),
    ]
    for i, (title, desc) in enumerate(pillars):
        x = 0.8 + i * 4.0
        add_card(slide, title, desc, x, 5.3, 3.5, 1.5)

    add_bottom_bar(slide)
    add_slide_number(slide, 31, total_slides)

    # =========================================================================
    # 保存
    # =========================================================================
    output_path = "/Users/rikohayashi/Downloads/AP/シャトレーゼ_インドネシア市場分析.pptx"
    prs.save(output_path)
    print(f"PowerPoint saved to: {output_path}")
    print(f"Total slides: {len(prs.slides)}")


if __name__ == "__main__":
    create_presentation()
