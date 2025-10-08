import requests
import re
from datetime import datetime, timezone

README_PATH = "README.md"
START_MARKER = "<!--START_SECTION:badges-->"
END_MARKER = "<!--END_SECTION:badges-->"
CREDLY_USER = "hector-rafael-rivero-marquez"

def fetch_badges():
    url = f"https://www.credly.com/users/{CREDLY_USER}/badges"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Failed to fetch Credly profile page.")
    return response.text

def extract_badge_html(page_html):
    # Extract badge blocks using regex (Credly uses <div class="badge-card">)
    badge_blocks = re.findall(r'<div class="badge-card.*?</div>', page_html, re.DOTALL)
    formatted = ""
    for block in badge_blocks[:20]:  # Limit to first 20 badges
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

    # Replace the section between the markers with new badges
    pattern = f"{START_MARKER}(.*?){END_MARKER}"
    new_section = f"{START_MARKER}\n{badge_html}\n{END_MARKER}"
    updated = re.sub(pattern, new_section, content, flags=re.DOTALL)

    # Update GitHub stats chart with timestamp to bust cache
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    updated = re.sub(r'(cache_bust=)\d+', f'\\1{timestamp}', updated)

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(updated)

if __name__ == "__main__":
    html = fetch_badges()
    badge_html = extract_badge_html(html)
    update_readme(badge_html)