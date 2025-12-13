# 🌐 Michalberg.cz - Osobní web

Statický web postavený na Hugo a hostovaný na GitHub Pages.

Chybí:
- nastavit DNS Hodnota: 185.199.111.153
```

**CNAME záznam (volitelně pro www):**
```
Typ: CNAME
Název: www
Hodnota: [tvuj-username].github.io
```

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

Případně jako parametr: **python import_articles.py "https://url-clanku.cz"**

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

Soubor `slug-registry.json` obsahuje registr všech URL. Při celkovém novém importu je potřeba soubor smazat

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