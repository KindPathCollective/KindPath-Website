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

# Public contact email, used in the footer and on the Contact page.
EMAIL = "info@kindpathcollective.org"

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
    ("Access and Intake", range(33, 34)),
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

    nav_links = []
    for href, label in NAV:
        current = ' class="active" aria-current="page"' if is_active(href) else ""
        nav_links.append(f'<a href="{nav_href(href)}"{current}>{label}</a>')
    nav_html = "\n".join(nav_links)
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
<a class="skip-link" href="#main">Skip to content</a>
<div class="crisis-banner" role="region" aria-label="Urgent help">
  <div class="container">
    <p>In immediate danger? Call <a href="tel:000">000</a>. KindPath is not a crisis service &mdash; <a href="{prefix}get-help.html">see who to call for urgent help</a>.</p>
  </div>
</div>
<header class="site-header">
  <div class="container header-inner">
    <a href="{prefix}index.html" class="brand">
      <img src="{prefix}assets/kindpath-logo.png" alt="KindPath Collective" class="brand-logo" width="831" height="311">
    </a>
    <nav class="site-nav" aria-label="Primary">{nav_html}</nav>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="site-footer">
  <div class="container footer-inner">
    <div>
      <img src="{prefix}assets/kindpath-logo.png" alt="KindPath Collective" class="footer-logo" width="831" height="311">
      <p class="footer-tagline">Free, broad-spectrum advocacy and research on Bundjalung Country.</p>
    </div>
    <div class="footer-contact">
      <p>Bundjalung Country, Northern NSW</p>
      <p>Nimbin NSW</p>
      <p><a href="mailto:{EMAIL}">{EMAIL}</a></p>
      <p>ABN 29 486 496 313</p>
    </div>
  </div>
  <div class="container">
    <p class="footer-links"><a href="{prefix}get-help.html">Get help now</a><a href="{prefix}get-help.html#disclaimer">Not a crisis service</a><a href="{prefix}contact.html#referrals">How referrals work</a></p>
    <p class="footer-legal">&copy; 2026 KindPath Collective Inc. KindPath Collective Inc is building toward NDIS registration; supports are currently delivered under our founders&rsquo; own sole-trader arrangements.</p>
  </div>
</footer>
</body>
</html>
"""


def service_lines() -> str:
    """The four public service lines. Wording stays inside the brief and the existing registration caveat."""
    return """
    <ul class="service-grid">
      <li class="service-card">
        <h3>Free social advocacy</h3>
        <p>Free social advocacy via the Life-Field tool. No NDIS plan is needed for this advocacy.</p>
      </li>
      <li class="service-card">
        <h3>NDIS Specialist Support Coordination</h3>
        <p>Specialist Support Coordination. Registration is still in progress, as noted below.</p>
      </li>
      <li class="service-card">
        <h3>KindPath Succession</h3>
        <p>Mentoring for people about to leave prison.</p>
      </li>
      <li class="service-card">
        <h3>Social Impact Consultancy</h3>
        <p>Social impact consultancy, alongside the advocacy and research.</p>
      </li>
    </ul>
    <p class="registration-note">KindPath Collective Inc is building toward NDIS registration. Until that registration is complete, supports are delivered under our founders&rsquo; own sole-trader arrangements.</p>
"""


def build_home():
    body = f"""
<section class="hero">
  <div class="container">
    <h1>Free, broad-spectrum advocacy and research</h1>
    <p class="hero-sub">Community authority before programs.</p>
    <p class="hero-location">Bundjalung Country, Northern NSW</p>
    <div class="hero-actions">
      <a href="#services" class="btn btn-primary">Four service lines</a>
      <a href="contact.html#referrals" class="btn btn-outline">How referrals work</a>
    </div>
  </div>
</section>

<section class="section" aria-labelledby="purpose-title">
  <div class="container prose">
    <h2 id="purpose-title">What we are here for</h2>
    <p>KindPath Collective is free, broad-spectrum advocacy and research on Bundjalung Country. Community authority comes before programs.</p>
    <p>We are not a crisis service. If you need help today, <a href="get-help.html">these services can help right now</a>.</p>
  </div>
