#!/usr/bin/env python3
"""
Import článků z externích URL do Hugo
Podporuje custom parsery pro české weby
"""

import sys
import os
import json
import requests
from datetime import datetime
from pathlib import Path
from slugify import slugify
import html2text
from urllib.parse import urlparse

# Import custom parserů
sys.path.insert(0, os.path.dirname(__file__))
from custom_parsers import get_parser_for_url

# Konfigurace
CONTENT_DIR = Path("content/posts")
IMAGES_DIR = Path("static/images")
SLUG_REGISTRY = Path("slug-registry.json")

def load_slug_registry():
    """Načte registr použitých slugů"""
    if SLUG_REGISTRY.exists():
        with open(SLUG_REGISTRY, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_slug_registry(registry):
    """Uloží registr slugů"""
    with open(SLUG_REGISTRY, 'w', encoding='utf-8') as f:
        json.dump(registry, f, indent=2, ensure_ascii=False)

def generate_unique_slug(title, registry):
    """Vygeneruje unikátní slug"""
    base_slug = slugify(title, max_length=60)
    slug = base_slug
    counter = 2
    
    while slug in registry:
        slug = f"{base_slug}-{counter}"
        counter += 1
    
    return slug, slug != base_slug

def download_image(url, slug):
    """Stáhne obrázek a vrátí lokální cestu"""
    if not url:
        return None
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        # Zjisti příponu
        ext = url.split('.')[-1].split('?')[0][:4]
        if ext not in ['jpg', 'jpeg', 'png', 'gif', 'webp']:
            ext = 'jpg'
        
        # Vytvoř složku pro aktuální rok
        year = datetime.now().year
        year_dir = IMAGES_DIR / str(year)
        year_dir.mkdir(parents=True, exist_ok=True)
        
        # Ulož obrázek
        filename = f"{slug}.{ext}"
        filepath = year_dir / filename
        
        with open(filepath, 'wb') as f:
            f.write(response.content)
        
        return f"/images/{year}/{filename}"
        
    except Exception as e:
        print(f"⚠️  Nepodařilo se stáhnout obrázek: {e}")
        return None

def create_markdown(data, slug, collision_note=None):
    """Vytvoří Markdown soubor článku"""
    CONTENT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Front matter
    front_matter = {
        'title': data.get('title', 'Bez titulku'),
        'date': data.get('published', datetime.now().strftime('%Y-%m-%d')),
        'slug': slug,
        'draft': False
    }
    
    # Přidej volitelná pole
    if data.get('description'):
        front_matter['description'] = data['description']
    
    if data.get('author'):
        front_matter['author'] = data['author']
    
    if data.get('source'):
        front_matter['source'] = data['source']
    
    if data.get('source_url'):
        front_matter['source_url'] = data['source_url']
    
    if data.get('image'):
        front_matter['image'] = data['image']
    
    if collision_note:
        front_matter['note'] = collision_note
    
    # Vytvoř obsah
    content = "---\n"
    for key, value in front_matter.items():
        if isinstance(value, str):
            # Escapuj uvozovky
            value = value.replace('"', '\\"')
            content += f'{key}: "{value}"\n'
        else:
            content += f'{key}: {value}\n'
    content += "---\n\n"
    content += data.get('content', '')
    
    # Ulož soubor
    filepath = CONTENT_DIR / f"{slug}.md"
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Vytvořen: {filepath}")
    return filepath

def import_article(url):
    """Importuje jeden článek z URL"""
    print(f"\n📥 Importuji: {url}")
    
    try:
        # Najdi parser
        parser = get_parser_for_url(url)
        if parser:
            print(f"   Parser: {parser.__class__.__name__}")
        else:
            print("   Parser: Universal (fallback)")
        
        # Stáhni stránku
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        # KRITICKÉ: Nastav správné kódování
        response.encoding = 'utf-8'
        
        # Parsuj
        if parser:
            data = parser.parse(response.text, url)
        else:
            # Fallback universal parser
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Základní extrakce
            title = None
            for tag in soup.find_all(['h1', 'title']):
                if tag.text.strip():
                    title = tag.text.strip()
                    break
            
            # Převeď HTML na Markdown
            h = html2text.HTML2Text()
            h.ignore_links = False
            content = h.handle(str(soup.find('body') or soup))
            
            data = {
                'title': title or 'Bez titulku',
                'content': content,
                'source_url': url
            }
        
        # Generuj slug
        registry = load_slug_registry()
        slug, had_collision = generate_unique_slug(data['title'], registry)
        
        collision_note = None
        if had_collision:
            print(f"⚠️  Kolize slugu! Použit: {slug}")
            collision_note = f"Slug změněn kvůli kolizi"
        
        # Stáhni obrázek
        if data.get('image'):
            local_image = download_image(data['image'], slug)
            if local_image:
                data['image'] = local_image
        
        # Vytvoř článek
        filepath = create_markdown(data, slug, collision_note)
        
        # Aktualizuj registr
        registry[slug] = {
            'title': data['title'],
            'url': url,
            'imported': datetime.now().isoformat()
        }
        save_slug_registry(registry)
        
        print(f"✅ Import dokončen: {slug}")
        return True
        
    except Exception as e:
        print(f"❌ Chyba při importu: {e}")
        import traceback
        traceback.print_exc()
        return False

def import_from_file(filepath):
    """Importuje články ze souboru (jeden URL na řádek)"""
    if not Path(filepath).exists():
        print(f"❌ Soubor nenalezen: {filepath}")
        return
    
    with open(filepath, 'r', encoding='utf-8') as f:
        urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    print(f"📋 Nalezeno {len(urls)} URL k importu")
    
    success = 0
    failed = 0
    
    for url in urls:
        if import_article(url):
            success += 1
        else:
            failed += 1
    
    print(f"\n📊 Výsledky: {success} úspěšných, {failed} selhání")

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python import_articles.py <URL>              # Import jednoho článku")
        print("  python import_articles.py <FILE>             # Import z textového souboru")
        print("\nPříklad:")
        print("  python import_articles.py 'https://denikreferendum.cz/clanek/...'")
        print("  python import_articles.py articles-to-import.txt")
        sys.exit(1)
    
    arg = sys.argv[1]
    
    # Je to URL nebo soubor?
    if arg.startswith('http://') or arg.startswith('https://'):
        import_article(arg)
    else:
        import_from_file(arg)

if __name__ == '__main__':
    main()