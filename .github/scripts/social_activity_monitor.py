import requests
import os
import sys

USER = "Adminrivero"
TOKEN = os.getenv("USER_PAT")

if not TOKEN:
    print("Error: USER_PAT environment variable is missing.")
    sys.exit(1)

headers = {'Authorization': f'token {TOKEN}'}

def get_all_users(endpoint):
    users = []
    page = 1
    while True:
        res = requests.get(f"https://api.github.com/users/{USER}/{endpoint}?per_page=100&page={page}", headers=headers)
        data = res.json()
        
        if not data or isinstance(data, dict): 
            break 
            
        users.extend([u['login'] for u in data])
        page += 1
    return set(users)

followers = get_all_users("followers")
following = get_all_users("following")
unfollowers = following - followers
summary_file = os.getenv("GITHUB_STEP_SUMMARY")

if summary_file:
    with open(summary_file, "a") as f:
        f.write(f"## 📊 GitHub Follower Status\n")
        f.write(f"- **Following:** {len(following)}\n")
        f.write(f"- **Followers:** {len(followers)}\n")
        f.write(f"- **Lost Followers:** {len(unfollowers)}\n\n")

        if unfollowers:
            f.write("### 🕵️ Sneaky Unfollowers:\n")
            for u in sorted(unfollowers):
                f.write(f"- [@{u}](https://github.com/{u})\n")
        else:
            f.write("### All good! No discrepancies detected in this week's social graph. ✅\n")
else:
    print("Summary file not found. This script is designed to run in GitHub Actions.")