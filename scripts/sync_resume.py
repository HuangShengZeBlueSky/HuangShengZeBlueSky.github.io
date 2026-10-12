#!/usr/bin/env python3
"""Sync the concise resume text to a standalone LaTeX source; does not compile."""
from pathlib import Path
import argparse, json
ROOT=Path(__file__).resolve().parents[1]
a=argparse.ArgumentParser();a.add_argument('--latex-path',type=Path,default=ROOT/'resume.tex');args=a.parse_args()
j=json.loads((ROOT/'content.json').read_text())['resume_profile']
def esc(s):
    for old,new in [('\\',r'\textbackslash{}'),('&',r'\&'),('%',r'\%'),('$',r'\$'),('#',r'\#'),('_',r'\_')]:s=s.replace(old,new)
    return s.replace('×',r'$\times$').replace('—','--').replace('–','--')
head=r'''\documentclass[10pt,a4paper,UTF8,fontset=fandol]{ctexart}
\usepackage[left=15mm,right=15mm,top=12mm,bottom=13mm]{geometry}
\usepackage{fontspec,enumitem,tabularx,titlesec,fancyhdr,lastpage}
\usepackage[hidelinks]{hyperref}
\hypersetup{pdftitle={黄胜泽：技术简历},pdfauthor={黄胜泽}}
\setlength{\parindent}{0pt}
\setlength{\parskip}{1pt}
\setlist[itemize]{leftmargin=1.15em,itemsep=1pt,topsep=2pt,parsep=0pt,label=\textbullet}
\titleformat{\section}{\fontsize{12}{14}\selectfont\bfseries}{}{0pt}{}[\vspace{-5pt}\rule{\linewidth}{0.45pt}]
\titlespacing*{\section}{0pt}{7pt}{4pt}
\newcommand{\entry}[3]{\vspace{2pt}\textbf{#1}\enspace {\small #2}\hfill {\small #3}\par}
\pagestyle{fancy}\fancyhf{}\renewcommand{\headrulewidth}{0pt}
\fancyfoot[L]{\footnotesize\href{https://huangshengzebluesky.github.io/}{huangshengzebluesky.github.io}}
\fancyfoot[R]{\footnotesize\thepage/\pageref{LastPage}}
\begin{document}
\fontsize{10.5}{13.7}\selectfont
\begin{center}
{\fontsize{20}{24}\selectfont\bfseries 黄胜泽}\\[3pt]
{\small 智能体评测与自进化\enspace $\cdot$\enspace 算法研究与工程}\\[3pt]
{\small 北京\enspace $\cdot$\enspace \href{mailto:1641335545@qq.com}{1641335545@qq.com}\enspace $\cdot$\enspace \href{https://huangshengzebluesky.github.io/}{技术网站}\enspace $\cdot$\enspace \href{https://github.com/HuangShengZeBlueSky}{GitHub}}
\end{center}
\vspace{-8pt}
\section{教育背景}
'''
s=head
for x in j['education']:s+='\\entry{'+esc(x['name'])+'}{'+esc(x['detail'])+'}{'+esc(x['date'])+'}\n'
s+='\\section{实习经历}\n'
for x in j['experience']:
    s+='\\entry{'+esc(x['name'])+'}{'+esc(x['role'])+'}{'+esc(x['date'])+'}\n\\begin{itemize}\n'
    for b in x['bullets']:s+='\\item \\textbf{'+esc(b['lead'])+'：}'+esc(b['text'])+'\n'
    s+='\\end{itemize}\n'
s+='\\section{论文与研究参与}\n'
for x in j['research']:
    s+='\\entry{\\href{'+x['url']+'}{'+esc(x['name'])+'}}{}{'+esc(x['role'])+'}\n'
    s+='\\begin{itemize}\n\\item '+esc(x['text'])+'\n\\end{itemize}\n'
s+='\\section{研究工程与个人项目}\n'
for x in j['projects']:
    s+='\\begin{itemize}\n\\item \\textbf{\\href{https://huangshengzebluesky.github.io/projects/'+x['id']+'.html}{'+esc(x['name'])+'}：}'+esc(x['text'])+'\n\\end{itemize}\n'
s+='\\section{专业技能}\n'
for x in j['skills']:s+='\\textbf{'+esc(x['label'])+'：}'+esc(x['text'])+'\\par\n'
s+='\\end{document}\n'
args.latex_path.write_text(s,encoding='utf-8')
print('Updated existing LaTeX source:',args.latex_path)
