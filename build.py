#!/usr/bin/env python3
"""
Static site generator for the KindPath Collective public website.

Run with: python build.py
Regenerates every .html file in the repo root and policies/ from the
templates and content below. Nothing here needs a build tool or server -
the output is plain static HTML/CSS, deployable to any static host
(GitHub Pages, Netlify, etc.).
"""
import re
from pathlib import Path
import markdown

ROOT = Path(__file__).parent
POLICIES_SRC = ROOT / "content" / "policies"
POLICIES_OUT = ROOT / "policies"
POLICIES_OUT.mkdir(exist_ok=True)

NAV = [
    ("index.html", "Home"),
    ("about.html", "About"),
    ("services.html", "Services"),
    ("policies/index.html", "Our Policies"),
    ("contact.html", "Contact"),
]

# NDIS Practice Standards module grouping, matching the folio's own index.
MODULES = [
    ("Rights and Responsibilities", range(1, 8)),
    ("Governance and Operational Management", range(8, 16)),
    ("Provision of Supports", range(16, 19)),
    ("Support Provision Environment", range(19, 21)),
    ("Workforce and Conduct", range(21, 33)),
]


def slugify(name: str) -> str:
    name = re.sub(r"^\d+_", "", name)
    name = name.replace("_", "-").lower()
    return name


def page(title: str, body: str, active: str = "", description: str = "") -> str:
    in_subdir = active == "policies"
    prefix = "../" if in_subdir else ""

    def nav_href(href: str) -> str:
        if in_subdir:
            # We're inside policies/, so policies/index.html -> index.html, everything else -> ../href
            return href.split("/")[-1] if href.startswith("policies/") else prefix + href
        return href

    def is_active(href: str) -> bool:
        if in_subdir:
            return href == "policies/index.html"
        return href == ("index.html" if active == "" else active)

    nav_html = "\n".join(
        f'<a href="{nav_href(href)}" class="{"active" if is_active(href) else ""}">{label}</a>'
        for href, label in NAV
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} | KindPath Collective</title>
<meta name="description" content="{description}">
<link rel="stylesheet" href="{prefix}assets/style.css">
</head>
<body>
<header class="site-header">
  <div class="container header-inner">
    <a href="{prefix}index.html" class="brand">
      <img src="{prefix}assets/kindpath-logo.png" alt="KindPath Collective" class="brand-logo">
    </a>
    <nav class="site-nav">{nav_html}</nav>
  </div>
</header>
<main>
{body}
</main>
<footer class="site-footer">
  <div class="container footer-inner">
    <div>
      <img src="{prefix}assets/kindpath-logo.png" alt="KindPath Collective" class="footer-logo">
      <p class="footer-tagline">Advocacy that is kind, clear, and on your side.</p>
    </div>
    <div class="footer-contact">
      <p>Bundjalung Country, Northern NSW</p>
      <p>557 Tuntable Falls Road, Nimbin NSW</p>
      <p><a href="mailto:sam@kindpathcollective.org">sam@kindpathcollective.org</a></p>
      <p>ABN 29 486 496 313</p>
    </div>
  </div>
  <div class="container">
    <p class="footer-legal">&copy; 2026 KindPath Collective Inc. KindPath Collective Inc is building toward NDIS registration; supports are currently delivered under our founders&rsquo; own sole-trader arrangements.</p>
  </div>
</footer>
</body>
</html>
"""


def build_home():
    body = """
<section class="hero">
  <div class="container">
    <h1>Advocacy &amp; NDIS Supports</h1>
    <p class="hero-sub">Kind, clear, and on your side.</p>
    <p class="hero-location">Bundjalung Country, Northern NSW</p>
    <div class="hero-actions">
      <a href="services.html" class="btn btn-primary">Our services</a>
      <a href="contact.html" class="btn btn-outline">Get in touch</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <h2>Our promise</h2>
    <div class="promise-grid">
      <div class="promise-card">
        <h3>Free social advocacy</h3>
        <p>Support to understand your rights and be heard, open to anyone, no NDIS plan needed.</p>
      </div>
      <div class="promise-card">
        <h3>Private &mdash; your information stays yours</h3>
        <p>We only share what you consent to, with who you consent to, and nothing else.</p>
      </div>
      <div class="promise-card">
        <h3>You&rsquo;re in charge, always</h3>
        <p>Every plan starts from what matters to you &mdash; not the paperwork.</p>
      </div>
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="container">
    <h2>Our services</h2>
    <div class="service-grid">
      <div class="service-card">
        <span class="service-status">Available now</span>
        <h3>Free social advocacy</h3>
        <p>Support to understand your rights and be heard &mdash; open to anyone, no NDIS plan needed.</p>
      </div>
      <div class="service-card">
        <span class="service-status">Available now</span>
        <h3>Goal &amp; action planning</h3>
        <p>Turning NDIS goals into real, practical plans, built around each person&rsquo;s own interests.</p>
      </div>
      <div class="service-card">
        <span class="service-status">Now, expanding</span>
        <h3>NDIS support &amp; coordination</h3>
        <p>Hands-on daily support, with connections to allied health and support coordinators.</p>
      </div>
      <div class="service-card">
        <span class="service-status">Expanding</span>
        <h3>Community &amp; connection</h3>
        <p>Helping people build the everyday relationships and community links that matter to them.</p>
      </div>
    </div>
    <p class="section-cta"><a href="services.html">More on how we work &rarr;</a></p>
  </div>
