# scrape_discourse.py
import requests
from bs4 import BeautifulSoup
import json
import time

BASE_URL = "https://discourse.onlinedegree.iitm.ac.in"
CATEGORY_URL = BASE_URL + "/c/tools-in-data-science/84"  # Adjust this if needed

def get_topic_links():
    print("Fetching topic links...")
    res = requests.get(CATEGORY_URL)
    soup = BeautifulSoup(res.text, 'html.parser')
    topic_tags = soup.find_all("a", class_="title raw-link raw-topic-link")
    topic_links = list(set([BASE_URL + tag['href'] for tag in topic_tags]))
    return topic_links

def scrape_topics(links):
    posts = []
    for i, url in enumerate(links):
        print(f"Scraping {i+1}/{len(links)}: {url}")
        try:
            res = requests.get(url)
            soup = BeautifulSoup(res.text, 'html.parser')
            post_text = soup.get_text()
            posts.append({"url": url, "content": post_text})
            time.sleep(1)
        except Exception as e:
            print(f"Failed to fetch {url}: {e}")
    return posts

if __name__ == "__main__":
    links = get_topic_links()
    data = scrape_topics(links)
    with open("discourse_posts.json", "w") as f:
        json.dump(data, f, indent=2)
    print("Saved to discourse_posts.json")
