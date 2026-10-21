# fuelpilotapp.com

The FuelPilot website: home page, privacy policy, terms of use, support and
account deletion. Plain HTML and CSS, hosted free on GitHub Pages.

## Pages

| URL | File | Used for |
|---|---|---|
| `/` | `index.html` | Home page |
| `/privacy/` | built from `_build/pages/privacy.html` | App Store Connect and Play Console privacy policy URL; `EXPO_PUBLIC_PRIVACY_URL` in the app |
| `/support/` | built from `_build/pages/support.html` | App Store Connect support URL |
| `/terms/` | built from `_build/pages/terms.html` | Terms of use (Apple's standard EULA still applies to App Store purchases) |
| `/delete-account/` | built from `_build/pages/delete-account.html` | Play Console "delete account" URL |

## Editing

- The home page is `index.html`; edit it directly.
- The other pages share a header and footer. Edit the body in `_build/pages/`,
  then run `python3 _build/build.py` from this folder to rebuild them.
- Styles are in `assets/site.css`. The font is Overpass (SIL Open Font
  License, `assets/fonts/OFL.txt`), served from this site so pages load
  nothing from other websites.

GitHub Pages leaves `_build/` out of the live site because the folder name
starts with an underscore.

## Hosting

GitHub Pages, from the `main` branch, root folder, with the custom domain in
`CNAME` (fuelpilotapp.com) and "Enforce HTTPS" on.

DNS at Porkbun for fuelpilotapp.com:

| Type | Host | Answer |
|---|---|---|
| A | (blank) | 185.199.108.153 |
| A | (blank) | 185.199.109.153 |
| A | (blank) | 185.199.110.153 |
| A | (blank) | 185.199.111.153 |
| CNAME | www | davidkulagin318-a11y.github.io |

## When the app is live

Swap the "Coming soon to the App Store" pill on the home page for Apple's
"Download on the App Store" badge, linked to
`https://apps.apple.com/app/id6823442691`, and add
`<meta name="apple-itunes-app" content="app-id=6823442691">` to the home
page's `<head>` for Safari's app banner.
