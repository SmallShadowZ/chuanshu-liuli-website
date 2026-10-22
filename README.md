# 川蜀琉璃 Flask 网站（PPT 融合版）

本项目根据用户提供的《“川蜀琉璃”——琉璃文化的现代传承与创新发展》PPT 内容和视觉风格制作。

## 本地运行（Windows + PyCharm + Python 3.13）

1. 解压 ZIP，在 PyCharm 中打开解压后的文件夹。
2. 打开 PyCharm 底部 Terminal。
3. 执行：
   ```bash
   python -m pip install -r requirements.txt
   python app.py
   ```
4. 浏览器访问 http://127.0.0.1:5000

## 页面
- `/` 首页：项目概述、产品与服务、技术创新、市场与商业模式、实施计划、财务规划、风险应对
- `/culture` 文化档案与搜索
- `/customize` 商务定制表单
- `/success` 提交成功页

## 设计
采用 PPT 的水墨山水、米白纸感、金色点缀和传统中式标题风格；网站产品图取自用户上传的 PPT 中的嵌入图片。

## 重新部署到 Render
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn app:app`
- Python 环境选 Python 3。

## 重要说明
1. 这是用于展示与学习的演示版本。商务表单目前写入 SQLite 数据库 `culture.db`，Render 免费实例的本地文件不保证持久保存，因此不要用它收集真实客户敏感信息。
2. 正式公开使用前，应配置强随机 `SECRET_KEY`、CSRF 防护、管理员身份验证、隐私政策、持久化数据库和备份。
3. PPT 中的财务部分有一处口径不一致：财务规划章节给出第一年至第三年销售目标 30、40、50 万元，预期成果部分另写“3年内实现年营收10.8万元”。网站暂展示财务规划章节的 30/40/50 万元目标，并标明是规划目标、不是实际业绩。正式对外展示前建议核对原始数据。
4. PPT 中的产品与市场信息作为项目规划内容展示，不代表相关产品已量产、渠道已建成或收入已实现。
