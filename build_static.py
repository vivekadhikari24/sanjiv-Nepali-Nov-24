import urllib.request
import re, os, json
from bs4 import BeautifulSoup

PAGES = [
    {
        "slug": "",
        "url": "https://sanjivnepali.com/",
        "out_file": "index.html",
        "title": "Master Sanjiv Nepali | Taekwondo Champion, Coach & Referee",
        "desc": "Official site of Master Sanjiv Nepali — 5th Dan Black Belt, International Taekwondo Gold Medalist, certified referee, and coach representing Nepal worldwide.",
        "type": "ProfilePage",
        "breadcrumb": None
    },
    {
        "slug": "about/",
        "url": "https://sanjivnepali.com/about/",
        "out_file": "about/index.html",
        "title": "About Master Sanjiv Nepali | 5th Dan Taekwondo Master",
        "desc": "Learn about Master Sanjiv Nepali, international Taekwondo champion, 5th Dan Kukkiwon Black Belt, referee, and coach from Nijgadh, Nepal to the USA.",
        "type": "AboutPage",
        "breadcrumb": "About"
    },
    {
        "slug": "journey/",
        "url": "https://sanjivnepali.com/journey/",
        "out_file": "journey/index.html",
        "title": "Career Journey & Milestones | Master Sanjiv Nepali",
        "desc": "Explore the athletic journey, championship milestones, and international medals of Master Sanjiv Nepali from 1998 to US Triple Crown and world tournaments.",
        "type": "ItemPage",
        "breadcrumb": "Journey"
    },
    {
        "slug": "gallery/",
        "url": "https://sanjivnepali.com/gallery/",
        "out_file": "gallery/index.html",
        "title": "Photo & Video Gallery | Master Sanjiv Nepali Archive",
        "desc": "Browse photos and video highlights of Master Sanjiv Nepali competing, officiating international tournaments, and training youth in martial arts.",
        "type": "CollectionPage",
        "breadcrumb": "Gallery"
    },
    {
        "slug": "press/",
        "url": "https://sanjivnepali.com/press/",
        "out_file": "press/index.html",
        "title": "Press & News Coverage | Master Sanjiv Nepali in Media",
        "desc": "Read national and international press coverage, news features, and media articles celebrating Master Sanjiv Nepali's achievements in martial arts.",
        "type": "CollectionPage",
        "breadcrumb": "Press"
    },
    {
        "slug": "contact/",
        "url": "https://sanjivnepali.com/contact/",
        "out_file": "contact/index.html",
        "title": "Contact Master Sanjiv Nepali | Seminar & Referee Booking",
        "desc": "Get in touch with Master Sanjiv Nepali for seminar bookings, black belt promotional examinations, private coaching, and tournament referee officiating.",
        "type": "ContactPage",
        "breadcrumb": "Contact"
    }
]

# NOTE: The static HTML files in this repository (e.g. index.html, about/index.html, etc.)
# are the canonical source of truth and have received full UI/UX and on-page optimization polish.
# To prevent accidentally overwriting polished pages, set FORCE_OVERWRITE = True before running this migration script.
FORCE_OVERWRITE = False

if not FORCE_OVERWRITE:
    print("Static pages are already generated and polished. To re-run full scrape migration, set FORCE_OVERWRITE = True in build_static.py.")
    exit(0)
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def generate_schema(page):
    canonical_url = f"https://sanjivnepali.com/{page['slug']}"
    graph = [
        {
            "@type": "Person",
            "@id": "https://sanjivnepali.com/#person",
            "name": "Master Sanjiv Nepali",
            "givenName": "Sanjiv",
            "familyName": "Nepali",
            "honorificPrefix": "Master",
            "jobTitle": ["5th Dan Black Belt", "International Taekwondo Champion", "Certified Referee", "Coach"],
            "url": "https://sanjivnepali.com/",
            "sameAs": [
                "https://x.com/TheSanjivNepali",
                "https://en.wikipedia.org/wiki/Sanjiv_Nepali",
                "https://www.wikidata.org/wiki/Q111812837"
            ],
            "image": "https://sanjivnepali.com/assets/uploads/MasterSanjiv-Nepali-2.png"
        },
        {
            "@type": "WebSite",
            "@id": "https://sanjivnepali.com/#website",
            "url": "https://sanjivnepali.com/",
            "name": "Master Sanjiv Nepali",
            "alternateName": "Sanjiv Nepali",
            "publisher": {
                "@id": "https://sanjivnepali.com/#person"
            },
            "inLanguage": "en-US"
        },
        {
            "@type": page["type"],
            "@id": f"{canonical_url}#webpage",
            "url": canonical_url,
            "name": page["title"],
            "description": page["desc"],
            "isPartOf": {
                "@id": "https://sanjivnepali.com/#website"
            },
            "about": {
                "@id": "https://sanjivnepali.com/#person"
            },
            "inLanguage": "en-US"
        }
    ]

    if page.get("breadcrumb"):
        graph.append({
            "@type": "BreadcrumbList",
            "@id": f"{canonical_url}#breadcrumb",
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": 1,
                    "name": "Home",
                    "item": "https://sanjivnepali.com/"
                },
                {
                    "@type": "ListItem",
                    "position": 2,
                    "name": page["breadcrumb"],
                    "item": canonical_url
                }
            ]
        })

    return {
        "@context": "https://schema.org",
        "@graph": graph
    }