</section>

<section class="section section-alt" id="services" aria-labelledby="services-title">
  <div class="container">
    <h2 id="services-title">Four service lines</h2>
{service_lines()}
    <p class="section-cta"><a href="services.html">More on how we work</a></p>
  </div>
</section>

<section class="section" aria-labelledby="promise-title">
  <div class="container">
    <h2 id="promise-title">How we work</h2>
    <ul class="promise-grid">
      <li class="promise-card">
        <h3>One steady presence</h3>
        <p>When services change and systems don&rsquo;t talk to each other, we stay. Free advocacy, no NDIS plan needed.</p>
      </li>
      <li class="promise-card">
        <h3>Private &mdash; your information stays yours</h3>
        <p>We only share what you consent to, with who you consent to, and nothing else.</p>
      </li>
      <li class="promise-card">
        <h3>You&rsquo;re in charge, always</h3>
        <p>Every plan starts from what matters to you &mdash; not the paperwork.</p>
      </li>
    </ul>
  </div>
</section>

<section class="section section-alt" aria-labelledby="reach-title">
  <div class="container prose">
    <h2 id="reach-title">How people reach us</h2>
    <p>We keep our caseload small on purpose, so we can stay with each person for the long haul. That means we work by referral: most people come to us through a support worker, GP, coordinator, local service, family member or carer.</p>
    <p>If you think we could help you or someone you support, <a href="contact.html#referrals">here is how referrals work</a>. If you need help today, <a href="get-help.html">these services can help right now</a>.</p>
    <h2>Research</h2>
    <p>Research sits with the advocacy. What we are learning, and the fact that we are not recruiting participants through this website, is on the <a href="about.html">About page</a>.</p>
  </div>
</section>
"""
    (ROOT / "index.html").write_text(
        page(
            "Home",
            body,
            description="Free, broad-spectrum advocacy and research on Bundjalung Country. Community authority before programs.",
        ),
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

    <h2>Why we stay small</h2>
    <p>The service system in our region is fragmented: people are passed between agencies, re-telling their story each time. What&rsquo;s usually missing is someone who stays. That&rsquo;s the job we&rsquo;ve chosen. To do it properly we keep a small, deliberate caseload and work by referral, partnering with other services rather than trying to become one big one.</p>

    <h2>What we&rsquo;re learning</h2>
    <p>Alongside our practice, we&rsquo;re researching how service fragmentation is actually experienced by practitioners and the people they support across the Northern Rivers, and how it has changed since the NDIS was introduced. We&rsquo;ll share what we find once it has been properly checked. We&rsquo;re not recruiting participants through this website.</p>

    <h2>Where we&rsquo;re at</h2>
    <p>KindPath Collective Inc is an incorporated association working toward its own NDIS Quality and
    Safeguards Commission registration. Until that registration is complete, supports are delivered by
    our founders as sole traders, operating to the same standard we&rsquo;re building the organisation
    around from day one &mdash; so the eventual transition is a change of paperwork, not a change of how
    support is actually delivered. You can read the practice standards we hold ourselves to on our
    <a href="policies/index.html">policies page</a>.</p>

    <h2>Our founders</h2>
    <p>KindPath was co-founded by Samuel Cross and Tristina Hay, based on Bundjalung Country in Nimbin, Northern NSW.</p>
  </div>
</section>
"""
    (ROOT / "about.html").write_text(
        page("About", body, active="about.html", description="KindPath Collective is a referral-based, broad-spectrum advocacy organisation on Bundjalung Country, Northern NSW."),
        encoding="utf-8",
    )


