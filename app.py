from flask import Flask, request, redirect, url_for, render_template_string, flash
import sqlite3
import os
from pathlib import Path

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "demo-only-change-before-production")

# 本地默认保存在项目目录；上线后可通过 DATABASE_PATH 指定持久化数据库位置
DB_PATH = Path(os.environ.get("DATABASE_PATH", str(Path(__file__).with_name("culture.db"))))

PAGE = r"""
<!doctype html>
<html lang="zh-CN">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="川蜀琉璃：传统琉璃文化的现代传承与创新发展">
    <title>{{ title }}｜川蜀琉璃</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
<header class="site-header">
    <a class="brand" href="{{ url_for('home') }}">
        <span class="brand-mark">琉</span>
        <span><strong>川蜀琉璃</strong><small>LIULI · CULTURE & DESIGN</small></span>
    </a>
    <button class="menu-toggle" aria-label="打开导航" onclick="document.querySelector('.nav-links').classList.toggle('open')">☰</button>
    <nav class="nav-links">
        <a href="{{ url_for('home') }}#story">项目概述</a>
        <a href="{{ url_for('culture_list') }}">文化档案</a>
        <a href="{{ url_for('home') }}#products">产品与服务</a>
        <a href="{{ url_for('home') }}#innovation">技术创新</a>
        <a class="nav-cta" href="{{ url_for('customize') }}">商务定制 ↗</a>
    </nav>
</header>

{% with messages = get_flashed_messages() %}
  {% if messages %}
  <div class="flash-wrap">{% for message in messages %}<div class="flash">{{ message }}</div>{% endfor %}</div>
  {% endif %}
{% endwith %}

{% if page == "home" %}
<section class="hero">
    <div class="hero-wash"></div>
    <div class="hero-content">
        <p class="eyebrow"><span></span> 非遗传承 · 当代设计 · 川蜀新意</p>
        <h1>让千年琉璃之美<br><em>照见当代生活</em></h1>
        <p class="hero-copy">以传统琉璃工艺为根，以现代设计为桥，探索文化传承、创意产品与生活美学的更多可能。</p>
        <div class="hero-actions">
            <a class="button button-dark" href="#products">探索琉璃作品 <span>↗</span></a>
            <a class="text-link" href="{{ url_for('culture_list') }}">走进琉璃文化 <span>→</span></a>
        </div>
        <div class="hero-note"><span class="note-line"></span> 传统工艺 · 现代表达</div>
    </div>
    <div class="hero-seal" aria-hidden="true"><span>川</span><span>蜀</span><span>琉</span><span>璃</span></div>
    <div class="hero-caption">GLASS ART / SICHUAN</div>
</section>

<section class="intro-strip" id="story">
    <div class="intro-label"><span class="section-index">01 / 项目概述</span><span class="tiny-rule"></span></div>
    <div class="intro-main">
        <h2>让传统工艺，<br><em>在当代重新发光。</em></h2>
        <p>“川蜀琉璃”以传承和弘扬中国传统琉璃文化为核心，结合现代设计理念、数字化技术与市场需求，探索兼具艺术价值、实用性与文化内涵的琉璃产品。</p>
        <p>项目希望连接设计、制作、销售与文化传播，让琉璃之美走进日常生活，也为青年创意实践提供新的舞台。</p>
        <a class="under-link" href="{{ url_for('culture_list') }}">阅读文化档案 <span>↗</span></a>
    </div>
    <div class="intro-stamp">以琉为媒<br>以艺传心</div>
</section>

<section class="section paper-section" id="background">
    <div class="section-heading">
        <div><span class="section-index">02 / 项目背景</span><h2>传承有根，创新有光</h2></div>
        <p>在传统工艺与当代生活之间，<br>寻找新的连接方式。</p>
    </div>
    <div class="three-points">
        <article class="point-card"><span class="point-number">一</span><h3>文化传承</h3><p>记录琉璃艺术的历史脉络与制作技艺，关注传统工艺的保护、整理与代际传承。</p></article>
        <article class="point-card"><span class="point-number">二</span><h3>市场机遇</h3><p>回应文化消费、艺术收藏、特色礼品与旅游纪念品等场景的多样化需求。</p></article>
        <article class="point-card"><span class="point-number">三</span><h3>青年参与</h3><p>通过现代设计、文化体验和创意实践，吸引更多年轻人了解并参与琉璃文化。</p></article>
    </div>
</section>

<section class="section product-section" id="products">
    <div class="section-heading">
        <div><span class="section-index">03 / 产品与服务</span><h2>琉光入器，雅意入常</h2></div>
        <a class="under-link" href="{{ url_for('culture_list') }}">浏览文化档案 <span>↗</span></a>
    </div>
    <div class="product-grid">
        <article class="product-card product-large">
            <div class="product-image"><img src="{{ url_for('static', filename='images/product-blue.jpg') }}" alt="蓝绿色琉璃艺术作品" loading="lazy"><span class="image-index">01</span></div>
            <div class="product-info"><span class="product-type">ART & HOME</span><h3>家居装饰</h3><p>以通透光泽和流动色彩，为空间带来艺术感。可探索琉璃摆件、灯具与装饰艺术。</p></div>
        </article>
        <article class="product-card">
            <div class="product-image"><img src="{{ url_for('static', filename='images/product-necklace.jpg') }}" alt="琉璃珠宝首饰" loading="lazy"><span class="image-index">02</span></div>
            <div class="product-info"><span class="product-type">JEWELRY</span><h3>珠宝首饰</h3><p>将琉璃的色彩与质感融入日常佩饰，表达独特的个人审美。</p></div>
        </article>
        <article class="product-card">
            <div class="product-image"><img src="{{ url_for('static', filename='images/product-vessel.jpg') }}" alt="琉璃器皿与文创作品" loading="lazy"><span class="image-index">03</span></div>
            <div class="product-info"><span class="product-type">CULTURAL CREATION</span><h3>川蜀文创</h3><p>结合地方历史、民俗与文化符号，开发具有地域特色的文创作品。</p></div>
        </article>
        <article class="product-card">
            <div class="product-image"><img src="{{ url_for('static', filename='images/product-glass.jpg') }}" alt="彩色琉璃作品" loading="lazy"><span class="image-index">04</span></div>
            <div class="product-info"><span class="product-type">CUSTOM MADE</span><h3>定制服务</h3><p>面向企业礼品、纪念品与个性化创意需求，探索专属设计方案。</p></div>
        </article>
    </div>
    <div class="service-bar">
        <div><span class="service-icon">✳</span><span><strong>设计定制</strong><small>根据需求探索个性化设计</small></span></div>
        <div><span class="service-icon">◉</span><span><strong>文化体验</strong><small>工艺体验、文化讲座与展览</small></span></div>
        <div><span class="service-icon">✧</span><span><strong>服务保障</strong><small>建立清晰的沟通与售后流程</small></span></div>
    </div>
</section>

<section class="section innovation-section" id="innovation">
    <div class="innovation-photo"><img src="{{ url_for('static', filename='images/artisan-work.jpg') }}" alt="传统琉璃工艺制作过程" loading="lazy"><div class="photo-caption">CRAFT IN MOTION<br><span>手艺，是时间留下的光。</span></div></div>
    <div class="innovation-copy">
        <span class="section-index">04 / 技术实现</span>
        <h2>古法为根，<br><em>新技为翼。</em></h2>
        <p>尊重传统琉璃制作经验，同时探索数字技术如何帮助设计、记录与传播，让古老工艺拥有更多当代表达。</p>
        <div class="tech-list">
            <div><span>01</span><section><h3>传统工艺传承</h3><p>以工艺记录、专业顾问与师徒培养为基础，重视技艺经验的整理与延续。</p></section></div>
            <div><span>02</span><section><h3>数字设计赋能</h3><p>探索数字化设计软件、3D 打印与 AI 辅助设计在造型研发中的应用。</p></section></div>
            <div><span>03</span><section><h3>品质与研发</h3><p>关注原材料、制作流程与成品检验，并通过合作研发持续探索新产品。</p></section></div>
        </div>
    </div>
</section>

<section class="section market-section" id="market">
    <div class="section-heading">
        <div><span class="section-index">05 / 市场与商业模式</span><h2>让琉璃走向更多生活场景</h2></div>
        <p>从一件作品出发，连接更多<br>消费者、空间与文化伙伴。</p>
    </div>
    <div class="market-grid">
        <article><span>01</span><h3>艺术与家居</h3><p>面向文化艺术爱好者、收藏者及注重空间美学的人群。</p></article>
        <article><span>02</span><h3>文创与礼品</h3><p>面向企业礼品、文化交流、纪念礼品与定制需求。</p></article>
        <article><span>03</span><h3>旅游与体验</h3><p>探索地方特色旅游纪念品、工艺体验与文化讲座。</p></article>
        <article><span>04</span><h3>线上与合作</h3><p>结合电商、社交媒体、展览活动与机构联名，拓展传播渠道。</p></article>
    </div>
    <div class="business-note"><span class="note-symbol">“</span><p>不止于销售一件琉璃作品，更希望让人理解作品背后的工艺、文化与创意。</p></div>
</section>

<section class="section roadmap-section" id="roadmap">
    <div class="section-heading">
        <div><span class="section-index">06 / 项目实施计划</span><h2>循序而进，持续生长</h2></div>
        <p>以下为项目规划方向，<br>具体进度以实际执行为准。</p>
    </div>
    <div class="timeline">
        <article><span class="timeline-dot">01</span><div><small>PHASE ONE</small><h3>项目启动</h3><p>团队组建、市场调研、产品定位与线上宣传平台搭建。</p></div></article>
        <article><span class="timeline-dot">02</span><div><small>PHASE TWO</small><h3>产品研发</h3><p>开展产品设计、工艺咨询、供应链沟通与样品测试。</p></div></article>
        <article><span class="timeline-dot">03</span><div><small>PHASE THREE</small><h3>市场推广</h3><p>探索线上推广、展览展示、体验活动与合作渠道。</p></div></article>
        <article><span class="timeline-dot">04</span><div><small>PHASE FOUR</small><h3>稳定发展</h3><p>根据反馈迭代产品，逐步建设品牌并拓展合作网络。</p></div></article>
    </div>
</section>

<section class="finance-section">
    <div class="finance-inner">
        <div><span class="section-index light-index">07 / 财务规划</span><h2>以清晰规划，<br><em>支撑长期发展。</em></h2><p>以下为 PPT 中的计划目标，并非实际经营业绩；正式对外展示前建议进一步核定预算与预测口径。</p></div>
        <div class="finance-stats">
            <div><small>预计启动资金</small><strong>20<span>万元</span></strong></div>
            <div><small>第一年销售目标</small><strong>30<span>万元</span></strong></div>
            <div><small>第二年销售目标</small><strong>40<span>万元</span></strong></div>
            <div><small>第三年销售目标</small><strong>50<span>万元</span></strong></div>
        </div>
    </div>
</section>

<section class="section risk-section">
    <div class="section-heading">
        <div><span class="section-index">08 / 风险评估与应对</span><h2>以长期主义，守护每一道光</h2></div>
    </div>
    <div class="risk-grid">
        <div><h3>市场竞争</h3><p>持续探索产品创新与品牌表达，关注用户反馈与市场变化。</p></div>
        <div><h3>技艺传承</h3><p>通过工艺记录、人才培养与专业合作，支持传统技艺延续。</p></div>
        <div><h3>原料供应</h3><p>建立供应商沟通机制，关注材料质量、成本与供给稳定性。</p></div>
        <div><h3>文化传播</h3><p>通过体验、展览与内容介绍，提升公众对琉璃文化的理解。</p></div>
    </div>
</section>

<section class="contact-banner">
    <div class="contact-ornament">琉</div>
    <div><span class="section-index light-index">LET'S CREATE SOMETHING MEANINGFUL</span><h2>让文化灵感，<br>成为独特的作品。</h2><p>欢迎就文创设计、企业礼品与文化合作提交需求。</p></div>
    <a class="button button-light" href="{{ url_for('customize') }}">提交定制需求 <span>↗</span></a>
</section>

{% elif page == "culture" %}
<section class="page-hero compact-hero"><span class="section-index">CULTURE ARCHIVE / 文化档案</span><h1>认识琉璃，<em>从文化开始。</em></h1><p>从传统工艺到当代设计，逐步记录川蜀琉璃项目的文化脉络。</p></section>
<main class="section archive-section">
    <form class="search-form" action="{{ url_for('culture_list') }}" method="get">
        <input name="q" value="{{ keyword }}" placeholder="搜索文化、工艺或产品关键词">
        <button class="button button-dark" type="submit">搜索 ↗</button>
    </form>
    <div class="archive-grid">
    {% for item in items %}
        <article class="archive-card"><span class="section-index">{{ item["category"] }}</span><h2>{{ item["title"] }}</h2><p>{{ item["summary"] }}</p><a class="under-link" href="{{ url_for('culture_detail', item_id=item['id']) }}">阅读详情 →</a></article>
    {% else %}<p>没有找到相关内容，请更换关键词试试。</p>{% endfor %}
    </div>
</main>

{% elif page == "detail" %}
<section class="page-hero compact-hero"><span class="section-index">CULTURE ARCHIVE / {{ item["category"] }}</span><h1>{{ item["title"] }}</h1><p>{{ item["summary"] }}</p></section>
<main class="section detail-section"><article class="detail-paper"><span class="section-index">文化记录</span><h2>项目简介</h2><p>{{ item["summary"] }}</p><h2>历史与工艺</h2><p>{{ item["history"] }}</p><a class="button button-dark" href="{{ url_for('culture_list') }}">返回文化档案</a></article></main>

{% elif page == "customize" %}
<section class="page-hero compact-hero"><span class="section-index">CUSTOMIZATION / 商务定制</span><h1>为每一份心意，<em>寻找独特表达。</em></h1><p>请填写您的定制想法。当前版本用于演示需求收集流程。</p></section>
<main class="section form-layout">
    <div class="form-aside"><span class="section-index">LET'S TALK</span><h2>把灵感，<br><em>交给琉璃。</em></h2><p>企业礼品、文化创意、活动合作或个性化作品，都可以从一次沟通开始。</p><div class="aside-seal">川蜀<br>琉璃</div></div>
    <form class="custom-form" method="post">
        <div class="form-row"><label>企业或个人名称 *<input name="company" required maxlength="100" value="{{ form.get('company','') }}"></label><label>联系人 *<input name="contact" required maxlength="50" value="{{ form.get('contact','') }}"></label></div>
        <div class="form-row"><label>电子邮箱 *<input name="email" type="email" required maxlength="120" value="{{ form.get('email','') }}"></label><label>联系电话<input name="phone" maxlength="30" value="{{ form.get('phone','') }}"></label></div>
        <label>定制类型 *<select name="service_type" required><option value="">请选择</option>{% for value in service_types %}<option value="{{ value }}" {% if form.get('service_type') == value %}selected{% endif %}>{{ value }}</option>{% endfor %}</select></label>
        <label>预算范围<input name="budget" placeholder="例如：1000—5000 元" value="{{ form.get('budget','') }}"></label>
        <label>具体需求 *<textarea name="description" rows="5" required maxlength="3000" placeholder="请描述用途、数量、风格偏好、交付时间等">{{ form.get('description','') }}</textarea></label>
        <p class="privacy-note">演示提示：请勿填写身份证号、银行卡号等敏感信息。</p>
        <button class="button button-dark" type="submit">提交定制需求 <span>↗</span></button>
    </form>
</main>

{% elif page == "success" %}
<section class="page-hero success-hero"><span class="success-mark">✓</span><h1>感谢您的信任。</h1><p>定制需求已提交。当前演示版会将记录保存在网站数据库中，但不会自动发送邮件。</p><a class="button button-dark" href="{{ url_for('home') }}">返回首页</a></section>
{% endif %}

<footer class="site-footer">
    <div class="footer-top"><a class="brand footer-brand" href="{{ url_for('home') }}"><span class="brand-mark">琉</span><span><strong>川蜀琉璃</strong><small>LIULI · CULTURE & DESIGN</small></span></a><p>传统工艺 · 当代设计 · 川蜀新意</p><a href="{{ url_for('customize') }}">商务合作 ↗</a></div>
    <div class="footer-bottom"><span>© 川蜀琉璃 · 文化展示与创意项目演示网站</span><span>让传统文化在当代生活中继续发光</span></div>
</footer>
</body>
</html>
"""

