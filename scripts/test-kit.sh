#!/usr/bin/env bash
# ==============================================================================
# Suite de Tests Déterministes d'Intégrité du Senior Agent Core
# Valide l'absence de régressions, la structure et la parité du kit.
# ==============================================================================

set -e

BOLD="\033[1m"
GREEN="\033[32m"
RED="\033[31m"
RESET="\033[0m"

echo -e "${BOLD}Lancement des tests d'intégrité du Senior Agent Core...${RESET}"

FAILED=0

check_test() {
  local description="$1"
  shift
  echo -n " - Test : $description ... "
  if "$@"; then
    echo -e "${GREEN}SUCCÈS${RESET}"
  else
    echo -e "${RED}ÉCHEC${RESET}"
    FAILED=$((FAILED + 1))
  fi
}

# 1. Test de Parité Templates vs Racine
test_template_parity() {
  cmp GEMINI.md templates/GEMINI.md && \
  cmp CLAUDE.md templates/CLAUDE.md && \
  cmp .cursorrules templates/.cursorrules
}
check_test "Parité stricte racine vs templates" test_template_parity

# 2. Test Anti-Slop & Sobriété Rédactionnelle
test_anti_slop() {
  python3 scripts/audit-slop.py README.md DESIGN.md CONTRIBUTING.md \
    guides/*.md checklists/*.md stacks/*.md docs/decisions/*.md tests/evals/*.md >/dev/null 2>&1
}
check_test "Audit anti-slop sans déchet textuel" test_anti_slop

# 3. Test de Pureté Unicode (Zéro Émoji dans les fichiers critiques)
test_zero_emoji() {
  python3 -c "
import sys, glob

files = glob.glob('guides/*.md') + glob.glob('checklists/*.md') + glob.glob('stacks/*.md') + ['AGENTS.md', 'GEMINI.md', 'CLAUDE.md', 'DESIGN.md', 'CONTRIBUTING.md']
has_emoji = False

for f in files:
    with open(f, 'r', encoding='utf-8') as fp:
        for num, line in enumerate(fp, 1):
            for ch in line:
                cp = ord(ch)
                if (0x1F600 <= cp <= 0x1F64F or 0x1F300 <= cp <= 0x1F5FF or
                    0x1F680 <= cp <= 0x1F6FF or 0x1F700 <= cp <= 0x1F77F or
                    0x1F780 <= cp <= 0x1F7FF or 0x1F800 <= cp <= 0x1F8FF or
                    0x1F900 <= cp <= 0x1F9FF or 0x1FA00 <= cp <= 0x1FAFF or
                    0x2600 <= cp <= 0x26FF or 0x2700 <= cp <= 0x27BF):
                    print(f'Emoji detecte dans {f}:{num} -> {ch}')
                    has_emoji = True

sys.exit(1 if has_emoji else 0)
"
}
check_test "Absence stricte d'émojis (zéro déchet visuel)" test_zero_emoji

# 4. Test d'Intégrité de install.sh (Syntaxe et déploiement simulé)
test_install_script() {
  bash -n install.sh && \
  mkdir -p /tmp/agent-test-run && \
  cd /tmp/agent-test-run && \
  "${OLDPWD}/install.sh" >/dev/null 2>&1 && \
  test -f BRAIN.md && \
  test -f DESIGN.md && \
  test -f AGENTS.md && \
  test -d guides && \
  test -d checklists && \
  test -d stacks && \
  test -f .semgrep.yml && \
  test -f .agent/config.yml && \
  cd - >/dev/null && \
  rm -rf /tmp/agent-test-run
}
check_test "Déploiement complet autonome via install.sh" test_install_script

# 5. Test de Numérotation Séquentielle des ADR
test_adr_sequencing() {
  python3 -c "
import glob, sys, re
adrs = sorted(glob.glob('docs/decisions/[0-9][0-9][0-9][0-9]-*.md'))
if not adrs:
    sys.exit(1)
expected = 1
for adr in adrs:
    m = re.search(r'([0-9]{4})-', adr)
    if not m or int(m.group(1)) != expected:
        sys.exit(1)
    expected += 1
sys.exit(0)
"
}
check_test "Numérotation séquentielle stricte des ADR" test_adr_sequencing

echo "---------------------------------------------------------"
if [ $FAILED -eq 0 ]; then
  echo -e "${GREEN}${BOLD}Tous les tests d'intégrité sont validés au vert.${RESET}"
  exit 0
else
  echo -e "${RED}${BOLD}$FAILED test(s) ont échoué.${RESET}"
  exit 1
fi
