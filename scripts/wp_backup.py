import os
import requests
import frontmatter
from markdownify import markdownify as md
from datetime import datetime
import re
import time

# WORDPRESS_API = "https://ccweb.byethost10.com/wp-json/wp/v2/posts"
WORDPRESS_API = "https://xin.a0001.net/wp-json/wp/v2/posts"

OUTPUT_DIR = "posts"
REQUEST_TIMEOUT = 10  # 增加超时时间

def fetch_posts():
    print("🌀 正在从 WordPress 获取文章列表...")
    
    all_posts = []
    page = 1
    max_pages = 50  # 安全限制
    
    while page <= max_pages:
        try:
            print(f"📡 请求第 {page} 页...")
            
            # 更简单的请求参数
            params = {
                "page": page,
                "per_page": 10,  # 减少每页数量
                "_fields": "id,title,slug,content,date,status"  # 只请求需要的字段
            }
            
            response = requests.get(
                WORDPRESS_API,
                params=params,
                timeout=REQUEST_TIMEOUT,
                headers={
                    "User-Agent": "WordPress-Backup-Script/1.0",
                    "Accept": "application/json"
                }
            )
            
            print(f"🔍 响应状态: {response.status_code}")
            
            if response.status_code == 200:
                posts = response.json()
                print(f"📊 第 {page} 页获取到 {len(posts)} 篇文章")
                
                if not posts:
                    print("📄 没有更多文章了")
                    break
                    
                all_posts.extend(posts)
                page += 1
                
                # 添加延迟，避免请求过快
                time.sleep(1)
                
            elif response.status_code == 400:
                print("❌ 400 错误：请求参数可能有问题")
                print(f"🔧 尝试的 URL: {response.url}")
                break
                
            elif response.status_code == 401:
                print("❌ 401 错误：需要认证")
                break
                
            elif response.status_code == 404:
                print("❌ 404 错误：API 端点不存在")
                break
                
            else:
                print(f"❌ 请求失败: {response.status_code}")
                print(f"📄 响应内容: {response.text[:200]}...")
                break
                
        except requests.exceptions.Timeout:
            print(f"⏰ 第 {page} 页请求超时")
            break
        except requests.exceptions.ConnectionError:
            print(f"🔌 第 {page} 页连接错误")
            break
        except Exception as e:
            print(f"💥 第 {page} 页发生错误: {e}")
            break
    
    print(f"📦 共获取 {len(all_posts)} 篇文章")
    return all_posts

def save_as_markdown(posts):
    if not posts:
        print("⚠️ 没有文章可保存")
        return
        
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"📝 正在保存 {len(posts)} 篇文章...")
    
    success_count = 0
    for i, post in enumerate(posts, 1):
        try:
            # 安全获取数据
            post_id = post.get("id", i)
            title_data = post.get("title", {})
            content_data = post.get("content", {})
            
            title = title_data.get("rendered", f"文章-{post_id}").strip()
            content = content_data.get("rendered", "")
            slug = post.get("slug", f"post-{post_id}")
            date = post.get("date", "")
            
            # 清理 HTML 标签
            if content:
                # 使用 markdownify 转换 HTML 到 Markdown
                content_md = md(content)
            else:
                content_md = "暂无内容"
            
            # 安全文件名
            safe_slug = re.sub(r'[^\w\-\.]', '_', slug)
            filename = f"{safe_slug}.md" if safe_slug else f"post-{post_id}.md"
            filepath = os.path.join(OUTPUT_DIR, filename)
            
            # 创建 Front Matter
            metadata = {
                "title": title,
                "date": date,
                "slug": slug,
                "id": post_id
            }
            
            # 组合内容
            post_content = f"""---
title: {title}
date: {date}
slug: {slug}
id: {post_id}
---

{content_md}
"""
            
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(post_content)
            
            success_count += 1
            print(f"✅ [{i}/{len(posts)}] 已保存: {filename}")
            
        except Exception as e:
            print(f"❌ 保存文章 {i} 失败: {e}")
            continue
    
    print(f"🎉 保存完成！成功 {success_count}/{len(posts)} 篇")

def test_api_connection():
    """测试 API 连接"""
    print("🔧 测试 API 连接...")
    try:
        response = requests.get(WORDPRESS_API, timeout=10)
        print(f"🔍 测试响应: {response.status_code}")
        if response.status_code == 200:
            print("✅ API 连接正常")
            return True
        else:
            print(f"❌ API 返回错误: {response.status_code}")
            print(f"📄 响应头: {dict(response.headers)}")
            return False
    except Exception as e:
        print(f"💥 连接测试失败: {e}")
        return False

if __name__ == "__main__":
    print(f"🚀 开始备份 WordPress 文章 ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")
    
    # 先测试连接
    if test_api_connection():
        posts = fetch_posts()
        if posts:
            save_as_markdown(posts)
            print("✅ 备份完成！")
        else:
            print("⚠️ 未获取到任何文章")
    else:
        print("❌ API 连接测试失败，请检查网络和 URL")