for p in PAGES:
    print(f"Fetching {p['url']}...")
    req = urllib.request.Request(p["url"], headers=headers)
    with urllib.request.urlopen(req) as res:
        raw_html = res.read().decode("utf-8")

    soup = BeautifulSoup(raw_html, "html.parser")

    # Extract body content (nav + main + footer)
    body = soup.find("body")
    if not body:
        print(f"Error: no body in {p['url']}")
        continue

    # Remove WordPress admin bar, scripts, query strings, and comment nodes if present
    for s in body.find_all(["script", "style"]):
        # Keep non-WP scripts if needed, but remove wp-includes / rankmath inline scripts
        s_text = s.string or ""
        s_src = s.get("src", "")
        if "wp-" in s_src or "sitekit" in s_src or "rankmath" in s_text.lower():
            s.decompose()

    body_html = "".join(str(c) for c in body.children if c.name)

    # Path rewrites in body_html
    # Replace uploads URLs
    body_html = re.sub(
        r'https?://sanjivnepali\.com/wp-content/uploads/[0-9]{4}/[0-9]{2}/([^"\'\s]+)',
        r'/assets/uploads/\1',
        body_html
    )
    body_html = re.sub(
        r'/wp-content/uploads/[0-9]{4}/[0-9]{2}/([^"\'\s]+)',
        r'/assets/uploads/\1',
        body_html
    )

    # Replace theme asset images
    body_html = re.sub(
        r'https?://sanjivnepali\.com/wp-content/themes/master-sanjiv-theme/assets/images/([^"\'\s]+)',
        r'/assets/images/\1',
        body_html
    )
    body_html = re.sub(
        r'/wp-content/themes/master-sanjiv-theme/assets/images/([^"\'\s]+)',
        r'/assets/images/\1',
        body_html
    )

    # Fix internal link trailing slashes
    for slug in ["about", "journey", "gallery", "press", "contact"]:
        body_html = re.sub(f'href="/{slug}"([\\s>])', f'href="/{slug}/"\\1', body_html)
        body_html = re.sub(f'href="https://sanjivnepali\\.com/{slug}"([\\s>])', f'href="/{slug}/"\\1', body_html)
        body_html = re.sub(f'href="https://sanjivnepali\\.com/{slug}/"([\\s>])', f'href="/{slug}/"\\1', body_html)

    # Fix home links
    body_html = re.sub(r'href="https://sanjivnepali\.com/?"([\\s>])', r'href="/"\1', body_html)

    # Specific Fix: Journey Page 404 broken link (/media -> /gallery/)
    if p["slug"] == "journey/":
        body_html = body_html.replace('href="/media"', 'href="/gallery/"')
        body_html = body_html.replace('href="/media/"', 'href="/gallery/"')

    # Specific Fix: About Page heading order (move h1 above h2)
    if p["slug"] == "about/":
        h2_pattern = r'(<h2[^>]*>From a Quiet Nepali Town to the Global Stage</h2>\s*)(<h1[^>]*>The Inspiring Life Story of[\s\S]*?</h1>)'
        def swap_headings(match):
            return match.group(2) + "\n            " + match.group(1)
        body_html = re.sub(h2_pattern, swap_headings, body_html)

    schema_json = json.dumps(generate_schema(p), indent=2)

    canonical_url = f"https://sanjivnepali.com/{p['slug']}"

    # Build full clean document
    full_html = f"""<!DOCTYPE html>
<html lang="en-US" class="light" style="scroll-behavior: smooth;">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{p['title']}</title>
    <meta name="description" content="{p['desc']}">
    <link rel="canonical" href="{canonical_url}">
    <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">

    <!-- Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet">

    <!-- CSS -->
    <link rel="stylesheet" href="/assets/css/output.css">

    <!-- OpenGraph Social Tags -->
    <meta property="og:locale" content="en_US">
    <meta property="og:type" content="website">
    <meta property="og:title" content="{p['title']}">
    <meta property="og:description" content="{p['desc']}">
    <meta property="og:url" content="{canonical_url}">
    <meta property="og:site_name" content="Master Sanjiv Nepali">
    <meta property="og:image" content="https://sanjivnepali.com/assets/uploads/MasterSanjiv-Nepali-2.png">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta property="og:image:alt" content="Master Sanjiv Nepali">

    <!-- Twitter / X Cards -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:site" content="@TheSanjivNepali">
    <meta name="twitter:creator" content="@TheSanjivNepali">
    <meta name="twitter:title" content="{p['title']}">
    <meta name="twitter:description" content="{p['desc']}">
    <meta name="twitter:image" content="https://sanjivnepali.com/assets/uploads/MasterSanjiv-Nepali-2.png">

    <!-- Structured Data (JSON-LD) -->
    <script type="application/ld+json">
{schema_json}
    </script>
</head>
<body class="bg-background text-on-background font-body-lg antialiased selection:bg-national-crimson selection:text-white">
{body_html}

    <script src="/assets/js/main.js"></script>
</body>
</html>
"""

    out_path = os.path.join(".", p["out_file"])
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(full_html)
    print(f"Generated {out_path} ({len(full_html)} bytes)")

print("\nAll 6 pages generated successfully!")