CULTURE_SEED = [
    ("琉璃文化与历史", "文化传承", "琉璃艺术承载着悠久的历史文化底蕴，其材质、色彩与制作方式形成独特的艺术语言。项目以文化记录和内容传播为基础，探索传统琉璃文化在当代的展示方式。"),
    ("传统琉璃制作工艺", "传统工艺", "传统琉璃制作需要对材料、火候、造型和工艺流程有细致把握。项目规划提出通过工艺顾问、师徒传承与数字化记录，支持传统经验的整理与传递。"),
    ("川蜀特色文化创意", "文化创意", "结合四川地区的历史文化与民俗元素，可探索开发地方特色琉璃文创产品，例如地域主题摆件、纪念品与文化礼品。具体设计应尊重文化来源并经过充分调研。"),
    ("数字设计与琉璃创新", "技术创新", "数字化设计软件、3D 打印及 AI 辅助设计可作为创意研发的探索方向，帮助设计师研究复杂造型与个性化表达；具体工艺适配需通过样品测试确认。"),
    ("琉璃与生活美学", "当代生活", "琉璃的通透质感和色彩表现可以延伸至家居装饰、珠宝首饰、文化创意和个性化定制等生活场景。")
]

def get_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS culture (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                category TEXT NOT NULL,
                summary TEXT NOT NULL,
                history TEXT NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS custom_requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company TEXT NOT NULL,
                contact TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT,
                service_type TEXT NOT NULL,
                budget TEXT,
                description TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        count = conn.execute("SELECT COUNT(*) FROM culture").fetchone()[0]
        if count == 0:
            conn.executemany(
                "INSERT INTO culture (title, category, summary, history) VALUES (?, ?, ?, ?)",
                [(title, category, summary, history) for title, category, history in CULTURE_SEED for summary in [history]]
            )

@app.route("/")
def home():
    return render_template_string(PAGE, title="首页", page="home")

@app.route("/culture")
def culture_list():
    keyword = request.args.get("q", "").strip()
    with get_db() as conn:
        if keyword:
            search = f"%{keyword}%"
            items = conn.execute("""
                SELECT * FROM culture
                WHERE title LIKE ? OR category LIKE ? OR summary LIKE ? OR history LIKE ?
                ORDER BY id
            """, (search, search, search, search)).fetchall()
        else:
            items = conn.execute("SELECT * FROM culture ORDER BY id").fetchall()
    return render_template_string(PAGE, title="文化档案", page="culture", items=items, keyword=keyword)

@app.route("/culture/<int:item_id>")
def culture_detail(item_id):
    with get_db() as conn:
        item = conn.execute("SELECT * FROM culture WHERE id = ?", (item_id,)).fetchone()
    if item is None:
        return "没有找到该文化项目。", 404
    return render_template_string(PAGE, title=item["title"], page="detail", item=item)

@app.route("/customize", methods=["GET", "POST"])
def customize():
    service_types = ["企业礼品定制", "传统文化设计", "文化活动策划", "文化 IP 合作", "其他需求"]
    form = request.form if request.method == "POST" else {}
    if request.method == "POST":
        company = request.form.get("company", "").strip()
        contact = request.form.get("contact", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        service_type = request.form.get("service_type", "").strip()
        budget = request.form.get("budget", "").strip()
        description = request.form.get("description", "").strip()
        if not all([company, contact, email, service_type, description]):
            flash("请填写所有必填项目。")
        elif service_type not in service_types:
            flash("请选择有效的定制类型。")
        elif len(company) > 100 or len(contact) > 50 or len(email) > 120 or len(description) > 3000:
            flash("部分内容超出长度限制，请检查后重新提交。")
        else:
            with get_db() as conn:
                conn.execute("""
                    INSERT INTO custom_requests
                    (company, contact, email, phone, service_type, budget, description)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (company, contact, email, phone, service_type, budget, description))
            return redirect(url_for("success"))
    return render_template_string(PAGE, title="商务定制", page="customize", form=form, service_types=service_types)

@app.route("/success")
def success():
    return render_template_string(PAGE, title="提交成功", page="success")

# Render / Gunicorn 加载 app 时也会初始化演示数据库
init_db()

if __name__ == "__main__":
    app.run(debug=True)
