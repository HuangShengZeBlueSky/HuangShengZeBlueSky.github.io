#!/usr/bin/env python3
"""Refresh LaTeX project prose from content.json and compile the full resume."""
from pathlib import Path
import json, re, shutil, subprocess, tempfile
ROOT=Path(__file__).resolve().parents[1]
projects={p['id']:p for p in json.loads((ROOT/'content.json').read_text())['projects']}
def escape(s):
    for a,b in [('\\',r'\textbackslash{}'),('&',r'\&'),('%',r'\%'),('$',r'\$'),('#',r'\#'),('_',r'\_')]:
        s=s.replace(a,b)
    return s.replace('×',r'$\times$').replace('→',r'$\rightarrow$').replace('–','--').replace('—','--')
def project(key,role=False):
    p=projects[key]
    return '\\project{'+escape(p['title'])+'}{'+(escape(p['role']) if role else '')+'}\n\\begin{itemize}\n'+''.join('\\item '+escape(t)+'\n' for t in p['resume'])+'\\end{itemize}\n'
source=(ROOT/'resume.tex').read_text()
groups={
 'INTERNSHIP':['autoharness','workbench','evaluation','finance-sandbox','medical-autope'],
 'RESEARCH':['robowm-bench','rewardweaver','multi-agent-benchmark','autope','flyreview'],
 'TOOLS':['educate-flywheel','echo']}
for name,keys in groups.items():
    replacement='% BEGIN '+name+'\n'+''.join(project(k,name=='RESEARCH') for k in keys)+'% END '+name
    source=re.sub(r'% BEGIN '+name+r'\n.*?% END '+name,lambda m:replacement,source,flags=re.S)
(ROOT/'resume.tex').write_text(source)
engine=shutil.which('tectonic') or shutil.which('xelatex')
if not engine:
    raise SystemExit('Install Tectonic or XeLaTeX, then rerun this script. resume.tex is ready.')
with tempfile.TemporaryDirectory(prefix='resume-latex-') as directory:
    if Path(engine).name=='tectonic':
        subprocess.run([engine,'--outdir',directory,str(ROOT/'resume.tex')],check=True)
    else:
        for _ in range(2):
            subprocess.run([engine,'-interaction=nonstopmode','-halt-on-error','-output-directory='+directory,str(ROOT/'resume.tex')],check=True)
    shutil.copy2(Path(directory)/'resume.pdf',ROOT/'resume.pdf')
print('Updated resume.tex and resume.pdf from content.json.')
