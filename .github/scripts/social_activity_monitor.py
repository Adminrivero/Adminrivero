import requests
import os
import sys

USER = "Adminrivero"
TOKEN = os.getenv("USER_PAT")

if not TOKEN:
    print("Error: USER_PAT environment variable is missing.")
    sys.exit(1)

headers = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github+json",
    "User-Agent": "social-activity-monitor",
}

def get_all_users(endpoint):
    users = []
    page = 1
    
    while True:
        res = requests.get(
            f"https://api.github.com/users/{USER}/{endpoint}?per_page=100&page={page}", 
            headers=headers, 
            timeout=30,
        )
        res.raise_for_status()
        data = res.json()
        
        if not data: 
            break 
            
        users.extend([u['login'] for u in data])
        page += 1
        
    return set(users)

try:
    followers = get_all_users("followers")
    following = get_all_users("following")
except requests.RequestException as exc:
    print(f"GitHub API request failed: {exc}")
    sys.exit(1)

unfollowers = following - followers
summary_file = os.getenv("GITHUB_STEP_SUMMARY")

if summary_file:
    with open(summary_file, "a", encoding="utf-8") as f:
        f.write(f"## 📊 GitHub Follower Status\n")
        f.write(f"- **Following:** {len(following)}\n")
        f.write(f"- **Followers:** {len(followers)}\n")
        f.write(f"- **Lost Followers:** {len(unfollowers)}\n\n")

        if unfollowers:
            f.write("### 🕵️ Sneaky Unfollowers:\n")
            for u in sorted(unfollowers):
                f.write(f"- [@{u}](https://github.com/{u})\n")
        else:
            f.write("### No discrepancies detected in this week's social graph. ✅\n")
else:
    print("Summary file not found. This script is designed to run in GitHub Actions.")