import requests
import json
import time

BASE_URL = "https://discourse.onlinedegree.iitm.ac.in"
CATEGORY_ID = 34

def get_topics():
    url = f"{BASE_URL}/c/courses/tds-kb/{CATEGORY_ID}.json"
    resp = requests.get(url)
    return resp.json().get("topic_list", {}).get("topics", [])

def get_filtered_posts(topic_id):
    url = f"{BASE_URL}/t/{topic_id}.json"
    resp = requests.get(url)
    posts = resp.json().get("post_stream", {}).get("posts", [])
    return [
        {
            "topic_id": topic_id,
            "created_at": p["created_at"],
            "text": p["cooked"]
        }
        for p in posts
        if "2025-01-01" <= p["created_at"][:10] <= "2025-04-14"
    ]

all_posts = []
topics = get_topics()
for topic in topics:
    all_posts += get_filtered_posts(topic["id"])
    time.sleep(1)

with open("discourse_posts.json", "w", encoding="utf-8") as f:
    json.dump(all_posts, f, indent=2, ensure_ascii=False)

