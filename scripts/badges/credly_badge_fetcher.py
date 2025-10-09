import requests

def fetch_badges_json(user_id):
    url = f"https://www.credly.com/users/{user_id}/badges.json"
    headers = {
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def extract_badges_html(json_data):
    badges = json_data.get("data", [])
    html = ""
    for badge in badges:
        try:
            badge_id = badge["id"]
            badge_name = badge["badge_template"]["name"]
            image_url = badge.get("image", {}).get("url") or badge.get("image_url")
            badge_url = f"https://www.credly.com/badges/{badge_id}"

            html += (
                f'<a href="{badge_url}" title="{badge_name}">'
                f'<img src="{image_url}" alt="{badge_name}" width="80" height="80" style="margin-right: 5px;">'
                f'</a>\n'
            )
        except KeyError as e:
            print(f"Skipping badge due to missing key: {e}")
    return html
