#!/usr/bin/env python3
"""
Custom parsery pro české weby
Extrahují metadata a obsah článků
"""

from bs4 import BeautifulSoup
from datetime import datetime
import html2text
import re

class ArticleParser:
    """Základní třída pro parsery"""
    
    def __init__(self):
        self.h = html2text.HTML2Text()
        self.h.ignore_links = False
        self.h.body_width = 0
    
    def parse(self, html, url):
        """Parsuj HTML a vrať slovník s daty"""
        raise NotImplementedError
    
    def clean_text(self, text):
        """Vyčistí text od přebytečných mezer"""
        if not text:
            return ""
        return re.sub(r'\s+', ' ', text).strip()
    
    def html_to_markdown(self, html):
        """Převede HTML na Markdown"""
        if not html:
            return ""
        return self.h.handle(str(html))

class DenikReferendumParser(ArticleParser):
    """Parser pro Deník Referendum"""
    
    def parse(self, html, url):
        soup = BeautifulSoup(html, 'html.parser')
        
        # Titulek - zkus og:title (nejspolehlivější)
        title = None
        og_title = soup.find('meta', property='og:title')
        if og_title and og_title.get('content'):
            title = og_title['content']
            # Odstraň prefix "Michal Berg: " pokud tam je
            if title.startswith('Michal Berg: '):
                title = title[13:]
            title = self.clean_text(title)
        
        # Fallback na h1
        if not title:
            title_tag = soup.find('h1')
            if title_tag:
                title = self.clean_text(title_tag.text)
        
        # Popis z og:description
        description = None
        og_desc = soup.find('meta', property='og:description')
        if og_desc and og_desc.get('content'):
            description = og_desc['content']
        
        # Hlavní obsah - aktualizovaný selektor
        content = ""
        article_body = soup.find('div', class_='text')
        if not article_body:
            article_body = soup.find('div', class_='articleContentWrapper')
        if article_body:
            content = self.html_to_markdown(article_body)
        
        # Datum z meta tagu
        published = None
        pub_time = soup.find('meta', property='article:published_time')
        if pub_time and pub_time.get('content'):
            published = pub_time['content'].split('T')[0]
        
        # Autor
        author = None
        author_tag = soup.find('span', class_='author')
        if author_tag:
            author = self.clean_text(author_tag.text)
        
        # Obrázek z og:image
        image = None
        og_image = soup.find('meta', property='og:image')
        if og_image and og_image.get('content'):
            image = og_image['content']
        
        return {
            'title': title or 'Bez titulku',
            'description': description,
            'content': content,
            'published': published,
            'author': author or 'Michal Berg',
            'source': 'Deník Referendum',
            'source_url': url,
            'image': image
        }

class RespektBlogParser(ArticleParser):
    """Parser pro Respekt Blog"""
    
    def parse(self, html, url):
        soup = BeautifulSoup(html, 'html.parser')
        
        # Titulek
        title = None
        title_tag = soup.find('h1')
        if title_tag:
            title = self.clean_text(title_tag.text)
        
        # Obsah článku - aktualizovaný selektor
        content = ""
        # Zkus post-content (nejlepší)
        article = soup.find('div', class_='post-content')
        if not article:
            # Fallback na layout_content-text
            article = soup.find('div', class_='layout_content-text')
        if not article:
            # Poslední fallback na main
            article = soup.find('main')
        
        if article:
            # Odstraň navigaci a další prvky
            for unwanted in article.find_all(['nav', 'aside', 'footer', 'script']):
                unwanted.decompose()
            content = self.html_to_markdown(article)
        
        # Datum
        published = None
        date_tag = soup.find('time')
        if date_tag and date_tag.get('datetime'):
            published = date_tag['datetime'].split('T')[0]
        
        # Obrázek
        image = None
        # Zkus og:image
        og_img = soup.find('meta', property='og:image')
        if og_img and og_img.get('content'):
            image = og_img['content']
        else:
            # Fallback na první img
            img_tag = soup.find('img')
            if img_tag and img_tag.get('src'):
                image = img_tag['src']
        
        return {
            'title': title or 'Bez titulku',
            'content': content,
            'published': published,
            'author': 'Michal Berg',
            'source': 'Respekt Blog',
            'source_url': url,
            'image': image
        }

class MediumSeznamParser(ArticleParser):
    """Parser pro Medium Seznam"""
    
    def parse(self, html, url):
        soup = BeautifulSoup(html, 'html.parser')
        
        # Titulek
        title = None
        title_tag = soup.find('h1')
        if title_tag:
            title = self.clean_text(title_tag.text)
        
        # Perex/popis
        description = None
        desc_tag = soup.find('meta', {'name': 'description'})
        if desc_tag and desc_tag.get('content'):
            description = desc_tag['content']
        
        # Obsah
        content = ""
        article = soup.find('article') or soup.find('div', class_='article-content')
        if article:
            content = self.html_to_markdown(article)
        
        # Datum
        published = None
        date_tag = soup.find('time')
        if date_tag and date_tag.get('datetime'):
            published = date_tag['datetime'].split('T')[0]
        
        # Obrázek
        image = None
        img_tag = soup.find('meta', {'property': 'og:image'})
        if img_tag and img_tag.get('content'):
            image = img_tag['content']
        
        return {
            'title': title or 'Bez titulku',
            'description': description,
            'content': content,
            'published': published,
            'author': 'Michal Berg',
            'source': 'Medium Seznam',
            'source_url': url,
            'image': image
        }

