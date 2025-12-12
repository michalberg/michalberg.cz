# 📦 Projekt: michalberg.cz - Kompletní přehled

## 🎯 Co je připraveno

Kompletní statický web s automatizovaným importem článků a plnou podporou GitHub Codespaces.

## 🚀 NOVÉ v této verzi

### GitHub Codespaces podpora
- ✅ `.devcontainer/` - kompletní konfigurace
- ✅ Automatický setup při startu
- ✅ VS Code extensions pro Hugo, Markdown, Python
- ✅ Port forwarding - Hugo preview v prohlížeči
- ✅ 60 hodin zdarma měsíčně

### Custom parsery pro tvé weby
- ✅ **Deník Referendum** - plně funkční parser
- ✅ **Respekt Blog** (berg.blog.respekt.cz) - plně funkční
- ✅ **Medium Seznam** - plně funkční parser
- ✅ **Finmag** - plně funkční parser
- ✅ Automatická detekce správného parseru
- ✅ Fallback na univerzální parser

### Nová dokumentace
- ✅ **CODESPACES.md** - kompletní guide pro práci v prohlížeči
- ✅ **test_parsers.py** - test script pro ověření parserů

---

## 📁 Struktura souborů (21 souborů)

```
michalberg-web/
│
├── 📄 Konfigurace
│   ├── config.toml                 ✅ Hugo konfigurace
│   ├── .gitignore                  ✅ Git ignore
│   ├── .gitmodules                 ✅ Hugo theme submodule
│   ├── requirements.txt            ✅ Python závislosti
│   └── init.sh                     ✅ Inicializační skript
│
├── 📚 Dokumentace
│   ├── README.md                   ✅ Hlavní dokumentace
│   ├── SETUP.md                    ✅ Setup guide
│   └── PROJECT_OVERVIEW.md         ✅ Tento soubor
│
├── 📝 Obsah
│   ├── content/
│   │   ├── posts/
│   │   │   └── vzorovy-clanek.md  ✅ Vzorový článek
│   │   └── pages/
│   │       ├── o-mne.md           ✅ O mně stránka
│   │       └── cv.md              ✅ CV stránka
│   │
│   └── static/
│       ├── CNAME                   ✅ Doména pro GitHub Pages
│       └── images/                 ✅ Složka pro obrázky
│
├── 🤖 Automatizace (GitHub Actions)
│   ├── .github/workflows/
│   │   ├── deploy.yml             ✅ Build & deploy webu
│   │   └── import-articles.yml    ✅ Automatický import článků
│   │
│   └── .github/scripts/
│       ├── import_articles.py     ✅ Import skript (univerzální)
│       ├── migrate_wordpress.py   ✅ WordPress migrace
│       └── custom_parsers.py      ✅ Site-specific parsery
│
└── 📋 Utility
    ├── articles-to-import.txt      ✅ Queue pro import
    └── slug-registry.json          🔄 Auto-generovaný registr URL
```

---

## ⚙️ Jak to funguje

### 1️⃣ Přidání článku z URL

```
Ty → articles-to-import.txt (přidáš URL)
  ↓
Git push
  ↓
GitHub Action: import-articles.yml
  ↓
Python: import_articles.py
  ├─ Stáhne článek
  ├─ Extrahuje metadata (titulek, datum, autor...)
  ├─ Stáhne obrázky
  ├─ Zkontroluje kolizi URL
  ├─ Vytvoří .md soubor
  └─ Commitne zpět do repo
  ↓
GitHub Action: deploy.yml
  ├─ Build Hugo webu
  └─ Deploy na GitHub Pages
  ↓
Web je live na michalberg.cz! ✅
```

### 2️⃣ Ručně vytvořený článek

```
Ty → content/posts/clanek.md (vytvoříš přes GitHub web)
  ↓
Git commit
  ↓
GitHub Action: deploy.yml
  ├─ Build Hugo webu
  └─ Deploy na GitHub Pages
  ↓
Web je live! ✅
```

### 3️⃣ WordPress migrace

```
Ty → wordpress-export.xml (nahraješ)
  ↓
Spustíš: python migrate_wordpress.py wordpress-export.xml
  ├─ Parsuje XML
  ├─ Vytvoří .md soubory
  ├─ Stáhne obrázky
  └─ Zachová URL strukturu
  ↓
Git push
  ↓
Deploy workflow
  ↓
Všechny články migrované! ✅
```

---

## 🔒 Ochrana před přepsáním URL

**Automatická detekce kolize:**

```python
# slug-registry.json
{
  "buran-babis": {
    "file": "content/posts/buran-babis.md",
    "url": "michalberg.cz/buran-babis/"
  }
}

# Nový import s názvem "Buran Babiš"
→ Slug: "buran-babis"
→ Kontrola: již existuje ❌
→ Řešení: "buran-babis-2" ✅
```

**Výsledek:**
- Originální článek: `michalberg.cz/buran-babis/`
- Nový článek: `michalberg.cz/buran-babis-2/`

---

## 🌐 URL struktura

