#!/usr/bin/env python3
"""グミ ポジショニングマップ分析レポート PPTX生成スクリプト"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
import os

# ─── カラーテーマ ───
NAVY = RGBColor(0x1B, 0x2A, 0x4A)
ACCENT_BLUE = RGBColor(0x3B, 0x82, 0xF6)
ACCENT_RED = RGBColor(0xEF, 0x44, 0x44)
ACCENT_GREEN = RGBColor(0x10, 0xB9, 0x81)
ACCENT_ORANGE = RGBColor(0xF5, 0x9E, 0x0B)
ACCENT_PURPLE = RGBColor(0x8B, 0x5C, 0xF6)
LIGHT_GRAY = RGBColor(0xF1, 0xF5, 0xF9)
MID_GRAY = RGBColor(0x94, 0xA3, 0xB8)
DARK_GRAY = RGBColor(0x47, 0x55, 0x69)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
BLACK = RGBColor(0x1E, 0x29, 0x3B)
TABLE_HEADER = RGBColor(0x1E, 0x3A, 0x5F)
TABLE_ROW1 = RGBColor(0xF8, 0xFA, 0xFC)
TABLE_ROW2 = RGBColor(0xE2, 0xE8, 0xF0)
HIGHLIGHT_BG = RGBColor(0xDB, 0xEA, 0xFE)
PINK = RGBColor(0xEC, 0x48, 0x99)
SOFT_PINK = RGBColor(0xFD, 0xF2, 0xF8)
SOFT_BLUE = RGBColor(0xEF, 0xF6, 0xFF)
SOFT_GREEN = RGBColor(0xEC, 0xFD, 0xF5)
SOFT_ORANGE = RGBColor(0xFF, 0xFB, 0xEB)
SOFT_PURPLE = RGBColor(0xF5, 0xF3, 0xFF)


def add_background(slide, color=WHITE):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_accent_bar(slide, left=0, top=0, width=None, height=Inches(0.06), color=ACCENT_BLUE):
    if width is None:
        width = Inches(13.33)
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    return shape


def add_side_bar(slide, color=NAVY):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(0.4), Inches(7.5))
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    return shape


def set_cell_text(cell, text, font_size=10, bold=False, color=BLACK, alignment=PP_ALIGN.LEFT):
    cell.text = ""
    p = cell.text_frame.paragraphs[0]
    p.alignment = alignment
    run = p.add_run()
    run.text = str(text)
    run.font.size = Pt(font_size)
    run.font.bold = bold
    run.font.color.rgb = color
    run.font.name = "Meiryo"
    cell.text_frame.word_wrap = True
    cell.vertical_anchor = MSO_ANCHOR.MIDDLE


def add_table(slide, rows_data, left, top, width, row_height=Inches(0.38),
              header_color=TABLE_HEADER, font_size=9, col_widths=None):
    rows = len(rows_data)
    cols = len(rows_data[0])
    table_shape = slide.shapes.add_table(rows, cols, left, top, width, row_height * rows)
    table = table_shape.table
    if col_widths:
        for i, w in enumerate(col_widths):
            table.columns[i].width = w
    for r_idx, row in enumerate(rows_data):
        for c_idx, val in enumerate(row):
            cell = table.cell(r_idx, c_idx)
            is_header = (r_idx == 0)
            if is_header:
                cell.fill.solid()
                cell.fill.fore_color.rgb = header_color
                set_cell_text(cell, val, font_size=font_size, bold=True, color=WHITE,
                              alignment=PP_ALIGN.CENTER)
            else:
                cell.fill.solid()
                cell.fill.fore_color.rgb = TABLE_ROW1 if r_idx % 2 == 1 else TABLE_ROW2
                set_cell_text(cell, val, font_size=font_size, bold=False, color=BLACK)
    return table_shape


def add_textbox(slide, text, left, top, width, height, font_size=12, color=BLACK,
                bold=False, alignment=PP_ALIGN.LEFT):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = alignment
    run = p.add_run()
    run.text = text
    run.font.size = Pt(font_size)
    run.font.color.rgb = color
    run.font.bold = bold
    run.font.name = "Meiryo"
    return txBox


def add_multiline_textbox(slide, lines, left, top, width, height, font_size=11, color=BLACK,
                           line_spacing=Pt(18)):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    for i, line in enumerate(lines):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.space_after = Pt(3)
        run = p.add_run()
        run.text = line
        run.font.size = Pt(font_size)
        run.font.color.rgb = color
        run.font.name = "Meiryo"
    return txBox


def add_callout_box(slide, text, left, top, width, height, bg_color=HIGHLIGHT_BG,
                    text_color=NAVY, font_size=11, bold=True):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    shape.line.fill.background()
    tf = shape.text_frame
    tf.word_wrap = True
    tf.margin_left = Pt(14)
    tf.margin_right = Pt(14)
    tf.margin_top = Pt(10)
    tf.margin_bottom = Pt(10)
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = text
    run.font.size = Pt(font_size)
    run.font.color.rgb = text_color
    run.font.bold = bold
    run.font.name = "Meiryo"
    return shape


def add_kpi_box(slide, label, value, left, top, width=Inches(2.8), height=Inches(1.2),
                bg_color=WHITE, value_color=ACCENT_BLUE):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    shape.line.color.rgb = RGBColor(0xE2, 0xE8, 0xF0)
    shape.line.width = Pt(1)
    tf = shape.text_frame
    tf.word_wrap = True
    tf.margin_left = Pt(10)
    tf.margin_right = Pt(10)
    tf.margin_top = Pt(8)
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    run = p.add_run()
    run.text = value
    run.font.size = Pt(24)
    run.font.color.rgb = value_color
    run.font.bold = True
    run.font.name = "Meiryo"
    p2 = tf.add_paragraph()
    p2.alignment = PP_ALIGN.CENTER
    run2 = p2.add_run()
    run2.text = label
    run2.font.size = Pt(9)
    run2.font.color.rgb = DARK_GRAY
    run2.font.name = "Meiryo"
    return shape


def add_content_slide(slide, title_text, section_num=""):
    add_background(slide, WHITE)
    add_side_bar(slide, NAVY)
    add_accent_bar(slide, left=Inches(0.4), top=Inches(1.1), height=Inches(0.03), color=ACCENT_PURPLE)
    if section_num:
        add_textbox(slide, section_num, Inches(0.6), Inches(0.2), Inches(1), Inches(0.4),
                    font_size=10, color=MID_GRAY)
    add_textbox(slide, title_text, Inches(0.6), Inches(0.4), Inches(12), Inches(0.7),
                font_size=22, color=NAVY, bold=True)


def add_dot(slide, label, left, top, color, font_size=8, dot_size=Inches(0.13)):
    dot = slide.shapes.add_shape(MSO_SHAPE.OVAL, left, top, dot_size, dot_size)
    dot.fill.solid()
    dot.fill.fore_color.rgb = color
    dot.line.fill.background()
    add_textbox(slide, label, left + dot_size + Inches(0.05), top - Inches(0.02),
                Inches(2.5), Inches(0.25), font_size=font_size, color=color, bold=True)


def create_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.33)
    prs.slide_height = Inches(7.5)
    blank = prs.slide_layouts[6]

    # ═══════════════════════════════════════════════
    # Slide 1: Title
    # ═══════════════════════════════════════════════
    slide = prs.slides.add_slide(blank)
    add_background(slide, NAVY)
    add_accent_bar(slide, top=Inches(0), height=Inches(0.08), color=ACCENT_PURPLE)
    add_accent_bar(slide, top=Inches(4.5), height=Inches(0.05), color=ACCENT_PURPLE)

    add_textbox(slide, "グミ市場", Inches(1.5), Inches(1.5), Inches(10), Inches(0.7),
                font_size=22, color=MID_GRAY)
    add_textbox(slide, "ポジショニングマップ\n分析レポート", Inches(1.5), Inches(2.2), Inches(10), Inches(1.5),
                font_size=42, color=WHITE, bold=True)
    add_textbox(slide, "2023〜2026年 新発売グミの市場トレンド分析",
                Inches(1.5), Inches(4.8), Inches(10), Inches(0.5),
                font_size=14, color=MID_GRAY)
    add_textbox(slide, "分析軸：「食感（ハード↔ソフト）」 × 「味の方向性（果汁感・ナチュラル↔刺激系）」",
                Inches(1.5), Inches(5.3), Inches(10), Inches(0.4),
                font_size=12, color=MID_GRAY)

    # ═══════════════════════════════════════════════
    # Slide 2: Overview
    # ═══════════════════════════════════════════════
    slide = prs.slides.add_slide(blank)
    add_content_slide(slide, "調査概要")

    add_kpi_box(slide, "対象期間", "2023-2026", Inches(0.6), Inches(1.5), Inches(3.8))
    add_kpi_box(slide, "新商品数", "27商品", Inches(4.7), Inches(1.5), Inches(3.8), value_color=ACCENT_PURPLE)
    add_kpi_box(slide, "分析対象", "新発売グミ", Inches(8.8), Inches(1.5), Inches(3.8))

    add_textbox(slide, "分析軸", Inches(0.6), Inches(3.2), Inches(12), Inches(0.4),
                font_size=16, color=NAVY, bold=True)

    # Axis explanation boxes
    shape1 = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(3.8), Inches(5.8), Inches(1.5))
    shape1.fill.solid()
    shape1.fill.fore_color.rgb = SOFT_PURPLE
    shape1.line.color.rgb = ACCENT_PURPLE
    shape1.line.width = Pt(2)
    add_textbox(slide, "横軸：食感", Inches(0.9), Inches(3.9), Inches(5), Inches(0.4),
                font_size=14, color=ACCENT_PURPLE, bold=True)
    add_textbox(slide, "ハード（噛み応え重視）← → ソフト（やわらかい・新食感）\n\n噛むことで得られる満足感から、\nもちもち・とろける等の新しい食感体験まで",
                Inches(0.9), Inches(4.3), Inches(5), Inches(1.0), font_size=10, color=DARK_GRAY)

    shape2 = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(3.8), Inches(5.8), Inches(1.5))
    shape2.fill.solid()
    shape2.fill.fore_color.rgb = SOFT_ORANGE
    shape2.line.color.rgb = ACCENT_ORANGE
    shape2.line.width = Pt(2)
    add_textbox(slide, "縦軸：味の方向性", Inches(7.1), Inches(3.9), Inches(5), Inches(0.4),
                font_size=14, color=ACCENT_ORANGE, bold=True)
    add_textbox(slide, "果汁感・ナチュラル ↑ ↓ 刺激系・酸味・人工的フレーバー\n\nフルーツ本来の味わいを追求する商品から、\n刺激・酸味・コラボ味など個性的な味まで",
                Inches(7.1), Inches(4.3), Inches(5), Inches(1.0), font_size=10, color=DARK_GRAY)

    add_callout_box(slide, "目的：直近3年間のグミ市場の新商品トレンドをポジショニングマップで可視化し、競合状況と市場機会を特定する",
                    Inches(0.6), Inches(5.8), Inches(12), Inches(0.5),
                    bg_color=HIGHLIGHT_BG, text_color=NAVY, font_size=11)

    # ═══════════════════════════════════════════════
    # Slide 3: Positioning Map
    # ═══════════════════════════════════════════════
    slide = prs.slides.add_slide(blank)
    add_content_slide(slide, "ポジショニングマップ")

    map_left = Inches(1.0)
    map_top = Inches(1.3)
    map_w = Inches(11.0)
    map_h = Inches(5.5)

    # Background quadrants
    # Top-left: Hard x Fruit
    q_tl = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,
        map_left, map_top, Inches(5.5), Inches(2.75))
    q_tl.fill.solid()
    q_tl.fill.fore_color.rgb = RGBColor(0xF0, 0xFD, 0xF4)  # soft green
    q_tl.line.fill.background()

    # Top-right: Soft x Fruit
    q_tr = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,
        Inches(6.5), map_top, Inches(5.5), Inches(2.75))
    q_tr.fill.solid()
    q_tr.fill.fore_color.rgb = RGBColor(0xFE, 0xF3, 0xC7)  # soft yellow
    q_tr.line.fill.background()

    # Bottom-left: Hard x Stimulus
    q_bl = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,
        map_left, Inches(4.05), Inches(5.5), Inches(2.75))
    q_bl.fill.solid()
    q_bl.fill.fore_color.rgb = RGBColor(0xFD, 0xF2, 0xF8)  # soft pink
    q_bl.line.fill.background()

    # Bottom-right: Soft x Stimulus
    q_br = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,
        Inches(6.5), Inches(4.05), Inches(5.5), Inches(2.75))
    q_br.fill.solid()
    q_br.fill.fore_color.rgb = RGBColor(0xF5, 0xF3, 0xFF)  # soft purple
    q_br.line.fill.background()

    # Axes
    # Vertical
    v_axis = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,
        Inches(6.48), map_top, Inches(0.04), map_h)
    v_axis.fill.solid()
    v_axis.fill.fore_color.rgb = DARK_GRAY
    v_axis.line.fill.background()
    # Horizontal
    h_axis = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,
        map_left, Inches(4.03), map_w, Inches(0.04))
    h_axis.fill.solid()
    h_axis.fill.fore_color.rgb = DARK_GRAY
    h_axis.line.fill.background()

    # Axis labels
    add_textbox(slide, "果汁感・ナチュラル", Inches(5.0), Inches(1.15), Inches(3), Inches(0.3),
                font_size=10, color=ACCENT_GREEN, bold=True, alignment=PP_ALIGN.CENTER)
    add_textbox(slide, "刺激・酸味・人工的", Inches(5.0), Inches(6.85), Inches(3), Inches(0.3),
                font_size=10, color=ACCENT_RED, bold=True, alignment=PP_ALIGN.CENTER)
    add_textbox(slide, "ハード", Inches(1.0), Inches(3.8), Inches(1.5), Inches(0.3),
                font_size=10, color=NAVY, bold=True, alignment=PP_ALIGN.CENTER)
    add_textbox(slide, "ソフト", Inches(10.5), Inches(3.8), Inches(1.5), Inches(0.3),
                font_size=10, color=ACCENT_PURPLE, bold=True, alignment=PP_ALIGN.CENTER)

    # Quadrant labels
    add_textbox(slide, "ハード×果汁\n2商品", Inches(1.2), Inches(1.4), Inches(2), Inches(0.5),
                font_size=9, color=ACCENT_GREEN, bold=True)
    add_textbox(slide, "ソフト×果汁\n10商品", Inches(10.0), Inches(1.4), Inches(2), Inches(0.5),
                font_size=9, color=ACCENT_ORANGE, bold=True)
    add_textbox(slide, "ハード×刺激\n5商品", Inches(1.2), Inches(6.2), Inches(2), Inches(0.5),
                font_size=9, color=PINK, bold=True)
    add_textbox(slide, "ソフト×刺激\n10商品", Inches(10.0), Inches(6.2), Inches(2), Inches(0.5),
                font_size=9, color=ACCENT_PURPLE, bold=True)

    # Dots - Top Left (Hard x Fruit) - green
    add_dot(slide, "果汁グミ弾力プラス", Inches(2.5), Inches(1.8), ACCENT_GREEN)
    add_dot(slide, "タフグミ グレーピーパンチ", Inches(2.0), Inches(2.6), ACCENT_GREEN)

    # Dots - Top Right (Soft x Fruit) - orange
    add_dot(slide, "とろみ～グミ", Inches(7.2), Inches(1.5), ACCENT_ORANGE, font_size=7)
    add_dot(slide, "つぶグミPREMIUM濃厚いちご", Inches(7.5), Inches(1.8), ACCENT_ORANGE, font_size=7)
    add_dot(slide, "つぶグミPREMIUM濃厚梨", Inches(9.5), Inches(1.5), ACCENT_ORANGE, font_size=7)
    add_dot(slide, "ネクター厳選果実グミ", Inches(8.0), Inches(2.1), ACCENT_ORANGE, font_size=7)
    add_dot(slide, "おとうふくん", Inches(9.0), Inches(2.4), ACCENT_ORANGE, font_size=7)
    add_dot(slide, "ピックミーピーチ", Inches(7.0), Inches(2.7), ACCENT_ORANGE, font_size=7)
    add_dot(slide, "もちゅグミ", Inches(9.2), Inches(2.8), ACCENT_ORANGE, font_size=7)
    add_dot(slide, "4Dグミ各種", Inches(8.5), Inches(3.2), ACCENT_ORANGE, font_size=7)
    add_dot(slide, "むちもっちバナナ", Inches(7.3), Inches(3.1), ACCENT_ORANGE, font_size=7)
    add_dot(slide, "ピュアラルグミ(既)", Inches(9.8), Inches(3.4), MID_GRAY, font_size=7)

    # Dots - Bottom Left (Hard x Stimulus) - pink
    add_dot(slide, "KAZITTE!", Inches(2.0), Inches(4.3), PINK, font_size=8)
    add_dot(slide, "忍者めしベイマックス", Inches(2.3), Inches(4.8), PINK, font_size=7)
    add_dot(slide, "タフグミ グレフルフィーバー", Inches(1.8), Inches(5.3), PINK, font_size=7)
    add_dot(slide, "コーラアップ ザハード(既)", Inches(2.5), Inches(5.8), MID_GRAY, font_size=7)
    add_dot(slide, "小梅グミ", Inches(3.5), Inches(6.0), PINK, font_size=7)
    add_dot(slide, "タフグミPRO(既)", Inches(3.0), Inches(6.3), MID_GRAY, font_size=7)

    # Dots - Bottom Right (Soft x Stimulus) - purple
    add_dot(slide, "しゃりinグミ", Inches(8.5), Inches(4.8), ACCENT_PURPLE, font_size=7)
    add_dot(slide, "ざくふにゅグミ", Inches(7.0), Inches(5.2), ACCENT_PURPLE, font_size=7)
    add_dot(slide, "Gumidy グミinキャンディ", Inches(9.0), Inches(4.3), ACCENT_PURPLE, font_size=7)
    add_dot(slide, "シークラゲグミ", Inches(7.5), Inches(5.5), ACCENT_PURPLE, font_size=7)
    add_dot(slide, "トッピンポップグミ", Inches(8.8), Inches(5.0), ACCENT_PURPLE, font_size=7)
    add_dot(slide, "チョコがけミント", Inches(9.5), Inches(5.5), ACCENT_PURPLE, font_size=7)
    add_dot(slide, "エッセルスーパーカップ味", Inches(7.0), Inches(5.8), ACCENT_PURPLE, font_size=7)
    add_dot(slide, "もちっとグミチョコ", Inches(9.2), Inches(6.0), ACCENT_PURPLE, font_size=7)
    add_dot(slide, "しらたまるグミ梅味", Inches(7.5), Inches(4.5), ACCENT_PURPLE, font_size=7)
    add_dot(slide, "4Dグミ悪魔の実", Inches(9.8), Inches(6.2), ACCENT_PURPLE, font_size=7)

    # Legend
    add_textbox(slide, "★ = 新商品（2023-2026）　　○ = 既存/リニューアル",
                Inches(3.5), Inches(7.0), Inches(6), Inches(0.3),
                font_size=9, color=MID_GRAY, alignment=PP_ALIGN.CENTER)

    # ═══════════════════════════════════════════════
    # Slide 4: Quadrant Summary
    # ═══════════════════════════════════════════════
    slide = prs.slides.add_slide(blank)
    add_content_slide(slide, "象限別の集計")

    # 4 boxes
    def add_quadrant_box(slide, title, count, examples, left, top, bg, border, title_color):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(5.8), Inches(2.5))
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg
        shape.line.color.rgb = border
        shape.line.width = Pt(2)
        add_textbox(slide, title, left + Inches(0.2), top + Inches(0.15),
                    Inches(4), Inches(0.4), font_size=14, color=title_color, bold=True)
        add_textbox(slide, count, left + Inches(4.5), top + Inches(0.15),
                    Inches(1), Inches(0.4), font_size=18, color=title_color, bold=True,
                    alignment=PP_ALIGN.RIGHT)
        add_multiline_textbox(slide, examples, left + Inches(0.3), top + Inches(0.7),
                               Inches(5.2), Inches(1.7), font_size=10, color=DARK_GRAY)

    add_quadrant_box(slide, "左上：ハード × 果汁", "2商品",
        ["果汁グミ弾力プラス（明治）", "タフグミ グレーピーパンチ（カバヤ）",
         "", "→ 比較的空白地帯。新商品開発の余地あり"],
        Inches(0.6), Inches(1.3), SOFT_GREEN, ACCENT_GREEN, ACCENT_GREEN)

    add_quadrant_box(slide, "右上：ソフト × 果汁", "10商品",
        ["とろみ～グミ（カンロ）、つぶグミPREMIUM各種", "ネクター厳選果実グミ（不二家）",
         "おとうふくん（カバヤ）、もちゅグミ、4Dグミ各種",
         "→ 最多タイ。ソフト+ナチュラルの組み合わせが人気"],
        Inches(6.8), Inches(1.3), SOFT_ORANGE, ACCENT_ORANGE, ACCENT_ORANGE)

    add_quadrant_box(slide, "左下：ハード × 刺激", "5商品",
        ["KAZITTE!（ロッテ）、忍者めしベイマックス（UHA）",
         "タフグミ グレフルフィーバー（カバヤ）、小梅グミ（ロッテ）",
         "", "→ ハード系の新規参入が2025年に活発化"],
        Inches(0.6), Inches(4.2), SOFT_PINK, PINK, PINK)

    add_quadrant_box(slide, "右下：ソフト × 刺激/新食感", "10商品",
        ["しゃりinグミ（カバヤ）、ざくふにゅグミ、Gumidy",
         "シークラゲグミ（カンロ）、トッピンポップグミ",
         "チョコがけミントグミ、もちっとグミチョコ（森永）",
         "→ 最も過密。差別化が難しくなっている"],
        Inches(6.8), Inches(4.2), SOFT_PURPLE, ACCENT_PURPLE, ACCENT_PURPLE)

    # ═══════════════════════════════════════════════
    # Slide 5: Hypothesis Verification
    # ═══════════════════════════════════════════════
    slide = prs.slides.add_slide(blank)
    add_content_slide(slide, "仮説の検証")

    add_callout_box(slide,
        "仮説：「ハード系と新食感系グミの発売が多い」",
        Inches(0.6), Inches(1.3), Inches(12), Inches(0.5),
        bg_color=SOFT_PURPLE, text_color=ACCENT_PURPLE, font_size=14)

    add_callout_box(slide,
        "結論：仮説は概ね正しい。ただし、より正確には「新食感系」の方がハード系より多い。",
        Inches(0.6), Inches(2.0), Inches(12), Inches(0.5),
        bg_color=NAVY, text_color=WHITE, font_size=14)

    # KPI boxes
    add_kpi_box(slide, "新食感系\nしゃり・もちもち・とろける・4D等", "56%", Inches(0.6), Inches(2.9),
                Inches(3.6), Inches(1.4), value_color=ACCENT_PURPLE)
    add_textbox(slide, "15商品", Inches(0.6), Inches(4.35), Inches(3.6), Inches(0.3),
                font_size=11, color=ACCENT_PURPLE, bold=True, alignment=PP_ALIGN.CENTER)

    add_kpi_box(slide, "ハード系\nタフグミ派生・KAZITTE!・忍者めし等", "26%", Inches(4.5), Inches(2.9),
                Inches(3.6), Inches(1.4), value_color=ACCENT_RED)
    add_textbox(slide, "7商品", Inches(4.5), Inches(4.35), Inches(3.6), Inches(0.3),
                font_size=11, color=ACCENT_RED, bold=True, alignment=PP_ALIGN.CENTER)

    add_kpi_box(slide, "従来型ソフト/果汁\nつぶグミPREMIUM・ネクター等", "18%", Inches(8.4), Inches(2.9),
                Inches(3.6), Inches(1.4), value_color=ACCENT_GREEN)
    add_textbox(slide, "5商品", Inches(8.4), Inches(4.35), Inches(3.6), Inches(0.3),
                font_size=11, color=ACCENT_GREEN, bold=True, alignment=PP_ALIGN.CENTER)

    # Bar visualization
    bar_top = Inches(5.0)
    bar_h = Inches(0.6)
    total_w = Inches(11.4)
    # 56%
    b1 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,
        Inches(0.6), bar_top, Inches(total_w.inches * 0.56), bar_h)
    b1.fill.solid()
    b1.fill.fore_color.rgb = ACCENT_PURPLE
    b1.line.fill.background()
    # 26%
    b2 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,
        Inches(0.6 + total_w.inches * 0.56), bar_top, Inches(total_w.inches * 0.26), bar_h)
    b2.fill.solid()
    b2.fill.fore_color.rgb = ACCENT_RED
    b2.line.fill.background()
    # 18%
    b3 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,
        Inches(0.6 + total_w.inches * 0.82), bar_top, Inches(total_w.inches * 0.18), bar_h)
    b3.fill.solid()
    b3.fill.fore_color.rgb = ACCENT_GREEN
    b3.line.fill.background()

    add_textbox(slide, "新食感系 56%", Inches(2.0), bar_top + Inches(0.1), Inches(3), Inches(0.4),
                font_size=11, color=WHITE, bold=True, alignment=PP_ALIGN.CENTER)
    add_textbox(slide, "ハード 26%", Inches(0.6 + total_w.inches * 0.56), bar_top + Inches(0.1),
                Inches(total_w.inches * 0.26), Inches(0.4),
                font_size=10, color=WHITE, bold=True, alignment=PP_ALIGN.CENTER)
    add_textbox(slide, "果汁 18%", Inches(0.6 + total_w.inches * 0.82), bar_top + Inches(0.1),
                Inches(total_w.inches * 0.18), Inches(0.4),
                font_size=9, color=WHITE, bold=True, alignment=PP_ALIGN.CENTER)

    # ═══════════════════════════════════════════════
    # Slide 6: Detailed Trends
    # ═══════════════════════════════════════════════
    slide = prs.slides.add_slide(blank)
    add_content_slide(slide, "詳細な傾向")

    # Trend 1
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(0.6), Inches(1.3), Inches(3.8), Inches(2.8))
    shape.fill.solid()
    shape.fill.fore_color.rgb = SOFT_PURPLE
    shape.line.color.rgb = ACCENT_PURPLE
    shape.line.width = Pt(2)
    add_textbox(slide, "1. 新食感系が最大勢力（56%）", Inches(0.9), Inches(1.45),
                Inches(3.2), Inches(0.4), font_size=13, color=ACCENT_PURPLE, bold=True)
    add_multiline_textbox(slide, [
        "カンロが4Dグミ・シークラゲ・とろみ～グミで",
        "「見た目×食感」の新カテゴリを開拓",
        "",
        "カバヤもしゃりinグミ・ピュアラルグミで",
        "複合食感に参入",
        "",
        "「もちゅ」「むちもっち」「ざくふにゅ」など",
        "オノマトペ系ネーミングが2025年に急増",
    ], Inches(0.9), Inches(1.9), Inches(3.2), Inches(2.0), font_size=9, color=DARK_GRAY)

    # Trend 2
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(4.7), Inches(1.3), Inches(3.8), Inches(2.8))
    shape.fill.solid()
    shape.fill.fore_color.rgb = SOFT_PINK
    shape.line.color.rgb = ACCENT_RED
    shape.line.width = Pt(2)
    add_textbox(slide, "2. ハード系も堅調（26%）", Inches(5.0), Inches(1.45),
                Inches(3.2), Inches(0.4), font_size=13, color=ACCENT_RED, bold=True)
    add_multiline_textbox(slide, [
        "ロッテが約3年ぶりの新ブランド",
        "「KAZITTE!」でハード市場に参入（2025年）",
        "",
        "カバヤはタフグミを軸にサブライン拡張",
        "PRO（機能性）・BAR（形状）・mini（サイズ）",
        "",
        "明治「コーラアップ ザ ハード」で",
        "既存ブランドの超ハード化",
    ], Inches(5.0), Inches(1.9), Inches(3.2), Inches(2.0), font_size=9, color=DARK_GRAY)

    # Trend 3
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(8.8), Inches(1.3), Inches(3.8), Inches(2.8))
    shape.fill.solid()
    shape.fill.fore_color.rgb = SOFT_GREEN
    shape.line.color.rgb = ACCENT_GREEN
    shape.line.width = Pt(2)
    add_textbox(slide, "3. プレミアム果汁系は少数", Inches(9.1), Inches(1.45),
                Inches(3.2), Inches(0.4), font_size=13, color=ACCENT_GREEN, bold=True)
    add_multiline_textbox(slide, [
        "つぶグミPREMIUM、ネクター厳選果実など",
        "「素材の質」で差別化",
        "",
        "数は少ないが高単価・プレミアム路線として",
        "存在感を発揮",
    ], Inches(9.1), Inches(1.9), Inches(3.2), Inches(2.0), font_size=9, color=DARK_GRAY)

    # Year trends
    add_textbox(slide, "4. 年別の変化", Inches(0.6), Inches(4.4),
                Inches(12), Inches(0.4), font_size=14, color=NAVY, bold=True)

    year_data = [
        ["年", "主な傾向"],
        ["2023", "4Dグミ・シークラゲなど SNS映え＋新食感 の起点"],
        ["2024", "トッピンポップ・しゃりin等 複合食感 の多様化"],
        ["2025", "KAZITTE!参入で ハード系競争激化 ＋オノマトペ食感の乱立"],
        ["2026", "タフグミ派生・小梅グミ等 既存ブランドのグミ展開 が加速"],
    ]
    add_table(slide, year_data, Inches(0.6), Inches(4.9), Inches(12),
              col_widths=[Inches(1.5), Inches(10.5)], font_size=10)

    # ═══════════════════════════════════════════════
    # Slide 7: Marketing Implications
    # ═══════════════════════════════════════════════
    slide = prs.slides.add_slide(blank)
    add_content_slide(slide, "マーケティング的示唆")

    # Red zone - crowded
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(0.6), Inches(1.3), Inches(5.8), Inches(2.8))
    shape.fill.solid()
    shape.fill.fore_color.rgb = RGBColor(0xFE, 0xF2, 0xF2)
    shape.line.color.rgb = ACCENT_RED
    shape.line.width = Pt(2)
    add_textbox(slide, "過密地帯（レッドオーシャン）", Inches(0.9), Inches(1.5),
                Inches(5.2), Inches(0.4), font_size=16, color=ACCENT_RED, bold=True)
    add_textbox(slide, "右下：ソフト × 刺激/新食感", Inches(0.9), Inches(2.0),
                Inches(5.2), Inches(0.4), font_size=14, color=NAVY, bold=True)
    add_multiline_textbox(slide, [
        "10商品が集中する最も過密な象限",
        "",
        "「しゃり」「ざくふにゅ」「もちっと」など",
        "新食感の差別化が限界に近づいている",
        "",
        "→ この領域での新商品は差別化困難",
    ], Inches(0.9), Inches(2.5), Inches(5.2), Inches(1.5), font_size=11, color=DARK_GRAY)

    # Blue zone - opportunity
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(6.8), Inches(1.3), Inches(5.8), Inches(2.8))
    shape.fill.solid()
    shape.fill.fore_color.rgb = SOFT_BLUE
    shape.line.color.rgb = ACCENT_BLUE
    shape.line.width = Pt(2)
    add_textbox(slide, "空白地帯（ブルーオーシャン）", Inches(7.1), Inches(1.5),
                Inches(5.2), Inches(0.4), font_size=16, color=ACCENT_BLUE, bold=True)
    add_textbox(slide, "左上：ハード × 果汁/ナチュラル", Inches(7.1), Inches(2.0),
                Inches(5.2), Inches(0.4), font_size=14, color=NAVY, bold=True)
    add_multiline_textbox(slide, [
        "わずか2商品しかない比較的空白地帯",
        "",
        "「噛み応えがあるのに果汁感がしっかりある」",
        "という商品は少ない",
        "",
        "→ 新商品開発の余地あり",
    ], Inches(7.1), Inches(2.5), Inches(5.2), Inches(1.5), font_size=11, color=DARK_GRAY)

    # Key insight
    add_callout_box(slide,
        "市場機会：「ハード × 果汁/ナチュラル」領域\n\n"
        "噛み応えがしっかりありながら、果汁感やナチュラルな味わいを持つグミは、\n"
        "現在ほとんど存在しない。素材感のある果汁と本格的な噛み応えを両立した商品が、\n"
        "次の差別化ポイントになる可能性が高い。",
        Inches(0.6), Inches(4.5), Inches(12), Inches(1.8),
        bg_color=NAVY, text_color=WHITE, font_size=13)

    # ═══════════════════════════════════════════════
    # Slide 8: Summary
    # ═══════════════════════════════════════════════
    slide = prs.slides.add_slide(blank)
    add_background(slide, NAVY)
    add_accent_bar(slide, top=Inches(0), height=Inches(0.08), color=ACCENT_PURPLE)
    add_accent_bar(slide, top=Inches(4.0), height=Inches(0.05), color=ACCENT_PURPLE)

    add_textbox(slide, "まとめ", Inches(1.5), Inches(1.2), Inches(10), Inches(0.6),
                font_size=18, color=MID_GRAY)
    add_textbox(slide, "グミ市場 ポジショニング分析の要点",
                Inches(1.5), Inches(1.8), Inches(10), Inches(0.8),
                font_size=30, color=WHITE, bold=True, alignment=PP_ALIGN.LEFT)

    add_multiline_textbox(slide, [
        "1. 新食感系が最大勢力（56%）、ハード系も堅調（26%）",
        "",
        "2. 「ソフト × 刺激/新食感」が最も過密（レッドオーシャン）",
        "",
        "3. 「ハード × 果汁/ナチュラル」が空白地帯（ブルーオーシャン）",
        "     噛み応え + 果汁感の両立が次の差別化機会",
        "",
        "4. 2025年以降、ハード系の競争が激化",
        "     ロッテ「KAZITTE!」参入、既存ブランドのグミ展開加速",
        "",
        "5. オノマトペ系ネーミングがトレンド",
        "     「もちゅ」「むちもっち」「ざくふにゅ」等で食感を訴求",
    ], Inches(1.5), Inches(4.3), Inches(10), Inches(3.0),
        font_size=13, color=RGBColor(0xCB, 0xD5, 0xE1))

    add_textbox(slide, "データソース：Yahoo!ニュース、カバヤ食品、明治公式サイト、ranking.net",
                Inches(1.5), Inches(7.0), Inches(10), Inches(0.3),
                font_size=9, color=MID_GRAY, alignment=PP_ALIGN.LEFT)

    # Save
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               "グミ_ポジショニングマップ分析レポート.pptx")
    prs.save(output_path)
    print(f"PPTX saved: {output_path}")
    return output_path


if __name__ == "__main__":
    create_presentation()
