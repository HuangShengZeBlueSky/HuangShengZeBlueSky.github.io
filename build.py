"""Build the public portfolio with Python's standard library."""
import json, shutil
from html import escape as e
from pathlib import Path
ROOT=Path(__file__).parent
OUT=ROOT/'dist'
data=json.loads((ROOT/'content.json').read_text())
projects=data['projects']
byid={p['id']:p for p in projects}
OUT.mkdir(exist_ok=True)
(OUT/'projects').mkdir(exist_ok=True)
shutil.copytree(ROOT/'assets',OUT/'assets',dirs_exist_ok=True)
(OUT/'.nojekyll').write_text('')
SITE='https://huangshengzebluesky.github.io'

def link(url,label,cls=''):
    return f'<a href="{e(url)}"'+(f' class="{cls}"' if cls else '')+(' target="_blank" rel="noopener noreferrer"' if url.startswith('http') else '')+f'>{e(label)}</a>'
def project_url(p,prefix=''):
    return prefix+'projects/'+p['id']+'.html'
def tags(p):
    return '<div class="tags">'+''.join(f'<span class="tag">{e(t)}</span>' for t in p['tags'])+'</div>'
def doc(title,body,prefix='',desc='黄胜泽的技术履历：Agent 评测、自进化与算法工程。',path=''):
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(title)} · 黄胜泽</title><meta name="description" content="{e(desc)}"><meta name="theme-color" content="#f7f5ef"><link rel="canonical" href="{SITE}/{path}"><meta property="og:title" content="{e(title)} · 黄胜泽"><meta property="og:description" content="{e(desc)}"><meta property="og:type" content="website"><link rel="icon" href="{prefix}assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="{prefix}assets/style.css"></head><body><header class="topbar"><nav class="shell nav" aria-label="主导航"><a class="brand" href="{prefix}index.html">黄胜泽 <small>SHENGZE HUANG</small></a><div class="nav-links"><a href="{prefix}index.html#engineering">工程</a><a href="{prefix}index.html#research">研究</a><a class="hide-mobile" href="{prefix}index.html#tools">工具</a><a class="button" href="{prefix}resume.html">完整履历 ↗</a></div></nav></header>{body}<footer class="shell footer"><span>黄胜泽 · Agent Systems &amp; Self-Evolution</span><span>更新于 2026.10 · {link('https://github.com/HuangShengZeBlueSky/HuangShengZeBlueSky.github.io','网站源码')} · {link('mailto:1641335545@qq.com','联系我')}</span></footer></body></html>'''

def row(p,i):
    return f'''<a class="project-row" href="{project_url(p)}"><span class="project-no">{i:02d}</span><div><h3>{e(p['title'])}</h3><p>{e(p['summary'])}</p>{tags(p)}</div><span class="arrow" aria-hidden="true">↗</span></a>'''
def card(p):
    links=link(project_url(p),'阅读技术说明 ↗')
    if p['links']: links+=link(p['links'][0]['url'],p['links'][0]['label'])
    return f'''<article class="research-card"><div class="card-kicker">{e(p['kicker'])}</div><h3>{link(project_url(p),p['title'])}</h3><p>{e(p['summary'])}</p><div class="card-links">{links}</div></article>'''
def section_head(index,title,sub):
    return f'<div class="section-header"><span class="section-index">{index}</span><div><h2>{title}</h2><p class="section-sub">{sub}</p></div></div>'

