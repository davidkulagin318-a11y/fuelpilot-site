"""Builds the text pages (privacy, terms, support, delete-account, 404) from the
page bodies in _build/pages/, wrapped in the shared header and footer.

Run from the repo root:  python3 _build/build.py
The home page (index.html) is edited directly. GitHub Pages does not publish
folders that start with an underscore, so _build/ stays out of the live site.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = ROOT / '_build' / 'pages'

# slug -> (output path, <title>, meta description, nav item to mark current)
SITE = {
    'privacy': ('privacy/index.html', 'Privacy policy | FuelPilot',
                'What data the FuelPilot app collects, why, where it goes, and how to delete it.', 'privacy'),
    'terms': ('terms/index.html', 'Terms of use | FuelPilot',
              'The terms for using the FuelPilot app, FuelPilot Pro and this website.', None),
    'support': ('support/index.html', 'Support | FuelPilot',
                'Help with FuelPilot: fuel prices, navigation, exports, receipts and FuelPilot Pro.', 'support'),
    'delete-account': ('delete-account/index.html', 'Delete your account | FuelPilot',
                       'How to delete your FuelPilot account and data, in the app or by email.', None),
    '404': ('404.html', 'Page not found | FuelPilot', 'This page does not exist.', None),
}

HEAD = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{description}">
{canonical}  <meta name="theme-color" content="#ffffff" media="(prefers-color-scheme: light)">
  <meta name="theme-color" content="#0d1620" media="(prefers-color-scheme: dark)">
  <meta property="og:site_name" content="FuelPilot">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:image" content="https://fuelpilotapp.com/assets/og.png">
  <link rel="icon" href="/favicon.ico" sizes="any">
  <link rel="icon" type="image/png" href="/assets/favicon-48.png">
  <link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
  <link rel="preload" href="/assets/fonts/overpass-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="/assets/site.css">
</head>
<body>
  <a class="skip" href="#main">Skip to content</a>

  <header class="site-header">
    <div class="wrap">
      <a class="brand" href="/" aria-label="FuelPilot home">
        <img src="/assets/icon-128.png" width="36" height="36" alt="">
        FuelPilot
      </a>
      <nav class="site-nav" aria-label="Main">
        <a href="/support/"{support_current}>Support</a>
        <a href="/privacy/"{privacy_current}>Privacy</a>
      </nav>
    </div>
  </header>

  <main id="main" class="page">
    <div class="wrap">
"""

FOOT = """    </div>
  </main>

  <footer class="site-footer">
    <div class="wrap">
      <nav class="footer-links" aria-label="Footer">
        <a href="/support/">Support</a>
        <a href="/privacy/">Privacy policy</a>
        <a href="/terms/">Terms of use</a>
        <a href="/delete-account/">Delete your account</a>
      </nav>
      <p>Questions? <a href="mailto:support@fuelpilotapp.com">support@fuelpilotapp.com</a></p>
      <p>&copy; 2026 David Kulagin</p>
    </div>
  </footer>
</body>
</html>
"""


def main() -> None:
    for slug, (out, title, description, current) in SITE.items():
        body = (PAGES / f'{slug}.html').read_text()
        url_path = '/' if slug == '404' else f'/{slug}/'
        canonical = '' if slug == '404' else f'  <link rel="canonical" href="https://fuelpilotapp.com{url_path}">\n'
        head = HEAD.format(
            title=title,
            description=description,
            canonical=canonical,
            support_current=' aria-current="page"' if current == 'support' else '',
            privacy_current=' aria-current="page"' if current == 'privacy' else '',
        )
        indented = ''.join(('      ' + line) if line.strip() else line for line in body.splitlines(True))
        target = ROOT / out
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(head + indented + FOOT)
        print('wrote', out)


if __name__ == '__main__':
    main()