### WordPress migrace
```
WordPress:  michalberg.cz/buran-babis/
Hugo:       michalberg.cz/buran-babis/
→ IDENTICKÉ ✅
```

### Nové články
```
Slug v front matter: "muj-clanek"
URL:                 michalberg.cz/muj-clanek/
```

### Archiv
```
michalberg.cz/archiv/2024/     → články z 2024
michalberg.cz/sources/respekt/ → články z Respektu
michalberg.cz/tags/politika/   → články s tagem politika
```

---

## 🚀 Deployment

**GitHub Pages:**
- ✅ Zdarma hosting
- ✅ HTTPS (Let's Encrypt)
- ✅ Custom domain (michalberg.cz)
- ✅ Automatický build při každém push
- ✅ CDN (globální distribuce)

**Build čas:**
- Hugo build: ~2 sekundy
- Deploy: ~30 sekund
- **Total: <1 minuta** od push po live web

---

## 🔧 Konfigurace

### config.toml
```toml
baseURL = "https://michalberg.cz/"
title = "Michal Berg"
theme = "PaperMod"

[permalinks]
  posts = "/:slug/"  # Zachování WordPress URL struktury

[params]
  # Sociální sítě, popis, atd.
```

### GitHub Actions
```yaml
# .github/workflows/import-articles.yml
Trigger: Push do articles-to-import.txt
Akce:    Import článků + commit

# .github/workflows/deploy.yml  
Trigger: Jakýkoliv push do main
Akce:    Hugo build + deploy na GitHub Pages
```

---

## 📊 Statistiky (očekávané)

**Performance:**
- Build rychlost: 1000+ stránek za sekundu
- Velikost stránky: ~50-100 KB
- Load time: <1 sekunda
- Lighthouse score: 95+ (všechny metriky)

**Kapacita:**
- GitHub Pages limit: 1 GB
- Odhadovaná kapacita: 5000+ článků
- Bandwidth limit: 100 GB/měsíc (soft)

---

## 🛠️ Technologie

**Core:**
- **Hugo** 0.121+ (Static Site Generator)
- **GitHub Pages** (Hosting)
- **GitHub Actions** (CI/CD)

**Import:**
- **Python** 3.11+
- **BeautifulSoup4** (HTML parsing)
- **Requests** (HTTP)
- **html2text** (HTML→Markdown)
- **python-slugify** (URL slugs)

**Theme:**
- **PaperMod** (Minimalistický Hugo theme)

---

## 📝 Co je potřeba udělat

### Před prvním použitím:

1. **Nahraj do GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin [tvůj-repo-url]
   git push -u origin main
   ```

2. **Přidej Hugo theme:**
   ```bash
   ./init.sh
   # nebo:
   git submodule add https://github.com/adityatelange/hugo-PaperMod.git themes/PaperMod
   ```

3. **Zapni GitHub Pages:**
   - Settings → Pages → Source: GitHub Actions

4. **Nastav doménu:**
   - Settings → Pages → Custom domain: michalberg.cz
   - U registrátora: DNS A records (viz README)

5. **Edituj obsah:**
   - `content/pages/o-mne.md`
   - `content/pages/cv.md`
   - `config.toml` (sociální sítě)

### První test:

6. **Test import:**
   - Přidej 1 URL do `articles-to-import.txt`
   - Commit & push
   - Zkontroluj Actions tab

7. **WordPress migrace:**
   - Exportuj WordPress XML
   - Spusť: `python migrate_wordpress.py export.xml`
   - Push

---

## 🎯 Features

### ✅ Implementováno

- ✅ Automatický import z URL
- ✅ WordPress migrace
- ✅ Detekce kolize URL
- ✅ Automatické stahování obrázků
- ✅ HTML → Markdown konverze
- ✅ GitHub Pages deploy
- ✅ Custom domain podpora
- ✅ Slug registry
- ✅ Archiv podle roku
- ✅ Taxonomie (tagy, zdroje)
- ✅ RSS feed
- ✅ Sitemap.xml
- ✅ SEO optimalizace

### 🔄 Připraveno pro rozšíření

- 🔄 Custom parsery pro specifické weby
- 🔄 AI enhancement (shrnutí, tagy)
- 🔄 Scheduled imports
- 🔄 Email notifikace

---

## 🆘 Troubleshooting

**Problem:** Build failuje
**Solution:** Zkontroluj Actions → červené ❌ → error log

**Problem:** Import článku selhal
**Solution:** Web může blokovat scraping → přidej ručně

**Problem:** URL kolize
**Solution:** Automaticky řešeno `-2`, `-3`, atd.

**Problem:** Obrázky se nenačítají
**Solution:** Zkontroluj HTTPS URL obrázků

---

## 📞 Support

- **Dokumentace:** README.md, SETUP.md
- **Issues:** GitHub Issues
- **Custom parsery:** custom_parsers.py

---

## 🎉 Ready to go!

Vše je připraveno. Stačí:

1. Nahraj do GitHubu
2. Zapni GitHub Pages
3. Nastav doménu
4. Začni přidávat články

**Odhadovaný čas setupu: 30 minut**

---

Vytvořeno: 2024-12-12
Verze: 1.0
