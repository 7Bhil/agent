#!/usr/bin/env bash
# ==============================================================================
# Script d'installation automatique du Senior Agent Core
# Permet d'injecter les règles senior dans n'importe quel projet en 1 commande.
# Usage:
#   curl -sSL https://raw.githubusercontent.com/7Bhil/agent/main/install.sh | bash
#   ou: ./install.sh
# ==============================================================================

set -e

BOLD="\033[1m"
GREEN="\033[32m"
BLUE="\033[34m"
YELLOW="\033[33m"
RESET="\033[0m"

echo -e "${BLUE}${BOLD}=====================================================${RESET}"
echo -e "${BLUE}${BOLD}   🚀 Installation du Senior Agent Core             ${RESET}"
echo -e "${BLUE}${BOLD}=====================================================${RESET}"

REPO_RAW_URL="https://raw.githubusercontent.com/7Bhil/agent/developp"

download_file() {
  local source_path="$1"
  local target_path="$2"
  echo -e "  📥 Téléchargement de ${YELLOW}${target_path}${RESET}..."
  mkdir -p "$(dirname "$target_path")"
  curl -sSL "${REPO_RAW_URL}/${source_path}" -o "$target_path"
}

# 1. Copie du guide universel AGENTS.md
download_file "AGENTS.md" "AGENTS.md"

# 2. Copie des templates selon les IDEs détectés ou disponibles
download_file "templates/.cursorrules" ".cursorrules"
download_file "templates/CLAUDE.md" "CLAUDE.md"

# 3. Copie des checklists indispensables
download_file "checklists/01-architecture-et-conception.md" ".agent/checklists/01-architecture.md"
download_file "checklists/02-qualite-et-clean-code.md" ".agent/checklists/02-clean-code.md"
download_file "checklists/03-securite-applicative-et-api.md" ".agent/checklists/03-securite.md"
download_file "checklists/04-conformite-rgpd-et-vie-privee.md" ".agent/checklists/04-rgpd.md"
download_file "checklists/05-tests-et-resilience.md" ".agent/checklists/05-tests.md"
download_file "checklists/06-performance-et-accessibilite.md" ".agent/checklists/06-performance-a11y.md"

echo ""
echo -e "${GREEN}${BOLD}✅ Félicitations ! Votre projet est maintenant configuré avec un agent Senior.${RESET}"
echo -e "   - Fichier universel généré : ${BOLD}AGENTS.md${RESET}"
echo -e "   - Configuration Cursor : ${BOLD}.cursorrules${RESET}"
echo -e "   - Configuration Claude : ${BOLD}CLAUDE.md${RESET}"
echo -e "   - Checklists de référence : ${BOLD}.agent/checklists/${RESET}"
