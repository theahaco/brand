#!/usr/bin/env python3
"""Generate LinkedIn profile banners; run with Python 3 and rsvg-convert.

Editable SVGs embed the website's brand fonts and original logo paths.
PNG rendering requires Space Grotesk and Spectral installed locally because
librsvg uses system fonts. The SVGs also contain webfonts for browser use.
Keep essential content outside the left 420 px to allow for profile photos.
"""

import base64
from html import escape
from pathlib import Path
import shutil
import subprocess
import xml.etree.ElementTree as ET


OUT = Path(__file__).resolve().parent
BRAND = OUT.parent
FONTS = BRAND.parent / "theaha.github.io/node_modules/@fontsource"
BLUE = "#1A3B60"
GREEN = "#47A019"
PINK = "#F6E2FF"
TAN = "#D6BDBE"


def font_face(family, slug, filename, style):
    data = base64.b64encode((FONTS / slug / "files" / filename).read_bytes()).decode()
    return (
        f"@font-face{{font-family:'{family}';font-style:{style};"
        f"font-weight:{400 if style == 'italic' else 500};"
        f"src:url(data:font/woff2;base64,{data}) format('woff2');}}"
    )


def logo(color):
    # Preserve the approved artwork exactly; only position and scale it.
    root = ET.parse(BRAND / "logos" / f"logotype_{color}.svg").getroot()
    paths = "".join(
        f'<path d="{p.attrib["d"]}"/>'
        for p in root.iter("{http://www.w3.org/2000/svg}path")
    )
    fill = "#FFFFFF" if color == "white" else BLUE
    return (
        f'<g id="aha-logo" aria-label="Aha" fill="{fill}" '
        'transform="translate(1304 59) scale(.18) translate(-250 -250)">'
        f"{paths}</g>"
    )


def text(x, y, content, size, color, display=False, extra=""):
    family = "Spectral" if display else "Space Grotesk"
    style = "italic" if display else "normal"
    weight = 400 if display else 500
    return (
        f'<text x="{x}" y="{y}" fill="{color}" font-family="{family}" '
        f'font-size="{size}" font-weight="{weight}" font-style="{style}" '
        f'{extra}>{escape(content)}</text>'
    )


CSS = font_face(
    "Space Grotesk", "space-grotesk",
    "space-grotesk-latin-500-normal.woff2", "normal",
) + font_face(
    "Spectral", "spectral", "spectral-latin-400-italic.woff2", "italic",
)


def save(name, title, description, body):
    svg = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<svg xmlns="http://www.w3.org/2000/svg" width="1584" height="396" '
        'viewBox="0 0 1584 396" role="img" aria-labelledby="title desc">\n'
        f"<title id=\"title\">{escape(title)}</title>\n"
        f"<desc id=\"desc\">{escape(description)}</desc>\n"
        f"<defs><style>{CSS}</style></defs>\n{body}\n</svg>\n"
    )
    path = OUT / f"{name}.svg"
    path.write_text(svg)
    subprocess.run(
        ["rsvg-convert", str(path), "--output", str(OUT / f"{name}.png")],
        check=True,
    )
    print(f"Created {name}.svg and {name}.png")


def main():
    if not shutil.which("rsvg-convert"):
        raise SystemExit("Install librsvg (brew install librsvg) to render the PNGs.")
    for slug in ("space-grotesk", "spectral"):
        shutil.copyfile(FONTS / slug / "LICENSE", OUT / f"LICENSE-{slug}.txt")

    # Option 1: full positioning statement, with a quiet blueprint field.
    grid = "".join(
        f'<path d="M{x} 0V396" stroke="white" stroke-opacity=".055"/>'
        for x in range(0, 405, 36)
    ) + "".join(
        f'<path d="M0 {y}H396" stroke="white" stroke-opacity=".055"/>'
        for y in range(0, 397, 36)
    )
    dark = f"""
<rect width="1584" height="396" fill="{BLUE}"/>
<g id="blueprint" aria-hidden="true">{grid}</g>
<g id="integration-paths" aria-hidden="true" fill="none" stroke-width="2">
  <path d="M-40 115H140Q160 115 160 135V177Q160 197 180 197H344" stroke="{PINK}" stroke-opacity=".38"/>
  <path d="M-40 279H96Q116 279 116 259V217Q116 197 136 197H344" stroke="{GREEN}" stroke-opacity=".85"/>
  <circle cx="344" cy="197" r="6" fill="{GREEN}" stroke="{BLUE}" stroke-width="3"/>
</g>
{logo("white")}
{text(450, 102, "BLOCKCHAIN INTEGRATION PARTNER", 17, PINK, extra='letter-spacing="2.3"')}
{text(446, 184, "We integrate institutions and protocols", 47, "#FFFFFF", True)}
{text(446, 246, "onto the networks we help build.", 47, "#FFFFFF", True)}
<path d="M450 301H494" stroke="{GREEN}" stroke-width="3"/>
{text(510, 308, "theaha.co", 22, "#FFFFFF")}
"""
    save(
        "linkedin-team-networks",
        "Aha — Blockchain integration partner",
        "We integrate institutions and protocols onto the networks we help build. theaha.co",
        dark,
    )

    # Option 2: shorter About-page message, with two equal interlocking routes.
    light = f"""
<rect width="1584" height="396" fill="{PINK}"/>
<g id="integration-paths" aria-hidden="true" fill="none" stroke-width="2">
  <path d="M-40 91H174Q198 91 198 115V185Q198 209 222 209H346" stroke="{BLUE}" stroke-opacity=".28"/>
  <path d="M-40 311H110Q134 311 134 287V233Q134 209 158 209H346" stroke="{GREEN}" stroke-opacity=".8"/>
  <circle cx="346" cy="209" r="7" fill="{GREEN}" stroke="{PINK}" stroke-width="3"/>
  <circle cx="62" cy="91" r="5" fill="{BLUE}" stroke="{PINK}" stroke-width="3"/>
  <circle cx="62" cy="311" r="5" fill="{GREEN}" stroke="{PINK}" stroke-width="3"/>
</g>
{logo("blue")}
{text(450, 102, "BLOCKCHAIN INTEGRATION PARTNER", 17, BLUE, extra='letter-spacing="2.3"')}
{text(446, 183, "We build the tooling.", 59, BLUE, True)}
{text(446, 252, "We do the integrations.", 59, BLUE, True)}
{text(450, 312, "Institutions · Protocols · Ecosystems", 21, BLUE)}
{text(1466, 312, "theaha.co", 22, BLUE, extra='text-anchor="end"')}
"""
    save(
        "linkedin-team-tooling",
        "Aha — We build the tooling. We do the integrations.",
        "Blockchain integration partner for institutions, protocols and ecosystems. theaha.co",
        light,
    )


if __name__ == "__main__":
    main()
