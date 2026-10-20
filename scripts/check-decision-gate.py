#!/usr/bin/env python3
"""
Garde-fou déterministe d'arbitrage architectural (Decision Gate).
Vérifie si les modifications du dépôt (staged ou diff avec HEAD) touchent des zones
critiques sans qu'un ADR ne soit ajouté ou mis à jour dans docs/decisions/.
Usage:
    python3 scripts/check-decision-gate.py [--staged]
"""

import subprocess
import sys
import os

# Fichiers et motifs déclenchant obligatoirement un arbitrage ADR
SENSITIVE_PATTERNS = [
    # Dépendances structurantes
    "package.json",
    "requirements.txt",
    "Cargo.toml",
    "go.mod",
    "composer.json",
    # Modélisation et persistance
    "schema.prisma",
    "drizzle.config",
    "migrations/",
    "alembic/",
    # Périmètres critiques sécurité et paiement
    "/auth/",
    "/payment/",
    "/webhook/",
    "security-handbook",
]

def get_changed_files(staged_only: bool = False) -> list[str]:
    cmd = ["git", "diff", "--name-only"]
    if staged_only:
        cmd.append("--cached")
    else:
        cmd.append("HEAD")

    try:
        output = subprocess.check_output(cmd, stderr=subprocess.DEVNULL, text=True)
        return [line.strip() for line in output.splitlines() if line.strip()]
    except subprocess.CalledProcessError:
        return []

def main():
    staged = "--staged" in sys.argv
    changed_files = get_changed_files(staged_only=staged)

    if not changed_files:
        # Aucun fichier modifié
        sys.exit(0)

    # Vérification de la présence d'un ADR dans le lot modifié
    has_adr = any(f.startswith("docs/decisions/") and f.endswith(".md") and not f.endswith("README.md") for f in changed_files)

    # Détection des zones critiques touchées
    triggered_rules = []
    for file_path in changed_files:
        for pattern in SENSITIVE_PATTERNS:
            if pattern in file_path:
                triggered_rules.append((file_path, pattern))

    if triggered_rules and not has_adr:
        print("Erreur [Decision Gate] : Modifications architecturales ou sensibles détectées sans ADR.", file=sys.stderr)
        print("Fichiers concernés :", file=sys.stderr)
        for f, pat in triggered_rules:
            print(f"  - {f} (motif sensible : {pat})", file=sys.stderr)
        print("\nProtocole requis :", file=sys.stderr)
        print("1. Convoquer le conseil d'arbitrage (guides/decision-council.md).", file=sys.stderr)
        print("2. Documenter la décision dans un nouvel ADR sous docs/decisions/XXXX-*.md.", file=sys.stderr)
        sys.exit(1)

    print("Decision Gate : Validation réussie (aucune modification critique orpheline d'ADR).")
    sys.exit(0)

if __name__ == "__main__":
    main()
