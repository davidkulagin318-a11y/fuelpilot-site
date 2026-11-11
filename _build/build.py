"""Builds every page of the site from the page bodies in _build/pages/, wrapped
in the shared header and footer.

Run from the repo root:  python3 _build/build.py
GitHub Pages does not publish folders that start with an underscore, so
_build/ stays out of the live site.
"""
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
              'The terms for using the FuelPilot app, FuelPilot Pro and this website.', None),
    'support': ('support/index.html', 'Support | FuelPilot',
                'Help with FuelPilot: fuel prices, Autopilot, navigation, exports, receipts and FuelPilot Pro.', 'support'),
    'delete-account': ('delete-account/index.html', 'Delete your account | FuelPilot',
                       'How to delete your FuelPilot account and data, in the app or by email.', None),
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
{canonical}  <meta name="theme-color" content="#0f0f10">
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
</head>
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
            main_open='  <main id="main">\n' if home else '  <main id="main" class="page">\n    <div class="wrap">\n',
        )
        pad = '    ' if home else '      '
        indented = ''.join((pad + line) if line.strip() else line for line in body.splitlines(True))
        foot = FOOT.format(main_close='  </main>' if home else '    </div>\n  </main>')
        target = ROOT / out
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(head + indented + foot)
        print('wrote', out)


if __name__ == '__main__':
    main()
