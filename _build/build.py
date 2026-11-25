"""Builds every page of the site from the page bodies in _build/pages/, wrapped
in the shared header and footer.

Run from the repo root:  python3 _build/build.py
GitHub Pages does not publish folders that start with an underscore, so
_build/ stays out of the live site.
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = ROOT / '_build' / 'pages'

HOME_TITLE = 'FuelPilot: navigation that plans your fuel stops'
HOME_DESC = ('FuelPilot is navigation that plans your fuel stops. It checks prices along your route, '
             'picks the cheapest stops you can reach and logs every trip for tax time.')

# slug -> (output path, <title>, meta description, nav item to mark current)
SITE = {
    'home': ('index.html', HOME_TITLE, HOME_DESC, None),
    'privacy': ('privacy/index.html', 'Privacy policy | FuelPilot',
                'What data the FuelPilot app collects, why, where it goes, and how to delete it.', 'privacy'),
    'terms': ('terms/index.html', 'Terms of use | FuelPilot',
              'The terms for using the FuelPilot app, FuelPilot Pro, FuelPilot Big Rig and this website.', None),
    'support': ('support/index.html', 'Support | FuelPilot',
                'Help with FuelPilot: fuel prices, Autopilot, navigation, Big Rig truck routes, exports, receipts and subscriptions.', 'support'),
    'delete-account': ('delete-account/index.html', 'Delete your account | FuelPilot',
                       'How to delete your FuelPilot account and data, in the app or by email.', None),
    'towing': ('towing/index.html', 'Fuel stop planner for towing a trailer or RV | FuelPilot',
               'Plan fuel stops around your real towing range. FuelPilot adjusts range for the trailer, picks the cheapest station you can reach and navigates you there.', None),
    'big-rig': ('big-rig/index.html', 'Truck GPS that plans your fuel stops | FuelPilot Big Rig',
                'Truck-legal routes for your rig\'s height, weight and length, fuel stops at truck stops and truck lanes only, and IFTA miles by state. For semis, hot shots and RVs.', None),
    'mileage-log': ('mileage-log/index.html', 'Automatic mileage log and fuel expense tracker | FuelPilot',
                    'FuelPilot logs every drive you navigate with miles, time and fuel. Tag trips business or personal and export a mileage log or fuel expense report.', None),
    '404': ('404.html', 'Page not found | FuelPilot', 'This page does not exist.', None),
}

# The site loads nothing from other websites and runs no scripts; this policy
# makes the browser enforce that. GitHub Pages can't send response headers, so
# it is set here in each page.
CSP = ("default-src 'none'; style-src 'self'; img-src 'self'; font-src 'self'; "
       "base-uri 'none'; form-action 'none'")

CHECK = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" '
         'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7"/></svg>')

HEAD = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta http-equiv="Content-Security-Policy" content="{csp}">
  <meta name="referrer" content="strict-origin-when-cross-origin">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <meta name="apple-itunes-app" content="app-id=6823442691">
{canonical}  <meta name="theme-color" content="#0f0f10">
  <meta name="color-scheme" content="dark">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="FuelPilot">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:image" content="https://fuelpilotapp.com/assets/og.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="/favicon.ico" sizes="any">
  <link rel="icon" type="image/png" href="/assets/favicon-48.png">
  <link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
  <link rel="preload" href="/assets/fonts/barlow-semi-condensed-regular.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="/assets/fonts/barlow-semi-condensed-semibold.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="/assets/site.css">
{jsonld}</head>
<body>
  <a class="skip" href="#main">Skip to content</a>

  <header class="site-header">
    <div class="wrap">
      <a class="brand" href="/" aria-label="FuelPilot home">
        <img src="/assets/icon-128.png" width="40" height="40" alt="">
        FuelPilot
      </a>
      <nav class="site-nav" aria-label="Main">
        <a href="/support/"{support_current}>Support</a>
        <a href="/privacy/"{privacy_current}>Privacy</a>
      </nav>
    </div>
  </header>

{main_open}"""

