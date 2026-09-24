#!/usr/bin/env bash
# ==============================================================================
# Script d'installation automatique du Senior Agent Core
# Déploie la configuration pour TOUS les assistants : Gemini, Copilot/Codex, Cursor, Claude, etc.
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
  echo -e "  📥 Déploiement de ${YELLOW}${target_path}${RESET}..."
  mkdir -p "$(dirname "$target_path")"
  curl -sSL "${REPO_RAW_URL}/${source_path}" -o "$target_path"
}

# 1. Standard Universel (Agents autonomes, Windsurf, Aider, Cline)
download_file "AGENTS.md" "AGENTS.md"

# 2. Google Gemini & Antigravity
download_file "templates/GEMINI.md" "GEMINI.md"

# 3. GitHub Copilot & OpenAI Codex (VS Code & Web)
download_file "templates/.github/copilot-instructions.md" ".github/copilot-instructions.md"

# 4. Cursor IDE
download_file "templates/.cursorrules" ".cursorrules"

# 5. Claude / Anthropic
download_file "templates/CLAUDE.md" "CLAUDE.md"

# 6. Checklists de référence indispensables
download_file "checklists/01-architecture-et-conception.md" ".agent/checklists/01-architecture.md"
download_file "checklists/02-qualite-et-clean-code.md" ".agent/checklists/02-clean-code.md"
download_file "checklists/03-securite-applicative-et-api.md" ".agent/checklists/03-securite.md"
download_file "checklists/04-conformite-rgpd-et-vie-privee.md" ".agent/checklists/04-rgpd.md"
download_file "checklists/05-tests-et-resilience.md" ".agent/checklists/05-tests.md"
download_file "checklists/06-performance-et-accessibilite.md" ".agent/checklists/06-performance-a11y.md"

echo ""
echo -e "${GREEN}${BOLD}✅ Terminé avec succès ! Vos assistants sont maintenant configurés en Senior :${RESET}"
echo -e "   - Google Gemini / Antigravity : ${BOLD}GEMINI.md${RESET}"
echo -e "   - GitHub Copilot / Codex      : ${BOLD}.github/copilot-instructions.md${RESET}"
echo -e "   - Agent Universel             : ${BOLD}AGENTS.md${RESET}"
echo -e "   - Cursor IDE                  : ${BOLD}.cursorrules${RESET}"
echo -e "   - Claude / Anthropic          : ${BOLD}CLAUDE.md${RESET}"
