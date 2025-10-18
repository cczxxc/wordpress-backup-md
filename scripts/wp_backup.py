import os
import requests
import frontmatter
from markdownify import markdownify as md
from datetime import datetime

# WORDPRESS_API = "https://ccweb.byethost10.com/wp-json/wp/v2/posts"
WORDPRESS_API = "https://xin.a0001.net/wp-json/wp/v2/posts"

OUTPUT_DIR = "posts"
REQUEST_TIMEOUT = 6  # 秒

def sanitize_filename(filename):
    """清理文件名中的非法字符"""
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

def fetch_posts():
    print("🌀 正在从 WordPress 获取文章列表...")
    page = 1
    posts = []
    max_pages = 10  # 限制最大页数
    
    while page <= max_pages:
        try:
            print(f"📡 请求第 {page} 页...")
            response = requests.get(
                WORDPRESS_API,
                params={"per_page": 20, "page": page},
                timeout=REQUEST_TIMEOUT
            )
            
            if response.status_code == 200:
                data = response.json()
                if not data:
                    print("📄 已到达最后一页")
                    break
                    
                posts.extend(data)
                print(f"✅ 第 {page} 页获取成功: {len(data)} 篇文章")
                page += 1
            else:
                print(f"⚠️ 请求失败: {response.status_code}")
                break
                
        except requests.exceptions.Timeout:
            print(f"⏰ 第 {page} 页请求超时，跳过...")
            page += 1
        except Exception as e:
            print(f"❌ 第 {page} 页错误: {e}")
            break
    
    print(f"📦 共获取 {len(posts)} 篇文章")
    return posts

def save_as_markdown(posts):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("📝 正在保存为 Markdown 文件...")
    
    success_count = 0
    for i, post in enumerate(posts, start=1):
        try:
            title = post.get("title", {}).get("rendered", "无标题").strip()
            content = post.get("content", {}).get("rendered", "")
            slug = post.get("slug", f"post-{i}").strip()
            date = post.get("date", "")

            # 安全处理文件名
            safe_slug = sanitize_filename(slug)
            if not safe_slug:
                safe_slug = f"post-{i}"

            filepath = os.path.join(OUTPUT_DIR, f"{safe_slug}.md")
            
            # 构建内容
            metadata = {"title": title, "date": date, "slug": slug}
            fm_post = frontmatter.Post(content, **metadata)
            
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(frontmatter.dumps(fm_post))
            
            success_count += 1
            print(f"✅ [{i}/{len(posts)}] 已保存: {filepath}")
            
        except Exception as e:
            print(f"❌ 保存第 {i} 篇文章失败: {e}")
            continue

    print(f"🎉 保存完成！成功 {success_count}/{len(posts)} 篇")

if __name__ == "__main__":
    try:
        print(f"🚀 开始备份 WordPress 文章")
        posts = fetch_posts()
        if posts:
            save_as_markdown(posts)
        else:
            print("⚠️ 未获取到任何文章")
    except Exception as e:
        print(f"💥 程序执行出错: {e}")