</section>
"""
    (ROOT / "index.html").write_text(
        page("Home", body, description="Free NDIS social advocacy, goal and action planning, and support coordination on Bundjalung Country, Northern NSW."),
        encoding="utf-8",
    )


def build_about():
    body = """
<section class="section page-header">
  <div class="container">
    <h1>Who we are</h1>
  </div>
</section>
<section class="section">
  <div class="container prose">
    <p>KindPath Collective is a broad-spectrum advocacy service, currently building toward full NDIS
    registration and operating today under our founders&rsquo; own sole-trader arrangements.</p>
    <p>We support people to understand their rights, make their own decisions, and get access to the
    services and supports they&rsquo;re entitled to &mdash; without jargon, and without an agenda that
    isn&rsquo;t theirs.</p>
    <p>Our approach starts from the person, not the paperwork: we listen first, then build the plan
    around what actually matters to them.</p>

    <h2>Where we&rsquo;re at</h2>
    <p>KindPath Collective Inc is an incorporated association working toward its own NDIS Quality and
    Safeguards Commission registration. Until that registration is complete, supports are delivered by
    our founders as sole traders, operating to the same standard we&rsquo;re building the organisation
    around from day one &mdash; so the eventual transition is a change of paperwork, not a change of how
    support is actually delivered. You can read the practice standards we hold ourselves to on our
    <a href="policies/index.html">policies page</a>.</p>

    <h2>Our founder</h2>
    <p>KindPath was founded by Samuel Cross, based on Bundjalung Country in Nimbin, Northern NSW.</p>
  </div>
</section>
"""
    (ROOT / "about.html").write_text(
        page("About", body, active="about.html", description="KindPath Collective is a broad-spectrum NDIS advocacy service based on Bundjalung Country, Northern NSW."),
        encoding="utf-8",
    )


def build_services():
    body = """
<section class="section page-header">
  <div class="container">
    <h1>Our services</h1>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="service-grid">
      <div class="service-card">
        <span class="service-status">Available now</span>
        <h3>Free social advocacy</h3>
        <p>Support to understand your rights and be heard &mdash; open to anyone, no NDIS plan needed.</p>
      </div>
      <div class="service-card">
        <span class="service-status">Available now</span>
        <h3>Goal &amp; action planning</h3>
        <p>Turning NDIS goals into real, practical plans, built around each person&rsquo;s own interests.</p>
      </div>
      <div class="service-card">
        <span class="service-status">Now, expanding</span>
        <h3>NDIS support &amp; coordination</h3>
        <p>Hands-on daily support, with connections to allied health and support coordinators.</p>
      </div>
      <div class="service-card">
        <span class="service-status">Expanding</span>
        <h3>Community &amp; connection</h3>
        <p>Helping people build the everyday relationships and community links that matter to them.</p>
      </div>
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="container">
    <h2>NDIS support, in practice</h2>
    <div class="promise-grid">
      <div class="promise-card">
        <h3>Plan navigation</h3>
        <p>Making sense of a plan&rsquo;s funding categories and what they can actually be used for.</p>
      </div>
      <div class="promise-card">
        <h3>Allied health &amp; support coordinator links</h3>
        <p>Working alongside a person&rsquo;s existing support coordinator and any allied health
        professionals, with clear consent for what&rsquo;s shared and with whom.</p>
      </div>
      <div class="promise-card">
        <h3>Goals into action</h3>
        <p>Every goal becomes a written, practical plan, built around a person&rsquo;s own gear,
        interests and routine &mdash; not a generic template.</p>
      </div>
    </div>
  </div>
</section>
"""
    (ROOT / "services.html").write_text(
        page("Services", body, active="services.html", description="Free social advocacy, goal and action planning, NDIS support coordination, and community connection."),
        encoding="utf-8",
    )


def build_contact():
    body = """
<section class="section page-header">
  <div class="container">
    <h1>Get in touch</h1>
  </div>
