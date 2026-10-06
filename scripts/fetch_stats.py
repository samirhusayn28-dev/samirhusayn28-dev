"""Public GitHub API -> data/stats.json (works without a token; Actions passes GITHUB_TOKEN for rate limit)."""
import os, json, requests
from collections import Counter

USER = os.environ.get("GH_USER", "samirhusayn28-dev")
H = {"Accept": "application/vnd.github+json", "User-Agent": "profile-readme-bot"}
if os.environ.get("GH_TOKEN"):
    H["Authorization"] = f"Bearer {os.environ['GH_TOKEN']}"

def get(url, **params):
    r = requests.get(url, headers=H, params=params, timeout=30)
    r.raise_for_status()
    return r.json()

u = get(f"https://api.github.com/users/{USER}")
repos = get(f"https://api.github.com/users/{USER}/repos", per_page=100, type="owner", sort="pushed")
own = [r for r in repos if not r["fork"] and r["name"].lower() != USER.lower()]  # skip forks + profile repo

langs = Counter()
for r in own[:40]:
    try:
        for k, v in get(r["languages_url"]).items():
            langs[k] += v
    except requests.RequestException:
        pass

keep = ("name", "description", "language", "stargazers_count", "forks_count", "pushed_at", "html_url")
data = {"user": USER, "created_at": u["created_at"], "followers": u["followers"], "following": u["following"],
        "public_repos": u["public_repos"], "stars": sum(r["stargazers_count"] for r in own),
        "forks": sum(r["forks_count"] for r in own), "langs": dict(langs.most_common()),
        "repos": [{k: r.get(k) for k in keep} for r in own]}
os.makedirs("data", exist_ok=True)
json.dump(data, open("data/stats.json", "w"), indent=1)
print(f"{USER}: {data['public_repos']} repos, {data['stars']} stars, {len(langs)} languages")
