#!/usr/bin/env python3
"""Build the illustrated resume source from the shared profile. No compilation."""
from pathlib import Path
import argparse, json
ROOT=Path(__file__).resolve().parents[1]
a=argparse.ArgumentParser();a.add_argument('--latex-path',type=Path,default=ROOT/'resume.tex');args=a.parse_args()
c=json.loads((ROOT/'content.json').read_text())['resume_profile']
def esc(s):
    for old,new in [('\\',r'\textbackslash{}'),('&',r'\&'),('%',r'\%'),('$',r'\$'),('#',r'\#'),('_',r'\_')]:s=s.replace(old,new)
    return s.replace('×',r'$\times$').replace('→',r'$\rightarrow$').replace('—','--').replace('–','--')
def entry(name,role,date=''):
    return r'\entry{'+esc(name)+'}{'+esc(role)+'}{'+esc(date)+'}\n'
def bullets(items):
    return '\\begin{itemize}\n'+''.join('\\item '+(r'\textbf{'+esc(x['lead'])+'：}'+esc(x['text']) if isinstance(x,dict) else esc(x))+'\n' for x in items)+'\\end{itemize}\n'
def fig(i):
    f=c['figures'][i]; n=len(f['nodes']); w=39 if n==4 else 54
    s='\\begin{center}\n{\\small\\bfseries '+esc(f['title'])+'}\\par\\vspace{4pt}\n\\begin{tikzpicture}[box/.style={draw=ink!45,fill=ink!4,rounded corners=2pt,align=center,text width='+str(w)+'mm,minimum height=15mm,inner sep=3pt,font=\\small},>={Stealth[length=1.6mm]}]\n'
    for k,(title,body) in enumerate(f['nodes']):
        s+='\\node[box] (n'+str(k)+') at ('+str(k*(w+6))+ 'mm,0) {\\textbf{'+esc(title)+'}\\\\[2pt]{\\footnotesize '+esc(body)+'}};\n'
        if k and i<2:s+='\\draw[->,ink!70] (n'+str(k-1)+'.east) -- (n'+str(k)+'.west);\n'
    s+='\\end{tikzpicture}\n\\par\\vspace{2pt}{\\footnotesize '+esc(f['caption'])+'}\n\\end{center}\n'
    return s
s=r'''\documentclass[10pt,a4paper,UTF8,fontset=fandol]{ctexart}
\usepackage[left=15mm,right=15mm,top=13mm,bottom=15mm]{geometry}
\usepackage{fontspec,enumitem,tabularx,titlesec,fancyhdr,lastpage,xcolor,tikz}
\usetikzlibrary{arrows.meta}
\usepackage[hidelinks]{hyperref}
\definecolor{ink}{HTML}{243B4A}
\hypersetup{pdftitle={黄胜泽：技术简历},pdfauthor={黄胜泽}}
\setlength{\parindent}{0pt}
\setlength{\parskip}{2pt}
\setlist[itemize]{leftmargin=1.1em,itemsep=4pt,topsep=3pt,parsep=0pt,label=\textbullet}
\titleformat{\section}{\fontsize{12}{15}\selectfont\bfseries\color{ink}}{}{0pt}{}[\vspace{-5pt}\rule{\linewidth}{0.5pt}]
\titlespacing*{\section}{0pt}{8pt}{5pt}
\newcommand{\entry}[3]{\vspace{2pt}\textbf{#1}\enspace {\small #2}\hfill {\small #3}\par}
\newcommand{\pagehead}[1]{{\large\bfseries 黄胜泽}\hfill {\small #1}\par\vspace{3pt}}
\pagestyle{fancy}\fancyhf{}\renewcommand{\headrulewidth}{0pt}
\fancyfoot[L]{\footnotesize\href{https://huangshengzebluesky.github.io/}{huangshengzebluesky.github.io}}
\fancyfoot[R]{\footnotesize\thepage/\pageref{LastPage}}
\begin{document}
\fontsize{10.5}{14.4}\selectfont
\begin{center}
{\fontsize{21}{25}\selectfont\bfseries 黄胜泽}\\[4pt]
{智能体评测与自进化\enspace $\cdot$\enspace 算法研究与工程}\\[3pt]
{\small 北京\enspace $\cdot$\enspace \href{mailto:1641335545@qq.com}{1641335545@qq.com}\enspace $\cdot$\enspace \href{https://huangshengzebluesky.github.io/}{技术网站}\enspace $\cdot$\enspace \href{https://github.com/HuangShengZeBlueSky}{GitHub}}
\end{center}
\vspace{-7pt}
\section{教育背景}
'''
for x in c['education']:s+=entry(x['name'],x['detail'],x['date'])
s+='\\section{实习经历 · 智能体运行与自进化}\n'
x=c['experience'][0];s+=entry(x['name'],x['role'],x['date'])
s+=fig(0)+bullets(x['bullets'][:7])
s+='\\newpage\n\\pagehead{实习经历 · 场景应用与实验基础设施}\n'
s+=entry(x['name'],x['role']+'（续）',x['date'])
s+=bullets(x['bullets'][7:])+fig(1)
s+='\\section{其他实习经历}\n'
for x in c['experience'][1:]:s+=entry(x['name'],x['role'],x['date'])+bullets(x['bullets'])
s+='\\section{专业技能}\n'
for x in c['skills']:s+=r'\textbf{'+esc(x['label'])+'：}'+esc(x['text'])+'\\par\n'
s+='\\vspace{8pt}{\\small 完整技术专题：\\href{https://huangshengzebluesky.github.io/learn.html}{huangshengzebluesky.github.io/learn.html}。网站展开数据结构、运行流程、设计取舍与实验边界。}\n'
s+='\\newpage\n\\fontsize{10.5}{13.2}\\selectfont\n\\setlist[itemize]{leftmargin=1.1em,itemsep=2pt,topsep=2pt,parsep=0pt}\n\\pagehead{论文研究与个人项目}\n\\section{论文与研究参与}\n'
for x in c['research']:
    s+=r'\textbf{\href{'+x['url']+'}{'+esc(x['name'])+'}}\\hfill{\\small '+esc(x['role'])+'}\\par\n'+bullets(x['points'])
s+=fig(2)+'\\section{研究工程与个人项目}\n'
for x in c['projects']:
    s+=r'\textbf{\href{https://huangshengzebluesky.github.io/projects/'+x['id']+'.html}{'+esc(x['name'])+'}}\\par\n'+bullets(x['points'])
s+='\\end{document}\n'
args.latex_path.write_text(s,encoding='utf-8')
print('Updated LaTeX:',args.latex_path)
