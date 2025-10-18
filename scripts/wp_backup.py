import os
import requests
import frontmatter
from markdownify import markdownify as md
from datetime import datetime
import re
import urllib.parse
import unicodedata
import html

# WORDPRESS_API = "https://ccweb.byethost10.com/wp-json/wp/v2/posts"
WORDPRESS_API = "https://xin.a0001.net/wp-json/wp/v2/posts"

OUTPUT_DIR = "posts"
REQUEST_TIMEOUT = 10  # 增加超时时间


def decode_slug(slug):
    """解码 URL 编码的 slug"""
    try:
        # 先解码 URL 编码
        decoded = urllib.parse.unquote(slug)
        # 再解码 HTML 实体
        decoded = html.unescape(decoded)
        return decoded
    except:
        return slug

def sanitize_filename(filename):
    """清理文件名，确保安全"""
    # 解码
    filename = decode_slug(filename)
    
    # 标准化 Unicode
    filename = unicodedata.normalize('NFKC', filename)
    
    # 替换非法字符
    filename = re.sub(r'[<>:"/\\|?*\x00-\x1F]', '_', filename)
    filename = re.sub(r'[\s]+', ' ', filename)  # 保留空格，用空格代替下划线
    
    # 限制长度
    if len(filename) > 100:
        filename = filename[:100]
    
    return filename.strip()

def fetch_posts():
    """获取所有文章"""
    print("🌀 正在从 WordPress 获取文章列表...")
    
    all_posts = []
    page = 1
    per_page = 100  # 每页最大可设为100，减少请求次数
    
    while True:
        try:
            print(f"📡 请求第 {page} 页...")
            
            params = {
                "page": page,
                "per_page": per_page,
                "status": "publish",
                "orderby": "date",
                "order": "desc"
            }
            
            response = requests.get(
                WORDPRESS_API,
                params=params,
                timeout=REQUEST_TIMEOUT
            )
            
            if response.status_code != 200:
                print(f"❌ 请求失败: {response.status_code}")
                break
            
            posts = response.json()
            if not posts:  # 空数组表示没有更多文章
                print("📄 已到达最后一页")
                break
            
            all_posts.extend(posts)
            print(f"✅ 第 {page} 页: 获取 {len(posts)} 篇文章，总计 {len(all_posts)} 篇")
            
            # 如果获取的文章数量少于每页数量，说明是最后一页
            if len(posts) < per_page:
                print("📄 已到达最后一页")
                break
                
            page += 1
            
            # 添加短暂延迟，避免请求过快
            import time
            time.sleep(0.5)
            
        except requests.exceptions.Timeout:
            print(f"⏰ 第 {page} 页请求超时")
            break
        except Exception as e:
            print(f"💥 第 {page} 页发生错误: {e}")
            break
    
    print(f"🎉 备份完成！共获取 {len(all_posts)} 篇文章")
    return all_posts

def save_as_markdown(posts):
    """保存文章为 Markdown 文件"""
    if not posts:
        print("⚠️ 没有文章可保存")
        return
        
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"📝 正在保存 {len(posts)} 篇文章...")
    
    success_count = 0
    for i, post in enumerate(posts, 1):
        try:
            # 获取文章数据
            post_id = post.get("id", i)
            title_data = post.get("title", {})
            content_data = post.get("content", {})
            
            # 解码标题和内容
            title = html.unescape(title_data.get("rendered", f"文章-{post_id}"))
            content = content_data.get("rendered", "")
            slug = post.get("slug", f"post-{post_id}")
            date = post.get("date", "")
            
            # 解码 slug 并生成安全文件名
            decoded_slug = decode_slug(slug)
            safe_filename = sanitize_filename(decoded_slug)
            
            # 如果文件名为空或无效，使用文章ID
            if not safe_filename or safe_filename == "." or safe_filename == "..":
                safe_filename = f"post-{post_id}"
            
            # 构建文件路径
            filepath = os.path.join(OUTPUT_DIR, f"{safe_filename}.md")
            
            # 转换 HTML 内容到 Markdown
            if content:
                content_md = md(content)
            else:
                content_md = "暂无内容"
            
            # 创建 Front Matter
            front_matter = f"""---
id: {post_id}
title: {title}
date: {date}
slug: {decoded_slug}
original_slug: {slug}
link: {post.get('link', '')}
status: {post.get('status', '')}
---

{content_md}
"""
            
            # 保存文件
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(front_matter)
            
            success_count += 1
            print(f"✅ [{i}/{len(posts)}] 已保存: {safe_filename}.md")
            print(f"   📄 原始slug: {slug}")
            print(f"   🔄 解码后: {decoded_slug}")
            
        except Exception as e:
            print(f"❌ 保存文章 {i} 失败: {e}")
            continue
    
    print(f"🎉 保存完成！成功 {success_count}/{len(posts)} 篇")

def test_connection():
    """测试连接"""
    print("🔧 测试 API 连接...")
    try:
        response = requests.get(WORDPRESS_API, params={"per_page": 1}, timeout=10)
        print(f"✅ 连接测试成功: {response.status_code}")
        return True
    except Exception as e:
        print(f"❌ 连接测试失败: {e}")
        return False

if __name__ == "__main__":
    print(f"🚀 开始备份 WordPress 文章 ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")
    
    if test_connection():
        posts = fetch_posts()
        if posts:
            save_as_markdown(posts)
            print("✅ 备份完成！")
        else:
            print("⚠️ 未获取到任何文章")
    else:
        print("❌ API 连接失败")
