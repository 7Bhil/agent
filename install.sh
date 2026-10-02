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
echo -e "${BLUE}${BOLD}    Installation du Senior Agent Core             ${RESET}"
echo -e "${BLUE}${BOLD}=====================================================${RESET}"

REPO_RAW_URL="${AGENT_CORE_URL:-https://raw.githubusercontent.com/7Bhil/agent/main}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" 2>/dev/null && pwd || echo "")"

download_file() {
  local source_path="$1"
  local target_path="$2"
  echo -e "   Déploiement de ${YELLOW}${target_path}${RESET}..."
  mkdir -p "$(dirname "$target_path")"

  if [ -n "$SCRIPT_DIR" ] && [ -f "${SCRIPT_DIR}/${source_path}" ] && [ "$SCRIPT_DIR" != "$(pwd)" ]; then
    cp "${SCRIPT_DIR}/${source_path}" "$target_path"
  else
    curl -sSL "${REPO_RAW_URL}/${source_path}" -o "$target_path"
  fi
}

# 1. Standard Universel (Agents autonomes, Windsurf, Aider, Cline)
download_file "AGENTS.md" "AGENTS.md"

# 2. Google Gemini & Antigravity
download_file "GEMINI.md" "GEMINI.md"

# 3. GitHub Copilot & OpenAI Codex (VS Code & Web)
download_file "templates/.github/copilot-instructions.md" ".github/copilot-instructions.md"

# 4. Cursor IDE
download_file ".cursorrules" ".cursorrules"

# 5. Claude / Anthropic
download_file "CLAUDE.md" "CLAUDE.md"

# 6. Mémoire Vivante (BRAIN.md) - Initialisation si absent
if [ ! -f "BRAIN.md" ]; then
  download_file "templates/BRAIN.md" "BRAIN.md"
fi

# 7. Cadre et Direction Artistique (DESIGN.md) - Initialisation si absent
if [ ! -f "DESIGN.md" ]; then
  download_file "DESIGN.md" "DESIGN.md"
fi

# 7. Guides d'Ingénierie Senior
GUIDES=(
  "architecture-and-design.md"
  "clean-code-node.md"
  "clean-technical-writing.md"
  "observability-and-logging.md"
  "onboard-codebase.md"
  "performance-a11y.md"
  "rgpd-developer.md"
  "security-handbook.md"
  "testing-strategy.md"
)
for guide in "${GUIDES[@]}"; do
  download_file "guides/${guide}" "guides/${guide}"
  # Miroir dans .agent/ pour compatibilité des chemins relatifs
  download_file "guides/${guide}" ".agent/guides/${guide}"
done

# 8. Checklists de référence indispensables
CHECKLISTS=(
  "01-architecture-et-conception.md:01-architecture.md"
  "02-qualite-et-clean-code.md:02-clean-code.md"
  "03-securite-applicative-et-api.md:03-securite.md"
  "04-conformite-rgpd-et-vie-privee.md:04-rgpd.md"
  "05-tests-et-resilience.md:05-tests.md"
  "06-performance-et-accessibilite.md:06-performance-a11y.md"
  "07-redaction-technique-anti-slop.md:07-redaction-anti-slop.md"
)
for entry in "${CHECKLISTS[@]}"; do
  src="${entry%%:*}"
  dest="${entry##*:}"
  download_file "checklists/${src}" "checklists/${src}"
  download_file "checklists/${src}" ".agent/checklists/${dest}"
done

# 9. Stacks d'Ingénierie Ciblées
STACKS=(
  "cpp.md"
  "database-management.md"
  "docker-containerization.md"
  "fintech.md"
  "java-spring.md"
  "laravel-php.md"
  "nodejs-backend.md"
  "python-fastapi-django.md"
  "react-nextjs.md"
)
for stack in "${STACKS[@]}"; do
  download_file "stacks/${stack}" "stacks/${stack}"
  download_file "stacks/${stack}" ".agent/stacks/${stack}"
done

# 10. Outillage Déterministe d'Ingénierie & Anti-Slop IA
download_file "scripts/audit-slop.py" "scripts/audit-slop.py"
chmod +x "scripts/audit-slop.py" 2>/dev/null || true
download_file "scripts/setup-git-hooks.sh" "scripts/setup-git-hooks.sh"
chmod +x "scripts/setup-git-hooks.sh" 2>/dev/null || true
download_file "scripts/test-kit.sh" "scripts/test-kit.sh"
chmod +x "scripts/test-kit.sh" 2>/dev/null || true

# Configuration automatique des Git hooks locaux
./scripts/setup-git-hooks.sh 2>/dev/null || true

# 11. Intégration Continue (GitHub Actions & GitLab CI adaptées aux projets cibles)
download_file "templates/.github/workflows/ci.yml" ".github/workflows/ci.yml"
download_file "templates/.gitlab-ci.yml" ".gitlab-ci.yml"

# 12. Template de Sécurité des Variables d'Environnement
if [ ! -f ".env.example" ]; then
  download_file "templates/.env.example" ".env.example"
fi

# 13. Configuration Débrayable du Kit & Règles d'Analyse Statique Semgrep
if [ ! -f ".agent/config.yml" ]; then
  download_file ".agent/config.yml" ".agent/config.yml"
fi
if [ ! -f ".semgrep.yml" ]; then
  download_file ".semgrep.yml" ".semgrep.yml"
fi

echo ""
echo -e "${GREEN}${BOLD}Terminé avec succès ! Vos assistants et pipelines CI sont configurés :${RESET}"
echo -e "   - Google Gemini / Antigravity : ${BOLD}GEMINI.md${RESET}"
echo -e "   - GitHub Copilot / Codex      : ${BOLD}.github/copilot-instructions.md${RESET}"
echo -e "   - Agent Universel             : ${BOLD}AGENTS.md${RESET}"
echo -e "   - Cursor IDE                  : ${BOLD}.cursorrules${RESET}"
echo -e "   - Claude / Anthropic          : ${BOLD}CLAUDE.md${RESET}"
echo -e "   - Mémoire Vivante             : ${BOLD}BRAIN.md${RESET}"
echo -e "   - Guides & Protocoles         : ${BOLD}guides/${RESET}"
echo -e "   - Checklists & Stacks         : ${BOLD}checklists/ et stacks/${RESET}"
echo -e "   - Script Anti-Slop IA         : ${BOLD}scripts/audit-slop.py${RESET}"
echo -e "   - Hooks Git Locaux            : ${BOLD}scripts/setup-git-hooks.sh${RESET}"
echo -e "   - Pipeline GitHub Actions     : ${BOLD}.github/workflows/ci.yml${RESET}"
echo -e "   - Pipeline GitLab CI          : ${BOLD}.gitlab-ci.yml${RESET}"
echo -e "   - Template Secrets            : ${BOLD}.env.example${RESET}"
