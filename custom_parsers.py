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
        
        # Titulek
        title = None
        title_tag = soup.find('h1', class_='article-title')
        if title_tag:
            title = self.clean_text(title_tag.text)
        
        # Perex
        description = None
        perex_tag = soup.find('div', class_='perex')
        if perex_tag:
            description = self.clean_text(perex_tag.text)
        
        # Hlavní obsah
        content = ""
        article_body = soup.find('div', class_='article-body')
        if article_body:
            content = self.html_to_markdown(article_body)
        
        # Datum
        published = None
        date_tag = soup.find('time')
        if date_tag and date_tag.get('datetime'):
            published = date_tag['datetime'].split('T')[0]
        
        # Autor
        author = None
        author_tag = soup.find('span', class_='author')
        if author_tag:
            author = self.clean_text(author_tag.text)
        
        # Obrázek
        image = None
        img_tag = soup.find('img', class_='article-image')
        if img_tag and img_tag.get('src'):
            image = img_tag['src']
            if not image.startswith('http'):
                image = 'https://denikreferendum.cz' + image
        
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
        
        # Obsah článku
        content = ""
        article = soup.find('article') or soup.find('div', class_='entry-content')
        if article:
            # Odstraň navigaci a další prvky
            for unwanted in article.find_all(['nav', 'aside', 'footer']):
                unwanted.decompose()
            content = self.html_to_markdown(article)
        
        # Datum
        published = None
        date_tag = soup.find('time')
        if date_tag and date_tag.get('datetime'):
            published = date_tag['datetime'].split('T')[0]
        
        # Obrázek
        image = None
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
        
        # Perex
        description = None
        perex_tag = soup.find('div', class_='perex') or soup.find('p', class_='lead')
        if perex_tag:
            description = self.clean_text(perex_tag.text)
        
        # Obsah
        content = ""
        article = soup.find('div', class_='article-content') or soup.find('article')
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
            'source': 'Finmag',
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
    
    return None  # Použije se universal fallback