class FinmagParser(ArticleParser):
    """Parser pro Finmag"""
    
    def parse(self, html, url):
        soup = BeautifulSoup(html, 'html.parser')
        
        # Titulek
        title = None
        title_tag = soup.find('h1')
        if title_tag:
            title = self.clean_text(title_tag.text)
        
        # Perex z og:description
        description = None
        og_desc = soup.find('meta', property='og:description')
        if og_desc and og_desc.get('content'):
            description = og_desc['content']
        
        # Obsah - aktualizovaný selektor
        content = ""
        # Zkus nejspecifičtější třídu
        article = soup.find('div', class_='article-detail__article_content__left__article')
        if not article:
            # Fallback na širší selektor
            article = soup.find('div', class_='article-detail__article_content__left')
        
        if article:
            # Odstraň footer, komentáře, reklamy
            for unwanted in article.find_all(['footer', 'aside', 'script']):
                unwanted.decompose()
            # Odstraň author box
            for author_box in article.find_all('div', class_=lambda x: x and 'author' in str(x).lower()):
                author_box.decompose()
            
            content = self.html_to_markdown(article)
        
        # Datum
        published = None
        date_tag = soup.find('time')
        if date_tag and date_tag.get('datetime'):
            published = date_tag['datetime'].split('T')[0]
        
        # Obrázek
        image = None
        img_tag = soup.find('meta', {'property': 'og:image'})
        if img_tag and img_tag.get('content'):
            image = img_tag['content']
        
        return {
            'title': title or 'Bez titulku',
            'description': description,
            'content': content,
            'published': published,
            'author': 'Michal Berg',
            'source': 'Finmag',
            'source_url': url,
            'image': image
        }

class EkolistParser(ArticleParser):
    """Parser pro Ekolist.cz"""
    
    def parse(self, html, url):
        soup = BeautifulSoup(html, 'html.parser')
        
        # Titulek - z tabulky s obsahem
        title = None
        # Ekolist má specifickou strukturu - titulek je v table/td
        for td in soup.find_all('td'):
            text = td.text.strip()
            # Hledáme řádek s datem a jménem autora
            if 'Michal Berg' in text and any(char.isdigit() for char in text):
                # Extrahuj titulek před datem
                parts = text.split('\n')
                if parts:
                    title_part = parts[0].strip()
                    # Odstraň "Michal Berg: " prefix
                    if title_part.startswith('Michal Berg:'):
                        title = title_part[12:].strip()
                    else:
                        title = title_part
                break
        
        # Fallback na h1 nebo og:title
        if not title:
            og_title = soup.find('meta', property='og:title')
            if og_title and og_title.get('content'):
                title = og_title['content']
                if title.startswith('Michal Berg:'):
                    title = title[12:].strip()
        
        # Datum - z textu tabulky
        published = None
        for td in soup.find_all('td'):
            text = td.text.strip()
            # Hledáme datum ve formátu DD.M.YYYY
            date_match = re.search(r'(\d{1,2})\.(\d{1,2})\.(\d{4})', text)
            if date_match:
                day, month, year = date_match.groups()
                published = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
                break
        
        # Popis - z prvního odstavce článku
        description = None
        # Najdi všechny odstavce
        paragraphs = soup.find_all('p')
        for p in paragraphs:
            text = p.text.strip()
            # První delší odstavec (víc než 100 znaků)
            if len(text) > 100 and not text.startswith('Přihlášení'):
                description = text[:300]
                break
        
        # Obsah - extrahuj text mezi titulkem a diskusí
        content = ""
        article_started = False
        content_parts = []
        
        for element in soup.find_all(['p', 'h2', 'h3']):
            text = element.text.strip()
            
            # Skip prázdné a navigační elementy
            if not text or text.startswith('Přihlášení') or 'Uživatelský e-mail' in text:
                continue
            
            # Začni od prvního odstavce s obsahem
            if not article_started and len(text) > 50:
                article_started = True
            
            if article_started:
                # Ukonči před diskusí
                if 'Online diskuse' in text or 'Další články autora' in text:
                    break
                
                # Přidej odstavec
                if element.name == 'p':
                    content_parts.append(text + '\n\n')
                elif element.name in ['h2', 'h3']:
                    content_parts.append(f"## {text}\n\n")
        
        content = ''.join(content_parts).strip()
        
        # Obrázek
        image = None
        og_img = soup.find('meta', property='og:image')
        if og_img and og_img.get('content'):
            image = og_img['content']
        
        return {
            'title': title or 'Bez titulku',
            'description': description,
            'content': content,
            'published': published,
            'author': 'Michal Berg',
            'source': 'Ekolist.cz',
            'source_url': url,
            'image': image
        }

def get_parser_for_url(url):
    """Vrátí správný parser podle URL"""
    url_lower = url.lower()
    
    if 'denikreferendum.cz' in url_lower:
        return DenikReferendumParser()
    elif 'berg.blog.respekt.cz' in url_lower:
        return RespektBlogParser()
    elif 'medium.seznam.cz' in url_lower:
        return MediumSeznamParser()
    elif 'finmag.cz' in url_lower:
        return FinmagParser()
    elif 'ekolist.cz' in url_lower:
        return EkolistParser()
    
    return None  # Použije se universal fallback