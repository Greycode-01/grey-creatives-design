#!/usr/bin/env python3
"""Grey Creatives Design: static page generator.

Reads projects.json and writes every HTML page plus assets/js/data.js, the sitemap and the
small image thumbnails. The site itself has no build step; this script only exists so the
header, footer and the seven project pages stay identical. Run:  python3 _tools/build.py
"""
import html, json, os, random, re
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
SITE = "https://greycreativesdesign.vercel.app"      # change this if your Vercel domain is different
NAME = "Grey Creatives Design"
EMAIL = "gr3ycreatives@gmail.com"
PHONE = "09167815551"
WA = "2349167815551"
WA_LINK = "https://wa.me/" + WA
STUDIO_URL = "https://greycreatives.vercel.app/"
DESC = "Grey Creatives Design is a branding and graphic design studio. We create logos, brand identities, print and stationery, signage and packaging."

data = json.load(open(os.path.join(HERE, "projects.json"), encoding="utf8"))
P = data["projects"]
esc = html.escape


def fill(t, **kw):
    for k, v in kw.items():
        t = t.replace("<<" + k + ">>", str(v))
    return t


def pimg(slug, n):
    return "assets/img/projects/%s/%s.webp" % (slug, n)


def dims(path):
    with Image.open(os.path.join(OUT, path)) as im:
        return im.size


def write(path, content):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w", encoding="utf8").write(content)


def slugify(n):
    return re.sub(r"[^a-z0-9]+", "-", n.lower()).strip("-")


# ------------------------------------------------------------------ icons
def ic(body, cls=""):
    return '<svg class="%s" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>' % (cls, body)


ICONS = {
    "home": '<path d="M3 11l9-8 9 8"/><path d="M5 10v10h5v-6h4v6h5V10"/>',
    "work": '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 10h18M9 10v10"/>',
    "logos": '<circle cx="12" cy="12" r="9"/><path d="M12 3c3.2 3 3.2 15 0 18M12 3c-3.2 3-3.2 15 0 18M3 12h18"/>',
    "services": '<path d="M12 3l2.4 6.6L21 12l-6.6 2.4L12 21l-2.4-6.6L3 12l6.6-2.4z"/>',
    "resume": '<path d="M7 3h7l5 5v13H7z"/><path d="M14 3v5h5M10 13h6M10 17h6"/>',
    "download": '<path d="M12 4v11M7 11l5 5 5-5M5 20h14"/>',
    "contact": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
    "search": '<circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/>',
    "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
    "moon": '<path d="M20 14.5A8.5 8.5 0 0 1 9.5 4a8.5 8.5 0 1 0 10.5 10.5z"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "close": '<path d="M6 6l12 12M18 6L6 18"/>',
    "menu": '<path d="M4 8h16M4 16h16"/>',
}
ARROW = ic(ICONS["arrow"])


# ------------------------------------------------------------------ shared chrome
NAV = [
    ("home", "Home", "index.html", "top"),
    ("work", "Work", "work.html", "identities"),
    ("logos", "Logos", "logos.html", "logos"),
    ("services", "Services", "index.html#services", "services"),
    ("resume", "Resume", "resume.html", ""),
    ("contact", "Contact", "#contact", "contact"),
]


def header(root, cur):
    links = []
    for key, label, href, sec in NAV:
        h = href if href.startswith("#") else root + href
        c = " is-cur" if key == cur else ""
        s = ' data-sec="%s"' % sec if sec else ""
        links.append('<a href="%s" class="nav-a%s" data-k="%s"%s>%s<span>%s</span></a>' % (h, c, key, s, ic(ICONS[key]), label))
    return fill('''<header class="hd" id="siteHeader">
  <a class="hd-brand" href="<<r>>index.html" aria-label="<<name>>, home"><i></i>Grey Creatives <em>Design</em></a>
  <nav class="hd-nav" id="navLinks" aria-label="Main">
    <div class="nav-top"><a class="hd-brand" href="<<r>>index.html" style="display:flex"><i></i>Grey Creatives <em>Design</em></a><button type="button" class="nav-close" id="navClose"><<close>>Close</button></div>
    <<links>>
    <div class="nav-foot"><b><<email>></b><span>WhatsApp <<phone>></span></div>
  </nav>
  <div class="hd-right">
    <button type="button" class="ibtn" id="searchBtn" aria-label="Search the site"><<search>></button>
    <button type="button" class="ibtn" id="themeToggle" aria-label="Switch to dark mode" aria-pressed="false"><<sun>><<moon>></button>
    <button type="button" class="nav-toggle" id="navToggle" aria-label="Open menu" aria-expanded="false" aria-controls="navLinks"><<menu>><span>Menu</span></button>
  </div>
</header>''', r=root, name=NAME, close=ic(ICONS["close"]), links="\n    ".join(links), email=EMAIL, phone=PHONE,
        search=ic(ICONS["search"]), sun=ic(ICONS["sun"], "i-sun"), moon=ic(ICONS["moon"], "i-moon"), menu=ic(ICONS["menu"]))


