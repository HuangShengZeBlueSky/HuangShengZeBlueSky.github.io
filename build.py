"""Build the maintained research portfolio from structured, reviewable content."""
import json, re, shutil, math
from html import escape as e
from pathlib import Path
ROOT=Path(__file__).parent;OUT=ROOT/'dist';SITE='https://huangshengzebluesky.github.io'
data=json.loads((ROOT/'content.json').read_text());projects=data['projects'];byid={p['id']:p for p in projects}
presentation=json.loads((ROOT/'presentation.json').read_text())
open_source=json.loads((ROOT/'open-source.json').read_text())
OUT.mkdir(exist_ok=True);(OUT/'projects').mkdir(exist_ok=True)
shutil.copytree(ROOT/'assets',OUT/'assets',dirs_exist_ok=True);(OUT/'.nojekyll').write_text('')
def link(url,label,cls=''):
 return f'<a href="{e(url)}" class="{cls}"'+(' target="_blank" rel="noopener noreferrer"' if url.startswith('http') else '')+f'>{e(label)}</a>'
def inline(text):
 out='';pos=0
 for m in re.finditer(r'\[([^\]]+)\]\((https?://[^\s)]+)\)',text):out+=e(text[pos:m.start()])+link(m[2],m[1]);pos=m.end()
 return out+e(text[pos:])
