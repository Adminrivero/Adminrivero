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
    
    # Define target badges with override properties
    target_badges = [
        {
            "target_name": "CS50P",
            "override_image_path": "./res/badges/cs50p_badge.png",
            "override_height": 80,
            "override_width": 90
        },
        {
            "target_name": "CS50P",
            "override_image_path": "./res/badges/cs50p_badge_w.png",
            "override_height": 80,
            "override_width": 110
        }
    ]
    
    for badge in badges:
        try:
            badge_id = badge["id"]
            badge_name = badge["badge_template"]["name"]
            
            # Get default remote image URL from Credly
            image_url = badge.get("image", {}).get("url") or badge.get("image_url")
            # Set default dimensions
            width, height = 80, 80
            
            # Check for overrides
            for target in target_badges:
                if target["target_name"] in badge_name:
                    image_url = target["override_image_path"]
                    height = target["override_height"]
                    width = target["override_width"]
                    break
            
            # Construct badge URL
            badge_url = f"https://www.credly.com/badges/{badge_id}"
            
            # Generate HTML snippet
            html += (
                f'<a href="{badge_url}" title="{badge_name}">'
                f'<img src="{image_url}" alt="{badge_name}" width="{width}" height="{height}" style="margin-right: 5px;">'
                f'</a>\n'
            )
        except KeyError as e:
            print(f"Skipping badge due to missing key: {e}")
    
    return html
