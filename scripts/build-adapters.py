#!/usr/bin/env python3
"""
Générateur déterministe d'instructions pour agents IA à partir de core/RULES.md et presets/.
Génère ou met à jour AGENTS.md, GEMINI.md, CLAUDE.md, .cursorrules et .github/copilot-instructions.md.
Usage:
    python3 scripts/build-adapters.py [--check]
"""

import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
CORE_PATH = os.path.join(ROOT_DIR, "core", "RULES.md")
PRESET_PATH = os.path.join(ROOT_DIR, "presets", "7bhil.md")

ADAPTER_TARGETS = {
    "AGENTS.md": "Standard Universel (Agents Autonomes, Windsurf, Cline, Aider)",
    "GEMINI.md": "Google Gemini & Antigravity IDE",
    "CLAUDE.md": "Anthropic Claude Desktop & CLI",
    ".cursorrules": "Cursor IDE Rule Specification",
    "templates/.github/copilot-instructions.md": "GitHub Copilot & OpenAI Codex",
}

HEADER_TEMPLATE = """<!--
  FICHIER GÉNÉRÉ AUTOMATIQUEMENT VIA scripts/build-adapters.py
  Source unique de vérité : core/RULES.md et presets/7bhil.md
  Ne modifiez pas ce fichier directement.
-->
"""

def read_file(path: str) -> str:
    if not os.path.isfile(path):
        print(f"Erreur: Fichier introuvable: {path}", file=sys.stderr)
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()

def build_content(target_name: str, core_text: str, preset_text: str) -> str:
    target_info = ADAPTER_TARGETS.get(target_name, target_name)
    content = [
        HEADER_TEMPLATE,
        f"# Configuration de l'Agent : {target_info}\n",
        "## Invariants du Core (Règles Universelles)",
        core_text,
        "\n---",
        "## Préférences & Conventions Locales",
        preset_text,
        ""
    ]
    return "\n".join(content)

def main():
    check_mode = "--check" in sys.argv
    core_text = read_file(CORE_PATH)
    preset_text = read_file(PRESET_PATH)

    has_diff = False

    for rel_path in ADAPTER_TARGETS:
        full_path = os.path.join(ROOT_DIR, rel_path)
        expected_content = build_content(rel_path, core_text, preset_text)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        if check_mode:
            if not os.path.isfile(full_path):
                print(f"[DIFF] {rel_path} est manquant.")
                has_diff = True
            else:
                with open(full_path, "r", encoding="utf-8") as f:
                    current_content = f.read()
                if current_content != expected_content:
                    print(f"[DIFF] {rel_path} n'est pas synchronisé avec le Core.")
                    has_diff = True
        else:
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(expected_content)
            # Synchronisation miroir dans templates/ si applicable
            if not rel_path.startswith("templates/"):
                tpl_path = os.path.join(ROOT_DIR, "templates", rel_path)
                os.makedirs(os.path.dirname(tpl_path), exist_ok=True)
                with open(tpl_path, "w", encoding="utf-8") as f:
                    f.write(expected_content)
            print(f"Génération validée : {rel_path}")

    if check_mode:
        if has_diff:
            print("Erreur: Les fichiers d'adapters sont désynchronisés. Exécutez: python3 scripts/build-adapters.py", file=sys.stderr)
            sys.exit(1)
        else:
            print("Succès: Tous les fichiers d'adapters sont rigoureusement synchronisés avec le Core.")
            sys.exit(0)

if __name__ == "__main__":
    main()
