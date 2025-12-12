#!/bin/bash

echo "🚀 Inicializace michalberg-web projektu..."
echo ""

# Zkontroluj, jestli je git repozitář
if [ ! -d ".git" ]; then
    echo "❌ Nejsi v git repozitáři!"
    echo "Spusť nejdřív: git init"
    exit 1
fi

# Přidej Hugo theme jako submodule
echo "📦 Přidávám Hugo PaperMod theme..."
git submodule add --force https://github.com/adityatelange/hugo-PaperMod.git themes/PaperMod

# Update submodules
echo "🔄 Aktualizuji submodules..."
git submodule update --init --recursive

echo ""
echo "✅ Inicializace dokončena!"
echo ""
echo "Další kroky:"
echo "1. Edituj config.toml (změň URL, sociální sítě)"
echo "2. Edituj content/pages/o-mne.md a cv.md"
echo "3. git add ."
echo "4. git commit -m 'Initial commit'"
echo "5. git push"
echo ""
echo "Pro lokální test: hugo server -D"
echo ""
