#!/usr/bin/env bash
# ==============================================================================
# Script d'installation automatique des Git Hooks locaux (zéro dépendance externe)
# Vérifie les messages de commit (format français, zéro émoji) et lance l'audit anti-slop
# ==============================================================================

set -e

HOOKS_DIR=".git/hooks"

if [ ! -d ".git" ]; then
  echo "Erreur : ce script doit être exécuté à la racine d'un dépôt Git."
  exit 1
fi

mkdir -p "$HOOKS_DIR"

# 1. Hook commit-msg : Contrôle de la convention de commit en français et zéro émoji
cat << 'EOF' > "$HOOKS_DIR/commit-msg"
#!/usr/bin/env bash
set -e

COMMIT_MSG_FILE="$1"
FIRST_LINE=$(head -n 1 "$COMMIT_MSG_FILE")

# Vérification du préfixe conventionnel
VALID_PREFIX="^(feat|fix|docs|refactor|test|style|chore|perf|ci)(\([a-z0-9_-]+\))?: .+"

if ! [[ "$FIRST_LINE" =~ $VALID_PREFIX ]]; then
  echo "ERREUR COMMIT: Le message de commit ne respecte pas les conventions du projet."
  echo "Format attendu: <type>(<scope>): <description en français>"
  echo "Types autorisés: feat, fix, docs, refactor, test, style, chore, perf, ci"
  echo "Exemple: feat(auth): ajout du contrôle de session avec jeton JWT"
  exit 1
fi

# Vérification de l'absence d'émojis dans le message de commit
python3 -c "
import sys

msg = open('$COMMIT_MSG_FILE', 'r', encoding='utf-8', errors='ignore').read()
for char in msg:
    cp = ord(char)
    if (0x1F600 <= cp <= 0x1F64F or
        0x1F300 <= cp <= 0x1F5FF or
        0x1F680 <= cp <= 0x1F6FF or
        0x1F700 <= cp <= 0x1F77F or
        0x1F780 <= cp <= 0x1F7FF or
        0x1F800 <= cp <= 0x1F8FF or
        0x1F900 <= cp <= 0x1F9FF or
        0x1FA00 <= cp <= 0x1FAFF or
        0x2600 <= cp <= 0x26FF or
        0x2700 <= cp <= 0x27BF):
        print('ERREUR COMMIT: Les émojis sont formellement interdits dans les messages de commit.')
        sys.exit(1)
"
EOF

chmod +x "$HOOKS_DIR/commit-msg"

# 2. Hook pre-commit : Audit anti-slop et détection de secrets gitleaks
cat << 'EOF' > "$HOOKS_DIR/pre-commit"
#!/usr/bin/env bash
set -e

# Détection de secrets via gitleaks si installé localement
if command -v gitleaks >/dev/null 2>&1; then
  gitleaks protect --staged --verbose --redact
fi

STAGED_MD_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.md$' || true)

if [ -n "$STAGED_MD_FILES" ] && [ -f "scripts/audit-slop.py" ]; then
  python3 scripts/audit-slop.py $STAGED_MD_FILES
fi
EOF

chmod +x "$HOOKS_DIR/pre-commit"

echo "Git hooks installés avec succès : commit-msg et pre-commit sont actifs."