internships=[p for p in projects if p['category']=='internship']
research=[byid[k] for k in ['robowm-bench','rewardweaver','multi-agent-benchmark','autope','flyreview']]
tools=[p for p in projects if p['category']=='tool']
body='''<main class="shell"><section class="hero"><div><p class="eyebrow">Research Notes / Engineering Portfolio</p><h1>让智能体从执行任务，<br>走向<em>持续进化。</em></h1><p class="intro">我关注大语言模型智能体的评测、反馈与自进化：从真实业务中的一次失败出发，找到可修改的能力与组件，再用可重复的实验检验改进。</p><p class="identity">黄胜泽 · 清华大学数学与人工智能硕士研究生<span>元理智能 · AutoHarness 算法负责实习生 · 2026.01—2026.10</span></p><div class="linkline"><a href="#engineering">阅读工程专题 ↓</a><a href="https://github.com/HuangShengZeBlueSky" target="_blank" rel="noopener noreferrer">GitHub ↗</a><a href="mailto:1641335545@qq.com">Email ↗</a></div></div><figure class="research-figure" aria-label="评测、归因、优化及复验构成智能体持续改进闭环"><div class="figure-label"><span>THE IMPROVEMENT LOOP</span><span>FIG. 01</span></div><div class="loop-item"><span class="loop-number">01</span><div class="loop-text"><strong>评测 · 看见真实行为</strong><span>业务环境 / 完整轨迹 / 多层指标</span></div></div><div class="loop-item"><span class="loop-number">02</span><div class="loop-text"><strong>归因 · 定位能力瓶颈</strong><span>失败分析 / 机制聚类 / 修改面选择</span></div></div><div class="loop-item"><span class="loop-number">03</span><div class="loop-text"><strong>优化 · 交付可运行的改进</strong><span>提示词 / Harness 插件 / 训练奖励</span></div></div><figcaption class="figure-note">↳ 回到相同任务与指标，验证下一轮改进。</figcaption></figure></section><div class="ribbon"><div><small>RESEARCH</small><b>RoboWM-Bench · CVPR Workshops 2026</b></div><div><small>RECOGNITION</small><b>State of AI Report 2026 收录</b></div><div><small>ENGINEERING</small><b>Agent 评测 · AutoHarness · 自进化</b></div></div>'''
body+='<section id="engineering" class="section">'+section_head('01 / ENGINEERING','从业务现场到自进化系统','元理智能实习专题。将环境、测评、优化与持续实验组织成一条完整的工程链路。')+'<div class="section-body">'
body+='''<div class="feature-head"><h3>元理智能</h3><div class="meta">AutoHarness 算法负责实习生<br>2026.01—2026.10 · 北京</div></div><p class="feature-lead">从医疗体检预约的提示词演化，到金融债务协商的沙箱和测评，再扩展到可修改运行组件的 AutoHarness。关注的不只是一次对话能否成功，也包括失败能否被复现、解释，并转化为可交付的系统改进。</p><div class="pipeline" aria-label="业务智能体研发链路"><div>业务场景<small>医疗 / 金融</small></div><div>实验环境<small>本地沙箱</small></div><div>分层测评<small>单轮 / 会话 / 结果</small></div><div>优化闭环<small>归因 / 候选 / 复验</small></div><div>持续运行<small>看板 / Skill</small></div></div>'''
body+=''.join(row(p,i+1) for i,p in enumerate(internships))
body+='''<div class="result-note"><b>29.73% → 60.81%</b> · DSH 插件受控实验中的任务成功率<small>Telecom 训练集 74 个任务，每任务 3 次，共 222 次评测；提示词与工具结果插件组合带来 31.08 个百分点提升。此处为训练集实验，未宣称留出测试或真实业务收益。</small></div></div></section>'''
body+='<section id="research" class="section">'+section_head('02 / RESEARCH','研究参与与技术项目','评测让问题可见，反馈决定下一步优化什么。保留与这条主线直接相关的论文和项目。')+'<div class="section-body research-grid">'+''.join(card(p) for p in research)+'</div></section>'
body+='<section id="tools" class="section">'+section_head('03 / TOOLS','把同一思路，带回人的工作','一端是持续改进的教育内容，一端是持续保存的工作意图。')+'<div class="section-body tool-grid">'
for i,p in enumerate(tools):
    flow='知识 → 出题 → 多路求解 → 审核 → 学习反馈 → 修订' if i==0 else '人的原始输入 → 工作主线 → 专注会话 → 回看与复盘'
    body+=f'<article class="tool-card"><div class="card-kicker">{e(p["kicker"])}</div><h3>{e(p["title"])}</h3><p>{e(p["summary"])}</p><div class="card-links">{link(project_url(p),"阅读产品与技术说明 ↗")}</div><div class="mini-flow">{flow}</div></article>'
body+='</div></section>'
body+='<section id="background" class="section">'+section_head('04 / BACKGROUND','教育与早期经历','从人工智能研究到工业知识与业务系统，持续积累模型、数据和工程之间的连接能力。')+'<div class="section-body"><div class="timeline">'
for date,title,desc in [
('2025.09—2028.06','清华大学 · 硕士研究生','数学与人工智能 · 预计 2028 年 6 月毕业'),
('2021.09—2025.06','北京航空航天大学 · 工学学士','人工智能 · 平均绩点 3.72 / 4.0'),
('2025.09—2026.01','中车数研院 · 智能体实习生','工业知识库与 Agentic RAG、多模型部署、工业智能体和时序异常检测。'),
('2024.07—2024.09','中电太极计算机研究所 · 自然语言处理研究实习生','光学字符识别与大语言模型结合的文档信息抽取流水线。')]:
    body+=f'<div class="timeline-row"><span class="timeline-time">{date}</span><div><h3>{title}</h3><p>{desc}</p></div></div>'
body+='''</div><p class="skills"><b>技术方向</b>　智能体评测、提示词演化、强化学习、自动科研、实验基础设施<br><b>工程栈</b>　Python、SQL、TypeScript、PyTorch、Pydantic、FastAPI、SQLite、Docker、Git</p><div class="linkline"><a href="resume.html">查看完整技术履历 ↗</a><a href="resume.pdf">下载 LaTeX 版简历 PDF ↓</a></div></div></section></main>'''
(OUT/'index.html').write_text(doc('智能体评测与自进化',body),encoding='utf-8')

