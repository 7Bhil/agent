#!/usr/bin/env bash
# ==============================================================================
# Script d'installation & Déploiement Sécurisé du Senior Agent Core
# Prend en charge : --dry-run, --force, détection des conflits et sauvegardes .bak
# ==============================================================================

set -e

BOLD="\033[1m"
GREEN="\033[32m"
BLUE="\033[34m"
YELLOW="\033[33m"
RED="\033[31m"
RESET="\033[0m"

DRY_RUN=false
FORCE=false
BACKUP=true

for arg in "$@"; do
  case $arg in
    --dry-run)
      DRY_RUN=true
      shift
      ;;
    --force)
      FORCE=true
      shift
      ;;
    --no-backup)
      BACKUP=false
      shift
      ;;
    -h|--help)
      echo "Usage: ./install.sh [OPTIONS]"
      echo "Options:"
      echo "  --dry-run    Affiche les actions sans modifier le système de fichiers."
      echo "  --force      Écrase les fichiers existants sans confirmation (crée un .bak si backup actif)."
      echo "  --no-backup  Ne crée pas de copie .bak lors du remplacement d'un fichier existant."
      exit 0
      ;;
  esac
done

echo -e "${BLUE}${BOLD}=====================================================${RESET}"
echo -e "${BLUE}${BOLD}    Senior Agent Core - Déploiement Sécurisé        ${RESET}"
if [ "$DRY_RUN" = true ]; then
  echo -e "${YELLOW}${BOLD}    [MODE DRY-RUN ACTIF : Aucune écriture disque]   ${RESET}"
fi
echo -e "${BLUE}${BOLD}=====================================================${RESET}"

REPO_RAW_URL="${AGENT_CORE_URL:-https://raw.githubusercontent.com/7Bhil/agent/main}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" 2>/dev/null && pwd || echo "")"

safe_deploy_file() {
  local source_path="$1"
  local target_path="$2"

  if [ -f "$target_path" ]; then
    if [ "$FORCE" = false ]; then
      echo -e "   [CONSERVÉ] ${YELLOW}${target_path}${RESET} existe déjà (utiliser --force pour écraser)."
      return 0
    else
      if [ "$BACKUP" = true ]; then
        if [ "$DRY_RUN" = true ]; then
          echo -e "   [SIMULATION BACKUP] ${target_path} -> ${target_path}.bak"
        else
          cp "$target_path" "${target_path}.bak"
          echo -e "   [BACKUP CRÉÉ] ${target_path}.bak"
        fi
      fi
    fi
  fi

  if [ "$DRY_RUN" = true ]; then
    echo -e "   [SIMULATION] Déploiement de ${GREEN}${target_path}${RESET}"
    return 0
  fi

  echo -e "   [DÉPLOIEMENT] ${GREEN}${target_path}${RESET}..."
  mkdir -p "$(dirname "$target_path")"

  if [ -n "$SCRIPT_DIR" ] && [ -f "${SCRIPT_DIR}/${source_path}" ] && [ "$SCRIPT_DIR" != "$(pwd)" ]; then
    cp "${SCRIPT_DIR}/${source_path}" "$target_path"
  else
    curl -sSL "${REPO_RAW_URL}/${source_path}" -o "$target_path"
  fi
}

# 1. Règles Universelles du Core & Presets
safe_deploy_file "core/RULES.md" "core/RULES.md"
safe_deploy_file "presets/7bhil.md" "presets/7bhil.md"

# 2. Adapters Multi-Agents
safe_deploy_file "AGENTS.md" "AGENTS.md"
safe_deploy_file "GEMINI.md" "GEMINI.md"
safe_deploy_file "templates/.github/copilot-instructions.md" ".github/copilot-instructions.md"
safe_deploy_file ".cursorrules" ".cursorrules"
safe_deploy_file "CLAUDE.md" "CLAUDE.md"

