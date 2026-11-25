#!/usr/bin/env python3
"""Short tracking links: fuelpilotapp.com/fb, /reddit, ...

Each one is a tiny page that sends iPhones (and computers) to the App Store
with an App Store Connect campaign tag, and Android phones to Google Play with
a referrer tag, so both stores show which channel an install came from.
/assets/go.js does the redirect; without scripts the page shows both buttons.

Run from the repo root:  python3 _build/links.py
Add a link: add a line to LINKS (short name -> campaign name) and run again.
"""
import os

APP_ID = "6823442691"
PLAY_ID = "com.ghostsystems.fuelpilot"
# Provider ID from an App Store Connect campaign link (the pt= number).
# Leave empty and the links still open the App Store, but aren't counted.
PROVIDER_ID = "129159671"

LINKS = {
    "fb": "fb_organic",
    "reddit": "reddit",
    "yt": "youtube",
    "ig": "instagram",
    "forum": "forums",
    "qr": "offline_qr",
    "bigrig": "bigrig",
    "pr": "press",
}

PAGE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="noindex">
  <meta http-equiv="Content-Security-Policy" content="default-src 'none'; script-src 'self'; base-uri 'none'">
  <link rel="canonical" href="https://fuelpilotapp.com/">
  <title>FuelPilot</title>
</head>
<body data-ios="{ios}" data-play="{play}">
  <p><a href="{ios}">Get FuelPilot on the App Store</a></p>
  <p><a href="{play}">Get FuelPilot on Google Play</a></p>
  <script src="/assets/go.js"></script>
</body>
</html>
"""

def store_url(campaign):
    url = f"https://apps.apple.com/app/id{APP_ID}"
    if PROVIDER_ID:
        url += f"?pt={PROVIDER_ID}&amp;ct={campaign}&amp;mt=8"
    return url

def play_url(campaign):
    return (f"https://play.google.com/store/apps/details?id={PLAY_ID}"
            f"&amp;referrer=utm_source%3D{campaign}%26utm_medium%3Dlink")

for name, campaign in LINKS.items():
    os.makedirs(name, exist_ok=True)
    with open(os.path.join(name, "index.html"), "w") as f:
        f.write(PAGE.format(ios=store_url(campaign), play=play_url(campaign)))
    print(f"/{name} -> {campaign}")
