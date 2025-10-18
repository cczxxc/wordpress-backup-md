import os
import requests
import frontmatter
from markdownify import markdownify as md
from datetime import datetime

# WP_API_BASE = "https://ccweb.byethost10.com/wp-json/wp/v2/posts"
WP_API_BASE = "https://xin.a0001.net/wp-json/wp/v2/posts"

OUTPUT_DIR = "posts"
REQUEST_TIMEOUT = 6  # 秒
PER_PAGE = 100        # 每页拉取文章数，最大100


def fetch_posts():
    print("🚀 Fetching posts from WordPress API...")
    posts = []
    page = 1
    while True:
        try:
            url = f"{WP_API_BASE}?per_page={PER_PAGE}&page={page}"
            r = requests.get(url, timeout=REQUEST_TIMEOUT)
            if r.status_code != 200:
                print(f"⚠️ HTTP {r.status_code} error, stop fetching.")
                break
            data = r.json()
            if not data:
                break
            posts.extend(data)
            print(f"📦 Page {page} fetched ({len(data)} posts)")
            page += 1
        except requests.exceptions.Timeout:
            print(f"⏰ Page {page} timeout, skipped")
            page += 1
        except requests.exceptions.RequestException as e:
            print(f"❌ Network error: {e}")
            break
    print(f"✅ Total posts fetched: {len(posts)}")
    return posts

def save_as_markdown(posts):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    new_count = 0
    updated_count = 0
    skipped_count = 0

    for i, p in enumerate(posts, start=1):
        slug = p.get("slug", f"post-{i}")
        title = p.get("title", {}).get("rendered", "无标题")
        date = p.get("date", "")
        link = p.get("link", "")
        content_html = p.get("content", {}).get("rendered", "")
        md_content = md(content_html)

        post_obj = frontmatter.Post(md_content, title=title, date=date, link=link)
        file_path = os.path.join(OUTPUT_DIR, f"{slug}.md")
        content_str = frontmatter.dumps(post_obj)

        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                old_content = f.read()
            if old_content.strip() == content_str.strip():
                skipped_count += 1
                print(f"⏭️ [{i}/{len(posts)}] No change: {title[:60]}")
                continue
            else:
                updated_count += 1
                print(f"✏️ [{i}/{len(posts)}] Updated: {title[:60]}")
        else:
            new_count += 1
            print(f"🆕 [{i}/{len(posts)}] New: {title[:60]}")

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content_str)

    print(f"\n🎉 Backup summary: New: {new_count}, Updated: {updated_count}, Skipped: {skipped_count}")


print(f"⏰ Backup started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
posts = fetch_posts()
if posts:
    save_as_markdown(posts)
else:
    print("⚠️ No posts found or API error.")
print("✅ Backup finished.")

