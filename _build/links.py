#!/usr/bin/env python3
"""Short tracking links: fuelpilotapp.com/fb, /reddit, ...

Each one is a tiny page that sends the visitor to the App Store with an
App Store Connect campaign tag, so Analytics shows which channel an install
came from. The site runs no scripts, so these use a plain meta refresh.

Run from the repo root:  python3 _build/links.py
Add a link: add a line to LINKS (short name -> campaign name) and run again.
"""
import os

APP_ID = "6823442691"
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
  <meta http-equiv="refresh" content="0; url={url}">
  <link rel="canonical" href="https://fuelpilotapp.com/">
  <title>FuelPilot</title>
</head>
<body>
  <p><a href="{url}">Get FuelPilot on the App Store</a></p>
</body>
</html>
"""

def store_url(campaign):
    url = f"https://apps.apple.com/app/id{APP_ID}"
    if PROVIDER_ID:
        url += f"?pt={PROVIDER_ID}&amp;ct={campaign}&amp;mt=8"
    return url

for name, campaign in LINKS.items():
    os.makedirs(name, exist_ok=True)
    with open(os.path.join(name, "index.html"), "w") as f:
        f.write(PAGE.format(url=store_url(campaign)))
    print(f"/{name} -> {campaign}")