def build_services():
    body = f"""
<section class="section page-header">
  <div class="container">
    <h1>How we help</h1>
  </div>
</section>

<section class="section">
  <div class="container prose">
    <p>KindPath doesn&rsquo;t specialise in one system. We stay with people across the whole journey &mdash; through NDIS, health, housing, family and community services &mdash; as one consistent presence when everything else feels fragmented. Specialist services do the specialist work; we make sure the person isn&rsquo;t lost between them.</p>
    <p>We work by referral and keep our caseload deliberately small. <a href="contact.html#referrals">How referrals work</a>.</p>
  </div>
</section>

<section class="section" aria-labelledby="service-lines-title">
  <div class="container">
    <h2 id="service-lines-title">Four service lines</h2>
{service_lines()}
  </div>
</section>
"""
    (ROOT / "services.html").write_text(
        page(
            "Services",
            body,
            active="services.html",
            description="KindPath's four service lines: free social advocacy, NDIS Specialist Support Coordination, KindPath Succession, and Social Impact Consultancy.",
        ),
        encoding="utf-8",
    )


def build_contact():
    body = f"""
<section class="section page-header">
  <div class="container">
    <h1>Get in touch</h1>
  </div>
</section>
<section class="section">
  <div class="container prose">
    <div class="callout"><strong>Need help right now?</strong> KindPath is not a crisis or 24-hour service. In immediate danger, call <a href="tel:000">000</a>. For other urgent support, see <a href="get-help.html">Get help now</a>.</div>

    <h2 id="referrals">How referrals work</h2>
    <p>KindPath works by referral. We keep our caseload small so we can stay with each person over time, which means we usually can&rsquo;t take direct requests from the public. There&rsquo;s still a path to us:</p>
    <ul class="pathway-list">
      <li><strong>Already working with a service?</strong> Ask your support worker, support coordinator, case manager or GP to refer you to KindPath.</li>
      <li><strong>Not connected to any service yet?</strong> A local community service or your GP can talk with you about what you need and refer you on. For disability supports, the <a href="get-help.html">Disability Gateway</a> is a good first call. If you can&rsquo;t find anyone to refer you, email us and we&rsquo;ll help you find a way in.</li>
      <li><strong>Referring someone?</strong> Services, family members and carers can all refer. Email <a href="mailto:{EMAIL}?subject=Referral">{EMAIL}</a> with &ldquo;Referral&rdquo; in the subject. Please make sure the person knows about and agrees to the referral before you send their details.</li>
    </ul>
    <p>If we&rsquo;re not the right fit, or our caseload is full, we&rsquo;ll tell you honestly and help point to someone who is.</p>

    <h2>Referral partners</h2>
    <p>We work alongside local health, disability, community and government services across the Northern Rivers, and we&rsquo;re building formal referral partnerships now. Details will be listed here once they&rsquo;re confirmed.</p>

    <h2>Contact details</h2>
    <ul class="contact-list">
      <li><strong>Email:</strong> <a href="mailto:{EMAIL}">{EMAIL}</a></li>
      <li><strong>Location:</strong> Nimbin NSW (Bundjalung Country)</li>
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
        page("Contact", body, active="contact.html", description="How referrals to KindPath Collective work, and how to contact us."),
        encoding="utf-8",
    )


def build_get_help():
    body = """<section class="section page-header">
  <div class="container">
    <h1>Get help now</h1>
  </div>
