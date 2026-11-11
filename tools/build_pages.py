"""Generate local SEO landing pages for Greenlight Permits & Takeoffs."""
import json, os, html

BASE = "https://greenlightpermits.github.io/"
ROOT = os.path.join(os.path.dirname(__file__), "..")

COUNTIES = {
    "miami-dade": {
        "name": "Miami-Dade County", "short": "Miami-Dade",
        "cities": ["Miami", "Miami Beach", "Hialeah", "Doral", "Coral Gables", "Homestead",
                   "Miami Gardens", "Aventura", "Kendall", "North Miami", "Miami Lakes",
                   "Unincorporated Miami-Dade"],
        "permit_note": ("Miami-Dade is a High-Velocity Hurricane Zone (HVHZ), so product approvals, "
                        "roofing and opening-protection details get extra scrutiny. Many cities run their "
                        "own building departments with their own portals and checklists, separate from the "
                        "county. Some, like the City of Miami, also require permit expediters to register "
                        "before working on projects there."),
        "permit_note_es": ("Miami-Dade es Zona de Huracanes de Alta Velocidad (HVHZ): aprobaciones de producto, "
                           "techos y protección de aberturas se revisan con más detalle. Muchas ciudades tienen "
                           "su propio departamento de construcción y su propio portal."),
    },
    "broward": {
        "name": "Broward County", "short": "Broward",
        "cities": ["Fort Lauderdale", "Hollywood", "Pembroke Pines", "Coral Springs", "Pompano Beach",
                   "Deerfield Beach", "Plantation", "Davie", "Sunrise", "Weston", "Miramar",
                   "Unincorporated Broward"],
        "permit_note": ("Broward is also a High-Velocity Hurricane Zone (HVHZ), and its many cities do not all "
                        "use the same permitting software or submittal rules. We know which portal, forms "
                        "and checklist each jurisdiction expects, so your package goes in complete the first time."),
        "permit_note_es": ("Broward también es zona HVHZ y sus ciudades usan distintos sistemas y requisitos. "
                           "Sabemos qué portal y qué formularios pide cada jurisdicción."),
    },
    "palm-beach": {
        "name": "Palm Beach County", "short": "Palm Beach",
        "cities": ["Boca Raton", "Delray Beach", "Boynton Beach", "West Palm Beach", "Jupiter",
                   "Wellington", "Lake Worth Beach", "Palm Beach Gardens", "Royal Palm Beach",
                   "Greenacres", "Lantana", "Unincorporated Palm Beach County"],
        "permit_note": ("Palm Beach County is outside the HVHZ, but each city still has its own building "
                        "department, fee schedule and review process, and unincorporated areas go to the county. "
                        "We are based in Boca Raton and work Palm Beach permits every week."),
        "permit_note_es": ("Palm Beach está fuera de la zona HVHZ, pero cada ciudad tiene su propio departamento "
                           "y proceso. Estamos en Boca Raton."),
    },
}

