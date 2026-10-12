# 黄胜泽 · 技术履历与研究专题

网站：https://huangshengzebluesky.github.io/

网站展开技术细节，简历保留个人贡献与关键结果。内容覆盖12个专题，通过学习路径组织场景工程、组件自进化、论文阅读及人机协作。

## 内容与维护

- `content.json` 的 `projects`：专题摘要、正文、流程、对照表、公开来源和可交互修改面。
- `content.json` 的 `learning`：路线索引及 AutoPE、AutoHarness、RewardWeaver 的方法对照。
- `content.json` 的 `resume_profile`：精简简历唯一文字来源，网页和 LaTeX 共用。
- `scripts/sync_resume.py`：同步简历文字到既有 LaTeX 文件，不编译，不更换编辑器。
- `resume.tex`：当前可编辑的简历。使用编辑器编译并导出 PDF。
- `resume.pdf`：保留原三页长版文件以兼容已分享的旧链接；当前简历入口是 `resume.html` 和 LaTeX 源码。
- `build.py` 和 `assets/`：静态页面生成及阅读界面，无前端依赖。

更新正文后运行：

```bash
python3 scripts/sync_resume.py
python3 build.py
```

正在编辑另一位置的既有源文件时，可用 `--latex-path /absolute/path/resume.tex` 同步；编辑器会自动更新预览。不要在编辑期间另建替代文档。

推送到 `main` 后自动发布 GitHub Pages。PDF需要时从当前编辑器导出，再替换存档文件。

## 表述原则

论文作者与研究参与者分别记录；训练集对照、单案例机制演示、留出集与业务效果分别陈述。方法版本数量不代表有效算法数量，评分通过不代表所有行为都正确。个人专题中教学示例与实际实验分开，公开内容不包含客户原始数据或私人会话。