</section>
<section class="section">
  <div class="container prose">
    <p>However is easiest for you &mdash; email, phone, through a support coordinator, or dropping by.
    There&rsquo;s no wrong way to reach out.</p>
    <ul class="contact-list">
      <li><strong>Email:</strong> <a href="mailto:sam@kindpathcollective.org">sam@kindpathcollective.org</a></li>
      <li><strong>Location:</strong> 557 Tuntable Falls Road, Nimbin NSW (Bundjalung Country)</li>
      <li><strong>ABN:</strong> 29 486 496 313</li>
    </ul>
    <h2>Want to make a complaint or give feedback?</h2>
    <p>You can tell us directly, in whatever way is easiest for you &mdash; and you can always contact
    the NDIS Commission directly too, on <strong>1800 035 544</strong>. See our
    <a href="policies/feedback-and-complaints-management-policy.html">Feedback and Complaints Management Policy</a>
    for the full detail.</p>
  </div>
</section>
"""
    (ROOT / "contact.html").write_text(
        page("Contact", body, active="contact.html", description="Get in touch with KindPath Collective."),
        encoding="utf-8",
    )


def build_policies():
    files = sorted(POLICIES_SRC.glob("*.md"))
    entries = []  # (number, title, slug)
    for f in files:
        m = re.match(r"(\d+)_(.+)", f.stem)
        num = int(m.group(1))
        try:
            raw_md = f.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            # markitdown's stdout redirect on Windows can mangle smart quotes into cp1252
            raw_md = f.read_text(encoding="cp1252")
        title_match = re.search(r"^#\s+(.+)$", raw_md, re.MULTILINE)
        title = title_match.group(1).strip() if title_match else f.stem
        slug = slugify(f.stem)
        entries.append((num, title, slug))

        html_body = markdown.markdown(raw_md, extensions=["extra", "sane_lists"])
        body = f"""
<section class="section page-header">
  <div class="container">
    <p class="breadcrumb"><a href="index.html">&larr; All policies</a></p>
  </div>
</section>
<section class="section">
  <div class="container prose policy-doc">
    {html_body}
  </div>
</section>
"""
        (POLICIES_OUT / f"{slug}.html").write_text(
            page(title, body, active="policies", description=f"{title} - KindPath Collective practice standards."),
            encoding="utf-8",
        )

    entries.sort(key=lambda e: e[0])
    by_module = []
    for mod_name, mod_range in MODULES:
        mod_entries = [e for e in entries if e[0] in mod_range]
        by_module.append((mod_name, mod_entries))

    list_html = ""
    for mod_name, mod_entries in by_module:
        items = "\n".join(
            f'<li><a href="{slug}.html">{num}. {title}</a></li>'
            for num, title, slug in mod_entries
        )
        list_html += f"""
    <div class="policy-module">
      <h3>{mod_name}</h3>
      <ul class="policy-list">
{items}
      </ul>
    </div>
"""

    body = f"""
<section class="section page-header">
  <div class="container">
    <h1>Our policies &amp; practice standards</h1>
  </div>
</section>
<section class="section">
  <div class="container prose">
    <p>KindPath Collective Inc is currently building toward NDIS Quality and Safeguards Commission
    registration. The policies below describe the practice standard our founders operate to today,
    as sole traders, in preparation for KindPath itself becoming the registered operating entity
    &mdash; the practice is real now; full registration is still in progress.</p>
  </div>
</section>
<section class="section section-alt">
  <div class="container">
    <div class="policy-modules">
{list_html}
    </div>
  </div>
</section>
"""
    (POLICIES_OUT / "index.html").write_text(
        page("Our Policies", body, active="policies", description="The NDIS practice standards KindPath Collective operates to."),
        encoding="utf-8",
    )


def build_css():
    css = """
:root {
  --navy: #0e3a5e;
  --navy-dark: #081726;
  --navy-light: #144b78;
  --gold: #f5b90a;
  --sage: #9cbc8a;
  --ink: #1e2a33;
  --muted: #5b6670;
  --bg: #f7f9fb;
  --surface: #ffffff;
  --border: #e3ebf2;
}
* { box-sizing: border-box; }
body {
  margin: 0; font-family: -apple-system, 'Inter', system-ui, sans-serif;
  color: var(--ink); background: var(--bg); line-height: 1.6;
}
.container { max-width: 1080px; margin: 0 auto; padding: 0 24px; }
a { color: var(--navy-light); }
h1, h2, h3 { color: var(--navy); line-height: 1.25; }
h1 { font-size: 40px; margin: 0 0 8px; }
h2 { font-size: 26px; margin: 0 0 20px; }
h3 { font-size: 18px; margin: 0 0 8px; }

.site-header { background: var(--surface); border-bottom: 1px solid var(--border); position: sticky; top: 0; z-index: 10; }
.header-inner { display: flex; align-items: center; justify-content: space-between; padding: 14px 24px; }
.brand-logo { height: 40px; display: block; }
.site-nav { display: flex; gap: 24px; }
.site-nav a { color: var(--muted); text-decoration: none; font-weight: 500; font-size: 14px; padding: 6px 0; border-bottom: 2px solid transparent; }
.site-nav a:hover, .site-nav a.active { color: var(--navy); border-bottom-color: var(--gold); }

