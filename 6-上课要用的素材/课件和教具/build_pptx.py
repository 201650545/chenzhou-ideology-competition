# -*- coding: utf-8 -*-
"""第1课《最喜欢的课》30页课件生成器
全部元素为 PPT 原生形状/文本框，可在 PowerPoint 中自由编辑、移动、加动画。
"""
import os, glob
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

NAVY = RGBColor(0x1B, 0x2A, 0x4A)
NAVY2 = RGBColor(0x24, 0x36, 0x5C)
NAVY3 = RGBColor(0x30, 0x45, 0x74)
GOLD = RGBColor(0xFF, 0xC8, 0x45)
GOLD_D = RGBColor(0xE0, 0xA0, 0x20)
CREAM = RGBColor(0xFD, 0xF6, 0xE3)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
GRAY = RGBColor(0xA8, 0xB6, 0xCE)
GREEN = RGBColor(0x5D, 0xC9, 0x9A)
CORAL = RGBColor(0xE8, 0x7A, 0x5A)

FONT = "微软雅黑"
SW, SH = 13.333, 7.5
M = 0.75

IMG_DIR = r"D:\Work\课程思政教学竞赛\6-上课要用的素材\课件和教具\生成图\课件配图"
OUT = r"D:\Work\课程思政教学竞赛\6-上课要用的素材\课件和教具\第1课_课件.pptx"

prs = Presentation()
prs.slide_width = Inches(SW)
prs.slide_height = Inches(SH)
BLANK = prs.slide_layouts[6]


def find_img(prefix):
    fs = glob.glob(os.path.join(IMG_DIR, prefix + "*.png"))
    return fs[0] if fs else None


def sld():
    s = prs.slides.add_slide(BLANK)
    bg = s.background.fill
    bg.solid()
    bg.fore_color.rgb = NAVY
    r = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(SW), Inches(SH))
    r.fill.solid()
    r.fill.fore_color.rgb = NAVY
    r.line.fill.background()
    r.shadow.inherit = False
    r.text_frame.text = ""
    return s


def box(s, x, y, w, h, fill=None, shape=MSO_SHAPE.ROUNDED_RECTANGLE, line=None, lw=1.0):
    sp = s.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    if shape == MSO_SHAPE.ROUNDED_RECTANGLE:
        try:
            sp.adjustments[0] = 0.06
        except Exception:
            pass
    if fill is None:
        sp.fill.background()
    else:
        sp.fill.solid()
        sp.fill.fore_color.rgb = fill
    if line is None:
        sp.line.fill.background()
    else:
        sp.line.color.rgb = line
        sp.line.width = Pt(lw)
    sp.shadow.inherit = False
    sp.text_frame.text = ""
    return sp


def txt(s, x, y, w, h, text, size=20, color=WHITE, bold=False, align=PP_ALIGN.LEFT,
        anchor=MSO_ANCHOR.TOP, spacing=1.25, font=FONT):
    tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = anchor
    lines = text.split("\n")
    for i, ln in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.line_spacing = spacing
        r = p.add_run()
        r.text = ln
        r.font.size = Pt(size)
        r.font.bold = bold
        r.font.color.rgb = color
        r.font.name = font
    return tb


def stars(s, n=14, seed=1):
    """背景装饰小星星"""
    import random
    random.seed(seed)
    placed = 0
    tries = 0
    while placed < n and tries < 200:
        tries += 1
        x = random.uniform(0.2, SW - 0.5)
        y = random.uniform(0.2, SH - 0.5)
        if 0.6 < x < SW - 0.6 and 1.0 < y < SH - 0.8:
            continue
        sz = random.choice([0.09, 0.12, 0.16])
        st = s.shapes.add_shape(MSO_SHAPE.STAR_5_POINT,
                                Inches(x), Inches(y), Inches(sz), Inches(sz))
        st.fill.solid()
        st.fill.fore_color.rgb = GOLD
        st.line.fill.background()
        st.shadow.inherit = False
        try:
            st.rotation = random.choice([0, 12, -10, 20])
        except Exception:
            pass
        placed += 1


