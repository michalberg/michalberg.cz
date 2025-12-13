#!/usr/bin/env python3
"""
Migrace WordPress exportu do Hugo
Parsuje XML a vytvoří Markdown soubory
"""

import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime
from slugify import slugify
import html2text
import requests
import re

CONTENT_DIR = Path("content/posts")
IMAGES_DIR = Path("static/images/wordpress")

def clean_html(html):
    """Převede HTML na Markdown"""
    h = html2text.HTML2Text()
    h.ignore_links = False
    h.body_width = 0
    return h.handle(html)

def download_wordpress_image(url, slug):
    """Stáhne obrázek z WordPressu"""
    if not url:
        return None
    
    try:
        IMAGES_DIR.mkdir(parents=True, exist_ok=True)
        
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        # Zjisti příponu
        ext = url.split('.')[-1].split('?')[0][:4]
        if ext not in ['jpg', 'jpeg', 'png', 'gif', 'webp']:
            ext = 'jpg'
        
        filename = f"{slug}.{ext}"
        filepath = IMAGES_DIR / filename
        
        with open(filepath, 'wb') as f:
            f.write(response.content)
        
        return f"/images/wordpress/{filename}"
        
    except Exception as e:
        print(f"⚠️  Nepodařilo se stáhnout obrázek {url}: {e}")
        return None

def parse_wordpress_xml(xml_file):
    """Parsuj WordPress XML export"""
    print(f"📖 Načítám WordPress export: {xml_file}")
    
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    # WordPress používá namespace
    namespaces = {
        'content': 'http://purl.org/rss/1.0/modules/content/',
        'wp': 'http://wordpress.org/export/1.2/',
        'dc': 'http://purl.org/dc/elements/1.1/',
        'excerpt': 'http://wordpress.org/export/1.2/excerpt/'
    }
    
    posts = []
    
    for item in root.findall('.//item'):
        # Typ (post/page)
        post_type = item.find('wp:post_type', namespaces)
        if post_type is None or post_type.text != 'post':
            continue
        
        # Status (publikováno/draft)
        status = item.find('wp:status', namespaces)
        if status is None or status.text != 'publish':
            continue
        
        # Titulek
        title = item.find('title')
        title = title.text if title is not None else 'Bez titulku'
        
        # Slug
        wp_slug = item.find('wp:post_name', namespaces)
        slug = wp_slug.text if wp_slug is not None else slugify(title)
        
        # Datum
        pub_date = item.find('wp:post_date', namespaces)
        if pub_date is not None and pub_date.text:
            date = pub_date.text.split()[0]
        else:
            date = datetime.now().strftime('%Y-%m-%d')
        
        # Obsah
        content_tag = item.find('content:encoded', namespaces)
        content = content_tag.text if content_tag is not None else ''
        
        # Autor
        author = item.find('dc:creator', namespaces)
        author = author.text if author is not None else 'Michal Berg'
        
        # Kategorie a tagy
        categories = []
        tags = []
        for category in item.findall('category'):
            domain = category.get('domain', '')
            if domain == 'category':
                categories.append(category.text)
            elif domain == 'post_tag':
                tags.append(category.text)
        
        # Excerpt
        excerpt_tag = item.find('excerpt:encoded', namespaces)
        excerpt = excerpt_tag.text if excerpt_tag is not None and excerpt_tag.text else None
        
        posts.append({
            'title': title,
            'slug': slug,
            'date': date,
            'content': content,
            'author': author,
            'categories': categories,
            'tags': tags,
            'excerpt': excerpt
        })
    
    return posts

def create_post_file(post):
    """Vytvoř Markdown soubor pro článek"""
    CONTENT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Escapuj uvozovky v title
    title_escaped = post['title'].replace('"', r'\"')
    
    # Front matter
    front_matter = f"""---
title: "{title_escaped}"
date: {post['date']}
slug: "{post['slug']}"
author: "{post['author']}"
"""
    
    if post.get('excerpt'):
        excerpt_escaped = post['excerpt'].replace('"', r'\"')[:200]
        front_matter += f'description: "{excerpt_escaped}"\n'
    
    if post.get('categories'):
        front_matter += f"categories: {post['categories']}\n"
    
    if post.get('tags'):
        front_matter += f"tags: {post['tags']}\n"
    
    front_matter += 'source: "WordPress"\n'
    front_matter += "---\n\n"
    
    # nePřeveď HTML na Markdown
    content = post['content'] if post['content'] else ''

    # Najdi obrázky v obsahu a stáhni je
    img_pattern = r'!\[.*?\]\((https?://[^\)]+)\)'
    images = re.findall(img_pattern, content)
    
    for img_url in images:
        if 'michalberg.cz' in img_url or 'wordpress.com' in img_url:
            local_path = download_wordpress_image(img_url, post['slug'])
            if local_path:
                content = content.replace(img_url, local_path)
    
    # Kompletní obsah
    full_content = front_matter + content
    
    # Ulož soubor
    filepath = CONTENT_DIR / f"{post['slug']}.md"
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(full_content)
    
    print(f"✅ {post['slug']}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python migrate_wordpress.py <wordpress-export.xml>")
        sys.exit(1)
    
    xml_file = sys.argv[1]
    
    if not Path(xml_file).exists():
        print(f"❌ Soubor nenalezen: {xml_file}")
        sys.exit(1)
    
    print("🚀 WordPress → Hugo migrace")
    print("="*60)
    
    # Parsuj XML
    posts = parse_wordpress_xml(xml_file)
    print(f"📊 Nalezeno {len(posts)} publikovaných článků")
    
    # Vytvoř soubory
    print("\n�� Vytvářím Markdown soubory...")
    for post in posts:
        create_post_file(post)
    
    print(f"\n✅ Migrace dokončena! Vytvořeno {len(posts)} článků")
    print(f"📁 Soubory: {CONTENT_DIR}")
    print(f"🖼️  Obrázky: {IMAGES_DIR}")

if __name__ == '__main__':
    main()
