# 🌐 Michalberg.cz - Osobní web

Statický web postavený na Hugo a hostovaný na GitHub Pages.

## 🚀 Rychlý start s GitHub Codespaces (doporučeno)

**Vše můžeš dělat přímo v prohlížeči - žádná lokální instalace!**

1. Nahraj projekt na GitHub
2. Klikni **Code** → **Codespaces** → **Create codespace**
3. Počkej ~2 minuty → Vše se nastaví automaticky!

**👉 [Podrobný Codespaces guide](CODESPACES.md)**

---

## 📋 Obsah

- [Rychlý start](#rychlý-start)
- [Nastavení domény](#nastavení-domény)
- [Přidávání článků](#přidávání-článků)
- [Migrace z WordPressu](#migrace-z-wordpressu)
- [Struktura projektu](#struktura-projektu)

---

## 🚀 Rychlý start

### 1. Fork nebo clone repozitáře

```bash
git clone https://github.com/[tvuj-username]/michalberg-web.git
cd michalberg-web
```

### 2. Zapni GitHub Pages

1. Jdi na **Settings** → **Pages**
2. Source: **GitHub Actions**
3. Hotovo! Web se automaticky buildne při každém push

---

## 🌐 Nastavení domény michalberg.cz

### 1. V GitHub repozitáři

Settings → Pages → Custom domain:
```
michalberg.cz
```
✅ Zaškrtni "Enforce HTTPS"

### 2. U registrátora domény (DNS nastavení)

Přidej tyto DNS záznamy:

**A záznamy:**
```
Typ: A
Název: @
Hodnota: 185.199.108.153
```
```
Typ: A  
Název: @
Hodnota: 185.199.109.153
```
```
Typ: A
Název: @
Hodnota: 185.199.110.153
```
```
Typ: A
Název: @
Hodnota: 185.199.111.153
```

**CNAME záznam (volitelně pro www):**
```
Typ: CNAME
Název: www
Hodnota: [tvuj-username].github.io
```

### 3. Čekej na propagaci

- DNS propagace: 15-60 minut
- HTTPS certifikát: dalších 5-10 minut
- Zkontroluj: https://www.whatsmydns.net/#A/michalberg.cz

---

## 📝 Přidávání článků

### Metoda 1: Import z URL (automaticky)

**Pro externí články (Respekt, Deník, Medium atd.):**

1. Přes GitHub web jdi na soubor `articles-to-import.txt`
2. Klikni **Edit** (ikona tužky)
3. Přidej URL článků (jeden na řádek):
   ```
   https://respekt.cz/clanek/muj-clanek
   https://denikreferendum.cz/clanek/dalsi-clanek
   ```
4. Můžeš zadat vlastní slug:
   ```
   https://medium.com/@autor/clanek|vlastni-slug-2024
   ```
5. Klikni **Commit changes**

**Co se stane:**
- GitHub Action automaticky stáhne články
- Vytvoří `.md` soubory v `content/posts/`
- Stáhne obrázky do `static/images/`
- Zkontroluje kolize URL (přidá `-2` pokud potřeba)
- Web se automaticky rebuild

### Metoda 2: Ručně vytvořit článek

**Pro vlastní články:**

1. Přes GitHub web jdi do `content/posts/`
2. Klikni **Add file** → **Create new file**
3. Název souboru: `muj-clanek.md`
4. Obsah:
   ```markdown
   ---
   title: "Název mého článku"
   date: 2024-12-12
   slug: "muj-clanek"
   draft: false
   tags: ["politika", "společnost"]
   sources: ["Vlastní"]
   ---
   
   # Nadpis
   
   Text článku...
   
   ## Podnadpis
   
   Další text...
   ```
5. Klikni **Commit new file**

**Výsledek:** `michalberg.cz/muj-clanek/`

### Metoda 3: Facebook posty (manuální kopírování)

1. Vytvoř nový soubor `content/posts/facebook-post-2024-12.md`
2. Zkopíruj text z Facebooku
3. Formát:
   ```markdown
   ---
   title: "Název postu"
   date: 2024-12-12
   slug: "facebook-post-2024-12"
   source: "Facebook"
   source_url: "https://facebook.com/tvuj-post"
   ---
   
   Zkopírovaný text z Facebooku...
   ```

---

## 🔄 Migrace z WordPressu

### 1. Exportuj z WordPressu

WordPress admin → Nástroje → Exportovat → Stáhnout export soubor

### 2. Nahraj do repozitáře

Přes GitHub web:
1. Jdi do root adresáře
2. **Add file** → **Upload files**
3. Nahraj `wordpress-export.xml`
4. Commit

### 3. Spusť migraci

GitHub Actions automaticky detekuje XML a spustí migraci, NEBO ručně:

```bash
# Lokálně (pokud máš Python)
pip install -r requirements.txt
python .github/scripts/migrate_wordpress.py wordpress-export.xml
```

**Co to udělá:**
- Převede všechny WordPress posty na Markdown
- Zachová původní URL strukturu (`/slug/`)
- Stáhne všechny obrázky
- Převede HTML na Markdown
- Zachová kategorie a tagy

---

## 📂 Struktura projektu

```
michalberg-web/
├── content/
│   ├── posts/              # Články (Markdown)
│   │   ├── vzorovy-clanek.md
│   │   └── ...
│   └── pages/              # Statické stránky
│       ├── o-mne.md
│       └── cv.md
├── static/
│   ├── images/             # Obrázky
│   │   ├── 2024/
│   │   └── wordpress/
│   └── CNAME              # Doména
├── .github/
│   ├── workflows/
│   │   ├── deploy.yml              # Build & deploy
│   │   └── import-articles.yml     # Import článků
│   └── scripts/
│       ├── import_articles.py      # Import skript
│       └── migrate_wordpress.py    # WordPress migrace
├── config.toml                     # Hugo konfigurace
├── articles-to-import.txt          # Queue pro import
├── slug-registry.json              # Registr URL (auto-generovaný)
└── requirements.txt                # Python závislosti
```

---

## 🎨 Archiv a taxonomie

Web automaticky vytváří:

### Podle roku
- `/archiv/2024/` - články z 2024
- `/archiv/2023/` - články z 2023

### Podle zdroje
- `/sources/respekt/` - články z Respektu
- `/sources/vlastni/` - vlastní články
- `/sources/facebook/` - Facebook posty

### Podle tagů
- `/tags/politika/`
- `/tags/spolecnost/`

---

## ⚙️ Detekce kolize URL

**Automatická ochrana proti přepsání článků:**

Když importuješ článek s URL která už existuje:
```
Existuje: michalberg.cz/buran-babis/
Importuješ: článek s názvem "Buran Babiš"
→ Automaticky vytvoří: michalberg.cz/buran-babis-2/
```

**Kolize jsou logované:**
```
⚠️  Kolize vyřešena: buran-babis → buran-babis-2
```

Soubor `slug-registry.json` obsahuje registr všech URL.

---

## 🔧 Editace stránek O mně a CV

1. Přes GitHub web jdi na `content/pages/o-mne.md`
2. Klikni **Edit** (ikona tužky)
3. Edituj text (Markdown formát)
4. **Commit changes**

Stejně pro `cv.md`.

---

## 🎯 Témata (Theme)

Aktuální téma: **PaperMod**

### Změna tématu

1. Edituj `config.toml`:
   ```toml
   theme = "NoveTheme"
   ```

2. Přidej theme jako submodule:
   ```bash
   git submodule add https://github.com/autor/theme themes/NoveTheme
   ```

Doporučené Hugo themes pro blogy:
- [PaperMod](https://github.com/adityatelange/hugo-PaperMod)
- [Hermit](https://github.com/Track3/hermit)
- [Terminal](https://github.com/panr/hugo-theme-terminal)

---

## 📊 Kontrola buildu

Po každém push:
1. Jdi na **Actions** tab v GitHub
2. Vidíš běžící workflow
3. Zelená ✅ = úspěch
4. Červená ❌ = chyba (klikni pro detail)

---

## 🐛 Troubleshooting

### Web se nebuildn

1. Zkontroluj Actions tab
2. Podívej se na error log
3. Nejčastější problémy:
   - Chybná syntax v Markdown front matter
   - Chybějící quote `"`
   - Neplatné datum

### Import článku selhal

1. Zkontroluj Actions → Import Articles
2. Možné příčiny:
   - URL není dostupná
   - Website blokuje scraping
   - Nestandardní struktura webu

**Řešení:** Přidej článek ručně (Metoda 2)

### URL kolize

Automaticky vyřešeno přidáním `-2`, `-3` atd.

Pokud chceš jiný slug:
1. Edituj soubor článku
2. Změň `slug: "novy-slug"`
3. Commit

---

## 📞 Kontakt & Podpora

- Issues: https://github.com/[username]/michalberg-web/issues
- Email: [tvuj-email]

---

## 📄 Licence

Obsah: © Michal Berg  
Code: MIT Licence
