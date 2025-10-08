from playwright.sync_api import sync_playwright
import re
from datetime import datetime

README_PATH = "README.md"
START_MARKER = "<!--START_SECTION:badges-->"
END_MARKER = "<!--END_SECTION:badges-->"
CREDLY_URL = "https://www.credly.com/users/hector-rafael-rivero-marquez/badges"

def fetch_badges_html():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(CREDLY_URL)
        page.wait_for_selector(".badge-card")  # Wait for badges to load
        html = page.content()
        browser.close()
        return html

def extract_badges(html):
    badge_blocks = re.findall(r'<div class="badge-card.*?</div>', html, re.DOTALL)
    formatted = ""
    for block in badge_blocks[:6]:
        img_match = re.search(r'<img.*?src="(.*?)".*?alt="(.*?)"', block)
        link_match = re.search(r'<a.*?href="(.*?)".*?>', block)
        if img_match and link_match:
            img_url, alt_text = img_match.groups()
            badge_url = "https://www.credly.com" + link_match.group(1)
            formatted += f'<a href="{badge_url}" target="_blank"><img src="{img_url}" alt="{alt_text}" width="100"/></a>\n'
    return formatted.strip()

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