def header(s, title, num=None, sub=None):
    """页眉：环节标签 + 标题"""
    if num:
        b = box(s, M, 0.42, 0.62, 0.62, GOLD, shape=MSO_SHAPE.OVAL)
        txt(s, M, 0.42, 0.62, 0.62, str(num), size=22, color=NAVY, bold=True, align=PP_ALIGN.CENTER,
            anchor=MSO_ANCHOR.MIDDLE)
    tx = M + (0.82 if num else 0)
    txt(s, tx, 0.42, SW - tx - M, 0.62, title, size=28, bold=True, color=WHITE,
        anchor=MSO_ANCHOR.MIDDLE)
    ln = box(s, M, 1.18, SW - 2 * M, 0.035, GOLD)
    if sub:
        txt(s, M, 1.32, SW - 2 * M, 0.4, sub, size=15, color=GRAY)


def footer(s, text):
    txt(s, M, SH - 0.62, SW - 2 * M, 0.35, text, size=12, color=GRAY)


def cards(s, items, x, y, w, h, gap=0.28, cols=None, fill=NAVY2, title_color=GOLD,
          body_color=WHITE, tsize=19, bsize=15):
    """并排卡片：items = [(标题, 正文), ...]"""
    n = len(items)
    cols = cols or n
    cw = (w - gap * (cols - 1)) / cols
    for i, (t, b) in enumerate(items):
        r, c = divmod(i, cols)
        cx = x + c * (cw + gap)
        cy = y + r * (h + gap)
        box(s, cx, cy, cw, h, fill, line=NAVY3, lw=0.75)
        txt(s, cx + 0.22, cy + 0.20, cw - 0.44, 0.4, t, size=tsize, bold=True, color=title_color)
        txt(s, cx + 0.22, cy + 0.72, cw - 0.44, h - 0.9, b, size=bsize, color=body_color, spacing=1.35)
    return


def pic(s, prefix, x, y, w, h):
    p = find_img(prefix)
    if not p:
        box(s, x, y, w, h, NAVY2, line=GOLD, lw=0.75)
        txt(s, x, y, w, h, "（配图待补）", size=14, color=GRAY, align=PP_ALIGN.CENTER,
            anchor=MSO_ANCHOR.MIDDLE)
        return False
    s.shapes.add_picture(p, Inches(x), Inches(y), width=Inches(w), height=Inches(h))
    return True