# 3. Index Mémoire Opérationnel & Mémoire Structurée
safe_deploy_file "BRAIN.md" "BRAIN.md"
safe_deploy_file ".agent/memory/project.md" ".agent/memory/project.md"
safe_deploy_file ".agent/memory/user.md" ".agent/memory/user.md"
safe_deploy_file ".agent/memory/constraints.md" ".agent/memory/constraints.md"
safe_deploy_file ".agent/memory/current-state.md" ".agent/memory/current-state.md"

# 4. Cadre et Direction Artistique (DESIGN.md et DESIGN-SYSTEM.md)
safe_deploy_file "DESIGN.md" "DESIGN.md"
safe_deploy_file "DESIGN-SYSTEM.md" "DESIGN-SYSTEM.md"

# 5. Guides d'Ingénierie Senior
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
  safe_deploy_file "guides/${guide}" "guides/${guide}"
  safe_deploy_file "guides/${guide}" ".agent/guides/${guide}"
done

# 6. Checklists d'Auto-Revue
CHECKLISTS=(
  "01-architecture-et-conception.md:01-architecture.md"
  "02-qualite-et-clean-code.md:02-clean-code.md"
  "03-securite-applicative-et-api.md:03-securite.md"
  "04-conformite-rgpd-et-vie-privee.md:04-rgpd.md"
  "05-tests-et-resilience.md:05-tests.md"
  "06-performance-et-accessibilite.md:06-performance-a11y.md"
  "07-redaction-technique-anti-slop.md:07-redaction-anti-slop.md"
  "08-cycle-de-travail-et-livraison.md:08-cycle-de-travail.md"
)
for entry in "${CHECKLISTS[@]}"; do
  src="${entry%%:*}"
  dest="${entry##*:}"
  safe_deploy_file "checklists/${src}" "checklists/${src}"
  safe_deploy_file "checklists/${src}" ".agent/checklists/${dest}"
done

# 7. Stacks Techniques Ciblées
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
  safe_deploy_file "stacks/${stack}" "stacks/${stack}"
  safe_deploy_file "stacks/${stack}" ".agent/stacks/${stack}"
done

# 8. Outillage Déterministe d'Ingénierie & Anti-Slop
safe_deploy_file "scripts/audit-slop.py" "scripts/audit-slop.py"
safe_deploy_file "scripts/setup-git-hooks.sh" "scripts/setup-git-hooks.sh"
safe_deploy_file "scripts/test-kit.sh" "scripts/test-kit.sh"
safe_deploy_file "scripts/build-adapters.py" "scripts/build-adapters.py"
safe_deploy_file "scripts/run-evals.py" "scripts/run-evals.py"

# 9. Bancs d'Évaluation Déterministe (Agent Evals)
safe_deploy_file "tests/evals/agent-scenarios.md" "tests/evals/agent-scenarios.md"
safe_deploy_file "tests/evals/security-scenarios.md" "tests/evals/security-scenarios.md"
safe_deploy_file "tests/evals/fintech-scenarios.md" "tests/evals/fintech-scenarios.md"

if [ "$DRY_RUN" = false ]; then
  chmod +x scripts/*.py scripts/*.sh 2>/dev/null || true
  ./scripts/setup-git-hooks.sh 2>/dev/null || true
fi

# 9. Intégration Continue (GitHub Actions & GitLab CI adaptées au client)
safe_deploy_file "templates/.github/workflows/ci.yml" ".github/workflows/ci.yml"
safe_deploy_file "templates/.gitlab-ci.yml" ".gitlab-ci.yml"

# 10. Gabarit Secrets, Config Débrayable & Semgrep
safe_deploy_file "templates/.env.example" ".env.example"
safe_deploy_file ".agent/config.yml" ".agent/config.yml"
safe_deploy_file ".semgrep.yml" ".semgrep.yml"

echo ""
if [ "$DRY_RUN" = true ]; then
  echo -e "${YELLOW}${BOLD}Simulation d'installation achevée. Aucun fichier n'a été altéré.${RESET}"
else
  echo -e "${GREEN}${BOLD}Installation terminée avec succès ! Environnement configuré et sécurisé.${RESET}"
fi
