from pathlib import Path
from html import escape as e
import json,re,shutil
from urllib.parse import urlparse

ROOT=Path(__file__).resolve().parent
DIST=ROOT/'dist'
if DIST.exists():shutil.rmtree(DIST)
DIST.mkdir();shutil.copytree(ROOT/'assets',DIST/'assets')
studies=json.loads((ROOT/'data/studies.json').read_text())
notes=json.loads((ROOT/'data/notes.json').read_text())
byid={s['id']:s for s in studies}
BASE='https://huangshengzebluesky.github.io'
def url(s):return f'/{s["category"]}/{s["id"]}.html'
def inline(t):
 t=e(str(t))
 def link(m):
  dest=m.group(2)
  if any(x in dest.lower() for x in ('resume.pdf','resume.html','resume.tex','/users/','localhost','127.0.0.1')):return m.group(1)
  if not dest.startswith(('https://','http://','#')):return m.group(1)
  return f'<a href="{dest}">{m.group(1)}</a>'
 t=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',link,t)
 t=re.sub(r'\*\*(.+?)\*\*',r'<strong>\1</strong>',t)
 return re.sub(r'`([^`]+)`',r'<code>\1</code>',t)
def page(path,title,body,active='',desc='黄胜泽的研究与实践：智能体、评测、自动实验与人机协作。'):
 nav=''.join(f'<a href="/{name}.html"'+(' aria-current="page"' if active==name else '')+f'>{label}</a>' for name,label in [('research','论文研究'),('projects','项目实践'),('writing','技术笔记'),('about','关于我')])
 doc=f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{e(title)} · 黄胜泽</title><meta name="description" content="{e(desc,quote=True)}"><meta name="theme-color" content="#214f43"><link rel="canonical" href="{BASE}/{path}"><link rel="stylesheet" href="/assets/style.css"><link rel="icon" type="image/svg+xml" href="/assets/favicon.svg"><link rel="alternate" type="application/rss+xml" title="研究与实践" href="/feed.xml"></head><body><a class="skip" href="#main">跳到正文</a><header class="top"><a class="brand" href="/">黄胜泽<span>研究与实践</span></a><nav aria-label="主导航">{nav}</nav></header>{body}<footer class="footer"><p>把问题讲清楚，把过程留下来。</p><div><a href="https://github.com/HuangShengZeBlueSky">GitHub ↗</a><a href="/writing.html">全部笔记</a><a href="/feed.xml">RSS</a></div><small>内容更新于 2026 年 11 月 · 独立研究与合作工作的身份分别注明。</small></footer><script src="/assets/site.js" defer></script></body></html>'''
 p=DIST/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(doc)
def card(s,n=None):
 return f'<a class="story" href="{url(s)}"><div class="story-meta">{e(s["name"])}<span>{e(s["role"])}</span></div><h3>{e(s["title"])}</h3><p>{e(s["summary"])}</p><span class="read">展开这项工作 <span aria-hidden="true">↗</span></span></a>'

home='''<main id="main"><section class="hero"><div><p class="eyebrow">SHENGZE HUANG · NOTES FROM RESEARCH & BUILDING</p><h1>AI 能回答，<br>怎样才能把事做成？</h1><p class="hero-second">从一句“帮我改个预约”开始。</p><p class="intro">我是黄胜泽。我研究让 AI 查信息、用工具、完成任务，也关心它怎样从失败中改进。这里先讲人会遇到的问题，再展开方法、实验，以及我在过程中形成的思考。</p><p class="agent-definition">能利用工具、连续推进任务的 AI 系统，通常被称为“智能体”。</p><div class="hero-actions"><a class="button" href="#one-task">从一个例子读起 ↓</a><a href="/about.html">认识我 ↗</a></div></div><aside class="current"><p class="eyebrow">最近在想</p><a href="/research/harness.html"><span>01 / 运行机制</span><h2>模型不换，能力还能怎样改进？</h2><p>让程序帮助它记住进度、使用信息和执行动作。</p></a><a href="/research/behavior.html"><span>02 / 训练反馈</span><h2>同一句建议，为什么有时会越界？</h2><p>先了解当时的处境，再评价它做得好不好。</p></a><a href="/projects/echo.html"><span>03 / 人机协作</span><h2>AI 说了很多，我的思路留在哪里？</h2><p>从自己的原话，找回专注与复盘。</p></a></aside></section>'''
home+='''<section class="section foundation" id="one-task"><div class="section-heading"><div><p class="eyebrow">START WITH ONE TASK</p><h2>客户要的是预约真的改好。</h2></div><p>说得通、做得对、能核对，<br>是需要分别考虑的事。</p></div><p class="customer-line">“帮我把周五的体检，改到周六。”</p><div class="task-chain" aria-label="完成改约需要的四个环节"><div><span>01</span><h3>了解当前情况</h3><p>原来约在哪里？订单是否有效？</p></div><div><span>02</span><h3>判断能否办理</h3><p>周六有名额吗？符合改约规则吗？</p></div><div><span>03</span><h3>实际执行操作</h3><p>处理原预约，保存新的日期和时段。</p></div><div><span>04</span><h3>核对办理结果</h3><p>记录确实更新了吗？告诉客户的结果对吗？</p></div></div><p class="foundation-text">这条链上，任何一处没接好，都可能出现“回答很流畅，事情却没办成”。要研究它，我们先准备能实际操作的模拟环境，再观察问题发生在哪里。</p><div class="improvement"><div class="improvement-heading"><h3>发现问题之后，可以从哪里改？</h3><p>一次失误可能涉及多个原因。先看三种方法分别改变什么。</p></div><div class="route-tabs" role="tablist" aria-label="三种改进对象"><button type="button" role="tab" id="route-harness" aria-controls="route-panel" aria-selected="true" data-route="harness">改运行程序</button><button type="button" role="tab" id="route-sft" aria-controls="route-panel" aria-selected="false" data-route="sft">补示范数据</button><button type="button" role="tab" id="route-reward" aria-controls="route-panel" aria-selected="false" data-route="reward">调整训练奖励</button></div><div class="route-panel" id="route-panel" role="tabpanel" aria-labelledby="route-harness" tabindex="0"><p class="eyebrow" id="route-name">AutoHarness</p><h4 id="route-title">让“已查到号源”和“已完成办理”成为不同的进度。</h4><p id="route-description">如果问题在于进度没有被稳定利用，可以让程序记录真实回执，把当前状态交给模型，并在工具执行前检查必要条件。</p><p class="route-change" id="route-change">改变的是外围运行程序，做事模型的权重保持固定。</p><a id="route-link" href="/research/harness.html">继续读这项研究 →</a></div></div></section>'''
home+='''<section class="section" id="start"><div class="section-heading"><div><p class="eyebrow">READING PATHS</p><h2>沿着一条线，读懂背后的工作。</h2></div><p>从你关心的问题进入。<br>代码、论文和方法图，都放在文章里。</p></div><div class="paths"><article><span>01</span><h3>先让它有地方做事</h3><p>业务资料不完整、环境不能直接用于训练，怎样准备可执行的模拟世界？</p><a href="/projects/world.html">商业模拟世界 →</a><a href="/projects/sft.html">从失败到训练数据 →</a></article><article><span>02</span><h3>再决定怎样让它改进</h3><p>改运行程序、选择训练奖励、构造可靠反馈，分别在解决什么问题？</p><a href="/research/harness.html">AutoHarness →</a><a href="/research/reward.html">RewardWeaver →</a><a href="/research/behavior.html">BehaviorWeaver →</a></article><article><span>03</span><h3>把研究变成可以用的东西</h3><p>让 AI 做实验、让题库从反馈中积累经验，也让人能重新掌握自己的工作。</p><a href="/projects/mlp.html">MLP 自动科研 →</a><a href="/projects/edu.html">教育飞轮 →</a><a href="/projects/echo.html">回声 →</a></article></div></section>'''
home+='<section class="section"><div class="section-heading"><div><p class="eyebrow">RESEARCH</p><h2>论文背后的问题。</h2></div><a href="/research.html">查看全部研究 ↗</a></div><div class="stories">'+''.join(card(byid[k]) for k in ('harness','reward','behavior','robo'))+'</div></section>'
home+='<section class="section writing-preview"><div class="section-heading"><div><p class="eyebrow">FIELD NOTES</p><h2>研究过程，也值得留下来。</h2></div><a href="/writing.html">21 篇既有技术笔记 ↗</a></div>'
for k in ('earth-agent-generalization','benchmark-audit','agent-tools-explained'):
 n=next(x for x in notes if x['id']==k);home+=f'<a class="note-row" href="/writing/{k}.html"><span>{e(n.get("published",n.get("updated","2026")))}</span><div><h3>{e(n["title"])}</h3><p>{e(n["summary"])}</p></div><span>↗</span></a>'
home+='</section><section class="section about-strip"><p class="eyebrow">A LITTLE ABOUT ME</p><h2>研究系统，也在系统里做研究。</h2><p>我在清华大学学习数学与人工智能。做过业务智能体的环境与评价、运行机制优化，也在探索自动实验、行为反馈，以及面向学习与专注的产品。我喜欢把抽象想法落到一条能看见输入、行动和结果的流程里。</p><a href="/about.html">更多关于我的工作方式 ↗</a></section></main>'
page('index.html','研究与实践',home)

for category,title,deck in [('research','论文研究','从具体问题进入方法，看看论文究竟想解释什么。'),('projects','项目实践','把想法变成可以运行、可以观察和继续改进的东西。')]:
 page(category+'.html',title,f'<main id="main" class="shell index"><p class="eyebrow">{category.upper()}</p><h1>{title}</h1><p class="index-deck">{deck}</p><div class="stories">'+''.join(card(s) for s in studies if s['category']==category)+'</div></main>',category)

for s in studies:
 meta=s['status'] if s['status'] and s['role'].split('·')[0].strip() in s['status'] else s['role']+(' · '+s['status'] if s['status'] else '')
 body=f'<main id="main" class="article-shell"><a class="back" href="/{s["category"]}.html">← 返回'+('论文研究' if s['category']=='research' else '项目实践')+f'</a><header class="article-head"><p class="eyebrow">{e(s["name"])}</p><h1>{e(s["title"])}</h1><p class="article-deck">{e(s["summary"])}</p><div class="byline">{e(meta)}<span>2026 年 11 月更新</span></div></header><div class="article-layout"><aside class="toc"><span>沿着问题读下去</span><a href="#problem">从一个例子开始</a><a href="#reasoning">一步步想清楚</a><a href="#diagram">先记住这条线</a><a href="#method">具体怎样做</a><a href="#result">怎样理解结果</a><a href="#reflection">我的思考</a><a href="#terms">名词与技术细节</a></aside><article class="prose">'
 body+=f'<section id="problem" class="opening"><p class="eyebrow">从一个例子开始</p><p>{inline(s["opening"])}</p><p class="minimum">{inline(s["minimum"])}</p></section><section id="reasoning"><h2>一步步想清楚</h2><ol class="reasoning">'
 for i,(title,description) in enumerate(s['logic'],1):body+=f'<li><span class="step-number">{i:02}</span><div><h3>{inline(title)}</h3><p>{inline(description)}</p></div></li>'
 body+='</ol></section><section id="diagram"><h2>先记住这条线</h2><div class="simple-flow" role="group" aria-label="方法的三个主要环节">'
 for i,(title,description) in enumerate(s['simple_flow'],1):body+=f'<div><span>{i:02}</span><h3>{inline(title)}</h3><p>{inline(description)}</p></div>'
 body+='</div></section><section id="method"><h2>我参与的工作，具体怎样落地</h2><ol class="method-steps">'
 for title,description in s['method_steps']:body+='<li><h3>'+inline(title)+'</h3><p>'+inline(description)+'</p></li>'
 body+=f'</ol></section><section class="example" id="example"><span>回到具体情境</span><p>{inline(s["example"])}</p></section><section id="result"><h2>做出了什么，结果意味着什么</h2><p>{inline(s["observation"])}</p><p>{inline(s["result_meaning"])}</p></section><section id="reflection"><h2>我怎样理解这件事</h2>'+''.join('<p>'+inline(t)+'</p>' for t in s['reflection'])+'</section>'
 body+='<section id="terms" class="deeper"><h2>想再往里看一点？</h2><details class="terms"><summary>几个名字，放回上下文理解</summary><dl>'+''.join('<dt>'+inline(term)+'</dt><dd>'+inline(description)+'</dd>' for term,description in s['glossary'])+'</dl></details>'
 body+=f'<details class="technical"><summary>完整方法图与技术路径</summary><figure><div class="figure-scroll"><img src="/assets/figures/{s["id"]}.svg" alt="{e(s["name"])} 完整方法图" loading="lazy"></div><figcaption>{e(s["guide"])}</figcaption></figure><p>{inline(s["method"])}</p></details>'
 q,a=s['followup'];body+='<details><summary>'+inline(q)+'</summary><p>'+inline(a)+'</p></details></section>'
 if s['links']:body+='<section class="further"><h2>继续读</h2>'+''.join(f'<a href="{e(u)}">{e(label)} ↗</a>' for label,u in s['links'])+'</section>'
 related={'world':'sft','sft':'harness','harness':'reward','reward':'behavior','behavior':'world','robo':'multiagent','multiagent':'mlp','mlp':'harness','fly':'echo','edu':'echo','echo':'edu'}
 t=byid[related[s['id']]];body+=f'<a class="next-story" href="{url(t)}"><span>另一项相关的工作</span><h3>{e(t["title"])}</h3><p>{e(t["summary"])}</p></a></article></div></main>'
 page(s['category']+'/'+s['id']+'.html',s['title'],body,s['category'],s['summary'])

def section_markup(sec):
 out='<section><h2>'+inline(sec.get('heading',''))+'</h2>'
 for t in sec.get('paragraphs',[])+sec.get('paragraphs_extra',[]):out+='<p>'+inline(t)+'</p>'
 if sec.get('bullets'):out+='<ul>'+''.join('<li>'+inline(x)+'</li>' for x in sec['bullets'])+'</ul>'
 table=sec.get('table')
 if isinstance(table,dict):
  out+='<div class="table-scroll"><table><thead><tr>'+''.join('<th>'+inline(x)+'</th>' for x in table.get('headers',[]))+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+inline(x)+'</td>' for x in row)+'</tr>' for row in table.get('rows',[]))+'</tbody></table></div>'
 if sec.get('code'):out+='<pre><code>'+e(str(sec['code']))+'</code></pre>'
 if sec.get('formula'):out+='<p class="formula">'+inline(sec['formula'])+'</p>'
 return out+'</section>'

update_map={'autoharness':'harness','plugin-evolution':'harness','dsh-loop-evolution':'harness','rewardweaver':'reward','robowm-bench':'robo','educate-flywheel':'edu','echo':'echo','finance-sandbox':'world','medical-autope':'world','multi-agent-benchmark':'multiagent','flyreview':'fly'}
for n in notes:
 date=n.get('updated',n.get('published','2026 年 10 月'))
 intro=f'<div class="archive-note">这是 {e(date)} 的研究记录，保留当时的问题和结果。'
 if n['id'] in update_map:
  latest=byid[update_map[n['id']]];intro+=f'相关工作的新整理见：<a href="{url(latest)}">{e(latest["name"])} ↗</a>'
 intro+='</div>'
 body=f'<main id="main" class="article-shell narrow"><a class="back" href="/writing.html">← 全部技术笔记</a><header class="article-head"><p class="eyebrow">FIELD NOTES · {e(date)}</p><h1>{e(n["title"])}</h1><p class="article-deck">{e(n["summary"])}</p></header><article class="prose">'+intro+''.join(section_markup(sec) for sec in n['sections'])
 links=[l for l in n.get('links',[]) if l.get('url','').startswith('https://') and not any(x in l['url'] for x in ('resume','feishu','overleaf'))]
 if links:body+='<section class="further"><h2>相关资料</h2>'+''.join('<a href="'+e(l['url'])+'">'+e(l.get('label','继续阅读'))+' ↗</a>' for l in links)+'</section>'
 body+='</article></main>';page('writing/'+n['id']+'.html',n['title'],body,'writing',n['summary'])

rows=''.join(f'<a class="note-row filter-item" href="/writing/{n["id"]}.html"><span>{e(n.get("updated","2026"))}</span><div><h2>{e(n["title"])}</h2><p>{e(n["summary"])}</p></div><span>↗</span></a>' for n in notes)
page('writing.html','技术笔记','<main id="main" class="shell index"><p class="eyebrow">WRITING</p><h1>把过程留下来。</h1><p class="index-deck">这里保留研究与工程中的问题、取舍和转折。旧记录注明日期，与新的工作介绍分开阅读。</p><label class="search">找一篇笔记<input id="note-search" type="search" placeholder="例如：归因、沙箱、数学、工具"></label><div id="note-list">'+rows+'</div><p id="no-results" hidden>暂时没有匹配的笔记。</p></main>','writing')
page('about.html','关于我','''<main id="main" class="article-shell narrow"><header class="article-head"><p class="eyebrow">ABOUT</p><h1>黄胜泽<br><span>Shengze Huang</span></h1><p class="article-deck">研究智能体怎样改进，也研究我们怎样判断它改进了。</p></header><article class="prose"><section><h2>我关注什么</h2><p>我在清华大学学习数学与人工智能。研究和实践主要围绕智能体：让它在业务环境里执行任务，记录失败发生在哪里，再选择改进数据、运行机制或训练奖励。</p><p>我也关心人怎样与这些系统一起工作。教育飞轮和回声从具体使用体验出发：知识怎样形成更好的练习，长对话怎样留下人的思路，一项工作怎样持续推进。</p></section><section><h2>我怎样工作</h2><p>从 2026 年 2 月起，我高强度使用 Coding Agent，尝试独立推进完整研究模块，把代码、实验、进度和看板放在同一条工作线上。AI Builder 对我来说，意味着既能提出问题，也愿意把流程跑通、读懂结果并持续修订。</p></section><section><h2>这个网站怎样读</h2><p>论文研究介绍方法背后的问题，并注明合作身份与稿件状态；项目实践记录实现、例子和观察；技术笔记保留当时的研究过程。正在研究的内容会继续变化，旧记录不会被悄悄改成事后全都知道的故事。</p></section><section class="further"><h2>找到我</h2><a href="https://github.com/HuangShengZeBlueSky">GitHub ↗</a><a href="/research.html">论文研究 →</a><a href="/projects.html">项目实践 →</a></section></article></main>''','about')

# Keep existing article URLs useful, without restoring the old CV pages.
aliases={'autoharness':'harness','rewardweaver':'reward','robowm-bench':'robo','multi-agent-benchmark':'multiagent','educate-flywheel':'edu','echo':'echo','flyreview':'fly','finance-sandbox':'world'}
def redirect(path,dest):
 if '/'+path==dest:return
 p=DIST/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(f'<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta http-equiv="refresh" content="0;url={e(dest)}"><title>前往文章</title><a href="{e(dest)}">继续阅读</a></html>')
for n in notes:redirect('projects/'+n['id']+'.html',url(byid[aliases[n['id']]]) if n['id'] in aliases else '/writing/'+n['id']+'.html')
redirect('learn.html','/writing.html');redirect('resources.html','/projects.html')
page('404.html','没有找到页面','<main id="main" class="shell index"><h1>这条路暂时没有内容。</h1><p>可以从研究、项目或笔记重新开始。</p><a class="button" href="/">返回首页</a></main>')
(DIST/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+BASE+'/sitemap.xml\n')
paths=[p.relative_to(DIST).as_posix() for p in DIST.rglob('*.html') if p.name!='404.html']
(DIST/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+BASE+'/'+e(p)+'</loc></url>' for p in paths)+'</urlset>')
rss='<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>黄胜泽 · 研究与实践</title><link>'+BASE+'</link><description>问题、方法与实践记录</description>'
for s in studies:rss+='<item><title>'+e(s['title'])+'</title><link>'+BASE+url(s)+'</link><guid>'+BASE+url(s)+'</guid><description>'+e(s['summary'])+'</description></item>'
(DIST/'feed.xml').write_text(rss+'</channel></rss>');(DIST/'.nojekyll').touch()
print(f'Built {len(studies)} current studies and {len(notes)} dated notes. No CV files or pages included.')
