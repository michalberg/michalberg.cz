# michalberg.cz

Osobni web Michala Berga. Staticka stranka postavena na [Hugo](https://gohugo.io/) s tematem [PaperMod](https://github.com/adityatelange/hugo-PaperMod), hostovana na GitHub Pages.

## Struktura projektu

```
michalberg.cz/
├── content/
│   ├── posts/              # Clanky (~200 Markdown souboru)
│   ├── pages/              # Staticke stranky (O mne, CV, Podcasty)
│   └── hledani.md          # Fulltext vyhledavaci stranka
├── data/
│   └── podcasty.yaml       # Data pro stranku podcastu
├── layouts/
│   ├── _default/
│   │   ├── list.html       # Override homepage (search box + clanky)
│   │   ├── single.html     # Override sablony clanku
│   │   ├── archives.html   # Archiv
│   │   └── podcasty.html   # Sablona stranky podcastu
│   └── partials/
│       └── post_meta.html  # Override meta informaci clanku
├── assets/
│   ├── css/extended/
│   │   └── search-home.css # Styly pro homepage vyhledavani
│   └── js/
│       └── fastsearch.js   # Override Fuse.js search (podpora URL hash)
├── static/
│   ├── images/             # Obrazky (wordpress/, 2025/, 2026/)
│   ├── favicon.ico         # Favicony
│   └── og-image.jpg        # Open Graph obrazek
├── themes/PaperMod/        # Hugo tema (git submodule)
├── config.toml             # Hugo konfigurace
├── slug-registry.json      # Registr URL (pro import)
├── articles-to-import.txt  # Fronta pro import clanku
└── .github/workflows/
    └── deploy.yml          # GitHub Actions: Hugo build + deploy
```

## Vyhledavani

Web pouziva klientsky fulltext pres [Fuse.js](https://fusejs.io/):

- **Homepage** - search box s live vysledky primo na strance
- **/hledani/** - dedicka vyhledavaci stranka (PaperMod built-in)
- Index se generuje z `index.json` (Hugo JSON output)

## Pridavani clanku

### Rucne

Vytvorit soubor v `content/posts/muj-clanek.md`:

```markdown
---
title: "Nazev clanku"
date: 2026-01-15
slug: "muj-clanek"
draft: false
tags: ["politika"]
sources: ["Vlastni"]
image: "/images/2026/muj-clanek.jpg"
---

Text clanku...
```

Vysledek: `michalberg.cz/muj-clanek/`

### Import z URL

Pridat URL do `articles-to-import.txt` (jeden na radek):

```
https://denikreferendum.cz/clanek/muj-clanek
https://medium.com/@autor/clanek|vlastni-slug
```

Spustit: `python import_articles.py "https://url-clanku.cz"`

## Deployment

Push na `main` automaticky spusti GitHub Actions workflow:
1. Build Hugo site
2. Deploy na GitHub Pages

Domena: **michalberg.cz**