</section>
<section class="section">
  <div class="container prose">
    <div class="callout"><strong>If you or someone else is in immediate danger, call <a href="tel:000">000</a></strong> (police, ambulance, fire).</div>
    <p>KindPath is not a crisis or 24-hour service, and we may not see messages quickly. If you need help now, these services can help.</p>
    <h2>Right now, any time</h2>
    <ul class="help-list">
      <li><strong>Lifeline</strong> &mdash; <a href="tel:131114">13 11 14</a><span>Crisis support and suicide prevention, 24/7. Text and online chat also available.</span></li>
      <li><strong>13YARN</strong> &mdash; <a href="tel:139276">13 92 76</a><span>Crisis support for Aboriginal and Torres Strait Islander people, 24/7, from mob.</span></li>
      <li><strong>NSW Mental Health Line</strong> &mdash; <a href="tel:1800011511">1800 011 511</a><span>Links you with NSW Health mental health services, 24/7. Also for worried family, friends and workers.</span></li>
      <li><strong>1800RESPECT</strong> &mdash; <a href="tel:1800737732">1800 737 732</a><span>Sexual assault, domestic and family violence counselling, 24/7.</span></li>
      <li><strong>Kids Helpline</strong> &mdash; <a href="tel:1800551800">1800 55 1800</a><span>Counselling for young people aged 5 to 25, 24/7.</span></li>
      <li><strong>Child Protection Helpline (NSW)</strong> &mdash; <a href="tel:132111">132 111</a><span>If you think a child or young person is at risk of significant harm, 24/7.</span></li>
      <li><strong>Link2home</strong> &mdash; <a href="tel:1800152152">1800 152 152</a><span>NSW homelessness information and referral, 24/7.</span></li>
      <li><strong>Police (non-emergency)</strong> &mdash; <a href="tel:131444">131 444</a><span>Police assistance when it isn&rsquo;t an emergency.</span></li>
    </ul>
    <h2>Business hours</h2>
    <ul class="help-list">
      <li><strong>Disability Gateway</strong> &mdash; <a href="tel:1800643787">1800 643 787</a><span>Information and referral for people with disability, families and carers. Monday to Friday, 8am to 8pm AEST.</span></li>
    </ul>
    <h2>If you need an interpreter or relay</h2>
    <p>Call TIS National on <a href="tel:131450">131 450</a> and ask them to connect you to any service above. If you are deaf or have difficulty hearing or speaking, use the National Relay Service &mdash; TTY users call <a href="tel:133677">133 677</a>, Speak and Listen users call <a href="tel:1300555727">1300 555 727</a>, then ask for the number you need.</p>
    <h2 id="disclaimer">KindPath is not a crisis service</h2>
    <p>KindPath Collective provides continuity-of-relationship advocacy by referral. We are not a crisis line, emergency service or 24-hour service. If you are in danger, in distress, or need urgent help outside our hours, contact 000 or one of the services above.</p>
    <p>Using this website, or contacting us through it, does not create a client or support relationship with KindPath. Information on this site is general and isn&rsquo;t a substitute for advice about your own situation.</p>
    <p class="footer-note" style="color:var(--muted);font-size:13px">Numbers checked 24 September 2026. If a number doesn&rsquo;t work, call 000 in an emergency and <a href="contact.html">let us know</a> so we can fix it.</p>
  </div>
