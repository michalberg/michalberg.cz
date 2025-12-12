# 🚀 Setup Guide - První spuštění

Tento dokument ti pomůže nastavit web od začátku.

## ✅ Checklist

### 1. GitHub repozitář

- [ ] Fork nebo vytvoř nový repozitář z tohoto projektu
- [ ] Nahraj všechny soubory do repozitáře
- [ ] Přidej Hugo theme:
  ```bash
  git submodule add https://github.com/adityatelange/hugo-PaperMod.git themes/PaperMod
  git submodule update --init --recursive
  ```

### 2. GitHub Pages

- [ ] Jdi do **Settings** → **Pages**
- [ ] Source: **GitHub Actions**
- [ ] Počkej na první build (Actions tab)
- [ ] Web bude na: `https://[username].github.io/michalberg-web/`

### 3. Vlastní doména (michalberg.cz)

- [ ] V GitHub: Settings → Pages → Custom domain → `michalberg.cz`
- [ ] ✅ Zaškrtni "Enforce HTTPS"
- [ ] U registrátora domény nastav DNS (viz README)
- [ ] Čekej 15-60 minut na propagaci

### 4. Editace obsahu

- [ ] Edituj `content/pages/o-mne.md`
- [ ] Edituj `content/pages/cv.md`
- [ ] Aktualizuj sociální sítě v `config.toml`

### 5. Přidání obsahu

**Vlastní článek:**
- [ ] Vytvoř první test článek přes GitHub web interface
- [ ] Zkontroluj, že se správně zobrazuje

**WordPress migrace:**
- [ ] Exportuj WordPress XML
- [ ] Nahraj do repozitáře
- [ ] Spusť: `python .github/scripts/migrate_wordpress.py wordpress-export.xml`

**Import externích článků:**
- [ ] Přidej 2-3 test URL do `articles-to-import.txt`
- [ ] Commit → zkontroluj, že se importovaly

---

## 🔧 Lokální testování (volitelné)

Pokud chceš testovat lokálně před push:

### Instalace Hugo

**macOS:**
```bash
brew install hugo
```

**Windows:**
```bash
choco install hugo-extended
```

**Linux:**
```bash
snap install hugo
```

### Spuštění lokálního serveru

```bash
cd michalberg-web
hugo server -D
```

Otevři: http://localhost:1313

---

## 📝 Testovací články

Pro otestování můžeš použít tyto veřejné URL:

```
https://www.irozhlas.cz/zpravy-domov/
https://echo24.cz/
```

Přidej je do `articles-to-import.txt` a commit.

---

## ⚙️ Konfigurace config.toml

Uprav tyto hodnoty:

```toml
baseURL = "https://michalberg.cz/"  # tvoje doména
title = "Michal Berg"                # název webu

[params]
  description = "..."                 # popis
  author = "Michal Berg"              # jméno
  
  # Sociální sítě
  [[params.socialIcons]]
    name = "facebook"
    url = "https://facebook.com/TVUJ_PROFIL"  # ← změň
  
  [[params.socialIcons]]
    name = "linkedin"
    url = "https://linkedin.com/in/TVUJ_PROFIL"  # ← změň
```

---

## 🎨 Změna tématu

Výchozí: **PaperMod** (minimalistické, rychlé)

Pro změnu:

1. Vyber téma z https://themes.gohugo.io/
2. Přidej jako submodule:
   ```bash
   git submodule add THEME_URL themes/THEME_NAME
   ```
3. Změň v `config.toml`:
   ```toml
   theme = "THEME_NAME"
   ```

---

## 🐍 Python setup (pro lokální import)

```bash
# Vytvoř virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instaluj závislosti
pip install -r requirements.txt

# Spusť import
python .github/scripts/import_articles.py
```

---

## ✅ Ověření, že vše funguje

### Test 1: Web je live
- [ ] Otevři `https://[username].github.io/michalberg-web/`
- [ ] Měl bys vidět vzorový článek

### Test 2: Vlastní doména
- [ ] Otevři `https://michalberg.cz`
- [ ] Zkontroluj HTTPS (zelený zámek)

### Test 3: Import článku
- [ ] Přidej URL do `articles-to-import.txt`
- [ ] Commit
- [ ] Zkontroluj Actions → Import Articles
- [ ] Měl by být nový soubor v `content/posts/`

### Test 4: Kolize URL
- [ ] Vytvoř článek s slug `test-clanek`
- [ ] Zkus importovat článek, který by měl stejný slug
- [ ] Měl by se vytvořit jako `test-clanek-2`

---

## 📞 Pomoc

Pokud narazíš na problém:

1. Zkontroluj **Actions** tab v GitHub
2. Klikni na červené ❌ a prohlédni error log
3. Vytvoř Issue s popisem problému

---

## 🎯 Další kroky

Po základním setupu:

- [ ] Přidej Google Analytics (volitelně)
- [ ] Nastav Google Search Console
- [ ] Submitni sitemap: `michalberg.cz/sitemap.xml`
- [ ] Přidej favicon (nahraj do `static/`)
- [ ] Customize CSS (vytvoř `assets/css/extended/custom.css`)

---

Hotovo! Tvůj web je připraven. 🎉
