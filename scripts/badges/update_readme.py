from credly_badge_fetcher import fetch_badges_json, extract_badges_html
import datetime

USER_ID = "6a916bbc-de5c-453a-8acd-63a7e3efa80c"
README_PATH = "README.md"
BADGE_START = "<!--START_SECTION:badges-->"
BADGE_END = "<!--END_SECTION:badges-->"

def update_readme():
    json_data = fetch_badges_json(USER_ID)
    badge_html = extract_badges_html(json_data)

    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    start = content.find(BADGE_START)
    end = content.find(BADGE_END)

    if start == -1 or end == -1:
        raise ValueError("Badge markers not found in README.md")

    updated = (
        content[:start + len(BADGE_START)] + "\n" +
        badge_html +
        content[end:]
    )

    # Update GitHub stats chart timestamp
    updated = update_stats_timestamp(updated)

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(updated)

def update_stats_timestamp(content):
    timestamp = datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S")
    return content.replace("cache_bust=", f"cache_bust={timestamp}")

if __name__ == "__main__":
    update_readme()