#!/usr/bin/env python3
"""
Test script pro custom parsery
Otestuje, zda parsery fungují pro tvé weby
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from custom_parsers import get_parser_for_url
import requests
from bs4 import BeautifulSoup

# Testovací URL
TEST_URLS = {
    'Deník Referendum': 'https://denikreferendum.cz/clanek/237231-chytra-odveta-na-trumpova-cla-zdanit-americke-oligarchy',
    'Respekt Blog': 'https://berg.blog.respekt.cz/emil-kutscha/index.html',
    'Medium Seznam': 'https://medium.seznam.cz/clanek/michal-berg-motoriste-budou-v-klimatu-couvat-logika-ciste-energie-je-stejne-smete-208153',
    'Finmag': 'https://www.finmag.cz/finance/403323-danova-spravedlnost-je-dobra-pro-pravici-i-levici'
}

def test_parser(name, url):
    """Otestuje parser pro danou URL"""
    print(f"\n{'='*60}")
    print(f"🧪 Test: {name}")
    print(f"   URL: {url}")
    print('='*60)
    
    try:
        # Najdi parser
        parser = get_parser_for_url(url)
        
        if not parser:
            print("❌ Žádný custom parser nenalezen!")
            return False
        
        print(f"✅ Nalezen parser: {parser.__class__.__name__}")
        
        # Stáhni stránku
        print("📥 Stahuji stránku...")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        # Parsuj
        print("🔍 Parsuji obsah...")
        data = parser.parse(response.text, url)
        
        # Validace
        print("\n📊 Výsledky:")
        print(f"   Titulek: {'✅' if data.get('title') else '❌'} {data.get('title', 'CHYBÍ')[:60]}...")
        print(f"   Autor: {data.get('author', 'nenalezen')}")
        print(f"   Datum: {data.get('published', 'nenalezeno')}")
        print(f"   Popis: {'✅' if data.get('description') else '⚠️'} {len(data.get('description', '')) if data.get('description') else 0} znaků")
        print(f"   Obrázek: {'✅' if data.get('image') else '⚠️'} {data.get('image', 'nenalezen')[:50]}")
        print(f"   Obsah: {'✅' if data.get('content') else '❌'} {len(data.get('content', '')) if data.get('content') else 0} znaků")
        
        if not data.get('title'):
            print("\n❌ SELHÁNÍ: Chybí titulek!")
            return False
        
        if not data.get('content'):
            print("\n❌ SELHÁNÍ: Chybí obsah!")
            return False
        
        print("\n✅ Parser funguje!")
        return True
        
    except Exception as e:
        print(f"\n❌ CHYBA: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Hlavní funkce - otestuje všechny parsery"""
    print("🚀 Test custom parserů pro michalberg.cz")
    print("=" * 60)
    
    results = {}
    
    for name, url in TEST_URLS.items():
        results[name] = test_parser(name, url)
    
    # Shrnutí
    print("\n" + "=" * 60)
    print("📊 SHRNUTÍ TESTŮ")
    print("=" * 60)
    
    for name, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {name}")
    
    total = len(results)
    passed = sum(1 for s in results.values() if s)
    
    print(f"\n🎯 Úspěšnost: {passed}/{total} ({int(passed/total*100)}%)")
    
    if passed == total:
        print("\n🎉 Všechny parsery fungují!")
        return 0
    else:
        print("\n⚠️  Některé parsery selhaly. Zkontroluj výše.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
