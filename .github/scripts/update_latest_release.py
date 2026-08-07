#!/usr/bin/env python3
"""Render the homepage Latest Release block from latest-release.json.

To change the featured book, edit latest-release.json only. Optional keys:
  audio_note  - text for a book-audio-badge line (headphones icon)
Each entry in "buttons" needs: url, class, icon, label.
"""
import json
import pathlib
import re

root = pathlib.Path(__file__).resolve().parents[2]
data = json.loads((root / "latest-release.json").read_text(encoding="utf-8"))
html = (root / "index.html").read_text(encoding="utf-8")

buttons = "\n".join(
    f'                        <a href="{data_b["url"]}" class="buy-button {data_b["class"]}" '
    f'target="_blank" rel="noopener noreferrer"><i class="{data_b["icon"]}" aria-hidden="true"></i> {data_b["label"]}</a>'
    for data_b in data["buttons"]
)
audio = ""
if data.get("audio_note"):
    audio = (
        '\n                    <p class="book-audio-badge">'
        '<i class="fas fa-headphones-alt" aria-hidden="true"></i> '
        f'{data["audio_note"]}</p>'
    )

block = f'''        <section aria-label="Latest release">
            <h2>Latest Release</h2>
            <div class="book-container">
                <a href="{data["page"]}" style="text-decoration: none;"><picture><source srcset="{data["cover"]}-500w.webp 500w, {data["cover"]}.webp 1500w" sizes="(max-width: 768px) 50vw, 250px" type="image/webp"><img src="{data["cover"]}.jpg" alt="{data["alt"]}" class="book-cover" width="250" height="375" loading="lazy"></picture></a>
                <div class="book-info">
                    <h3><a href="{data["page"]}" style="color: inherit; text-decoration: none;">{data["title"]}</a></h3>
                    <p>{data["description"]}</p>{audio}
                    <div class="buy-group">
{buttons}
                    </div>
                    <p class="ku-badge"><i class="fab fa-amazon" aria-hidden="true"></i> {data["ku_line"]}</p>
                </div>
            </div>
        </section>'''

new = re.sub(
    r'[ \t]*<section aria-label="Latest release">.*?</section>',
    lambda m: block,
    html,
    count=1,
    flags=re.S,
)
if new != html:
    (root / "index.html").write_text(new, encoding="utf-8")
    print("Latest Release block updated.")
else:
    print("No change.")