def project_url(p,prefix=''):return prefix+'projects/'+p['id']+'.html'
def tags(p):return '<div class="tags">'+''.join('<span>'+e(t)+'</span>' for t in p['tags'])+'</div>'
def doc(title,body,prefix='',desc='黄胜泽的研究与工程：智能体评测、自进化与人机协作。',path=''):
 return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(title)} · 黄胜泽</title><meta name="description" content="{e(desc)}"><meta name="theme-color" content="#f7f6f2"><link rel="canonical" href="{SITE}/{path}"><meta property="og:title" content="{e(title)} · 黄胜泽"><meta property="og:description" content="{e(desc)}"><meta property="og:type" content="website"><link rel="icon" href="{prefix}assets/favicon.svg"><link rel="stylesheet" href="{prefix}assets/style.css"></head><body><a class="skip" href="#main">跳到正文</a><header class="topbar"><nav class="shell nav" aria-label="主导航"><a class="brand" href="{prefix}index.html"><span class="monogram">H.</span><span>黄胜泽<small>SHENGZE HUANG</small></span></a><div class="nav-links"><a href="{prefix}index.html#selected">代表作</a><a href="{prefix}index.html#open-source">开源项目</a><a class="hide-mobile" href="{prefix}learn.html">专题索引</a><a class="hide-mobile" href="{prefix}index.html#about">关于</a><a class="nav-resume" href="{prefix}resume.html">简历 <span>↗</span></a></div></nav></header>{body}<footer class="shell footer"><div><strong>持续实验，持续理解。</strong><p>黄胜泽 · 智能体评测与自进化</p></div><div><a href="mailto:1641335545@qq.com">Email ↗</a><a href="https://github.com/HuangShengZeBlueSky">GitHub ↗</a><a href="{prefix}resume.pdf">简历 PDF ↓</a><small>更新于 2026.10 · <a href="https://github.com/HuangShengZeBlueSky/HuangShengZeBlueSky.github.io">网站源码</a></small></div></footer><script src="{prefix}assets/site.js" defer></script></body></html>'''
def node(x,y,w,h,title,sub='',active=False):
 return f'<g><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5" class="node {"node-active" if active else ""}"/><text x="{x+w/2}" y="{y+h/2-(7 if sub else -5)}" text-anchor="middle" class="node-title {"light" if active else ""}">{e(title)}</text>'+(f'<text x="{x+w/2}" y="{y+h/2+17}" text-anchor="middle" class="node-sub {"light" if active else ""}">{e(sub)}</text>' if sub else '')+'</g>'
def edge(path,id):return f'<path d="{path}" class="edge" marker-end="url(#{id})"/>'
def diagram(key,compact=False):
 v=presentation[key];kind=v['kind'];aid='arrow-'+key+('-small' if compact else '')
 s=f'<svg class="architecture" viewBox="0 0 800 370" role="img" aria-label="{e(v["short"])}机制图"><defs><marker id="{aid}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs><text x="30" y="29" class="svg-label">SYSTEM / {e(key.upper())}</text>'
 if kind=='grid':
  for i,t in enumerate(['描述','校验','结果处理','技能','记忆']):s+=f'<text x="{215+i*116}" y="85" text-anchor="middle" class="node-sub">{t}</text>'
  for row,t in enumerate(['智能体','业务工具','会话状态']):
   s+=f'<text x="100" y="{137+row*75}" text-anchor="middle" class="node-title">{t}</text>'
   for col in range(5):
    active=(row,col) in [(0,0),(1,1),(1,2),(2,4)]
    s+=node(164+col*116,105+row*75,102,55,'方法' if active else '·','',active)
  s+='<text x="400" y="350" text-anchor="middle" class="node-sub">对象 × 修改面 → 方法选择 → 可执行插件组合</text>'
 elif kind=='layers':
  for i,(a,b) in enumerate([('01 单轮执行','路由 · 工具调用 · 回复一致性'),('02 会话策略','技巧 · 节奏 · 多轮一致性'),('03 业务终态','和解 · 提交 · 签约')]):s+=node(80,60+i*93,640,73,a,b,i==2)
 elif kind=='lanes':
  s+=edge('M 130 122 V 157',aid)+edge('M 380 215 V 256',aid)+edge('M 380 235 H 503 V 250',aid)+edge('M 248 187 H 295',aid)+edge('M 465 187 H 520',aid)+edge('M 610 218 V 256',aid)
  s+=node(45,60,210,60,'智能体 / 技能路由','保持原有调用方式')+node(45,157,205,60,'13 个本地业务工具','Python · 参数模型',True)+node(295,157,170,60,'状态转换','预览 / 提交 / 合同')+node(520,157,230,60,'轨迹记录','模型 · 工具 · 状态差异')
  s+=node(270,256,142,60,'业务库','业务事实')+node(432,256,142,60,'记忆库','会话状态')+node(594,256,142,60,'历史库','保留记录')
  s+='<text x="500" y="94" text-anchor="middle" class="node-sub">可重置的业务状态，可追溯的运行历史</text>'
 elif kind=='branch':
  a,b=('人手操作视频','机器人操作视频') if key=='robowm-bench' else ('MPE 环境','Football 环境')
  middle,sub=('动作恢复','重定向 / 逆动力学') if key=='robowm-bench' else ('模型—环境接口','语义观测 / 结构化动作')
  s+=edge('M 222 115 H 260 V 182 H 292',aid)+edge('M 222 250 H 260 V 182',aid)+edge('M 508 182 H 555',aid)+edge('M 660 217 V 269',aid)
  s+=node(32,80,190,70,a)+node(32,215,190,70,b)+node(292,146,216,72,middle,sub,True)+node(555,146,210,72,'环境执行','动作、接触与任务状态')+node(555,269,210,65,'结果与轨迹','成功判定 / 过程解释')
 elif kind=='binding':
  for i,t in enumerate(['一句原始想法','项目中的问题','后续补充输入']):s+=node(35,67+i*90,175,55,t)+edge(f'M 210 {95+i*90} H 255 V 185 H 294',aid)
  s+=node(294,148,205,76,'工作主线','正在专注的那件事',True)+edge('M 499 185 H 559',aid)+node(559,148,205,76,'专注会话','持续接收相关输入')+edge('M 661 224 V 282 H 500',aid)+node(293,267,207,60,'回看与复盘','原文 + 回答 + 摘要版本')
 elif kind=='lineage':
  s+=node(45,145,165,66,'固定父版本','条件与完整配置')+edge('M 210 178 H 260 V 105 H 295',aid)+edge('M 260 178 V 256 H 295',aid)
  s+=node(295,73,185,65,'候选 A','假设与修改')+node(295,224,185,65,'候选 B','独立对照')+edge('M 480 105 H 520 V 178 H 580',aid)+edge('M 480 256 H 520 V 178',aid)+node(580,145,175,66,'评测与决定','晋升 / 保留父版',True)
  s+='<text x="400" y="340" text-anchor="middle" class="node-sub">产物交接 · 版本关系 · 逐案例比较</text>'
 else:
  titles=[x['title'] for x in v['steps']];coords=[(55,65),(500,65),(500,230),(55,230)]
  for path in ['M 290 103 H 494','M 617 141 V 224','M 500 268 H 296','M 172 230 V 147']:s+=edge(path,aid)
  for i,(x,y) in enumerate(coords):s+=node(x,y,235,76,f'0{i+1} {titles[i]}','',i==2)
  s+='<text x="395" y="189" text-anchor="middle" class="cycle-center">反馈 → 下一轮</text>'
 return s+'</svg>'
def explorer(p):
 v=presentation[p['id']];s=f'<figure class="method-figure"><div class="figure-top"><span>机制图解</span><span>点击步骤，阅读具体含义 ↓</span></div><div class="diagram-scroll">{diagram(p["id"])}</div><div class="step-explorer"><div class="step-buttons" role="group" aria-label="选择机制步骤">'
 for i,x in enumerate(v['steps']):s+=f'<button data-step="{i}" aria-pressed="{str(i==0).lower()}"><span>0{i+1}</span>{e(x["title"])}</button>'
 s+='</div>'
 for i,x in enumerate(v['steps']):s+=f'<div class="step-detail" data-panel="{i}"'+(' hidden' if i else '')+f'><strong>{e(x["title"])}</strong><p>{e(x["body"])}</p></div>'
 return s+'</div><figcaption>依据项目机制重绘的解释图；不代表实时运行界面。</figcaption></figure>'
def catalog_item(p,i):
 v=presentation[p['id']];category={'internship':'engineering','research':'research','tool':'tools'}.get(p['category'],'research')
 if p['id'] in ['multi-agent-benchmark','autope','flyreview']:category='research'
 return f'<a class="catalog-item" data-category="{category}" data-search="{e(p["title"]+" "+p["summary"])}" href="projects/{p["id"]}.html"><span class="item-index">{i:02d}</span><div><span class="item-label">{e(p["kicker"])}</span><h3>{e(v["short"])}</h3><p>{e(v["question"])}</p></div><span class="item-arrow">↗</span></a>'
def render_section(section):
 s=''.join(f'<p>{inline(t)}</p>' for t in section.get('paragraphs',[]))
 if section.get('flow'):s+='<ol class="technical-flow">'+''.join(f'<li><span>{i+1:02d}</span><strong>{e(x["title"])}</strong><p>{e(x["body"])}</p></li>' for i,x in enumerate(section['flow']))+'</ol>'
 if section.get('formula'):s+=f'<div class="formula">{e(section["formula"])}</div>'
 if section.get('table'):
  t=section['table'];s+='<div class="table-scroll" role="region" aria-label="数据与设计对照" tabindex="0"><table><thead><tr>'+''.join('<th>'+e(str(x))+'</th>' for x in t['headers'])+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+e(str(x))+'</td>' for x in r)+'</tr>' for r in t['rows'])+'</tbody></table></div>'
 if section.get('bullets'):s+='<ul>'+''.join('<li>'+inline(t)+'</li>' for t in section['bullets'])+'</ul>'
 if section.get('code'):
  code=section['code'];s+='<div class="code-block"><div>'+e(code['language'])+'</div><pre><code>'+e(code['text'])+'</code></pre></div>'
 if section.get('callout'):
  x=section['callout'];s+='<aside class="callout"><strong>'+e(x['label'])+'</strong><p>'+inline(x['text'])+'</p></aside>'
 return s
# Homepage
body='''<main id="main"><section class="shell hero"><div class="hero-copy"><p class="eyebrow"><span class="status-dot"></span> RESEARCH & ENGINEERING / BEIJING</p><h1>黄胜泽<span>Shengze Huang</span></h1><p class="hero-thesis">理解智能体的行为，<br>构建能够持续改进的系统。</p><p class="hero-bio">清华大学数学与人工智能硕士研究生。<br>在元理智能负责 AutoHarness 算法与实验链路，研究评测、失败归因和运行组件优化。</p><div class="hero-links"><a class="button-primary" href="#selected">探索代表作 <span>↓</span></a><a href="#open-source">浏览开源项目 ↓</a><a href="resume.pdf">下载简历 ↗</a><a href="https://github.com/HuangShengZeBlueSky">GitHub ↗</a></div></div><div class="hero-map"><div class="figure-top"><span>MY RESEARCH QUESTION</span><span>01 — 03</span></div><h2>失败之后，<br>系统改变什么？</h2><div class="hero-object-tabs" role="group" aria-label="选择优化对象"><button data-object="prompt" aria-pressed="true">提示词</button><button data-object="harness" aria-pressed="false">运行组件</button><button data-object="reward" aria-pressed="false">训练奖励</button></div><div class="hero-object" data-object-panel="prompt"><span class="object-code">AutoPE</span><p>从阶段反馈中选择局部策略，<br>改写下一轮对话的提示词。</p><div class="object-track"><span>交互</span><i>→</i><span>反馈</span><i>→</i><b>策略更新</b></div><a href="projects/medical-autope.html">进入医疗预约案例 ↗</a></div><div class="hero-object" data-object-panel="harness" hidden><span class="object-code">AutoHarness</span><p>定位失败机制，选择工具、记忆<br>或执行约束中的具体修改面。</p><div class="object-track"><span>轨迹</span><i>→</i><span>归因</span><i>→</i><b>组件装配</b></div><a href="projects/autoharness.html">探索方法与插件 ↗</a></div><div class="hero-object" data-object-panel="reward" hidden><span class="object-code">RewardWeaver</span><p>从当前能力瓶颈选择过程奖励，<br>影响下一阶段强化学习。</p><div class="object-track"><span>瓶颈</span><i>→</i><span>奖励</span><i>→</i><b>参数训练</b></div><a href="projects/rewardweaver.html">阅读论文机制 ↗</a></div><p class="map-note">三个不同的优化对象，同一条反馈研究主线。</p></div></section><div class="shell credentials"><span>清华大学 <small>数学与人工智能</small></span><span>CVPR Workshops 2026 <small>RoboWM-Bench</small></span><span>State of AI Report 2026 <small>基准综述收录</small></span></div>'''
body+='<section id="selected" class="shell home-section"><div class="section-heading"><div><p class="eyebrow">SELECTED WORK / 01</p><h2>研究问题，落在系统里。</h2></div><p>从可重复的业务实验，到模型能力的评价。<br>每项工作都有方法、实现和结果边界。</p></div><div class="selected-grid">'
for key,tag,desc in [('autoharness','ENGINEERING / 元理智能','从“改提示词”扩展到“改运行组件”。逐例归因、方法级插件与受控回归，最终交付一个可运行的 Harness。'),('robowm-bench','RESEARCH / 共同作者','让生成视频进入机器人仿真，以真正的任务执行检验世界模型。')]:
 body+=f'<a class="selected-work" href="projects/{key}.html"><div class="selected-art">{diagram(key,True)}</div><div class="selected-copy"><span class="eyebrow">{tag}</span><h3>{presentation[key]["short"]}<span>↗</span></h3><p>{desc}</p><span class="read-link">阅读机制、实现与实验</span></div></a>'
body+='</div><div class="experiment-strip"><div><span class="eyebrow">CONTROLLED EXPERIMENT</span><strong>29.73% <i>→</i> 60.81%</strong><span>Telecom 训练集任务成功率</span></div><p>固定模型、任务、预算与评分器，比较提示词和工具结果插件组合。74 个任务，每题 3 次，共 222 次评测；增加 31.08 个百分点。</p><a href="projects/autoharness.html">如何得到这个结果 ↗</a></div></section>'
body+='''<section class="shell home-section"><div class="section-heading"><div><p class="eyebrow">RESEARCH / 02</p><h2>论文与研究参与</h2></div><a class="text-link" href="learn.html?filter=research">查看研究专题 ↗</a></div><div class="publication-list">'''
for key,date,role in [('robowm-bench','2026.05','共同作者 · CVPR Workshops'),('rewardweaver','2026.10','研究参与 · 公开预印本')]:
 v=presentation[key];body+=f'<a class="publication" href="projects/{key}.html"><span class="pub-date">{date}</span><div><span class="item-label">{role}</span><h3>{v["short"]}</h3><p>{e(v["question"])}</p></div><span class="pub-link">精读笔记 ↗</span></a>'
body+='</div></section>'
body+='''<section id="engineering" class="shell home-section"><div class="section-heading"><div><p class="eyebrow">TECHNICAL ATLAS / 03</p><h2>把整条链路讲清楚。</h2></div><p>环境、测评、优化与持续实验。<br>选择一个问题，进入完整的技术专题。</p></div>'''
body+='<div class="catalog" data-catalog><div class="catalog-controls"><div class="filter-buttons" role="group" aria-label="专题分类"><button data-filter="all" aria-pressed="true">全部专题 <small>12</small></button><button data-filter="engineering" aria-pressed="false">场景与系统</button><button data-filter="research" aria-pressed="false">研究方法</button><button data-filter="tools" aria-pressed="false">个人工具</button></div><label class="search-label"><span>⌕</span><input type="search" placeholder="搜索问题、方法或项目" aria-label="搜索专题"></label></div><div class="catalog-grid">'+''.join(catalog_item(p,i+1) for i,p in enumerate(projects))+'</div><p class="empty-state" hidden>没有匹配专题。可以换一个关键词，或选择全部专题。</p></div></section>'
body+='<section id="tools" class="tools-band"><div class="shell"><div class="section-heading"><div><p class="eyebrow">HUMAN × AI / 04</p><h2>让反馈也服务于人的工作。</h2></div><p>一个面向知识与学习，<br>一个面向人的输入、专注与长期上下文。</p></div><div class="product-grid">'
for key in ['educate-flywheel','echo']:
 v=presentation[key];body+=f'<a class="product-feature" href="projects/{key}.html"><span class="eyebrow">PERSONAL PROJECT</span><h3>{v["short"]} <span>↗</span></h3><p>{e(v["question"])}</p>{diagram(key,True)}<span class="read-link">产品机制 · 数据结构 · 具体案例</span></a>'
body+='</div></div></section>'
# Curated public repositories, maintained separately from long-form reports.
body+='<section id="open-source" class="shell home-section"><div class="section-heading"><div><p class="eyebrow">OPEN SOURCE / 05</p><h2>更多项目，从这里出发。</h2></div><p>从智能体实验到日常应用。<br>阅读项目简介，打开代码或在线文档。</p></div><div class="catalog" data-catalog><div class="catalog-controls"><div class="filter-buttons" role="group" aria-label="开源项目分类">'
for value,label in [('all','全部项目'),('evaluation','智能体评测'),('automation','自动实验与协作'),('learning','模型与知识学习'),('applications','个人应用')]:
 body+=f'<button data-filter="{value}" aria-pressed="{str(value=="all").lower()}">{label}</button>'
body+='</div><label class="search-label"><span>⌕</span><input type="search" placeholder="搜索名称、用途或仓库" aria-label="搜索开源项目"></label></div><div class="repository-grid">'
for p in open_source:
 repo='https://github.com/HuangShengZeBlueSky/'+p['repo']
 search=' '.join([p['title'],p['repo'],p['summary'],p['kind']])
 body+=f'<article class="catalog-item repository-card" data-category="{e(p["category"])}" data-search="{e(search)}"><span class="item-label">{e(p["kind"])}</span><h3>{link(repo,p["title"])}</h3><p>{e(p["summary"])}</p><small class="repository-name">{e(p["repo"])}</small><div class="repository-links">{link(repo,"查看代码 ↗")}'
 if p.get('website'):body+=link(p['website'],'在线文档 ↗')
 body+='</div></article>'
body+='</div><p class="empty-state" hidden>没有匹配项目，请换一个关键词或分类。</p></div><p class="repository-note">'+link('https://github.com/HuangShengZeBlueSky?tab=repositories','查看全部 GitHub 仓库 ↗')+'</p></section>'
body+='''<section id="about" class="shell home-section about"><div><p class="eyebrow">BACKGROUND / 06</p><h2>连接研究问题<br>与工程现场。</h2><p>我关注如何把模型行为转化为可观察、可解释、可改进的系统。研究和工程之间，实验是共同的语言。</p><div class="hero-links"><a href="mailto:1641335545@qq.com">联系我 ↗</a><a href="resume.html">完整履历 ↗</a></div></div><div class="timeline">'''
for date,title,detail in [('2026.01—2026.10','元理智能','AutoHarness 算法负责实习生'),('2025.09—2028.06','清华大学','数学与人工智能硕士研究生 · 预计毕业'),('2025.09—2026.01','中车数研院','工业知识库、智能体与时序研究'),('2021.09—2025.06','北京航空航天大学','人工智能 · 工学学士 · 平均绩点 3.72 / 4.0')]:body+=f'<div><span>{date}</span><h3>{title}</h3><p>{detail}</p></div>'
body+='</div></section></main>'
(OUT/'index.html').write_text(doc('研究、系统与持续改进',body))
# Technical reports
related={'medical-autope':['autope','evaluation','finance-sandbox'],'finance-sandbox':['evaluation','autoharness'],'evaluation':['finance-sandbox','rewardweaver'],'autoharness':['workbench','rewardweaver'],'workbench':['autoharness','echo'],'robowm-bench':['multi-agent-benchmark','evaluation'],'rewardweaver':['autope','autoharness'],'autope':['medical-autope','rewardweaver'],'flyreview':['workbench','educate-flywheel'],'educate-flywheel':['flyreview','echo'],'echo':['workbench','educate-flywheel'],'multi-agent-benchmark':['robowm-bench','evaluation']}
for p in projects:
 v=presentation[p['id']];sections=p['sections'];minutes=max(3,math.ceil(len(json.dumps(sections,ensure_ascii=False))/420));contents='';toc=''
 for i,s in enumerate(sections):
  sid='section-'+str(i+1);toc+=f'<a href="#{sid}"><span>{i+1:02d}</span>{e(s["heading"])}</a>'
  contents+=f'<section id="{sid}"><h2><span>{i+1:02d}</span>{e(s["heading"])}</h2>{render_section(s)}</section>'
 if p.get('surface_map'):
  toc+='<a href="#surface-map"><span>↳</span>交互：选择修改面</a>';contents+='<section id="surface-map"><h2><span>↳</span>从失败信号选择修改面</h2><p>下面的地图展示可干预位置与承载方式。每个例子用于解释方法选择，不是自动给失败打标签的固定规则。</p><div class="surface-explorer"><div class="surface-buttons" role="group" aria-label="选择修改面">'
  for i,x in enumerate(p['surface_map']):contents+=f'<button data-surface="surface-{i}" aria-pressed="{str(i==0).lower()}">{e(x["label"])}</button>'
  contents+='</div>'
  for i,x in enumerate(p['surface_map']):contents+=f'<div class="surface-panel" id="surface-{i}"'+(' hidden' if i else '')+f'><h3>{e(x["label"])}</h3><dl><dt>失败信号</dt><dd>{e(x["signal"])}</dd><dt>修改对象</dt><dd>{e(x["change"])}</dd><dt>承载方式</dt><dd>{e(x["layer"])}</dd><dt>示例</dt><dd>{e(x["example"])}</dd></dl></div>'
  contents+='</div></section>'
 if p['links']:contents+='<section class="sources" id="sources"><h2><span>↗</span>资料与延伸阅读</h2>'+''.join(link(x['url'],x['label']+' ↗') for x in p['links'])+'</section>'
 contents+='<nav class="related" aria-label="相关专题"><span class="eyebrow">CONTINUE READING</span>'+''.join(f'<a href="{key}.html"><strong>{presentation[key]["short"]}</strong><span>{e(presentation[key]["question"])} ↗</span></a>' for key in related.get(p['id'],[]))+'</nav>'
 body=f'<div class="reading-progress" aria-hidden="true"></div><main id="main" class="article-shell"><header class="article-header"><a class="back" href="../learn.html">← 专题索引</a><div class="article-kicker"><span>{e(p["kicker"])}</span><span>约 {minutes} 分钟 · 2026.10.13</span></div><h1>{e(p["title"])}</h1><p class="article-question">{e(v["question"])}</p><p class="abstract">{e(p["summary"])}</p><div class="article-meta"><p>{e(p["role"])}</p>{tags(p)}</div></header><section class="takeaways" aria-label="阅读要点"><span class="eyebrow">AT A GLANCE</span><ol>'+''.join('<li>'+e(t)+'</li>' for t in v['takeaways'])+'</ol></section>'+explorer(p)+f'<div class="article-body"><aside class="article-aside"><div class="toc-heading">本页目录 <span>{len(sections):02d} 节</span></div><nav aria-label="本页目录">{toc}</nav><a class="toc-top" href="#main">返回顶部 ↑</a></aside><article class="article-content">{contents}</article></div></main>'
 (OUT/'projects'/f'{p["id"]}.html').write_text(doc(p['title'],body,'../',p['summary'],'projects/'+p['id']+'.html'))
# Learning guide
body='<main id="main" class="shell index-page"><header class="index-header"><p class="eyebrow">TECHNICAL FIELD NOTES</p><h1>专题索引</h1><p>先选择想解决的问题，再沿着环境、评价与优化往下读。</p></header><div class="catalog" data-catalog><div class="catalog-controls"><div class="filter-buttons" role="group" aria-label="专题分类"><button data-filter="all" aria-pressed="true">全部</button><button data-filter="engineering" aria-pressed="false">场景与系统</button><button data-filter="research" aria-pressed="false">研究方法</button><button data-filter="tools" aria-pressed="false">个人工具</button></div><label class="search-label"><span>⌕</span><input type="search" placeholder="搜索专题" aria-label="搜索专题"></label></div><div class="catalog-grid">'+''.join(catalog_item(p,i+1) for i,p in enumerate(projects))+'</div><p class="empty-state" hidden>没有匹配专题，请换一个关键词。</p></div><div class="reading-routes"><div class="section-heading"><div><p class="eyebrow">READING PATHS</p><h2>四条阅读路径</h2></div></div>'
for route in data['learning']['routes']:
 body+='<section class="route"><span class="eyebrow">'+e(route['label'])+'</span><h3>'+e(route['title'])+'</h3><p>'+e(route['description'])+'</p><ol>'+''.join('<li>'+link('projects/'+k+'.html',presentation[k]['short']+' ↗')+'</li>' for k in route['projects'])+'</ol></section>'
body+='</div><div class="learning-content">'
for s in data['learning']['sections']:body+='<section><h2>'+e(s['heading'])+'</h2>'+render_section(s)+'</section>'
body+='</div></main>';(OUT/'learn.html').write_text(doc('专题索引与阅读路径',body,path='learn.html'))

cv=data['resume_profile']
resume='<div class="resume-actions"><a href="index.html">← 返回技术网站</a><div><a class="button" href="resume.pdf" download="黄胜泽-简历.pdf">下载最新 PDF ↓</a>　<a href="resume.tex">LaTeX 源码 ↓</a>　<button onclick="window.print()">打印 / 保存 PDF</button></div></div><main id="main" class="resume-sheet compact"><h1>'+e(cv['name'])+'</h1><p class="resume-contact">北京 · 1641335545@qq.com · github.com/HuangShengZeBlueSky<br>'+e(cv['direction'])+'</p><h2>教育背景</h2>'
for x in cv['education']:
    resume+=f'<div class="resume-group"><h3>{e(x["name"])}<span class="date">{e(x["date"])}</span></h3><p class="roleline">{e(x["detail"])}</p></div>'
resume+='<h2>实习经历</h2>'
for x in cv['experience']:
    resume+=f'<h3>{e(x["name"])} · {e(x["role"])}<span class="date">{e(x["date"])}</span></h3><ul>'
    for item in x['bullets']: resume+=f'<li><strong>{e(item["lead"])}：</strong>{e(item["text"])}</li>'
    resume+='</ul>'
resume+='<h2>论文与研究参与</h2>'
for x in cv['research']:
    resume+=f'<div class="resume-group"><h3>{link(x["url"],x["name"])}</h3><p class="roleline">{e(x["role"])}</p><p>{e(x["text"])}</p></div>'
resume+='<h2>研究工程与个人项目</h2>'
for x in cv['projects']:
    resume+=f'<div class="resume-group"><p><strong>{link("projects/"+x["id"]+".html",x["name"])}：</strong>{e(x["text"])}</p></div>'
resume+='<h2>核心方法图解</h2>'
for figure in cv['figures']:
    resume+='<figure class="cv-figure"><h3>'+e(figure['title'])+'</h3><div class="cv-flow">'
    for title,body in figure['nodes']:
        resume+='<div><strong>'+e(title)+'</strong><p>'+e(body)+'</p></div>'
    resume+='</div><figcaption>'+e(figure['caption'])+'</figcaption></figure>'
resume+='<h2>专业技能</h2>'
for x in cv['skills']: resume+=f'<p><strong>{e(x["label"])}：</strong>{e(x["text"])}</p>'
resume+='</main>'
(OUT/'resume.html').write_text(doc('技术履历',resume,path='resume.html'),encoding='utf-8')
if (ROOT/'resume.tex').exists(): shutil.copy2(ROOT/'resume.tex',OUT/'resume.tex')
# Publish the PDF exported from the same current LaTeX source.
if (ROOT/'resume.pdf').exists(): shutil.copy2(ROOT/'resume.pdf',OUT/'resume.pdf')
(OUT/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+SITE+'/sitemap.xml\n')
urls=['','resume.html','learn.html']+['projects/'+p['id']+'.html' for p in projects]
(OUT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+SITE+'/'+u+'</loc></url>' for u in urls)+'</urlset>')
print(f'Built {len(projects)} technical reports, reading guide and illustrated resume.')
