#!/usr/bin/env python3
"""Build the complete three-page resume from the personal site's content source."""
from pathlib import Path
from html import escape
import json

from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / 'content.json'
OUTPUT = ROOT / 'resume.pdf'
W, H = A4
LEFT, RIGHT, TOP, BOTTOM = 45, 45, 45, 42
WIDTH = W - LEFT - RIGHT
INK = HexColor('#192A32')
TEAL = HexColor('#126A68')
GRAY = HexColor('#53636B')
LIGHT = HexColor('#CEDBDC')

if Path('/System/Library/Fonts/STHeiti Light.ttc').exists():
    pdfmetrics.registerFont(TTFont('ResumeCN', '/System/Library/Fonts/STHeiti Light.ttc', subfontIndex=0))
    pdfmetrics.registerFont(TTFont('ResumeCN-Bold', '/System/Library/Fonts/STHeiti Medium.ttc', subfontIndex=0))
else:
    from reportlab.pdfbase.cidfonts import UnicodeCIDFont
    pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
    for name in ['ResumeCN', 'ResumeCN-Bold']:
        font = UnicodeCIDFont('STSong-Light')
        font.fontName = name
        pdfmetrics.registerFont(font)
pdfmetrics.registerFontFamily('ResumeCN', normal='ResumeCN', bold='ResumeCN-Bold')

STYLES = {
    'body': ParagraphStyle('body', fontName='ResumeCN', fontSize=10.5, leading=16.6,
                           textColor=INK, wordWrap='CJK', spaceAfter=0),
    'small': ParagraphStyle('small', fontName='ResumeCN', fontSize=9.1, leading=13.7,
                            textColor=GRAY, wordWrap='CJK'),
    'title': ParagraphStyle('title', fontName='ResumeCN-Bold', fontSize=12.1, leading=18.4,
                            textColor=INK, wordWrap='CJK'),
    'section': ParagraphStyle('section', fontName='ResumeCN-Bold', fontSize=14, leading=20,
                              textColor=TEAL, wordWrap='CJK'),
}

def clean(value):
    return str(value).replace('**', '').replace('｜', ' | ').replace('世界模型基准综述', '基准综述')

class Resume:
    def __init__(self):
        self.canvas = Canvas(str(OUTPUT), pagesize=A4)
        self.canvas.setTitle('黄胜泽 | 技术履历完整版')
        self.canvas.setAuthor('黄胜泽')
        self.page = 0
        self.y = H - TOP
        self.bottoms = []

    def p(self, text, style='body', indent=0, after=0):
        p = Paragraph(escape(clean(text)), STYLES[style])
        _, height = p.wrap(WIDTH - indent, 1000)
        if self.y - height < BOTTOM + 9:
            raise RuntimeError(f'Page {self.page}: content exceeds available space at {text[:45]}')
        p.drawOn(self.canvas, LEFT + indent, self.y - height)
        self.y -= height + after

    def bullet(self, text):
        self.canvas.setFillColor(TEAL)
        self.canvas.circle(LEFT + 3, self.y - 6.8, 1.3, fill=1, stroke=0)
        self.p(text, indent=13, after=4)

    def section(self, title, gap=12):
        self.y -= gap
        self.p(title, 'section', after=5)
        self.canvas.setStrokeColor(LIGHT)
        self.canvas.setLineWidth(0.6)
        self.canvas.line(LEFT, self.y, W-RIGHT, self.y)
        self.y -= 11

    def block(self, title, bullets, meta=None, gap=9):
        self.p(title, 'title', after=3)
        if meta:
            self.p(meta, 'small', after=5)
        for item in bullets:
            self.bullet(item)
        self.y -= gap

    def new_page(self, label):
        if self.page:
            self.finish_page()
            self.canvas.showPage()
        self.page += 1
        self.y = H - TOP
        if self.page > 1:
            self.canvas.setFillColor(INK)
            self.canvas.setFont('ResumeCN-Bold', 17)
            self.canvas.drawString(LEFT, self.y - 17, '黄胜泽')
            self.canvas.setFillColor(GRAY)
            self.canvas.setFont('ResumeCN', 9)
            self.canvas.drawRightString(W-RIGHT, self.y - 13, label)
            self.y -= 33

    def finish_page(self):
        self.bottoms.append(round(self.y, 1))
        c = self.canvas
        c.setStrokeColor(LIGHT)
        c.setLineWidth(0.5)
        c.line(LEFT, 35, W-RIGHT, 35)
        c.setFillColor(GRAY)
        c.setFont('ResumeCN', 8)
        c.drawString(LEFT, 23, '黄胜泽 · 技术履历完整版 · 2026.10')
        c.drawRightString(W-RIGHT, 23, f'{self.page} / 3')

    def save(self):
        self.finish_page()
        self.canvas.save()
        print(json.dumps({'output': str(OUTPUT), 'pages': self.page,
                          'content_bottom_points': self.bottoms}, ensure_ascii=False))