FOOT = """{main_close}

  <footer class="site-footer">
    <div class="wrap">
      <nav class="footer-links" aria-label="Footer">
        <a href="/towing/">Towing and RVs</a>
        <a href="/big-rig/">Truckers</a>
        <a href="/mileage-log/">Mileage log</a>
        <a href="/support/">Support</a>
        <a href="/privacy/">Privacy policy</a>
        <a href="/terms/">Terms of use</a>
        <a href="/delete-account/">Delete your account</a>
      </nav>
      <p>Questions? <a href="mailto:support@fuelpilotapp.com">support@fuelpilotapp.com</a></p>
      <p>&copy; 2026 Ghost Systems LLC</p>
    </div>
  </footer>
</body>
</html>
"""


APP_STORE = 'https://apps.apple.com/app/id6823442691'
PLAY = 'https://play.google.com/store/apps/details?id=com.ghostsystems.fuelpilot'

# Structured data. Search engines and AI assistants read these facts directly,
# so keep them in step with the plans section on the home page.
ORG = {
    '@type': 'Organization',
    '@id': 'https://fuelpilotapp.com/#org',
    'name': 'Ghost Systems LLC',
    'url': 'https://fuelpilotapp.com/',
    'logo': 'https://fuelpilotapp.com/assets/icon-512.png',
    'email': 'support@fuelpilotapp.com',
    'founder': {'@type': 'Person', 'name': 'David Kulagin', 'jobTitle': 'Founder'},
    'sameAs': ['https://www.instagram.com/fuelpilotapp', 'https://www.youtube.com/@fuelpilotapp'],
}


def offer(name, price, period=None):
    o = {'@type': 'Offer', 'name': name, 'price': price, 'priceCurrency': 'USD'}
    if period:
        o['priceSpecification'] = {
            '@type': 'UnitPriceSpecification', 'price': price, 'priceCurrency': 'USD',
            'billingDuration': 1, 'unitCode': 'MON' if period == 'month' else 'ANN',
        }
    return o


APP = {
    '@type': 'MobileApplication',
    '@id': 'https://fuelpilotapp.com/#app',
    'name': 'FuelPilot',
    'description': ('Turn-by-turn navigation for iPhone and Android that plans your fuel stops. It knows your tank size, '
                    'learns your real MPG and checks fuel prices along your whole route, then picks the cheapest stations '
                    'you can reach. Towing mode, truck-legal routing (Big Rig) and a trip logbook with mileage and IFTA exports.'),
    'url': 'https://fuelpilotapp.com/',
    'image': 'https://fuelpilotapp.com/assets/icon-512.png',
    'screenshot': 'https://fuelpilotapp.com/assets/phone-screen.webp',
    'operatingSystem': 'iOS, Android',
    'applicationCategory': 'TravelApplication',
    'applicationSubCategory': 'Navigation',
    'downloadUrl': [APP_STORE, PLAY],
    'installUrl': [APP_STORE, PLAY],
    'countriesSupported': ['US', 'CA'],
    'inLanguage': 'en',
    'publisher': {'@id': 'https://fuelpilotapp.com/#org'},
    'audience': {'@type': 'Audience', 'audienceType': 'Drivers of diesel pickups, RVs, trailers, hot shots and semis; people who log miles for work'},
    'featureList': [
        'Turn-by-turn navigation with spoken directions',
        'Fuel Autopilot: plans every fuel stop for the trip at the cheapest station you can reach',
        'Fuel prices along your route',
        'Learns your real MPG from fill-ups',
        'Towing mode adjusts range for a trailer',
        'Big Rig: truck-legal routes for height, weight and length; truck stops and truck lanes only',
        'Automatic trip logbook',
        'Mileage log, fuel expense and IFTA exports',
        'Receipt photo reading',
    ],
    'offers': [
        offer('Free', '0'),
        offer('FuelPilot Pro monthly', '7.99', 'month'),
        offer('FuelPilot Pro yearly', '49.99', 'year'),
        offer('FuelPilot Big Rig monthly', '19.99', 'month'),
        offer('FuelPilot Big Rig yearly', '199.99', 'year'),
    ],
}


def text(fragment: str) -> str:
    """Plain text from a bit of page HTML."""
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', fragment))).strip()


def faq_pairs(body: str):
    """Question/answer pairs: every <h3> that asks a question, with the paragraphs
    under it. On pages with a <!-- faq --> block, only that block counts."""
    m = re.search(r'<!-- faq -->(.*?)<!-- /faq -->', body, re.S)
    region = m.group(1) if m else body
    pairs = []
    for q, a in re.findall(r'<h3>(.*?)</h3>(.*?)(?=<h[23]|<!-- /faq|$)', region, re.S):
        q = text(q)
        if q.endswith('?'):
            pairs.append((q, ' '.join(text(p) for p in re.findall(r'<p>(.*?)</p>', a, re.S))))
    return pairs


