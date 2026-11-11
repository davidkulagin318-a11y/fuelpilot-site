# fuelpilotapp.com

The FuelPilot website: home page, privacy policy, terms of use, support and
account deletion. Plain HTML and CSS, hosted free on GitHub Pages.

## Pages

| URL | File | Used for |
|---|---|---|
| `/` | built from `_build/pages/home.html` | Home page |
| `/privacy/` | built from `_build/pages/privacy.html` | App Store Connect and Play Console privacy policy URL; `EXPO_PUBLIC_PRIVACY_URL` in the app |
| `/support/` | built from `_build/pages/support.html` | App Store Connect support URL |
| `/terms/` | built from `_build/pages/terms.html` | Terms of use (Apple's standard EULA still applies to App Store purchases) |
| `/delete-account/` | built from `_build/pages/delete-account.html` | Play Console "delete account" URL |

## Editing

- Every page shares one header and footer. Edit the body in `_build/pages/`
  (`home.html` is the home page), then run `python3 _build/build.py` from this
  folder to rebuild them all.
- Styles are in `assets/site.css`. The look matches the app: graphite, the
  logo's blue, Barlow Semi Condensed (SIL Open Font License,
  `assets/fonts/OFL.txt`), squared shapes.
- The site loads nothing from other websites and runs no scripts. Each page
  carries a Content-Security-Policy that enforces this (set in `build.py`), so
  don't add inline `style="..."` attributes or `<script>` tags; they won't run.
- `.well-known/security.txt` has an `Expires` date. Move it forward once a year.

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

Swap the "Coming soon to the App Store" pill in `_build/pages/home.html` for Apple's
"Download on the App Store" badge, linked to
`https://apps.apple.com/app/id6823442691`, and add
`<meta name="apple-itunes-app" content="app-id=6823442691">` to `HEAD` in
`_build/build.py` for Safari's app banner.