</section>
"""
    (ROOT / "get-help.html").write_text(
        page("Get help now", body, active="get-help.html", description="Urgent and after-hours help in NSW. KindPath Collective is not a crisis service."),
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
  --navy: #154A73;
  --yellow: #F7BC0D;
  --ink: #1a242c;
  --muted: #3d4c59;
  --bg: #f4f7f8;
  --surface: #ffffff;
  --border: #d5e0e8;
  --on-navy: #ffffff;
  --on-navy-soft: #e7eef3;
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
:target { scroll-margin-top: 11.5rem; }
body {
  margin: 0;
  font-family: -apple-system, 'Inter', system-ui, sans-serif;
  color: var(--ink);
  background: var(--bg);
  line-height: 1.6;
  font-size: 1.0625rem;
}
img { max-width: 100%; }
.container { width: min(67.5rem, 100%); margin-inline: auto; padding-inline: 1rem; }
a { color: var(--navy); text-decoration: underline; text-underline-offset: 0.15em; }
h1, h2, h3 { color: var(--navy); line-height: 1.25; text-align: left; }
h1 { font-size: clamp(1.75rem, 4vw + 1rem, 2.75rem); margin: 0 0 0.5rem; }
h2 { font-size: clamp(1.35rem, 1.5vw + 1rem, 1.7rem); margin: 0 0 1rem; }
h3 { font-size: 1.125rem; margin: 0 0 0.4rem; }

.skip-link {
  position: absolute;
  left: 0.75rem;
  top: 0;
  transform: translateY(-120%);
  background: var(--yellow);
  color: var(--navy);
  border: 2px solid var(--navy);
  padding: 0.6rem 0.9rem;
  z-index: 30;
  font-weight: 700;
  text-decoration: none;
}
.skip-link:focus { transform: none; top: 0.5rem; }

.site-header {
  background: var(--surface);
  border-bottom: 3px solid var(--navy);
  position: sticky;
  top: 0;
  z-index: 10;
}
.header-inner {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 0.25rem;
  padding-block: 0.75rem;
}
.brand-logo { display: block; height: 44px; width: auto; max-width: 70vw; }
.site-nav { display: flex; flex-wrap: wrap; gap: 0.15rem 0.85rem; width: 100%; }
.site-nav a {
  color: var(--muted);
  text-decoration: none;
  font-weight: 600;
  font-size: 1rem;
  min-height: 44px;
  display: inline-flex;
  align-items: center;
  padding: 0.35rem 0.1rem;
  border-bottom: 3px solid transparent;
}
.site-nav a:hover, .site-nav a.active { color: var(--navy); border-bottom-color: var(--navy); }

.hero { background: var(--navy); color: var(--on-navy); padding: 2.5rem 0 2.25rem; text-align: center; }
.hero h1, .hero h2, .hero h3 { color: var(--on-navy); text-align: center; }
.hero-sub { font-size: 1.25rem; color: var(--yellow); font-weight: 700; margin: 0 0 0.35rem; }
.hero-location { color: var(--on-navy-soft); margin: 0 0 1.5rem; font-size: 1rem; }
.hero-actions { display: flex; flex-direction: column; gap: 0.75rem; align-items: stretch; }

.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 44px;
  padding: 0.7rem 1.25rem;
  border-radius: 999px;
  text-decoration: none;
  font-weight: 700;
  font-size: 1rem;
  line-height: 1.2;
}
.btn-primary { background: var(--yellow); color: var(--navy); border: 2px solid var(--navy); }
.btn-primary:hover { background: #fff; }
.btn-outline { border: 2px solid var(--on-navy); color: var(--on-navy); background: transparent; }
.btn-outline:hover { background: rgba(255,255,255,.12); }

.section { padding: 2.5rem 0; }
.section-alt { background: var(--surface); border-top: 1px solid var(--border); border-bottom: 1px solid var(--border); }
.page-header { padding: 2rem 0 0.25rem; }
.page-header h1 { margin-bottom: 0; }

.promise-grid, .service-grid {
  list-style: none;
  padding: 0;
  margin: 1.25rem 0 0;
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
}
.promise-card, .service-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-top: 4px solid var(--navy);
  border-radius: 14px;
  padding: 1.15rem 1.15rem 1.25rem;
}
.registration-note {
  margin: 1.25rem 0 0;
  padding: 1rem 1.1rem;
  background: var(--bg);
  border: 1px solid var(--border);
  border-left: 4px solid var(--navy);
  border-radius: 10px;
  max-width: 46rem;
}
.section-cta { margin-top: 1.5rem; }
.section-cta a { font-weight: 700; }

.prose { max-width: 42rem; }
.prose h2 { margin-top: 2rem; }
.prose > h2:first-child { margin-top: 0; }
.prose p { margin: 0 0 1rem; }
.contact-list { list-style: none; padding: 0; }
.contact-list li { padding: 0.55rem 0; border-bottom: 1px solid var(--border); }

.policy-modules { display: grid; grid-template-columns: 1fr; gap: 1.5rem; }
.policy-module h3 { color: var(--navy); border-bottom: 3px solid var(--navy); padding-bottom: 0.4rem; }
.policy-list { list-style: none; padding: 0; margin: 0; }
.policy-list li { padding: 0.35rem 0; }
.policy-list a { color: var(--ink); }

.breadcrumb a { font-size: 0.95rem; color: var(--muted); }
.policy-doc { overflow-x: auto; }
.policy-doc h1 { font-size: 1.6rem; }
.policy-doc h2 { font-size: 1.15rem; margin-top: 1.6rem; }
.policy-doc ul, .policy-doc ol { padding-left: 1.25rem; }
.policy-doc table { width: 100%; border-collapse: collapse; margin: 1rem 0; font-size: 0.95rem; }
.policy-doc th, .policy-doc td { border: 1px solid var(--border); padding: 0.5rem 0.6rem; text-align: left; vertical-align: top; }
.policy-doc th { background: var(--bg); }

.site-footer { background: var(--navy); color: var(--on-navy-soft); padding: 2.5rem 0 1.25rem; margin-top: 2rem; }
.footer-inner { display: flex; flex-direction: column; gap: 1.5rem; }
.footer-logo {
  display: block;
  height: 44px;
  width: auto;
  max-width: 70vw;
  background: #fff;
  padding: 6px 8px;
  border-radius: 8px;
  margin-bottom: 0.75rem;
}
.footer-tagline { color: var(--yellow); font-weight: 700; margin: 0; max-width: 28rem; }
.footer-contact p { margin: 0.15rem 0; font-size: 1rem; }
.footer-contact a { color: var(--on-navy); }
.footer-legal {
  font-size: 0.875rem;
  color: var(--on-navy-soft);
  margin-top: 1.5rem;
  padding-top: 1rem;
  border-top: 1px solid rgba(255,255,255,.45);
}
.footer-links a {
  color: var(--on-navy);
  display: inline-block;
  margin: 0.15rem 1rem 0.15rem 0;
  padding-block: 0.45rem;
}

.crisis-banner { background: var(--navy); color: var(--on-navy); font-size: 1rem; }
.crisis-banner p { margin: 0; padding: 0.7rem 0; text-align: center; }
.crisis-banner a { color: var(--yellow); font-weight: 700; }
:focus-visible { outline: 3px solid var(--navy); outline-offset: 3px; }
.hero :focus-visible,
.site-footer :focus-visible,
.crisis-banner :focus-visible { outline-color: var(--yellow); }
.help-list { list-style: none; padding: 0; margin: 0 0 1.5rem; }
.help-list li { padding: 0.75rem 0; border-bottom: 1px solid var(--border); }
.help-list strong { color: var(--navy); }
.help-list a[href^="tel"] { font-weight: 700; }
.help-list span { display: block; color: var(--muted); font-size: 0.95rem; }
.callout {
  background: var(--surface);
  border: 1px solid var(--border);
  border-left: 4px solid var(--navy);
  border-radius: 10px;
  padding: 1rem 1.15rem;
  margin: 0 0 1.5rem;
}
.pathway-list { padding-left: 1.25rem; }
.pathway-list li { margin-bottom: 0.75rem; }

@media (min-width: 40rem) {
  .hero-actions { flex-direction: row; justify-content: center; }
  .hero-actions .btn { width: auto; }
  .service-grid { grid-template-columns: 1fr 1fr; }
}
@media (min-width: 48rem) {
  :target { scroll-margin-top: 6rem; }
  .container { padding-inline: 1.5rem; }
  .header-inner { flex-direction: row; align-items: center; justify-content: space-between; }
  .site-nav { width: auto; justify-content: flex-end; }
  .brand-logo, .footer-logo { height: 48px; }
  .section { padding: 4rem 0; }
  .hero { padding: 4.5rem 0 3.5rem; }
  .policy-modules { grid-template-columns: 1fr 1fr; gap: 2rem 3rem; }
  .footer-inner { flex-direction: row; justify-content: space-between; align-items: flex-start; }
}
@media (min-width: 64rem) {
  .promise-grid { grid-template-columns: repeat(3, 1fr); }
}
@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
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
    build_get_help()
    build_policies()
    print("Built site into", ROOT)