def main():
    data = json.loads(CONTENT.read_text())
    # Project bindings are kept here so the PDF shares the site's reviewed prose.
    projects = data['projects']
    by_id = {p['id']: p for p in projects}
    r = Resume()
    r.new_page('智能体自进化与行业实践')
    c = r.canvas
    c.setFont('ResumeCN-Bold', 27)
    c.setFillColor(INK)
    c.drawString(LEFT, r.y-27, '黄胜泽')
    c.setFont('ResumeCN', 10)
    c.setFillColor(TEAL)
    c.drawRightString(W-RIGHT, r.y-22, '智能体自进化 · 自动科研 · 评测与仿真')
    r.y -= 41
    r.p('北京 | 1641335545@qq.com | github.com/HuangShengZeBlueSky', 'small', after=3)
    r.section('教育背景', gap=7)
    r.p('清华大学 | 数学与人工智能 硕士研究生', 'title', after=1)
    r.p('2025.09 - 2028.06（预计）', 'small', after=7)
    r.p('北京航空航天大学 | 人工智能 工学学士', 'title', after=1)
    r.p('2021.09 - 2025.06 | 平均绩点：3.72 / 4.0', 'small', after=1)
    r.section('元理智能 · 实习经历', gap=10)
    r.p('AutoHarness 算法负责实习生 | 北京 | 2026.01 - 2026.10', 'title', after=9)
    for key in ['medical-autope', 'finance-sandbox', 'evaluation', 'autoharness', 'workbench']:
        p = by_id[key]
        r.block(p['title'], p['resume'], gap=7)

    r.new_page('科研、论文与开放研究')
    r.section('科研与研究项目', gap=1)
    for key in ['multi-agent-benchmark', 'autope', 'flyreview', 'robowm-bench', 'rewardweaver']:
        p = by_id[key]
        r.block(p['title'], p['resume'], meta=p.get('kicker'), gap=14)

    r.new_page('人工智能提效工具与工程积累')
    r.section('人工智能提效工具', gap=1)
    for key in ['educate-flywheel', 'echo']:
        p = by_id[key]
        r.block(p['title'], p['resume'], meta=p.get('kicker'), gap=11)

    r.section('过往实习经历', gap=7)
    r.block('中车数研院 | 智能体实习生', [
        '推进 Agentic RAG 工业知识库，打通文字识别、对话、向量表示与重排序链路，结合 Qwen2.5-VL、实体焦点抽取和混合检索，支持工业文档解析与问答。',
        '参与 OpenAgent 工业智能体及 OpenLTM 时序检测系统，实现基于 XML 系统提示词的分层路由、Xinference 多模型部署，并开展基于 AutoTimes 的时序异常检测实验。',
    ], meta='北京 | 2025.09 - 2026.01', gap=8)
    r.block('中电太极计算机研究所 | 自然语言处理研究实习生', [
        '构建文字识别与大语言模型结合的端到端信息抽取流水线，通过开源模型、思维链和规则后处理，支持 PDF 文档关键信息抽取。',
    ], meta='北京 | 2024.07 - 2024.09', gap=8)

    r.section('专业技能', gap=4)
    r.p('编程与数据：Python、C/C++、SQL、TypeScript、React、Vite。', after=5)
    r.p('模型与应用：PyTorch、Hugging Face、LangChain、Pydantic AI、DeepSeek Harness、vLLM、Xinference、FastAPI。', after=5)
    r.p('研究方向：大语言模型智能体、多智能体协作、提示词自动演化、强化学习、检索增强生成、评测基准与自动科研。', after=5)
    r.p('工程实践：Linux、Git、Docker、Neo4j；沙箱迁移、轨迹记录、失败归因、实验设计、状态机工作流及进度可视化。')
    r.save()

if __name__ == '__main__':
    main()
