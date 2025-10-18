import os
import requests
import frontmatter
from markdownify import markdownify as md
from datetime import datetime

# 你的 WordPress REST API 地址
WP_API = "https://ccweb.byethost10.com/wp-json/wp/v2/posts?per_page=100"

OUTPUT_DIR = "posts"

def fetch_posts():
    posts = []
    page = 1
    while True:
        url = f"{WP_API}&page={page}"
        r = requests.get(url)
        if r.status_code != 200:
            break
        data = r.json()
        if not data:
            break
        posts.extend(data)
        page += 1
    return posts

def save_as_markdown(posts):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for p in posts:
        slug = p["slug"]
        title = p["title"]["rendered"]
        date = p["date"]
        link = p["link"]
        content_html = p["content"]["rendered"]
        md_content = md(content_html)

        post = frontmatter.Post(md_content, title=title, date=date, link=link)
        file_path = os.path.join(OUTPUT_DIR, f"{slug}.md")

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(frontmatter.dumps(post))   # ✅ 改这里

    print(f"✅ Saved {len(posts)} posts to '{OUTPUT_DIR}'")


if __name__ == "__main__":
    posts = fetch_posts()
    if posts:
        save_as_markdown(posts)
    else:
        print("⚠️ No posts found or API error.")
