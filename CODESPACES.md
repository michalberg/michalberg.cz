# 🚀 GitHub Codespaces Guide

Tento projekt je plně připraven pro GitHub Codespaces - můžeš všechno dělat přímo v prohlížeči!

## ✅ Co je GitHub Codespaces?

- **VS Code v prohlížeči** - plnohodnotné vývojové prostředí
- **Vše předinstalováno** - Python, Hugo, Git, všechny závislosti
- **60 hodin zdarma** měsíčně (pro osobní účty)
- **Žádná lokální instalace** - vše běží v cloudu

---

## 🎯 Jak začít

### 1. Nahraj projekt na GitHub

```bash
# Vytvoř nový repozitář na github.com
# Pojmenuj ho např: michalberg-web

# V repozitáři:
# Add file → Upload files
# Přetáhni všechny soubory z rozbalené složky
# Commit
```

### 2. Otevři Codespace

```
V tvém GitHub repozitáři:
→ Klikni na zelené tlačítko "Code"
→ Záložka "Codespaces"
→ "Create codespace on main"
```

Počkej ~2 minuty, Codespace se vytvoří a nastaví automaticky! ✨

### 3. Co se stane automaticky

Když se Codespace spustí, automaticky:
- ✅ Nainstaluje Python balíčky
- ✅ Stáhne Hugo theme (PaperMod)
- ✅ Vytvoří slug-registry.json
- ✅ Všechno připraví k použití

---

## 📝 Základní použití

### Spustit Hugo preview

V terminálu (dole v Codespace):

```bash
hugo server -D
```

→ Automaticky se otevře náhled webu v prohlížeči!
→ URL bude typu: `https://abc-123.preview.app.github.dev`

### Importovat článek

```bash
python .github/scripts/import_articles.py "https://denikreferendum.cz/clanek/..."
```

Nebo přidej URL do `articles-to-import.txt` a spusť:

```bash
python .github/scripts/import_articles.py
```

### Migrovat WordPress

```bash
# Nejdřív nahraj wordpress-export.xml do repozitáře
python .github/scripts/migrate_wordpress.py wordpress-export.xml
```

### Vytvořit nový článek

**Možnost 1: V terminálu**
```bash
hugo new posts/muj-clanek.md
```

**Možnost 2: V Explorer (levý panel)**
```
→ content/posts/
→ Pravé tlačítko → New File
→ Název: muj-clanek.md
```

---

## 🔧 Editace souborů

### Přes VS Code Editor (v Codespace)

1. **Explorer** (levý panel) - procházej soubory
2. **Klikni na soubor** - otevře se v editoru
3. **Edituj** - změny se ukládají automaticky
4. **Source Control** (levý panel) - Git commit & push

### Markdown preview

- Otevři .md soubor
- Klikni na ikonu 🔍 vpravo nahoře
- Zobrazí se preview

---

## 📊 Workflow

### Jednorázová migrace

```bash
# 1. WordPress
python .github/scripts/migrate_wordpress.py wordpress.xml

# 2. Batch import externích článků
# Edituj articles-to-import.txt (přidej všechny URL)
python .github/scripts/import_articles.py

# 3. Commit & push
git add .
git commit -m "Migrace dokončena"
git push
```

### Průběžné přidávání

**Vlastní článek:**
```
1. Explorer → content/posts/ → New File
2. Vytvoř muj-clanek.md
3. Napiš Markdown
4. Source Control → Commit → Push
```

**Import z URL:**
```bash
# V terminálu:
python .github/scripts/import_articles.py "URL"
git add .
git commit -m "Import článku"
git push
```

**Facebook post:**
```
1. Vytvoř content/posts/facebook-post.md
2. Zkopíruj text z Facebooku
3. Commit & push
```

---

## 🎨 Editace stránek

### O mně & CV

```
content/pages/o-mne.md
content/pages/cv.md
```

Edituj přes VS Code editor → Save → Commit & Push

### Konfigurace webu

```
config.toml
```

Změň:
- `baseURL`
- Sociální sítě
- Menu
- atd.

---

## 🔍 Testování před publikací

### 1. Hugo preview

```bash
hugo server -D
```

→ Vidíš web včetně draft článků

### 2. Zkontroluj URL

```bash
cat slug-registry.json | grep "slug-který-chceš-zkontrolovat"
```

### 3. Test importu

```bash
# Test na jednom článku:
python .github/scripts/import_articles.py "URL"

# Zkontroluj vytvořený soubor:
ls -l content/posts/
```

---

## 💾 Git operace

### Commit změn

**V terminálu:**
```bash
git add .
git commit -m "Popis změny"
git push
```

**Přes UI:**
```
1. Source Control (levý panel)
2. Vlož commit message
3. Klikni ✓ Commit
4. Sync Changes (push)
```

### Zobrazit změny

```bash
git status
git diff
```

---

## 🚨 Troubleshooting

### Hugo theme chybí

```bash
git submodule add https://github.com/adityatelange/hugo-PaperMod.git themes/PaperMod
git submodule update --init --recursive
```

### Python balíčky chybí

```bash
pip install -r requirements.txt
```

### Import selhal

```bash
# Zkus s verbose výstupem:
python .github/scripts/import_articles.py "URL" --verbose
```

### Port 1313 je obsazený

```bash
# Vypni běžící Hugo:
pkill hugo

# Spusť znovu:
hugo server -D
```

---

## ⚡ Keyboard Shortcuts

- **Ctrl+`** - Otevři/zavři terminál
- **Ctrl+P** - Rychlé otevření souboru
- **Ctrl+Shift+P** - Command Palette
- **Ctrl+/** - Komentář/odkomentuj řádek
- **Ctrl+S** - Ulož soubor
- **Ctrl+F** - Najdi v souboru
- **Ctrl+Shift+F** - Najdi v projektu

---

## 📦 Zastavení/Smazání Codespace

### Zastavit (ušetří hodiny)

```
github.com → Codespaces
→ Tvůj codespace → ... → Stop
```

### Smazat (už nepotřebuješ)

```
github.com → Codespaces
→ Tvůj codespace → ... → Delete
```

**Poznámka:** Vše je v Git repozitáři, takže nic neztratíš!

---

## 🎯 Tipy & Triky

### 1. Automatické buildování

Po každém push do `main` branch se web automaticky rebuild a deploy na GitHub Pages.

### 2. Preview článků s draft: true

```bash
hugo server -D
```

`-D` flag zobrazí i draft články.

### 3. Rychlý import více článků

```
# articles-to-import.txt:
https://denikreferendum.cz/clanek/1
https://respekt.cz/blog/clanek/2
https://medium.seznam.cz/clanek/3
```

```bash
python .github/scripts/import_articles.py
```

### 4. Zkontroluj kolize URL

```bash
python -c "import json; print(json.dumps(json.load(open('slug-registry.json')), indent=2))"
```

---

## 🔗 Užitečné odkazy

- **GitHub Codespaces docs:** https://docs.github.com/en/codespaces
- **Hugo docs:** https://gohugo.io/documentation/
- **Markdown guide:** https://www.markdownguide.org/
- **Tvůj web:** https://michalberg.cz (po nastavení domény)

---

## ✅ Checklist pro první spuštění

- [ ] Projekt nahraný na GitHub
- [ ] Codespace vytvořen a spuštěn
- [ ] `hugo server -D` funguje
- [ ] Test import 1 článku
- [ ] Editace o-mne.md a cv.md
- [ ] Aktualizace config.toml
- [ ] První commit & push
- [ ] Zkontrolovat GitHub Actions
- [ ] Nastavit custom domain

---

**Vše je připraveno! Můžeš začít.** 🎉