def jsonld(slug: str, body: str, title: str, url: str) -> str:
    graph = []
    if slug == 'home':
        graph += [ORG, APP, {'@type': 'WebSite', '@id': 'https://fuelpilotapp.com/#site', 'name': 'FuelPilot',
                             'url': 'https://fuelpilotapp.com/', 'publisher': {'@id': 'https://fuelpilotapp.com/#org'}}]
    elif slug in ('towing', 'big-rig', 'mileage-log'):
        graph.append({'@type': 'WebPage', 'name': title, 'url': url, 'about': {'@id': 'https://fuelpilotapp.com/#app'},
                      'breadcrumb': {'@type': 'BreadcrumbList', 'itemListElement': [
                          {'@type': 'ListItem', 'position': 1, 'name': 'FuelPilot', 'item': 'https://fuelpilotapp.com/'},
                          {'@type': 'ListItem', 'position': 2, 'name': text(re.search(r'<h1>(.*?)</h1>', body).group(1)), 'item': url}]}})
    pairs = faq_pairs(body) if slug in ('home', 'support', 'towing', 'big-rig', 'mileage-log') else []
    if pairs:
        graph.append({'@type': 'FAQPage', 'url': url, 'mainEntity': [
            {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in pairs]})
    if not graph:
        return ''
    data = json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False, indent=1)
    return '  <script type="application/ld+json">\n' + data.replace('</', '<\\/') + '\n  </script>\n'


def llms_full() -> str:
    """llms-full.txt: the site's own words as plain text, built from the same
    pages so it never drifts from them."""
    out = [Path(ROOT / 'llms.txt').read_text().strip(), '']
    for slug, label in (('home', 'Home page'), ('towing', 'Towing and RVs'), ('big-rig', 'Big Rig, for truckers'),
                        ('mileage-log', 'Mileage log'), ('support', 'Support and FAQ')):
        body = (PAGES / f'{slug}.html').read_text()
        body = re.sub(r'<(svg|ul class="toc"|p class="cta-row")[^>]*>.*?</(svg|ul|p)>', '', body, flags=re.S)
        body = re.sub(r'<section class="hero">.*?</section>', '', body, flags=re.S)
        url = 'https://fuelpilotapp.com/' + ('' if slug == 'home' else slug + '/')
        out.append(f'\n## {label} ({url})\n')
        for tag, inner in re.findall(r'<(h1|h2|h3|p|li|dt|dd)[^>]*>(.*?)</\1>', body, re.S):
            t = text(inner.replace('{check}', ''))
            if not t:
                continue
            out.append({'h1': '### ', 'h2': '### ', 'h3': '#### ', 'li': '- ', 'dt': '- ', 'dd': '  '}.get(tag, '') + t)
    return '\n'.join(out).replace('\n\n\n', '\n\n') + '\n'


def main() -> None:
    for slug, (out, title, description, current) in SITE.items():
        body = (PAGES / f'{slug}.html').read_text().replace('{check}', CHECK)
        home = slug == 'home'
        url_path = '/' if home else f'/{slug}/'
        canonical = '' if slug == '404' else f'  <link rel="canonical" href="https://fuelpilotapp.com{url_path}">\n'
        head = HEAD.format(
            csp=CSP,
            title=title,
            description=description,
            canonical=canonical,
            support_current=' aria-current="page"' if current == 'support' else '',
            privacy_current=' aria-current="page"' if current == 'privacy' else '',
            jsonld=jsonld(slug, body, title, 'https://fuelpilotapp.com' + url_path),
            main_open='  <main id="main">\n' if home else '  <main id="main" class="page">\n    <div class="wrap">\n',
        )
        pad = '    ' if home else '      '
        indented = ''.join((pad + line) if line.strip() else line for line in body.splitlines(True))
        foot = FOOT.format(main_close='  </main>' if home else '    </div>\n  </main>')
        target = ROOT / out
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(head + indented + foot)
        print('wrote', out)
    (ROOT / 'llms-full.txt').write_text(llms_full())
    print('wrote llms-full.txt')


if __name__ == '__main__':
    main()
