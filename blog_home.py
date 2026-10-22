"""Editorial homepage: articles and research questions lead; repositories are secondary."""
from html import escape as e

def render_home(projects, presentation, catalog_item, link, routes):
    byid={p['id']:p for p in projects}
    body='''<main id="main"><section class="shell hero blog-hero"><div class="hero-copy"><p class="eyebrow"><span class="status-dot"></span> SHENGZE HUANG / TECHNICAL NOTES</p><h1>黄胜泽<span>思路，系统，与实验。</span></h1><p class="hero-thesis">研究智能体怎样改进，<br>也研究我们怎样知道它改进了。</p><p class="hero-bio">这里记录我在智能体评测、自进化、城市预测和数学教育中的实践：问题怎么拆，系统怎么搭，实验说明了什么。</p><div class="hero-links"><a class="button-primary" href="#latest">阅读精选文章 <span>↓</span></a><a href="#paths">选择阅读主线 ↗</a></div></div><a class="journal-cover" href="projects/earth-agent.html"><span class="eyebrow">FEATURED ESSAY / 实验复盘</span><h2>预测更准了，<br>究竟是谁的贡献？</h2><p>从五个城市案例，拆开模型推理、固定公式与辅助模态的作用。</p><div class="cover-stat"><strong>6.74<span>%</span></strong><p>插件版相对 DSH 基线的平均误差下降<br>五案例开发集 · 三次重复</p></div><div class="cover-question">总体改善，为什么碳排放仍弱于原始版？<span>阅读全文 ↗</span></div></a></section>'''
    body+='<section id="latest" class="shell home-section"><div class="section-heading"><div><p class="eyebrow">SELECTED ESSAYS / 01</p><h2>从问题出发，写到实验结论。</h2></div><p>工程、架构、数据与实践。<br>每篇文章都沿着一个具体问题展开。</p></div><div class="essay-grid">'
    for key in ['autoharness','finance-sandbox','earth-agent','math-teaching','educate-flywheel','echo']:
        p=byid[key];v=presentation[key]
        body+=f'<a class="essay-card" href="projects/{key}.html"><span class="eyebrow">{e(p["kicker"].split(" · ")[0])} · {e(p["updated"])}</span><h3>{e(p["title"])}</h3><p>{e(p["summary"])}</p><div class="essay-bottom"><span>{e(" / ".join(p["tags"][:2]))}</span><span>阅读文章 ↗</span></div></a>'
    body+='</div></section>'
    body+='<section id="paths" class="tools-band"><div class="shell"><div class="section-heading"><div><p class="eyebrow">LINES OF INQUIRY / 02</p><h2>四条持续探索的主线。</h2></div><p>文章之间有方法上的联系。<br>从你关心的问题开始读。</p></div><div class="blog-routes">'
    for route in routes:
        body+=f'<section class="blog-route"><span class="eyebrow">{e(route["label"])}</span><h3>{e(route["title"])}</h3><p>{e(route["description"])}</p><ol>'+''.join('<li>'+link('projects/'+k+'.html',presentation[k]['short']+' ↗')+'</li>' for k in route['projects'])+'</ol></section>'
    body+='</div></div></section>'
    body+=f'<section id="selected" class="shell home-section"><div class="section-heading"><div><p class="eyebrow">ALL ARTICLES / 03</p><h2>技术文章与研究笔记</h2></div><p>{len(projects)} 篇长文，沿着具体问题阅读。<br>可按主题筛选，也可搜索方法与关键词。</p></div><div class="catalog" data-catalog><div class="catalog-controls"><div class="filter-buttons" role="group" aria-label="文章分类"><button data-filter="all" aria-pressed="true">全部文章</button><button data-filter="engineering" aria-pressed="false">场景与系统</button><button data-filter="research" aria-pressed="false">研究方法</button><button data-filter="tools" aria-pressed="false">教育与协作</button></div><label class="search-label"><span>⌕</span><input type="search" placeholder="搜索问题、方法或文章" aria-label="搜索文章"></label></div><div class="catalog-grid">'
    ordered=sorted(projects,key=lambda p:p.get('updated','2026.10.13'),reverse=True)
    body+=''.join(catalog_item(p,i+1) for i,p in enumerate(ordered))+'</div><p class="empty-state" hidden>没有匹配文章，请换一个关键词或分类。</p></div></section>'
    body+='''<section class="shell home-section"><div class="section-heading"><div><p class="eyebrow">PAPERS & METHODS / 04</p><h2>论文与研究参与</h2></div><p>从方法问题进入论文。<br>作者身份与研究参与分别说明。</p></div><div class="publication-list">'''
    for key,date,role in [('robowm-bench','2026.05','共同作者 · CVPR Workshops'),('rewardweaver','2026.10','研究参与 · 公开预印本')]:
        v=presentation[key];body+=f'<a class="publication" href="projects/{key}.html"><span class="pub-date">{date}</span><div><span class="item-label">{role}</span><h3>{e(v["short"])}</h3><p>{e(v["question"])}</p></div><span class="pub-link">阅读方法 ↗</span></a>'
    body+='</div></section><section id="about" class="shell home-section blog-about"><div><p class="eyebrow">ABOUT THE AUTHOR</p><h2>黄胜泽 / Shengze Huang</h2><p>清华大学数学与人工智能硕士研究生。关注智能体评测、运行组件优化与人机协作，实践覆盖业务实验系统、城市预测与数学教学工具。</p><p>我希望把一次实验里真正有价值的内容留下来：一个问题是如何被发现的，一个设计为什么有效，以及结果在哪些条件下仍然成立。</p><div class="hero-links"><a href="resume.html">完整履历 ↗</a><a href="mailto:1641335545@qq.com">联系我 ↗</a><a href="feed.xml">订阅文章 ↗</a></div></div><aside id="open-source"><span class="eyebrow">FURTHER EXPLORATION</span><h3>实现与延伸资料</h3><p>代码与文档是技术文章的延伸。已整理的公开仓库保留在独立资源页。</p><a class="text-link" href="resources.html">浏览资源索引 ↗</a></aside></section></main>'
    return body

def render_resources(items,link):
    groups=[('evaluation','智能体评测'),('automation','自动实验与协作'),('learning','模型与知识学习'),('applications','个人应用')]
    body='<main id="main" class="shell index-page"><header class="index-header"><p class="eyebrow">CODE & REFERENCES</p><h1>实现与延伸资料</h1><p>技术文章之外，可以继续阅读的公开代码与在线文档。</p><a href="index.html">← 返回技术博客</a></header>'
    for category,title in groups:
        body+=f'<section class="resource-section"><h2>{title}</h2><div class="repository-grid">'
        for p in items:
            if p['category']!=category:continue
            url='https://github.com/HuangShengZeBlueSky/'+p['repo']
            body+=f'<article class="repository-card"><span class="item-label">{e(p["kind"])}</span><h3>{link(url,p["title"])}</h3><p>{e(p["summary"])}</p><div class="repository-links">{link(url,"查看实现 ↗")}'
            if p.get('website'):body+=link(p['website'],'在线文档 ↗')
            body+='</div></article>'
        body+='</div></section>'
    return body+'</main>'