def footer(root):
    return fill('''<footer class="ft">
  <div class="wrap">
    <div class="ft-grid">
      <div>
        <a class="ft-brand" href="<<r>>index.html"><i></i>Grey Creatives <em>Design</em></a>
        <p class="sm">A branding and graphic design studio. Logos, brand identities, print, signage and packaging.</p>
      </div>
      <div>
        <h4>Explore</h4>
        <ul>
          <li><a href="<<r>>work.html">Work</a></li>
          <li><a href="<<r>>logos.html">Logos</a></li>
          <li><a href="<<r>>index.html#services">Services</a></li>
          <li><a href="<<r>>resume.html">Resume</a></li>
        </ul>
      </div>
      <div>
        <h4>Say hello</h4>
        <ul>
          <li><a href="mailto:<<email>>"><<email>></a></li>
          <li><a href="<<wa>>" target="_blank" rel="noopener">WhatsApp <<phone>></a></li>
          <li><a href="<<studio>>" target="_blank" rel="noopener">Grey Creatives, our web studio</a></li>
        </ul>
      </div>
    </div>
    <div class="ft-base"><span>&copy; 2026 Grey Creatives Design. All rights reserved.</span><span>Designed and built by Grey Creatives.</span></div>
  </div>
</footer>''', r=root, email=EMAIL, phone=PHONE, wa=WA_LINK, studio=STUDIO_URL)


def head(title, desc, path, root, img=None, page="", ld=""):
    img = img or SITE + "/og-image.png"
    return fill('''<!DOCTYPE html>
<html lang="en" data-root="<<root>>">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<script>(function(){var t='light';try{var v=localStorage.getItem('gcd-theme');if(v==='dark'||v==='light'){t=v;}}catch(e){}if(t==='dark'){document.documentElement.setAttribute('data-theme','dark');}})();</script>
<title><<title>></title>
<meta name="description" content="<<desc>>">
<meta name="theme-color" content="#FAFAF8">
<link rel="canonical" href="<<canon>>">
<link rel="icon" type="image/png" sizes="32x32" href="<<root>>assets/favicon-32.png">
<link rel="icon" type="image/png" sizes="48x48" href="<<root>>assets/favicon-48.png">
<link rel="shortcut icon" href="<<root>>favicon.ico">
<link rel="apple-touch-icon" href="<<root>>assets/apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="<<name>>">
<meta property="og:title" content="<<title>>">
<meta property="og:description" content="<<desc>>">
<meta property="og:url" content="<<canon>>">
<meta property="og:image" content="<<img>>">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="<<title>>">
<meta name="twitter:description" content="<<desc>>">
<meta name="twitter:image" content="<<img>>">
<link rel="preload" href="<<root>>assets/fonts/plus-jakarta-sans-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="<<root>>assets/css/site.css">
<<ld>>
</head>
<body data-page="<<page>>">
<a class="skip" href="#main">Skip to content</a>
''', root=root, title=esc(title), desc=esc(desc), canon=SITE + path, img=img, name=NAME, page=page, ld=ld)


def tail(root, extra=""):
    return fill('''<script src="<<r>>assets/js/data.js"></script>
<script src="<<r>>assets/js/core.js"></script>
<<extra>></body>
</html>
''', r=root, extra=extra)


def cta_band(root, text=None, heading=None):
    heading = heading or 'Have a brand to <em>build?</em>'
    text = text or "Hello Grey Creatives Design, I would like to talk about a project."
    wa = WA_LINK + "?text=" + __import__("urllib.parse", fromlist=["quote"]).quote(text)
    return fill('''<section class="pane contact cta-band" id="contact">
  <div class="wrap ct">
    <h2><<h>></h2>
    <p class="lead">Tell us about your business and what you need. We reply with next steps and a clear plan.</p>
    <div class="ct-lines">
      <div class="ct-line"><a class="big" href="mailto:<<email>>"><<email>></a><button type="button" class="copy" data-copy="<<email>>" data-msg="Email copied">Copy</button></div>
      <div class="ct-line"><a class="big" href="<<wa>>" target="_blank" rel="noopener">WhatsApp <<phone>></a><button type="button" class="copy" data-copy="<<phone>>" data-msg="Number copied">Copy</button></div>
    </div>
  </div>
</section>''', h=heading, email=EMAIL, phone=PHONE, wa=wa)


# ------------------------------------------------------------------ derived data
FEATURES = {p["slug"]: p for p in P}
ORDER = [p["slug"] for p in P]


def cover_path(p):
    return pimg(p["slug"], p["images"][p["cover"] - 1][0])


