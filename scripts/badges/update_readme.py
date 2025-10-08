from datetime import datetime
import re
import os
from scripts.badges.credly_scraper import fetch_badges_html, extract_badges

README_PATH = "README.md"
START_MARKER = "<!--START_SECTION:badges-->"
END_MARKER = "<!--END_SECTION:badges-->"

def update_readme(badge_html):
    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    pattern = f"{START_MARKER}(.*?){END_MARKER}"
    new_section = f"{START_MARKER}\n{badge_html}\n{END_MARKER}"
    updated = re.sub(pattern, new_section, content, flags=re.DOTALL)

    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    updated = re.sub(r'(cache_bust=)\d+', f'\\1{timestamp}', updated)

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(updated)

if __name__ == "__main__":
    html = fetch_badges_html()
    badge_html = extract_badges(html)
    update_readme(badge_html)