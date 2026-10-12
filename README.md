# 黄胜泽 · 技术履历

个人技术网站，围绕智能体评测、自进化与算法工程，包含实习专题、研究参与、个人工具及完整履历。

站点：https://huangshengzebluesky.github.io/

## 维护

- `content.json`：12 个项目的内容。修改标题、摘要、技术章节、简历条目和公开参考链接。
- `build.py`：生成首页、专题文章和网页版履历。
- `assets/style.css`：视觉和打印样式。
- `resume.pdf`：当前可下载的三页 LaTeX 完整版简历。
- `resume.tex`：可独立编译的 LaTeX 源码与排版模板。
- `scripts/build_resume_pdf.py`：从 `content.json` 同步项目文字到 LaTeX 源码，再编译 PDF。

本机安装 Tectonic 或 XeLaTeX 后，运行 `python3 scripts/build_resume_pdf.py`，将更新后的 `resume.tex` 和 PDF 一起提交。项目措辞统一修改 `content.json`，版式与教育、早期实习信息修改 `resume.tex`。

本地预览：

```bash
python3 build.py
python3 -m http.server 8765 --directory dist
```

推送到 `main` 后，GitHub Actions 自动构建并部署 GitHub Pages。静态网站不依赖数据库、第三方字体或前端运行框架。

## 内容约定

区分论文作者与研究贡献参与，区分模拟实验与业务效果。实验数字必须带任务、数据范围和评测口径；进行中的能力不能写成已交付结果。网站保留完整技术叙事，精简简历从各项目的 `resume` 条目继续删减。