SERVICES = {
    "permit-expediting": {
        "title": "Permit Expediting in {county}",
        "h1": "Permit expediting in {short}, done for contractors",
        "meta": ("Permit expediting for contractors in {county}, FL: application prep, online submittal, "
                 "plan review comments and inspection scheduling. Flat fees from $150. Hablamos español."),
        "lead": ("We prepare and submit your permit applications in {county} as your authorized agent, "
                 "track every plan review comment, handle resubmittals and schedule inspections, so you "
                 "stay on the job instead of on hold with the building department."),
        "bullets": ["Roofing and re-roof permits", "Windows, doors and shutters",
                    "Kitchen and bath remodels", "Additions and new homes",
                    "Commercial build-outs", "Electrical, plumbing and mechanical trade permits"],
        "price": "From $150 per permit plus government fees",
        "es": ("Tramitamos permisos de construcción en {county} para contratistas: preparación, envío en "
               "línea, respuesta a comentarios e inspecciones. Precio fijo desde $150."),
        "cta_service": "permit",
    },
    "construction-takeoffs": {
        "title": "Construction Takeoffs in {county}",
        "h1": "Construction takeoffs for {short} contractors, back in 48 hours",
        "meta": ("Quantity takeoffs for contractors in {county}, FL: drywall, framing, tile, paint, roofing, "
                 "concrete or full projects. Excel + marked-up PDF in 48 hours, from $250. Hablamos español."),
        "lead": ("Send your plans and get a clean quantity takeoff back in 48 hours: an Excel sheet by item "
                 "and area plus a marked-up PDF showing exactly what was counted. You add your own pricing "
                 "and bid more jobs in {short} without hiring an estimator."),
        "bullets": ["Drywall and metal-stud or wood framing", "Tile and flooring",
                    "Paint (walls and ceilings)", "Roofing", "Concrete and masonry",
                    "Full-project takeoffs for GCs and remodelers"],
        "price": "From $250 per takeoff · 15% off at 5+ takeoffs a month",
        "es": ("Takeoffs de cantidades para contratistas en {county}: drywall, framing, losa, pintura, techo, "
               "concreto o proyecto completo. Excel + PDF marcado en 48 horas, desde $250."),
        "cta_service": "takeoff",
    },
}

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} | Greenlight Permits &amp; Takeoffs</title>
<meta name="description" content="{meta}">
<link rel="canonical" href="{url}">
<meta property="og:title" content="{title} | Greenlight Permits &amp; Takeoffs">
<meta property="og:description" content="{meta}">
<meta property="og:url" content="{url}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@700;800&family=Inter:wght@400;600&display=swap" rel="stylesheet">
<script type="application/ld+json">{schema}</script>
<style>
:root{{--green:#12a150;--green-d:#0b7a3b;--ink:#13201a;--muted:#5b6b63;--line:#e3e9e5;--bg:#f6f8f6}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:Inter,system-ui,sans-serif;color:var(--ink);background:var(--bg);line-height:1.6;font-size:17px}}
h1,h2{{font-family:Archivo,Inter,system-ui,sans-serif;line-height:1.15}}
a{{color:var(--green-d)}}
.wrap{{max-width:980px;margin:0 auto;padding:0 20px}}
header{{background:#fff;border-bottom:1px solid var(--line)}}
.nav{{display:flex;justify-content:space-between;align-items:center;height:62px}}
.logo{{display:flex;align-items:center;gap:10px;font-family:Archivo,Inter,sans-serif;font-weight:800;font-size:18px;text-decoration:none;color:var(--ink)}}
.light{{display:inline-flex;flex-direction:column;gap:3px;background:var(--ink);padding:5px 6px;border-radius:8px}}
.light i{{width:8px;height:8px;border-radius:50%;background:#3a4a42}}.light i:last-child{{background:var(--green)}}
.btn{{display:inline-block;background:var(--green);color:#fff;text-decoration:none;font-weight:600;padding:13px 20px;border-radius:10px}}
.btn:hover{{background:var(--green-d)}}
.btn-o{{background:#fff;color:var(--ink);border:1.5px solid var(--ink)}}.btn-o:hover{{background:var(--ink);color:#fff}}
.hero{{background:var(--ink);color:#fff;padding:56px 0}}
.hero h1{{font-size:clamp(30px,4.6vw,46px);margin-bottom:16px}}
.hero p{{color:#c9d6cf;max-width:680px;margin-bottom:24px;font-size:18px}}
.price{{display:inline-block;background:rgba(18,161,80,.18);color:#7fe3a8;border:1px solid rgba(127,227,168,.35);padding:5px 12px;border-radius:999px;font-size:14px;font-weight:600;margin-bottom:18px}}
section{{padding:44px 0}}
h2{{font-size:28px;margin-bottom:14px}}
.card{{background:#fff;border:1px solid var(--line);border-radius:14px;padding:26px;margin-bottom:18px}}
ul.check{{list-style:none;display:grid;grid-template-columns:1fr 1fr;gap:8px 20px}}
@media(max-width:640px){{ul.check{{grid-template-columns:1fr}}}}
ul.check li:before{{content:"✓ ";color:var(--green);font-weight:700}}
.chips{{display:flex;flex-wrap:wrap;gap:8px}}
.chips span{{background:#fff;border:1px solid var(--line);border-radius:999px;padding:6px 13px;font-size:15px}}
.es{{border-left:4px solid var(--green);padding-left:16px;color:var(--muted)}}
.links a{{display:inline-block;margin:0 14px 8px 0}}
footer{{background:var(--ink);color:#a9bab1;padding:30px 0;font-size:14px}}
footer a{{color:#cfe9d9}}
</style>
</head>
<body>
<header><div class="wrap nav"><a class="logo" href="{base}"><span class="light"><i></i><i></i><i></i></span>Greenlight Permits &amp; Takeoffs</a><a class="btn" href="{base}#start">Get a quote</a></div></header>
<div class="hero"><div class="wrap">
<span class="price">{price}</span>
<h1>{h1}</h1>
<p>{lead}</p>
<a class="btn" href="{base}#start">Upload your plans</a> &nbsp; <a class="btn btn-o" href="{base}#quote" style="background:transparent;color:#fff;border-color:#fff">See your price</a>
</div></div>
<section><div class="wrap">
<div class="card"><h2>What we handle in {short}</h2><ul class="check">{bullets}</ul></div>
{note_block}
<div class="card"><h2>Cities we serve in {county}</h2><div class="chips">{cities}</div></div>
<div class="card"><h2>How it works</h2>
<p><b>1. Upload your plans</b> and job details on our site. <b>2. Get a confirmed flat fee</b> the same business day. <b>3. We deliver</b>: {deliver}</p></div>
<div class="card es" lang="es"><h2>En español</h2><p>{es}</p></div>
<div class="card"><h2>Other services and areas</h2><div class="links">{other_links}</div></div>
<p style="text-align:center;margin-top:10px"><a class="btn" href="{base}#start">Start a request for {short}</a></p>
</div></section>
<footer><div class="wrap"><b style="color:#fff">Greenlight Permits &amp; Takeoffs</b> · Serving Miami-Dade, Broward &amp; Palm Beach · <a href="{base}">Home</a><br>
We prepare and submit permit applications as the authorized agent of licensed contractors and owner-builders, and provide quantity takeoffs. We are not a law firm and do not prepare or review contracts, lien documents or releases.</div></footer>
</body>
</html>
"""

def slug(svc, county):
    return f"{svc}-{county}"

def build():
    pages = []
    for svc_key, svc in SERVICES.items():
        for c_key, c in COUNTIES.items():
            s = slug(svc_key, c_key)
            url = f"{BASE}{s}/"
            fmt = {"county": c["name"], "short": c["short"]}
            title = svc["title"].format(**fmt)
            meta = svc["meta"].format(**fmt)
            note_block = ""
            if svc_key == "permit-expediting":
                note_block = (f'<div class="card"><h2>Permitting in {c["short"]}: what to know</h2>'
                              f'<p>{html.escape(c["permit_note"])}</p></div>')
            deliver = ("your permit submitted, comments answered and tracked to approval."
                       if svc_key == "permit-expediting" else
                       "an Excel quantity sheet and a marked-up PDF in your inbox within 48 hours.")
            others = []
            for s2k, s2 in SERVICES.items():
                for c2k, c2 in COUNTIES.items():
                    if (s2k, c2k) == (svc_key, c_key):
                        continue
                    others.append(f'<a href="{BASE}{slug(s2k, c2k)}/">{s2["title"].format(county=c2["name"], short=c2["short"])}</a>')
            schema = {
                "@context": "https://schema.org", "@type": "Service",
                "name": title, "serviceType": title.split(" in ")[0],
                "areaServed": {"@type": "AdministrativeArea", "name": c["name"] + ", FL"},
                "provider": {"@type": "ProfessionalService", "name": "Greenlight Permits & Takeoffs",
                             "url": BASE, "areaServed": ["Miami-Dade County, FL", "Broward County, FL", "Palm Beach County, FL"],
                             "knowsLanguage": ["en", "es"]},
                "description": meta, "url": url,
            }
            page = TEMPLATE.format(
                title=html.escape(title), meta=html.escape(meta), url=url, base=BASE,
                schema=json.dumps(schema, ensure_ascii=False),
                price=html.escape(svc["price"]), h1=html.escape(svc["h1"].format(**fmt)),
                lead=html.escape(svc["lead"].format(**fmt)), short=html.escape(c["short"]),
                county=html.escape(c["name"]),
                bullets="".join(f"<li>{html.escape(b)}</li>" for b in svc["bullets"]),
                note_block=note_block,
                cities="".join(f"<span>{html.escape(x)}</span>" for x in c["cities"]),
                deliver=deliver, es=html.escape(svc["es"].format(**fmt) + " " + (c["permit_note_es"] if svc_key == "permit-expediting" else "")),
                other_links="".join(others),
            )
            out_dir = os.path.join(ROOT, s)
            os.makedirs(out_dir, exist_ok=True)
            with open(os.path.join(out_dir, "index.html"), "w") as f:
                f.write(page)
            pages.append((s, title))
    # sitemap + robots
    urls = [BASE] + [f"{BASE}{s}/" for s, _ in pages]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        sm.append(f"  <url><loc>{u}</loc><lastmod>2026-11-11</lastmod></url>")
    sm.append("</urlset>")
    with open(os.path.join(ROOT, "sitemap.xml"), "w") as f:
        f.write("\n".join(sm) + "\n")
    with open(os.path.join(ROOT, "robots.txt"), "w") as f:
        f.write(f"User-agent: *\nAllow: /\n\nSitemap: {BASE}sitemap.xml\n")
    return pages

if __name__ == "__main__":
    for s, t in build():
        print(s, "|", t)
