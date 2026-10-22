# 黄胜泽的技术博客

网站：https://huangshengzebluesky.github.io/

围绕智能体评测、系统自进化、城市预测与数学教育，记录问题、思路、架构、方法、数据和实验判断。首页按最新文章、阅读主线、全文索引与研究参与组织；代码仓库保留在独立资源页，作为延伸阅读。

## 内容维护

- `content.json`：技术文章、阅读路径和既有简历文字。文章区分已完成实验、教学示例与进行中的工作。
- `presentation.json`：每篇文章的问题、阅读要点及可点击的机制图解。
- `blog_home.py`：博客首页与资源索引。
- `blog_interactions.py`：文章内的数学演示结构。
- `open-source.json`：资源页的公开仓库和文档入口。
- `build.py` 与 `assets/`：静态页面、交互、文章订阅与站点索引。

运行 `python3 build.py` 生成 `dist/`；推送到 `main` 自动发布 GitHub Pages。

简历文字与 `resume.tex`、`resume.pdf` 单独维护；新增博客文章不会自动修改简历文件。不要把内部路径、账户、会话记录或原始业务数据放进公开文章。实验结果注明范围和时间，不将重复次数写成独立样本数量。