def make_thumbs():
    os.makedirs(os.path.join(OUT, "assets/img/thumbs"), exist_ok=True)
    os.makedirs(os.path.join(OUT, "assets/img/wall"), exist_ok=True)
    for p in P:
        with Image.open(os.path.join(OUT, cover_path(p))) as im:
            im = im.convert("RGB"); im.thumbnail((120, 120)); sq = Image.new("RGB", (120, 120), (255, 255, 255))
            im2 = Image.open(os.path.join(OUT, cover_path(p))).convert("RGB")
            w, h = im2.size; s = min(w, h); im2 = im2.crop(((w - s) // 2, (h - s) // 2, (w - s) // 2 + s, (h - s) // 2 + s)).resize((96, 96))
            im2.save(os.path.join(OUT, "assets/img/thumbs/%s.webp" % p["slug"]), "WEBP", quality=70)
    for item in COLLAGE:
        slug, n = item[0], item[1]
        src = os.path.join(OUT, pimg(slug, n))
        dst = os.path.join(OUT, "assets/img/wall/%s-%s.webp" % (slug, n))
        if not os.path.exists(dst):
            with Image.open(src) as im:
                im = im.convert("RGB"); im.thumbnail((640, 640)); im.save(dst, "WEBP", quality=74)


def write_data():
    projects = []
    for p in P:
        projects.append({
            "slug": p["slug"], "title": p["title"], "sector": p["sector"], "tagline": p["tagline"], "short": p["short"],
            "tags": p["services"], "palette": p["palette"], "tone": p["tone"], "count": len(p["images"]),
            "cover": cover_path(p), "coverAlt": p["images"][p["cover"] - 1][1], "thumb": "assets/img/thumbs/%s.webp" % p["slug"],
            "href": "work/%s.html" % p["slug"],
        })
    logos = [{"n": n, "f": f, "bg": bg} for n, f, bg in data["logos"]]
    js = "window.GCD=" + json.dumps({"email": EMAIL, "phone": PHONE, "waLink": WA_LINK, "projects": projects, "logos": logos}, ensure_ascii=False, separators=(",", ":")) + ";\n"
    write("assets/js/data.js", js)


# ------------------------------------------------------------------ home
COLLAGE = [
    # slug/img, x, y, w, rotate, z, depth
    ("zavia-apparel", "01", 3, 5, 30, -6, 2, 1.0),
    ("relief-motion", "01", 31, 1, 47, 3, 1, 0.6),
    ("three-strands", "01", 65, 17, 32, 5, 3, 1.3),
    ("zuria-cosmetics", "02", 8, 33, 37, 4, 4, 0.8),
    ("shayan-private-equity", "02", 43, 43, 34, -5, 5, 1.1),
    ("relief-motion", "03", 70, 56, 27, -3, 6, 1.5),
    ("zavron", "01", 14, 66, 34, 2, 3, 0.7),
    ("zavia-apparel", "04", 52, 73, 22, 7, 7, 1.2),
]


def collage():
    out = []
    for i, (slug, n, x, y, w, r, z, d) in enumerate(COLLAGE):
        src = "assets/img/wall/%s-%s.webp" % (slug, n)
        iw, ih = dims(src)
        out.append('<a class="cl" href="work/%s.html" aria-label="%s" data-d="%s" style="--x:%s%%;--y:%s%%;--w:%s%%;--r:%sdeg;--z:%s;--i:%s"><img src="%s" alt="" width="%s" height="%s" decoding="async"><span class="cl-tag">%s</span></a>'
                   % (slug, esc(FEATURES[slug]["title"]), d, x, y, w, r, z, i, src, iw, ih, esc(FEATURES[slug]["title"])))
    return "\n        ".join(out)


def bands():
    words = ["Logo design", "Brand identity", "Print and stationery", "Signage", "Packaging", "Social media graphics", "Mockups"]
    names = [n for n, _, _ in data["logos"]]
    a = "".join("<span>%s</span>" % esc(w) for w in words * 2)
    b = "".join("<span>%s</span>" % esc(n) for n in names)
    return fill('''<div class="bands" aria-hidden="true">
  <div class="band a"><div class="band-track"><div class="band-set"><<a>></div><div class="band-set"><<a>></div></div></div>
  <div class="band b"><div class="band-track"><div class="band-set"><<b>></div><div class="band-set"><<b>></div></div></div>
</div>''', a=a, b=b)


def services_html():
    rots = [(-16, 10, -5), (14, -12, 4), (-8, -16, -3), (18, 14, 6), (-20, -4, 3), (10, 18, -6), (0, 0, 2)]
    pics, rows = [], []
    for i, s in enumerate(data["services"]):
        slug, n = s["img"].split("/")
        tx, ty, r = rots[i % len(rots)]
        pics.append('<div class="svc-pic" style="--tx:%spx;--ty:%spx;--r:%sdeg;z-index:%s"><img src="%s" alt="" loading="lazy" decoding="async"></div>' % (tx, ty, r, 7 - i, pimg(slug, n)))
        rows.append('''<li class="svc-item">
          <button type="button" class="svc-row" aria-expanded="false"><h3>%s</h3><span class="go">%s</span></button>
          <div class="svc-more"><div><p>%s</p><a class="link" href="%s">See examples %s</a></div></div>
        </li>''' % (esc(s["name"]), ARROW, esc(s["text"]), s["link"], ARROW))
    return '''<div class="svc">
        <div class="svc-stage" aria-hidden="true">%s</div>
        <ul class="svc-list">%s</ul>
      </div>''' % ("".join(pics), "".join(rows))


def process_html():
    steps = "".join('<li class="step"><b>%d</b><h3>%s</h3><p>%s</p></li>' % (i + 1, esc(t), esc(d)) for i, (t, d) in enumerate(data["process"]))
    return '<ol class="steps" style="list-style:none;margin:0;padding:0">%s</ol>' % steps


def process_steps_only():
    steps = "".join('<li class="step"><b>%d</b><h3>%s</h3><p>%s</p></li>' % (i + 1, esc(t), esc(d)) for i, (t, d) in enumerate(data["process"]))
    return '<ol class="steps" style="list-style:none;margin:0;padding-top:20px">%s</ol>' % steps


def home():
    ld = '<script type="application/ld+json">%s</script>' % json.dumps({
        "@context": "https://schema.org", "@type": "Organization", "name": NAME, "url": SITE + "/", "email": EMAIL,
        "description": DESC, "logo": SITE + "/assets/apple-touch-icon.png"}, ensure_ascii=False)
    h = head(NAME, DESC, "/", "", page="home", ld=ld)
    h += header("", "home")
    needs = ["Logo design", "Brand identity", "Print and stationery", "Social media graphics", "Signage", "Packaging", "Something else"]
    chips = "".join('<label class="chip"><input type="checkbox" name="need" value="%s"><span>%s</span></label>' % (esc(n), esc(n)) for n in needs)
    body = fill('''<main id="main">
<section class="hero" id="top">
  <div class="wrap hero-grid">
    <div class="hero-copy">
      <p class="pill"><i></i>Brand identity and graphic design studio</p>
      <h1><span class="nw">We design brands</span> <em>people remember.</em></h1>
      <p class="lede">Grey Creatives Design is the branding and graphic design practice of Grey Creatives. We create logos, brand identities, print, stationery and signage that make a business look established from day one.</p>
      <div class="cta-row"><a class="btn btn-ink" href="work.html">View our work <<arrow>></a><a class="btn btn-line" href="logos.html">Logo design</a></div>
      <p class="hero-fields">Identities for healthcare, fashion, finance, agriculture, cosmetics and trade.</p>
    </div>
    <div class="collage">
      <<collage>>
      <a class="sticker" href="logos.html" aria-label="Logo design: see our logos">
        <svg class="ring" viewBox="0 0 100 100" aria-hidden="true"><defs><path id="ringPath" d="M50,50 m-37,0 a37,37 0 1,1 74,0 a37,37 0 1,1 -74,0"/></defs><text textLength="226" lengthAdjust="spacing"><textPath href="#ringPath" textLength="226" lengthAdjust="spacing">Logos • Identity • Print • Signage •</textPath></text></svg>
        <svg class="arr" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 17L17 7M9 7h8v8"/></svg>
      </a>
    </div>
  </div>
</section>

<<bands>>

<section class="sec" id="identities">
  <div class="wrap">
    <div class="sh"><h2>Identities, from the first mark to the finished sign.</h2><p>Seven brands, each carried from the logo to the wall, the card and the bag. Turn the pages.</p></div>
    <div class="bk" id="book" aria-label="Brand identities, shown as an open book"></div>
    <noscript><p style="text-align:center;margin-top:20px"><a class="link" href="work.html">Browse all work</a></p></noscript>
    <p style="text-align:center;margin-top:36px"><a class="link" href="work.html">Browse all our work <<arrow>></a></p>
  </div>
</section>

<section class="sec pane logos-pane" id="logos">
  <div class="wrap">
    <div class="sh"><h2>Every mark we have drawn, on one globe.</h2><p>Drag to spin. Hover a logo to bring it forward, then click to see it full size.</p></div>
    <div class="gl-wrap">
      <div class="gl-stage" id="glStage" role="group" aria-label="A globe of our logos">
        <i class="gl-ring r1"></i><i class="gl-ring r2"></i><i class="gl-ring r3"></i>
        <div class="gl-field"></div><div class="gl-tip" aria-hidden="true"></div>
      </div>
      <p class="gl-hint">Need only a logo? <a class="link" href="logos.html" style="color:var(--gold-2)">Open the logo gallery <<arrow>></a></p>
    </div>
  </div>
</section>

<section class="sec" id="services">
  <div class="wrap">
    <div class="sh"><h2>What we design.</h2><p>From a single logo to a complete identity and everything it needs to appear on.</p></div>
    <<services>>
  </div>
</section>

<section class="sec" id="process" style="padding-top:0">
  <div class="wrap">
    <div class="sh"><h2>How we work.</h2><p>Four steps, with you involved at each one.</p></div>
    <<process>>
  </div>
</section>

<section class="pane contact" id="contact">
  <div class="wrap ct-grid">
    <div class="ct">
      <h2>Have a brand to <em>build?</em></h2>
      <p class="lead">Tell us about your business and what you need. We reply with next steps and a clear plan.</p>
      <div class="ct-lines">
        <div class="ct-line"><a class="big" href="mailto:<<email>>"><<email>></a><button type="button" class="copy" data-copy="<<email>>" data-msg="Email copied">Copy</button></div>
        <div class="ct-line"><a class="big" href="<<wa>>" target="_blank" rel="noopener">WhatsApp <<phone>></a><button type="button" class="copy" data-copy="<<phone>>" data-msg="Number copied">Copy</button></div>
      </div>
    </div>
    <form class="form" id="enqForm" novalidate>
      <fieldset><legend>What do you need?</legend><div class="chips"><<chips>></div></fieldset>
      <div><label class="t" for="enqName">Your name</label><input class="fld" id="enqName" name="name" type="text" autocomplete="name" placeholder="Your name"></div>
      <div><label class="t" for="enqMsg">About your project</label><textarea class="fld" id="enqMsg" name="message" placeholder="Tell us about your business and what you would like designed"></textarea></div>
      <div class="cta-row"><button type="button" class="btn btn-gold" id="enqWa">Send on WhatsApp</button><button type="button" class="btn btn-line" id="enqMail">Send by email</button></div>
      <p class="form-note">This opens WhatsApp or your email app with your message ready to send.</p>
    </form>
  </div>
</section>
</main>
''', arrow=ARROW, collage=collage(), bands=bands(), services=services_html(), process=process_html(),
        email=EMAIL, phone=PHONE, wa=WA_LINK, chips=chips)
    h += body + footer("")
    h += tail("", '<script src="assets/js/globe.js"></script>\n<script src="assets/js/home.js"></script>\n')
    write("index.html", h)


# ------------------------------------------------------------------ work
FILTERS = ["Logo & identity", "Print & stationery", "Signage", "Packaging", "Social & campaign graphics"]


def work():
    h = head("Work | " + NAME, "Brand identities by Grey Creatives Design: logos, stationery, signage and packaging for healthcare, fashion, finance, agriculture, cosmetics and trade.", "/work", "", page="work")
    h += header("", "work")
    cards = []
    for i, p in enumerate(P):
        cov = cover_path(p)
        cards.append('''<a class="wc" href="work/%s.html" data-p="%d" data-tags="%s" style="--tone:%s">
        <div class="wc-img"><img src="%s" alt="%s" loading="%s" decoding="async"><span class="wc-view" aria-hidden="true">View</span></div>
        <div class="wc-cap"><h2>%s</h2><p>%s</p><p class="tg">%s</p></div>
      </a>''' % (p["slug"], i % 4, esc("|".join(p["services"])), p["tone"], cov, esc(p["images"][p["cover"] - 1][1]), "eager" if i < 2 else "lazy", esc(p["title"]), esc(p["tagline"]), esc(p["sector"] + " · " + ", ".join(p["services"]))))
    btns = '<button type="button" data-f="all" aria-pressed="true">All work</button>' + "".join('<button type="button" data-f="%s" aria-pressed="false">%s</button>' % (esc(f), esc(f)) for f in FILTERS)
    h += fill('''<main id="main">
<section class="pg"><div class="wrap">
  <div class="pg-top"><h1>Brand <em>identities.</em></h1><p class="lede" style="max-width:26em">Logos, stationery, signage and packaging, carried through as one consistent brand. Open any project for the full gallery.</p></div>
  <div class="filters" id="filters" role="group" aria-label="Filter work"><<btns>></div>
</div></section>
<section><div class="wrap"><div class="mosaic" id="mosaic">
      <<cards>>
</div></div></section>
</main>
''', btns=btns, cards="\n      ".join(cards))
    h += cta_band("") + footer("")
    h += tail("", '<script src="assets/js/pages.js"></script>\n')
    write("work.html", h)


# ------------------------------------------------------------------ project pages
def project(i, p):
    root = "../"
    slug = p["slug"]
    cov = cover_path(p)
    h = head("%s | %s" % (p["title"], NAME), "%s. %s" % (p["tagline"], p["short"]), "/work/" + slug, root, img=SITE + "/" + cov, page="project")
    h += header(root, "work")
    imgs = p["images"]
    lead_n, lead_alt = imgs[0]
    lead = '<figure class="plead" style="--tone:%s"><button type="button" data-lb="g" data-full="%s" data-alt="%s" aria-label="Open image full size: %s"><img src="%s" alt="%s" width="%d" height="%d"></button></figure>' % (
        p["tone"], root + pimg(slug, lead_n), esc(lead_alt), esc(lead_alt), root + pimg(slug, lead_n), esc(lead_alt), *dims(pimg(slug, lead_n)))
    gal = []
    for j, (n, alt) in enumerate(imgs[1:]):
        w, hh = dims(pimg(slug, n))
        gal.append('<figure class="gi" data-p="%d" style="--tone:%s"><button type="button" data-lb="g" data-full="%s" data-alt="%s" aria-label="Open image full size: %s"><img src="%s" alt="%s" width="%d" height="%d" loading="lazy" decoding="async"></button><figcaption>%s</figcaption></figure>' % (
            j % 4, p["tone"], root + pimg(slug, n), esc(alt), esc(alt), root + pimg(slug, n), esc(alt), w, hh, esc(alt)))
    sw = "".join('<button type="button" class="sw" data-copy="%s" data-msg="%s copied" style="background:%s;color:%s" aria-label="Copy %s %s"><b>%s</b><small>%s</small></button>' % (
        c[1], c[1], c[1], "#fff" if sum(int(c[1][k:k + 2], 16) for k in (1, 3, 5)) < 400 else "#141412", esc(c[0]), c[1], esc(c[0]), c[1]) for c in p["palette"])
    dl = "".join("<li>%s</li>" % esc(d) for d in p["deliverables"])
    prev = FEATURES[ORDER[(i - 1) % len(ORDER)]]
    nxt = FEATURES[ORDER[(i + 1) % len(ORDER)]]
    pager = '''<nav class="pager" aria-label="More projects">
  <a class="pg-link" href="%s.html"><img src="%s" alt="" width="96" height="96"><span><small>Previous project</small><b>%s</b></span></a>
  <a class="pg-link nx" href="%s.html"><span><small>Next project</small><b>%s</b></span><img src="%s" alt="" width="96" height="96"></a>
</nav>''' % (prev["slug"], root + "assets/img/thumbs/%s.webp" % prev["slug"], esc(prev["title"]), nxt["slug"], esc(nxt["title"]), root + "assets/img/thumbs/%s.webp" % nxt["slug"])
    h += fill('''<main id="main">
<section class="ph pg" style="padding-bottom:clamp(28px,4vw,48px)"><div class="wrap">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="../work.html">Work</a><span aria-hidden="true">/</span><span><<title>></span></nav>
  <h1><<title>></h1>
  <p class="ph-tag"><<tagline>></p>
  <dl class="ph-meta">
    <div><dt>Sector</dt><dd><<sector>></dd></div>
    <div><dt>What we designed</dt><dd><<scope>></dd></div>
    <div><dt>In the gallery</dt><dd><<count>> images</dd></div>
  </dl>
</div></section>
<section><div class="wrap"><<lead>></div></section>
<section class="sec" style="padding-bottom:0"><div class="wrap">
  <div class="ov"><div><h3>The brief</h3><p><<brief>></p></div><div><h3>The identity</h3><p><<identity>></p></div></div>
  <div class="ov2"><div><h3>Colour</h3><div class="pal"><<sw>></div></div><div><h3>What we delivered</h3><ul class="dl"><<dl>></ul></div></div>
</div></section>
<section class="sec" style="padding-bottom:0"><div class="wrap"><div class="gal"><<gal>></div><<pager>></div></section>
<div style="height:var(--sec)"></div>
</main>
''', title=esc(p["title"]), tagline=esc(p["tagline"]), sector=esc(p["sector"]), scope=esc(", ".join(p["services"])), count=len(imgs), lead=lead,
        brief=esc(p["brief"]), identity=esc(p["identity"]), sw=sw, dl=dl, gal="\n".join(gal), pager=pager)
    h += cta_band(root, "Hello Grey Creatives Design, I saw the %s project and would like something similar." % p["title"]) + footer(root)
    h += tail(root)
    write("work/%s.html" % slug, h)


# ------------------------------------------------------------------ logos
def logos():
    h = head("Logo design | " + NAME, "Logo design by Grey Creatives Design. Browse the marks we have drawn for businesses and foundations, then tell us about yours.", "/logos", "", page="logos")
    h += header("", "logos")
    rnd = random.Random(11)
    order = list(range(len(data["logos"])))
    rnd.shuffle(order)
    sizes = [196, 148, 172, 132, 184, 156, 140, 188]
    pins = []
    for k, i in enumerate(order):
        n, f, bg = data["logos"][i]
        s = sizes[k % len(sizes)]
        r = rnd.choice([-6, -4, -3, -2, 2, 3, 4, 6])
        dy = rnd.choice([-26, -12, 0, 14, 30])
        pins.append('<button type="button" class="pin-i" style="--s:%dpx;--r:%ddeg;--dy:%dpx;background:%s" data-logo="%d" aria-label="%s logo, open full size"><img src="assets/img/logos/%s.webp" alt="" width="420" height="420" loading="lazy" decoding="async"><span class="nm">%s</span></button>' % (s, r, dy, bg, i, esc(n), f, esc(n)))
    msg = "Hello Grey Creatives Design, I need a logo designed. My business is "
    feat = [
        ("A mark built for your business", "We study what you do and who you serve, then draw a logo that is simple, memorable and easy to recognise at any size."),
        ("The versions you will use", "Colour, one-colour and compact versions, so the logo works on a sign, a card, a social profile and a stamp."),
        ("Files ready to use", "Clean final files for print and screen, with a mockup that shows your logo in place before you commit."),
    ]
    feath = "".join("<div><h3>%s</h3><p>%s</p></div>" % (esc(a), esc(b)) for a, b in feat)
    h += fill('''<main id="main">
<section class="pg lg-hero"><div class="wrap">
  <p class="pill"><i></i>Logo design only</p>
  <h1>A logo that <em>looks the part.</em></h1>
  <p class="lede">Only need a logo? You are in the right place. Spin the globe, pick any mark to see it full size, then tell us about your business.</p>
  <div class="cta-row"><a class="btn btn-ink" href="<<wa>>" target="_blank" rel="noopener">Ask for a logo on WhatsApp <<arrow>></a><a class="btn btn-line" href="mailto:<<email>>?subject=Logo%20design">Email us</a></div>
</div></section>

<section class="pane logos-pane" style="padding-block:clamp(24px,4vw,56px)" aria-label="Logo globe">
  <div class="wrap">
    <div class="gl-wrap">
      <div class="gl-stage" id="glStage" role="group" aria-label="A globe of our logos" style="height:clamp(460px,64vw,760px)">
        <i class="gl-ring r1"></i><i class="gl-ring r2"></i><i class="gl-ring r3"></i>
        <div class="gl-field"></div><div class="gl-tip" aria-hidden="true"></div>
      </div>
      <p class="gl-hint"><b>Drag</b> to spin. <b>Hover</b> to pop a logo forward. <b>Click</b> to open it.</p>
    </div>
  </div>
</section>

<section class="sec"><div class="wrap">
  <div class="sh"><h2>The whole collection, pinned up.</h2><p>Every logo in one scatter. Hover to straighten one, click to look closely.</p></div>
  <div class="pin"><<pins>></div>
</div></section>

<section class="sec" style="padding-top:0"><div class="wrap">
  <div class="sh"><h2>What a logo order includes.</h2></div>
  <div class="feat"><<feat>></div>
</div></section>

<section class="sec" style="padding-top:0"><div class="wrap">
  <div class="sh"><h2>How a logo comes together.</h2><p>The same four steps we use for full identities, kept short.</p></div>
  <<process>>
</div></section>

<section class="sec" style="padding-top:0"><div class="wrap" style="text-align:center">
  <p class="lede" style="margin-inline:auto">Need a full brand with stationery, signage and packaging?</p>
  <p style="margin-top:14px"><a class="link" href="work.html">See our brand identities <<arrow>></a></p>
</div></section>
</main>
''', wa=WA_LINK + "?text=" + __import__("urllib.parse", fromlist=["quote"]).quote(msg), arrow=ARROW, email=EMAIL, pins="".join(pins), feat=feath, process=process_steps_only())
    h += cta_band("", msg + "...", "Ready for your <em>logo?</em>") + footer("")
    h += tail("", '<script src="assets/js/globe.js"></script>\n<script src="assets/js/pages.js"></script>\n')
    write("logos.html", h)


RESUME_PDF = "assets/resume/Moses-Israel-Timilehin-Resume.pdf"
R_EXP = [
    ("Grey Creatives Studio", "Web &amp; Branding Studio", "Developer &amp; Lead Designer", "July 2026 – Present", [
        "Lead client projects end to end, from brief and UI design through development, launch and revision rounds, delivering websites for IntelPRO Solutions, YA Foundation, Three Strands Health &amp; Wellness, Shayan Private Equity and Zavron Group.",
        "Build custom features beyond static pages: a PHP and SQLite learning platform with Google sign-in and an admin dashboard, an email breach checker, an investment returns calculator, and news and job feeds that update themselves.",
        "Set the studio's standards for responsive multi-page layouts, light and dark themes and page speed, and handle domain, hosting, email and Search Console setup so every site launches ready to be found."]),
    ("Grey Creatives Design", "Branding and graphic design", "Brand Designer", "January 2024 – June 2026", [
        "Developed 20+ complete brand identities, from logo suites and colour and typography systems to brand guideline documents and ready-to-use templates, applied consistently across print, signage, social media and web.",
        "Designed the branded templates and collateral that keep a business consistent as it grows: letterheads, business cards, sticker labels, signage and social media post templates.",
        "Delivered identities for Shayan Private Equity, Zavron Group (Zavia Apparel and Zuria Cosmetics), Three Strands Health &amp; Wellness, Abiola Farms, Relief Motion Physiotherapy and Dealer Global Auto."]),
    ("Freelance", "Lagos, Nigeria", "Photographer, Designer &amp; Web Developer", "January 2024 – June 2026", [
        "Design and develop websites for independent clients, managing brief, feedback rounds and handover directly with each one.",
        "Shoot and edit studio, product, event and brand photography, and cut promotional videos in CapCut."]),
]
R_PROJ = [
    ("Shayan Private Equity", "Investment platform and brand identity", "Web &amp; Brand Designer", "Figma, Illustrator, HTML, CSS, JavaScript, REST APIs, Supabase", "See the identity", "work/shayan-private-equity.html", [
        "Designed and built the website for an investment and wealth-management firm: investment plans, a returns calculator, a multicurrency view (NGN, USD, GBP, EUR), a live market overview, training and loans pages, a chat assistant, and login and sign-up screens.",
        "Created the full brand identity: logo, colour and typography system, brand guidelines, and templates for social media, presentations and investor communications."]),
    ("Zavron Group", "Trade and distribution website, brand architecture", "Web &amp; Brand Designer", "Figma, Illustrator, HTML, CSS, JavaScript", "See the identity", "work/zavron.html", [
        "Designed and built the website for a pan-African trade and distribution company, with its services, two consumer brands, offices in Lagos, Accra and Kigali, and a partnership request form with a confirmation flow.",
        "Built the brand system behind the group and its two brands, Zavia Apparel and Zuria Cosmetics: logos, colour and type palettes, brand guidelines and social media templates that make them read as one family."]),
    ("Three Strands Health &amp; Wellness", "Website and brand identity", "Web &amp; Brand Designer", "Illustrator, Photoshop, HTML, CSS, JavaScript", "See the identity", "work/three-strands.html", [
        "Designed and built the website for a psychiatric and family nurse practice.",
        "Developed the complete identity: logo, brand guidelines, signage, print stationery and social media templates, applied consistently across every patient touchpoint."]),
    ("Abiola Farms and Relief Motion", "Brand identity systems", "Brand Designer", "Adobe Illustrator, Photoshop, CorelDRAW", "See Abiola Farms", "work/abiola-farms.html", [
        "Abiola Farms: built a full identity system, with logo suite, colour and typography, letterhead, business card, farm-stand signage and sticker labels as one cohesive set, published as a Behance case study.",
        "Relief Motion Physiotherapy: developed the logo and brand system with ready-to-use templates for a physiotherapy practice."]),
    ("YA Foundation", "Website and learning platform", "Lead Developer &amp; Designer", "HTML, CSS, JavaScript, PHP, SQLite, Google OAuth, REST APIs", "yafoundationglobal.org", "https://yafoundationglobal.org", [
        "Built a multi-page light and dark site for the Yemi Ademiluyi Foundation with programmes, events and team pages, a free data-breach checker and a 100 AI Tools directory.",
        "Added a learning platform: student accounts with Google sign-in, three free courses (AI, Cyber Security, Data Privacy), an aptitude test, self-service certificates and an admin dashboard."]),
    ("IntelPRO Solutions", "Cybersecurity company website", "Developer &amp; Designer", "HTML, CSS, JavaScript, REST APIs, SEO", "intelproglobal.com", "https://intelproglobal.com", [
        "Designed a multi-page corporate site in the client's brand colours, with services, leadership profiles, certification credentials, a jobs board and a cyber news hub.",
        "Built an on-site email breach checker, a news feed that curates and credits stories from their original sources, and job listings that update themselves and drop closed roles."]),
]
R_SKILLS = [
    ("Design", "Figma, Illustrator, Photoshop, CorelDRAW, Canva, Brand Identity Systems"),
    ("Video and photo", "Premiere Pro, CapCut, Photography"),
    ("Languages and tools", "HTML, CSS, JavaScript, TypeScript, PHP, Python, SQL"),
    ("Frontend and web", "React, Tailwind CSS, Responsive Design, Light/Dark Theming, SEO"),
    ("Backend and data", "SQLite, MySQL, PostgreSQL, Supabase, Firebase"),
    ("APIs and auth", "REST API Integration, Google OAuth"),
    ("Tools and deployment", "Git, GitHub, VS Code, Vercel, cPanel, Google Search Console"),
]


def resume():
    desc = "Resume of Moses Israel Timilehin, brand designer and software engineer behind Grey Creatives Design. Experience, projects, skills and education, with a PDF to download."
    h = head("Resume | " + NAME, desc, "/resume", "", page="resume")
    h += header("", "resume")
    dl = ic(ICONS["download"])
    exp = ""
    for co, sub, role, when, bl in R_EXP:
        exp += '<article class="rx"><div class="rx-when">%s</div><div class="rx-main"><h3>%s <span>%s</span></h3><p class="rx-role">%s</p><ul>%s</ul></div></article>' % (when, co, sub, role, "".join("<li>%s</li>" % b for b in bl))
    proj = ""
    for ti, kind, role, tools, label, href, bl in R_PROJ:
        ext = href.startswith("http")
        a = '<a class="link" href="%s"%s>%s %s</a>' % (href, ' target="_blank" rel="noopener"' if ext else "", label, ARROW)
        proj += '<article class="rp"><div class="rp-h"><div><h3>%s</h3><p class="rp-k">%s</p></div>%s</div><p class="rp-r"><b>%s</b> &middot; %s</p><ul>%s</ul></article>' % (ti, kind, a, role, tools, "".join("<li>%s</li>" % b for b in bl))
    skills = "".join("<div><dt>%s</dt><dd>%s</dd></div>" % (a, b) for a, b in R_SKILLS)
    h += fill('''<main id="main">
<section class="pg rs-hero"><div class="wrap rs-top">
  <div>
    <p class="pill"><i></i>Resume</p>
    <h1>Moses Israel <em>Timilehin.</em></h1>
    <p class="rs-role">Brand designer and software engineer</p>
    <p class="lede">Takes a client from logo to launch: brand identity, interface and a fast, production-ready website. Has delivered 20+ complete brand identities and multiple client websites, and adds photography and video editing to every brand.</p>
    <div class="cta-row"><a class="btn btn-ink" href="<<pdf>>" download>Download PDF <<dl>></a><a class="btn btn-line" href="<<wa>>" target="_blank" rel="noopener">Message on WhatsApp</a></div>
  </div>
  <aside class="rs-card" aria-label="Details">
    <dl>
      <div><dt>Based in</dt><dd>Lagos, Nigeria</dd></div>
      <div><dt>Studios</dt><dd>Grey Creatives, Grey Creatives Design</dd></div>
      <div><dt>Email</dt><dd><a href="mailto:<<email>>"><<email>></a></dd></div>
      <div><dt>Web studio</dt><dd><a href="<<studio>>" target="_blank" rel="noopener">greycreatives.vercel.app</a></dd></div>
      <div><dt>Behance</dt><dd><a href="https://www.behance.net/greypixels" target="_blank" rel="noopener">behance.net/greypixels</a></dd></div>
      <div><dt>GitHub</dt><dd><a href="https://github.com/Greycode-01" target="_blank" rel="noopener">github.com/Greycode-01</a></dd></div>
    </dl>
  </aside>
</div></section>

<section class="sec"><div class="wrap">
  <div class="sh"><h2>Experience.</h2></div>
  <div class="rx-list"><<exp>></div>
</div></section>

<section class="sec" style="padding-top:0"><div class="wrap">
  <div class="sh"><h2>Selected <em>projects.</em></h2><p>Brand identity work links to its full gallery on this site.</p></div>
  <div class="rp-list"><<proj>></div>
</div></section>

<section class="sec" style="padding-top:0"><div class="wrap rs-cols">
  <div>
    <div class="sh"><h2>Skills.</h2></div>
    <dl class="rs-skills"><<skills>></dl>
  </div>
  <div>
    <div class="sh"><h2>Education.</h2></div>
    <div class="rs-edu">
      <div><b>BSc. Computer Science</b><span>Olabisi Onabanjo University, Ogun State</span><small>Graduated June 2026</small></div>
      <div><b>ND, Science Laboratory Technology</b><span>The Polytechnic Ibadan, Oyo State</span><small>2022</small></div>
    </div>
    <div class="sh" style="margin-top:clamp(32px,5vw,56px)"><h2>Certifications.</h2></div>
    <div class="rs-edu">
      <div><b>Web Development &amp; IT</b><span>HIIT, Ikeja, Lagos</span><small>May – September 2025</small></div>
      <div><b>Professional Photography Training</b><span>Authentic Studio, Alakuko, Lagos</span><small>2018 – 2020</small></div>
    </div>
  </div>
</div></section>
</main>
''', pdf=RESUME_PDF, dl=dl, wa=WA_LINK, email=EMAIL, studio=STUDIO_URL, exp=exp, proj=proj, skills=skills)
    h += cta_band("", "Hello Grey Creatives Design, I saw your resume and would like to talk.", "Let us work <em>together.</em>") + footer("")
    h += tail("")
    write("resume.html", h)


def not_found():
    h = head("Page not found | " + NAME, "That page does not exist. Head back to Grey Creatives Design.", "/404", "", page="404")
    h += header("", "")
    h += '''<main id="main" class="nf"><div><h1>404</h1><p>We could not find that page. It may have moved, or the link may be mistyped.</p><div class="cta-row" style="justify-content:center"><a class="btn btn-ink" href="index.html">Back to home</a><a class="btn btn-line" href="work.html">See our work</a></div></div></main>
'''
    h += tail("")
    write("404.html", h)


def sitemap():
    urls = ["/", "/work", "/logos", "/resume"] + ["/work/" + p["slug"] for p in P]
    x = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join("  <url><loc>%s%s</loc></url>\n" % (SITE, u) for u in urls) + "</urlset>\n"
    write("sitemap.xml", x)
    write("robots.txt", "User-agent: *\nAllow: /\nSitemap: %s/sitemap.xml\n" % SITE)


if __name__ == "__main__":
    make_thumbs()
    write_data()
    home(); work(); logos(); resume(); not_found()
    for i, p in enumerate(P):
        project(i, p)
    sitemap()
    print("built", 6 + len(P), "pages")