for p in projects:
    contents=''
    aside=''
    for i,s in enumerate(p['sections']):
        sid=f'section-{i+1}'
        aside+=f'<a href="#{sid}">{e(s["heading"])}</a>'
        contents+=f'<section id="{sid}"><h2>{e(s["heading"])}</h2>'
        contents+=''.join(f'<p>{e(t)}</p>' for t in s.get('paragraphs',[]))
        if s.get('bullets'): contents+='<ul>'+''.join(f'<li>{e(t)}</li>' for t in s['bullets'])+'</ul>'
        contents+='</section>'
    if p['links']: contents+='<div class="sources"><strong>延伸阅读</strong>'+''.join(link(x['url'],x['label']+' ↗') for x in p['links'])+'</div>'
    body=f'''<main class="article-shell"><header class="article-header"><a class="back" href="../index.html#{'engineering' if p['category']=='internship' else 'research' if p['category']=='research' else 'tools'}">← 返回专题索引</a><p class="eyebrow">{e(p['kicker'])}</p><h1>{e(p['title'])}</h1><p class="abstract">{e(p['summary'])}</p>{tags(p)}<p class="section-sub">{e(p['role'])}</p></header><div class="article-body"><aside class="article-aside" aria-label="本页目录">{aside}</aside><article class="article-content">{contents}</article></div></main>'''
    (OUT/'projects'/f'{p["id"]}.html').write_text(doc(p['title'],body,'../',p['summary'],'projects/'+p['id']+'.html'),encoding='utf-8')

resume='''<div class="resume-actions"><a href="index.html">← 返回技术网站</a><div><a href="resume.pdf">下载 PDF ↓</a>　<button onclick="window.print()">打印 / 另存为 PDF</button></div></div><main class="resume-sheet"><h1>黄胜泽</h1><p class="resume-contact">北京 · 1641335545@qq.com · github.com/HuangShengZeBlueSky<br>智能体评测与自进化 · 算法研究与工程</p><h2>教育背景</h2><h3>清华大学 · 数学与人工智能硕士研究生<span class="date">2025.09—2028.06（预计）</span></h3><h3>北京航空航天大学 · 人工智能工学学士<span class="date">2021.09—2025.06</span></h3><p>平均绩点：3.72 / 4.0</p><h2>重点实习经历</h2><h3>元理智能 · AutoHarness 算法负责实习生<span class="date">2026.01—2026.10</span></h3>'''
for p in [byid[k] for k in ['autoharness','workbench','evaluation','finance-sandbox','medical-autope']]:
    resume+=f'<div class="no-break"><h3>{e(p["title"])}</h3><ul>'+''.join(f'<li>{e(s)}</li>' for s in p['resume'])+'</ul></div>'
resume+='<h2>研究参与与技术项目</h2>'
for p in research:
    resume+=f'<div class="no-break"><h3>{e(p["title"])}</h3><p>{e(p["role"])}</p><ul>'+''.join(f'<li>{e(s)}</li>' for s in p['resume'])+'</ul></div>'
resume+='<h2>人工智能提效工具</h2>'
for p in tools:
    resume+=f'<div class="no-break"><h3>{e(p["title"])}</h3><ul>'+''.join(f'<li>{e(s)}</li>' for s in p['resume'])+'</ul></div>'
resume+='''<h2>其他实习经历</h2><div class="no-break"><h3>中车数研院 · 智能体实习生<span class="date">2025.09—2026.01</span></h3><ul><li>推进工业知识库的 Agentic RAG 链路，整合文档识别、对话、向量表示与重排序，结合 Qwen2.5-VL、实体焦点抽取和混合检索支持工业文档问答。</li><li>参与 OpenAgent 工业智能体与 OpenLTM 时序检测系统，实现系统提示分层路由、Xinference 多模型部署及基于 AutoTimes 的时序异常检测实验。</li></ul></div><div class="no-break"><h3>中电太极计算机研究所 · 自然语言处理研究实习生<span class="date">2024.07—2024.09</span></h3><ul><li>构建文档识别与大语言模型结合的信息抽取流水线，使用开源模型、分步推理和规则后处理，支持 PDF 关键信息结构化抽取。</li></ul></div><h2>专业技能</h2><p>编程与工程：Python、C/C++、SQL、TypeScript、React、Vite、Linux、Git、Docker。<br>模型与系统：PyTorch、Hugging Face、vLLM、Xinference、Pydantic、FastAPI、SQLite、Neo4j。<br>研究与实践：大语言模型智能体、提示词优化、多智能体系统、强化学习、检索增强生成、基准设计、失败归因、实验工作流。</p></main>'''
(OUT/'resume.html').write_text(doc('完整技术履历',resume,path='resume.html'),encoding='utf-8')
if (ROOT/'resume.pdf').exists(): shutil.copy2(ROOT/'resume.pdf',OUT/'resume.pdf')
(OUT/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+SITE+'/sitemap.xml\n')
urls=['','resume.html']+['projects/'+p['id']+'.html' for p in projects]
(OUT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+SITE+'/'+u+'</loc></url>' for u in urls)+'</urlset>')
print(f'Built {len(projects)} project reports, homepage and full resume in dist/')
