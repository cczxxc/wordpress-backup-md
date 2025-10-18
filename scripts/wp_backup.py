import os
import requests
import frontmatter
from datetime import datetime

# WordPress JSON API 地址
# WORDPRESS_API = "https://ccweb.byethost10.com/wp-json/wp/v2/posts"
WORDPRESS_API = "https://xin.a0001.net/wp-json/wp/v2/posts"
OUTPUT_DIR = "backup"

# 访问超时时间（秒）
REQUEST_TIMEOUT = 10

def fetch_posts():
    print("🌀 正在从 WordPress 获取文章列表...")
    page = 1
    posts = []
    while True:
        try:
            response = requests.get(
                WORDPRESS_API,
                params={"per_page": 20, "page": page},
                timeout=REQUEST_TIMEOUT  # ← 加上超时
            )
            if response.status_code == 200:
                data = response.json()
                if not data:
                    break
                posts.extend(data)
                print(f"✅ 已获取第 {page} 页 ({len(posts)} 篇文章)")
                page += 1
            else:
                print(f"⚠️ 请求失败: {response.status_code}")
                break
        except requests.exceptions.Timeout:
            print(f"⏰ 请求超时（第 {page} 页，已跳过）")
            page += 1
        except requests.exceptions.RequestException as e:
            print(f"❌ 网络错误（第 {page} 页）: {e}")
            break
    print(f"📦 共获取 {len(posts)} 篇文章。")
    return posts


def save_as_markdown(posts):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("📝 正在保存为 Markdown 文件...")
    for i, post in enumerate(posts, start=1):
        title = post.get("title", {}).get("rendered", "无标题")
        content = post.get("content", {}).get("rendered", "")
        slug = post.get("slug", f"post-{i}")
        date = post.get("date", "")

        # 构建 Markdown 文件
        metadata = {
            "title": title,
            "date": date,
            "slug": slug,
        }
        fm_post = frontmatter.Post(content, **metadata)

        filepath = os.path.join(OUTPUT_DIR, f"{slug}.md")
        with open(filepath, "w", encoding="utf-8") as f:
            frontmatter.dump(fm_post, f)

        print(f"✅ [{i}/{len(posts)}] 已保存: {filepath}")

    print("🎉 所有文章已成功保存！")


if __name__ == "__main__":
    print(f"🚀 开始备份 WordPress 文章 ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")
    posts = fetch_posts()
    if posts:
        save_as_markdown(posts)
    else:
        print("⚠️ 未获取到任何文章。")