# ---------------------------------------------------------------- 页面内容
def top_band(s, title, sub, tsize=44, ssize=18, band_h=1.72):
    """整幅配图页顶部实色横幅（保证标题清晰可读）"""
    b = box(s, 0, 0, SW, band_h, NAVY, shape=MSO_SHAPE.RECTANGLE)
    box(s, 0, band_h - 0.05, SW, 0.05, GOLD, shape=MSO_SHAPE.RECTANGLE)
    txt(s, 0, 0.30, SW, 0.85, title, size=tsize, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    txt(s, 0, band_h - 0.62, SW, 0.42, sub, size=ssize, color=GOLD, align=PP_ALIGN.CENTER)


def p01(s):
    p = find_img("img01")
    if p:
        s.shapes.add_picture(p, Inches(0), Inches(0), width=Inches(SW), height=Inches(SH))
    else:
        stars(s, 18, seed=3)
    band = box(s, 0, 0, SW, 1.85, NAVY, shape=MSO_SHAPE.RECTANGLE)
    box(s, 0, 1.80, SW, 0.05, GOLD, shape=MSO_SHAPE.RECTANGLE)
    txt(s, 0, 0.34, SW, 1.0, "最喜欢的课", size=50, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    txt(s, 0, 1.25, SW, 0.45, "四年级 · 心理健康教育 · 第 1 课", size=19, color=GOLD, align=PP_ALIGN.CENTER)
    txt(s, 0, 6.85, SW, 0.45, "承认有不喜欢，并学会对待它", size=17, color=GRAY, align=PP_ALIGN.CENTER)


def p02(s):
    header(s, "今天我们要做的事")
    items = [
        ("① 涂星星", "给 12 门课\n涂上你心里的星"),
        ("② 看不同", "一样的课表\n每个人不一样"),
        ("③ 说理由", "喜欢和不喜欢\n都是有原因的"),
        ("④ 缺了它", "假如没有这门课\n我们会怎么样"),
        ("⑤ 走一步", "两个小行动\n带回家里去"),
        ("⑥ 说发现", "今天我最大的\n发现是……"),
    ]
    cards(s, items, M, 1.85, SW - 2 * M, 2.0, cols=3, gap=0.3)
    footer(s, "一节课 40 分钟 · 一张学习单，正面写完翻反面")


def p03(s):
    header(s, "我们班的 12 门课", sub="先看看这一学期，我们都要学些什么")
    subs = ["语文", "数学", "道德与法治", "音乐", "美术", "体育与健康",
            "信息科技", "科学", "劳动", "心理健康", "英语", "综合实践活动"]
    x0, y0 = M, 1.95
    cw, ch, gap = 2.8, 0.95, 0.28
    for i, nm in enumerate(subs):
        r, c = divmod(i, 4)
        cx = x0 + c * (cw + gap)
        cy = y0 + r * (ch + gap)
        box(s, cx, cy, cw, ch, NAVY2, line=NAVY3, lw=0.75)
        txt(s, cx, cy, cw, ch, nm, size=19, color=WHITE, align=PP_ALIGN.CENTER,
            anchor=MSO_ANCHOR.MIDDLE)
    footer(s, "每一门都在你的课表里 · 每一门都有它的位置")


def p04(s):
    # 环节一 标题页
    pass  # 底色由 sld() 全幅矩形提供
    b = box(s, SW / 2 - 0.85, 1.5, 1.7, 1.7, GOLD, shape=MSO_SHAPE.OVAL)
    txt(s, SW / 2 - 0.85, 1.5, 1.7, 1.7, "1", size=54, bold=True, color=NAVY,
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    txt(s, 0, 3.5, SW, 0.9, "我的课表星星榜", size=46, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    txt(s, 0, 4.5, SW, 0.5, "环节一 · 涂星自评（5 分钟）", size=20, color=GOLD, align=PP_ALIGN.CENTER)
    stars(s, 12, seed=11)


def p05(s):
    header(s, "怎么涂", 1, sub="打开学习单 · 正面 · 环节一")
    items = [
        ("★★★  三颗星", "最喜欢。上这门课的时候，\n时间过得特别快。"),
        ("★★   两颗星", "还不错。说不上喜欢，\n也不讨厌。"),
        ("★    一颗星", "不太喜欢。上课的时候，\n总想看窗外。"),
    ]
    cards(s, items, M, 2.0, SW - 2 * M, 2.2, cols=3, gap=0.3)
    box(s, M, 4.7, SW - 2 * M, 1.3, NAVY2, line=GOLD, lw=0.75)
    txt(s, M + 0.3, 4.85, SW - 2 * M - 0.6, 1.0,
        "涂你心里真实的星，不用看别人的。\n没有哪一颗是错的。", size=20, color=GOLD, bold=True)


def p06(s):
    header(s, "现在，开始涂吧", 1)
    pic(s, "img02", M, 1.9, 5.4, 3.6)
    box(s, M + 5.75, 1.9, SW - 2 * M - 5.75, 3.6, NAVY2, line=NAVY3, lw=0.75)
    txt(s, M + 6.0, 2.15, SW - 2 * M - 6.25, 3.2,
        "给 12 门课都涂上星星。\n\n"
        "音乐响起就开始，\n音乐停下就放下笔。\n\n"
        "不用和同桌商量，\n这是你自己的星星。", size=21, color=WHITE, spacing=1.5)
    footer(s, "教师：播放轻音乐约 3 分钟，巡视不评价、不指导")


def p07(s):
    header(s, "你涂出了什么？", 1)
    items = [
        ("看一看", "哪门课三星？\n哪门课只有一颗？"),
        ("想一想", "有没有哪一门，\n你犹豫了很久才下笔？"),
        ("比一比", "同桌之间，\n涂得一样吗？"),
    ]
    cards(s, items, M, 2.05, SW - 2 * M, 2.3, cols=3, gap=0.3)
    box(s, M, 4.85, SW - 2 * M, 1.2, NAVY2, line=GOLD, lw=0.75)
    txt(s, M + 0.3, 5.0, SW - 2 * M - 0.6, 0.9,
        "教师引导语：「谁愿意说说，你给哪门课涂了三颗星？又给哪门课只涂了一颗？」",
        size=16, color=GOLD)


def p08(s):
    pass  # 底色由 sld() 全幅矩形提供
    pic(s, "img03", SW / 2 - 3.0, 1.25, 6.0, 3.4)
    txt(s, 0, 4.85, SW, 0.9, "一样的课表，不一样的星星", size=40, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    txt(s, 0, 5.8, SW, 0.5, "环节二 · 引出主题（3 分钟）", size=19, color=GOLD, align=PP_ALIGN.CENTER)
    stars(s, 10, seed=21)


def p09(s):
    header(s, "为什么会不一样？", 2)
    items = [
        ("有人喜欢", "跑起来、唱起来、\n画出来的课"),
        ("有人喜欢", "安安静静、\n想明白一道题的课"),
        ("每个人都不同", "喜欢不一样，\n一点也不奇怪"),
    ]
    cards(s, items, M, 2.05, SW - 2 * M, 2.3, cols=3, gap=0.3)
    box(s, M, 4.85, SW - 2 * M, 1.2, NAVY2, line=GOLD, lw=0.75)
    txt(s, M + 0.3, 5.0, SW - 2 * M - 0.6, 0.9,
        "教师引导语：「同一张课表，涂出来的星星却不一样。这说明了什么？」",
        size=16, color=GOLD)


def p10(s):
    header(s, "喜欢可以说，不喜欢也可以说", 2)
    box(s, M + 1.0, 1.95, SW - 2 * M - 2.0, 3.1, CREAM)
    txt(s, M + 1.35, 2.3, SW - 2 * M - 2.7, 2.4,
        "这节课，我们不比谁更喜欢学习。\n\n"
        "不喜欢，是一种真实的感受。\n"
        "先把它说出来，我们才有可能\n"
        "好好地对待它。", size=24, color=NAVY, bold=True, spacing=1.5)
    footer(s, "教师：只停 10 秒左右，给安全感，不展开教育")


def p11(s):
    pass  # 底色由 sld() 全幅矩形提供
    pic(s, "img04", SW / 2 - 3.0, 1.25, 6.0, 3.4)
    txt(s, 0, 4.85, SW, 0.9, "喜欢，是有理由的", size=44, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    txt(s, 0, 5.8, SW, 0.5, "环节三 · 说理由（8 分钟）", size=19, color=GOLD, align=PP_ALIGN.CENTER)
    stars(s, 10, seed=31)


def p12(s):
    header(s, "喜欢的理由", 3)
    items = [
        ("有意思", "上课像在玩，\n不知不觉就下课了"),
        ("有成就感", "我做出来了，\n我真棒"),
        ("有人陪", "有好朋友一起上，\n还有老师夸我"),
        ("有用处", "学了马上能用，\n生活里真的用得上"),
    ]
    cards(s, items, M, 2.05, SW - 2 * M, 2.3, cols=4, gap=0.26)
    footer(s, "教师：把学生说出的理由，归到这四栏里板书")


def p13(s):
    header(s, "不喜欢的理由", 3)
    items = [
        ("太难了", "听不懂，\n怎么努力都跟不上"),
        ("没意思", "老师讲，\n我坐着等下课"),
        ("用不上", "长大了又用不到，\n学它干什么"),
        ("会紧张", "怕被点名，\n怕答错被笑"),
    ]
    cards(s, items, M, 2.05, SW - 2 * M, 2.3, cols=4, gap=0.26)
    footer(s, "教师：四条都写下来，尤其是「用不上」——下一页要用到它")


def p14(s):
    header(s, "在教室里，把它抓出来", 3, sub="针对那句「这门课我以后用不上」")
    pic(s, "img05", M, 1.85, 5.2, 3.5)
    box(s, M + 5.55, 1.85, SW - 2 * M - 5.55, 3.5, NAVY2, line=NAVY3, lw=0.75)
    txt(s, M + 5.85, 2.1, SW - 2 * M - 6.15, 3.1,
        "你说「美术」没用 ——\n  教室后面那块板报是谁画的？\n\n"
        "你说「数学」没用 ——\n  昨天买零食，找钱你算过没有？\n\n"
        "你说「体育」没用 ——\n  你上次生病，请了几天假？", size=17, color=WHITE, spacing=1.35)
    footer(s, "教师：不反驳，只提问 —— 让证据从他自己的生活里冒出来")


def p15(s):
    header(s, "小挑战：找一找", 3)
    box(s, M + 0.8, 1.9, SW - 2 * M - 1.6, 3.3, CREAM)
    txt(s, M + 1.2, 2.2, SW - 2 * M - 2.4, 2.7,
        "有没有哪一门课 ——\n\n"
        "你嘴上说「没用」，\n"
        "但其实天天都在用？\n\n"
        "想好了，在学习单正面写下来。", size=25, color=NAVY, bold=True, spacing=1.45)
    footer(s, "给 1 分钟 · 写在学习单正面「说理由」那一栏")


def p16(s):
    p = find_img("img06")
    if p:
        s.shapes.add_picture(p, Inches(0), Inches(0), width=Inches(SW), height=Inches(SH))
    else:
        stars(s, 12, seed=41)
    top_band(s, "假如没有这门课……", "环节四 · 高潮（12 分钟）", tsize=44, ssize=18)


def p17(s):
    header(s, "认领一门课", 4)
    box(s, M, 1.95, 5.7, 3.4, NAVY2, line=GOLD, lw=0.75)
    txt(s, M + 0.3, 2.2, 5.1, 2.9,
        "4 人小班\n\n"
        "每人认领 1 门课，\n"
        "4 个人 4 门课，\n"
        "把黑板拼成 4 块。", size=21, color=WHITE, spacing=1.4)
    box(s, M + 6.0, 1.95, SW - 2 * M - 6.0, 3.4, NAVY2, line=GOLD, lw=0.75)
    txt(s, M + 6.3, 2.2, SW - 2 * M - 6.6, 2.9,
        "30 人大班\n\n"
        "4 人一组，每组认领 1 门，\n"
        "7～8 个组拼成 7～8 块，\n"
        "看看少了哪一块。", size=21, color=WHITE, spacing=1.4)
    footer(s, "认领哪一门？就认领你星星最少的那一门 · 亲手把它从课表上拿下来，卡片留着，等会儿要贴回去")


def p18(s):
    header(s, "想一想：整整一星期没有它", 4)
    box(s, M + 1.0, 1.9, SW - 2 * M - 2.0, 1.5, CREAM)
    txt(s, M + 1.3, 2.05, SW - 2 * M - 2.6, 1.2,
        "如果整整一个星期都没有这门课，\n我们会变成什么样？", size=26, color=NAVY, bold=True,
        align=PP_ALIGN.CENTER, spacing=1.4)
    items = [
        ("体育课没了", "我们什么时候\n才能跑一跑？"),
        ("音乐课没了", "我们什么时候\n才能唱两句？"),
        ("美术课没了", "教室会不会\n少了很多颜色？"),
    ]
    cards(s, items, M, 3.75, SW - 2 * M, 1.9, cols=3, gap=0.3)
    footer(s, "教师：一个个问下去 —— 每一问都落在学生自己的日子里")


def p19(s):
    header(s, "哪些事情会变得不一样？", 4)
    box(s, M, 1.95, SW - 2 * M, 3.3, NAVY2, line=NAVY3, lw=0.75)
    txt(s, M + 0.4, 2.2, SW - 2 * M - 0.8, 2.8,
        "把小组讨论的结果，\n写在学习单反面「假如没有这门课」那一栏。\n\n"
        "写的时候想一想：\n"
        "—— 那几天，我会少了什么？\n"
        "—— 我们班会少了什么？", size=21, color=WHITE, spacing=1.45)
    footer(s, "给 4 分钟讨论 · 然后每组说一句")


def p20(s):
    header(s, "让那门课，开口说话", 4, sub="心理剧 · 角色互换 —— 你就是那门被你冷落的课")
    pic(s, "img07", M, 1.85, 5.0, 3.4)
    box(s, M + 5.35, 1.85, SW - 2 * M - 5.35, 3.4, CREAM)
    txt(s, M + 5.65, 2.1, SW - 2 * M - 5.95, 2.9,
        "现在，你就是那门课。\n\n"
        "它被你冷落了整整一年。\n\n"
        "它想对你说一句话 ——\n"
        "会是什么？", size=23, color=NAVY, bold=True, spacing=1.45)
    footer(s, "教师：写完请 3～4 人站起来说 · 不评价、不纠正，只说「谢谢你说出来」")


def p21(s):
    header(s, "它现在还在课表外面", 4)
    box(s, M + 0.9, 1.85, SW - 2 * M - 1.8, 1.9, CREAM)
    txt(s, M + 1.3, 2.05, SW - 2 * M - 2.6, 1.5,
        "既然少了一门课我们会不舒服，\n"
        "那为什么学校还要把它排进课表？\n"
        "—— 这个问题，交给你们回答。", size=22, color=NAVY, bold=True, spacing=1.4)
    box(s, M + 0.9, 4.05, SW - 2 * M - 1.8, 1.95, NAVY2, line=GOLD, lw=0.75)
    txt(s, M + 1.3, 4.25, SW - 2 * M - 2.6, 1.6,
        "刚才是你自己把它请出去的。\n"
        "现在——你还愿意让它一直留在外面吗？", size=24, color=GOLD, bold=True,
        align=PP_ALIGN.CENTER, spacing=1.4)
    footer(s, "教师：不倒数、不催；有人不贴，就说「好，那它先留在这里」")


def p22(s):
    """22+23 合并页：思政桥（严格 25–35 秒，教师只把镜头拉远，不宣布答案）"""
    header(s, "把镜头拉远一点", 4)
    # 左侧 2/3：中国
    box(s, M, 1.85, 7.3, 3.6, NAVY2, line=GOLD, lw=0.75)
    pic(s, "img08", M + 0.25, 2.05, 3.3, 2.05)
    txt(s, M + 3.75, 2.05, 3.4, 3.1,
        "中　国\n\n"
        "祖冲之 · 张衡\n"
        "袁隆平 · 屠呦呦\n"
        "北斗 · 嫦娥\n"
        "中国天眼 · 量子九章", size=16, color=WHITE, spacing=1.5)
    # 右侧 1/3：世界
    box(s, M + 7.6, 1.85, SW - 2 * M - 7.6, 3.6, NAVY2, line=GOLD, lw=0.75)
    txt(s, M + 7.9, 2.1, SW - 2 * M - 8.2, 3.1,
        "世　界\n\n"
        "气候变暖\n"
        "疾病与健康\n"
        "粮食与饥饿\n"
        "太空与海洋", size=16, color=WHITE, spacing=1.5)
    box(s, M, 5.65, SW - 2 * M, 0.85, CREAM)
    txt(s, M + 0.3, 5.72, SW - 2 * M - 0.6, 0.7,
        "老师只是把镜头拉远了。刚才那个道理，其实是你们自己先发现的。",
        size=17, color=NAVY, bold=True)
    footer(s, "严格 25–35 秒 · 教授不讲知识背景、不提问、不展开知识竞赛")


def p24(s):
    pass  # 底色由 sld() 全幅矩形提供
    pic(s, "img10", SW / 2 - 3.0, 1.25, 6.0, 3.4)
    txt(s, 0, 4.85, SW, 0.9, "我的两个小行动", size=44, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    txt(s, 0, 5.8, SW, 0.5, "环节五 · 迁移应用（7 分钟）", size=19, color=GOLD, align=PP_ALIGN.CENTER)
    stars(s, 10, seed=51)


def p25(s):
    header(s, "行动一：给不喜欢的课，想个办法", 5)
    box(s, M, 1.95, 5.7, 3.3, NAVY2, line=GOLD, lw=0.75)
    txt(s, M + 0.3, 2.2, 5.1, 2.8,
        "那门课是：《　　　》\n\n"
        "我的小办法是：\n"
        "＿＿＿＿＿＿＿＿＿＿\n"
        "＿＿＿＿＿＿＿＿＿＿\n"
        "＿＿＿＿＿＿＿＿＿＿", size=20, color=WHITE, spacing=1.5)
    box(s, M + 6.0, 1.95, SW - 2 * M - 6.0, 3.3, NAVY2, line=NAVY3, lw=0.75)
    txt(s, M + 6.3, 2.2, SW - 2 * M - 6.6, 2.8,
        "可以想的方向：\n\n"
        "· 上课前先翻一遍书\n"
        "· 给自己定一个小目标\n"
        "· 不懂的地方当天问\n"
        "· 找一个学得好的同桌", size=19, color=WHITE, spacing=1.5)
    footer(s, "写在学习单反面 · 环节五 第一块")


def p26(s):
    header(s, "行动二：给最喜欢的课，多走一步", 5)
    box(s, M, 1.95, 5.7, 3.3, NAVY2, line=GOLD, lw=0.75)
    txt(s, M + 0.3, 2.2, 5.1, 2.8,
        "那门课是：《　　　》\n\n"
        "我要多走的这一步是：\n"
        "＿＿＿＿＿＿＿＿＿＿\n"
        "＿＿＿＿＿＿＿＿＿＿\n"
        "＿＿＿＿＿＿＿＿＿＿", size=20, color=WHITE, spacing=1.5)
    box(s, M + 6.0, 1.95, SW - 2 * M - 6.0, 3.3, NAVY2, line=NAVY3, lw=0.75)
    txt(s, M + 6.3, 2.2, SW - 2 * M - 6.6, 2.8,
        "可以想的方向：\n\n"
        "· 多做一道难题\n"
        "· 找一本相关的课外书\n"
        "· 把作品做得更好一点\n"
        "· 教一教还不会的同学", size=19, color=WHITE, spacing=1.5)
    footer(s, "写在学习单反面 · 环节五 第二块")


def p27(s):
    header(s, "这些成长，有一个名字", 5)
    items = [
        ("德", "道德与法治"),
        ("智", "语文 数学 英语\n科学 信息科技"),
        ("体", "体育与健康"),
        ("美", "音乐 美术"),
        ("劳", "劳动 综合实践"),
    ]
    cards(s, items, M, 2.0, SW - 2 * M, 2.2, cols=5, gap=0.24)
    box(s, M, 4.7, SW - 2 * M, 1.35, CREAM)
    txt(s, M + 0.3, 4.9, SW - 2 * M - 0.6, 1.0,
        "每门课都好好学，是给自己打底子；\n最喜欢的那门，值得多花点时间。",
        size=22, color=NAVY, bold=True, spacing=1.4)
    footer(s, "先「全面」，再「个性」—— 顺序不能反")


def p28(s):
    pass  # 底色由 sld() 全幅矩形提供
    pic(s, "img11", SW / 2 - 3.0, 1.25, 6.0, 3.4)
    txt(s, 0, 4.85, SW, 0.9, "今天，我最大的发现", size=44, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    txt(s, 0, 5.8, SW, 0.5, "环节六 · 反馈收口（5 分钟）", size=19, color=GOLD, align=PP_ALIGN.CENTER)
    stars(s, 10, seed=61)


def p29(s):
    header(s, "写下一句话", 6)
    box(s, M + 1.2, 1.95, SW - 2 * M - 2.4, 2.6, CREAM)
    txt(s, M + 1.5, 2.25, SW - 2 * M - 3.0, 2.0,
        "今天，你对一门原来不太喜欢的课，\n有没有一点新的想法？\n\n"
        "＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿\n"
        "＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿",
        size=22, color=NAVY, bold=True, spacing=1.45)
    footer(s, "写在学习单反面最后一行 · 下课前收上来，读两句就下课")


def p30(s):
    pass  # 底色由 sld() 全幅矩形提供
    stars(s, 20, seed=71)
    txt(s, 0, 1.7, SW, 1.0, "把你的星空，点亮", size=50, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    ln = box(s, SW / 2 - 1.0, 2.95, 2.0, 0.06, GOLD)
    box(s, M + 2.0, 3.5, SW - 2 * M - 4.0, 2.3, NAVY2, line=GOLD, lw=0.75)
    txt(s, M + 2.35, 3.8, SW - 2 * M - 4.7, 1.8,
        "课后小任务\n\n"
        "1. 把「两个小行动」真的做一次\n"
        "2. 下周上课，告诉我们它有没有用\n"
        "3. 把学习单贴在自己的书桌前", size=20, color=WHITE, spacing=1.5)
    txt(s, 0, 6.35, SW, 0.5, "承认有不喜欢，并学会对待它", size=18, color=GOLD, align=PP_ALIGN.CENTER)


# 播放主流程 19 页（按镜像 Extended 审稿意见排序：由近及远，再回到自己）
PLAY = [p01, p03, p05, p07, p09, p10, p12, p13, p14, p17,
        p18, p19, p20, p21, p22, p25, p26, p27, p29]

# 备用页 10 页（课堂不播，保留为资源；可在 PowerPoint 中隐藏或删除）
HIDDEN = [p02, p04, p06, p08, p11, p15, p16, p24, p28, p30]

for fn in PLAY:
    fn(sld())

for fn in HIDDEN:
    s_ = sld()
    fn(s_)
    txt(s_, SW - M - 2.4, 0.16, 2.4, 0.34, "备用 · 可隐藏",
        size=12, color=GRAY, align=PP_ALIGN.RIGHT)

prs.save(OUT)
print("saved:", OUT, "slides:", len(prs.slides.__iter__.__self__._sldIdLst))
