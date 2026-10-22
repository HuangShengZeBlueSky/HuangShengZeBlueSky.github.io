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
def doc(title,body,prefix='',desc='黄胜泽的技术博客：记录智能体评测、自进化、城市预测与数学教育中的思路、架构、方法和实验。',path=''):
 return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(title)} · 黄胜泽</title><meta name="description" content="{e(desc)}"><meta name="theme-color" content="#f7f6f2"><link rel="alternate" type="application/rss+xml" title="黄胜泽的技术博客" href="{prefix}feed.xml"><link rel="canonical" href="{SITE}/{path}"><meta property="og:title" content="{e(title)} · 黄胜泽"><meta property="og:description" content="{e(desc)}"><meta property="og:type" content="website"><link rel="icon" href="{prefix}assets/favicon.svg"><link rel="stylesheet" href="{prefix}assets/style.css"></head><body><a class="skip" href="#main">跳到正文</a><header class="topbar"><nav class="shell nav" aria-label="主导航"><a class="brand" href="{prefix}index.html"><span class="monogram">H.</span><span>黄胜泽<small>SHENGZE HUANG</small></span></a><div class="nav-links"><a href="{prefix}index.html#latest">精选文章</a><a href="{prefix}index.html#paths">研究主线</a><a class="hide-mobile" href="{prefix}learn.html">文章索引</a><a class="hide-mobile" href="{prefix}index.html#about">关于</a><a class="nav-resume" href="{prefix}resume.html">简历 <span>↗</span></a></div></nav></header>{body}<footer class="shell footer"><div><strong>持续实验，持续理解。</strong><p>黄胜泽 · 智能体评测与自进化</p></div><div><a href="mailto:1641335545@qq.com">Email ↗</a><a href="https://github.com/HuangShengZeBlueSky">GitHub ↗</a><a href="{prefix}resume.pdf">简历 PDF ↓</a><small>更新于 2026.10 · <a href="https://github.com/HuangShengZeBlueSky/HuangShengZeBlueSky.github.io">网站源码</a></small></div></footer><script src="{prefix}assets/site.js" defer></script></body></html>'''
def node(x,y,w,h,title,sub='',active=False):
 return f'<g><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5" class="node {"node-active" if active else ""}"/><text x="{x+w/2}" y="{y+h/2-(7 if sub else -5)}" text-anchor="middle" class="node-title {"light" if active else ""}">{e(title)}</text>'+(f'<text x="{x+w/2}" y="{y+h/2+17}" text-anchor="middle" class="node-sub {"light" if active else ""}">{e(sub)}</text>' if sub else '')+'</g>'
def edge(path,id):return f'<path d="{path}" class="edge" marker-end="url(#{id})"/>'
def diagram(key,compact=False):
 v=presentation[key];kind=v['kind'];aid='arrow-'+key+('-small' if compact else '')
 s=f'<svg class="architecture" viewBox="0 0 800 370" role="img" aria-label="{e(v["short"])}机制图"><defs><marker id="{aid}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs><text x="30" y="29" class="svg-label">SYSTEM / {e(key.upper())}</text>'
 if kind=='pipeline':
  coords=[(45,65),(435,65),(435,225),(45,225)]
  for path in ['M 365 105 H 427','M 595 145 V 217','M 435 265 H 373']:s+=edge(path,aid)
  for i,(x,y) in enumerate(coords):s+=node(x,y,320,80,f'0{i+1} '+v['steps'][i]['title'],'',i==2)
  s+='<text x="400" y="350" text-anchor="middle" class="node-sub">'+e(v['short'])+' · 从问题到可复核的结论</text>'
 elif kind=='grid':
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
from blog_interactions import secant_demo
def render_section(section):
 s=''.join(f'<p>{inline(t)}</p>' for t in section.get('paragraphs',[]))
 if section.get('flow'):s+='<ol class="technical-flow">'+''.join(f'<li><span>{i+1:02d}</span><strong>{e(x["title"])}</strong><p>{e(x["body"])}</p></li>' for i,x in enumerate(section['flow']))+'</ol>'
 if section.get('demo')=='secant':s+=secant_demo()
 if section.get('formula'):s+=f'<div class="formula">{e(section["formula"])}</div>'
 if section.get('table'):
  t=section['table'];s+='<div class="table-scroll" role="region" aria-label="数据与设计对照" tabindex="0"><table><thead><tr>'+''.join('<th>'+e(str(x))+'</th>' for x in t['headers'])+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+e(str(x))+'</td>' for x in r)+'</tr>' for r in t['rows'])+'</tbody></table></div>'
 if section.get('bullets'):s+='<ul>'+''.join('<li>'+inline(t)+'</li>' for t in section['bullets'])+'</ul>'
 if section.get('code'):
  code=section['code'];s+='<div class="code-block"><div>'+e(code['language'])+'</div><pre><code>'+e(code['text'])+'</code></pre></div>'
 if section.get('callout'):
  x=section['callout'];s+='<aside class="callout"><strong>'+e(x['label'])+'</strong><p>'+inline(x['text'])+'</p></aside>'
 return s
# Personal technical blog and secondary source directory.
from blog_home import render_home, render_resources
body=render_home(projects,presentation,catalog_item,link,data['learning']['routes'])
(OUT/'index.html').write_text(doc('技术博客',body))
(OUT/'resources.html').write_text(doc('实现与延伸资料',render_resources(open_source,link),path='resources.html'))
# Technical reports
related={'medical-autope':['autope','evaluation','finance-sandbox'],'finance-sandbox':['evaluation','autoharness'],'evaluation':['finance-sandbox','rewardweaver'],'autoharness':['workbench','rewardweaver'],'workbench':['autoharness','echo'],'robowm-bench':['multi-agent-benchmark','evaluation'],'rewardweaver':['autope','autoharness'],'autope':['medical-autope','rewardweaver'],'flyreview':['workbench','educate-flywheel'],'educate-flywheel':['flyreview','echo'],'echo':['workbench','educate-flywheel'],'multi-agent-benchmark':['robowm-bench','evaluation']}
related.update({'earth-agent':['plugin-evolution','benchmark-audit','evaluation'],'plugin-evolution':['autoharness','workbench','earth-agent'],'math-teaching':['math-animation','educate-flywheel','flyreview'],'math-animation':['math-teaching','educate-flywheel'],'benchmark-audit':['autoharness','earth-agent','evaluation']})
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
 body=f'<div class="reading-progress" aria-hidden="true"></div><main id="main" class="article-shell"><header class="article-header"><a class="back" href="../learn.html">← 文章索引</a><div class="article-kicker"><span>{e(p["kicker"])}</span><span>约 {minutes} 分钟 · {e(p.get("updated", "2026.10.13"))}</span></div><h1>{e(p["title"])}</h1><p class="article-question">{e(v["question"])}</p><p class="abstract">{e(p["summary"])}</p><div class="article-meta"><p>{e(p["role"])}</p>{tags(p)}</div></header><section class="takeaways" aria-label="阅读要点"><span class="eyebrow">AT A GLANCE</span><ol>'+''.join('<li>'+e(t)+'</li>' for t in v['takeaways'])+'</ol></section>'+explorer(p)+f'<div class="article-body"><aside class="article-aside"><div class="toc-heading">本页目录 <span>{len(sections):02d} 节</span></div><nav aria-label="本页目录">{toc}</nav><a class="toc-top" href="#main">返回顶部 ↑</a></aside><article class="article-content">{contents}</article></div></main>'
 (OUT/'projects'/f'{p["id"]}.html').write_text(doc(p['title'],body,'../',p['summary'],'projects/'+p['id']+'.html'))
# Learning guide
body='<main id="main" class="shell index-page"><header class="index-header"><p class="eyebrow">TECHNICAL FIELD NOTES</p><h1>文章索引</h1><p>先选择想解决的问题，再沿着环境、评价与优化往下读。</p></header><div class="catalog" data-catalog><div class="catalog-controls"><div class="filter-buttons" role="group" aria-label="专题分类"><button data-filter="all" aria-pressed="true">全部</button><button data-filter="engineering" aria-pressed="false">场景与系统</button><button data-filter="research" aria-pressed="false">研究方法</button><button data-filter="tools" aria-pressed="false">教育与协作</button></div><label class="search-label"><span>⌕</span><input type="search" placeholder="搜索专题" aria-label="搜索专题"></label></div><div class="catalog-grid">'+''.join(catalog_item(p,i+1) for i,p in enumerate(projects))+'</div><p class="empty-state" hidden>没有匹配专题，请换一个关键词。</p></div><div class="reading-routes"><div class="section-heading"><div><p class="eyebrow">READING PATHS</p><h2>四条阅读路径</h2></div></div>'
for route in data['learning']['routes']:
 body+='<section class="route"><span class="eyebrow">'+e(route['label'])+'</span><h3>'+e(route['title'])+'</h3><p>'+e(route['description'])+'</p><ol>'+''.join('<li>'+link('projects/'+k+'.html',presentation[k]['short']+' ↗')+'</li>' for k in route['projects'])+'</ol></section>'
body+='</div><div class="learning-content">'
for s in data['learning']['sections']:body+='<section><h2>'+e(s['heading'])+'</h2>'+render_section(s)+'</section>'
body+='</div></main>';(OUT/'learn.html').write_text(doc('文章索引与阅读路径',body,path='learn.html'))

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
urls=['','resume.html','learn.html','resources.html']+['projects/'+p['id']+'.html' for p in projects]
(OUT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+SITE+'/'+u+'</loc></url>' for u in urls)+'</urlset>')
print(f'Built {len(projects)} technical reports, reading guide and illustrated resume.')

# Subscription feed contains public article summaries only.
from xml.etree.ElementTree import Element, SubElement, tostring
rss=Element('rss',version='2.0');channel=SubElement(rss,'channel')
for tag,value in [('title','黄胜泽的技术博客'),('link',SITE),('description','智能体、预测与教育中的思路、架构、方法和实验'),('language','zh-CN')]:SubElement(channel,tag).text=value
for p in sorted(projects,key=lambda p:p.get('updated','2026.10.13'),reverse=True):
 item=SubElement(channel,'item');url=SITE+'/projects/'+p['id']+'.html'
 for tag,value in [('title',p['title']),('link',url),('guid',url),('description',p['summary'])]:SubElement(item,tag).text=value
(OUT/'feed.xml').write_bytes(tostring(rss,encoding='utf-8',xml_declaration=True))