.hero { background: linear-gradient(160deg, var(--navy) 0%, var(--navy-dark) 100%); color: #fff; padding: 90px 0 70px; text-align: center; }
.hero h1 { color: #fff; font-size: 48px; margin-bottom: 12px; }
.hero-sub { font-size: 22px; color: var(--gold); font-style: italic; margin: 0 0 6px; }
.hero-location { color: rgba(255,255,255,.7); margin: 0 0 32px; font-size: 14px; }
.hero-actions { display: flex; gap: 16px; justify-content: center; }

.btn { display: inline-block; padding: 12px 28px; border-radius: 999px; text-decoration: none; font-weight: 600; font-size: 15px; }
.btn-primary { background: var(--gold); color: var(--navy-dark); }
.btn-primary:hover { filter: brightness(1.06); }
.btn-outline { border: 1.5px solid rgba(255,255,255,.5); color: #fff; }
.btn-outline:hover { border-color: #fff; }

.section { padding: 64px 0; }
.section-alt { background: var(--surface); border-top: 1px solid var(--border); border-bottom: 1px solid var(--border); }
.section h2 { text-align: center; }
.page-header { padding: 56px 0 8px; }
.page-header h1 { margin-bottom: 0; }

.promise-grid, .service-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; margin-top: 32px; }
.service-grid { grid-template-columns: repeat(2, 1fr); }
.promise-card, .service-card {
  background: var(--surface); border: 1px solid var(--border); border-radius: 14px; padding: 24px;
}
.service-status {
  display: inline-block; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: .05em;
  color: var(--navy); background: rgba(156,188,138,.25); padding: 3px 10px; border-radius: 999px; margin-bottom: 10px;
}
.section-cta { text-align: center; margin-top: 32px; }
.section-cta a { font-weight: 600; text-decoration: none; }

.prose { max-width: 760px; margin: 0 auto; }
.prose h2 { margin-top: 40px; }
.prose p { margin: 0 0 16px; }
.contact-list { list-style: none; padding: 0; }
.contact-list li { padding: 6px 0; border-bottom: 1px solid var(--border); }

.policy-modules { display: grid; grid-template-columns: repeat(2, 1fr); gap: 32px 48px; }
.policy-module h3 { color: var(--navy); border-bottom: 2px solid var(--gold); padding-bottom: 8px; }
.policy-list { list-style: none; padding: 0; margin: 0; }
.policy-list li { padding: 6px 0; }
.policy-list a { text-decoration: none; color: var(--ink); font-size: 14px; }
.policy-list a:hover { color: var(--navy-light); text-decoration: underline; }

.breadcrumb a { text-decoration: none; font-size: 13px; color: var(--muted); }
.policy-doc h1 { font-size: 26px; }
.policy-doc h2 { font-size: 18px; text-align: left; margin-top: 28px; }
.policy-doc ul, .policy-doc ol { padding-left: 22px; }
.policy-doc table { width: 100%; border-collapse: collapse; margin: 16px 0; font-size: 14px; }
.policy-doc th, .policy-doc td { border: 1px solid var(--border); padding: 8px 10px; text-align: left; }
.policy-doc th { background: var(--bg); }

.site-footer { background: var(--navy-dark); color: rgba(255,255,255,.85); padding: 40px 0 20px; margin-top: 40px; }
.footer-inner { display: flex; justify-content: space-between; gap: 32px; flex-wrap: wrap; }
.footer-logo { height: 34px; filter: brightness(0) invert(1); opacity: .9; margin-bottom: 10px; }
.footer-tagline { font-style: italic; color: var(--gold); margin: 0; }
.footer-contact p { margin: 2px 0; font-size: 14px; }
.footer-contact a { color: #fff; }
.footer-legal { font-size: 12px; color: rgba(255,255,255,.5); margin-top: 28px; padding-top: 16px; border-top: 1px solid rgba(255,255,255,.12); }

@media (max-width: 720px) {
  .promise-grid, .service-grid, .policy-modules { grid-template-columns: 1fr; }
  .header-inner { flex-direction: column; gap: 10px; }
  .site-nav { flex-wrap: wrap; justify-content: center; }
  .hero h1 { font-size: 34px; }
}
"""
    (ROOT / "assets").mkdir(exist_ok=True)
    (ROOT / "assets" / "style.css").write_text(css, encoding="utf-8")


if __name__ == "__main__":
    build_css()
    build_home()
    build_about()
    build_services()
    build_contact()
    build_policies()
    print("Built site into", ROOT)
