#!/usr/bin/env python3
"""Audit déterministe de style technique et détection anti-slop IA.

Outil autonome sans dépendance externe (Python 3 stdlib uniquement).
Analyse les fichiers Markdown et texte pour détecter les tics d'écriture,
formules creuses, affaiblissements de propos (hedging) et remplissages typiques
des textes générés par IA en français et en anglais.

Usage :
    python3 scripts/audit-slop.py fichier.md [autres_fichiers...]
    python3 scripts/audit-slop.py --selftest
    python3 scripts/audit-slop.py --json fichier.md
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import NamedTuple

__version__ = "1.0.0"


class SlopHit(NamedTuple):
    file_path: str
    line_number: int
    rule_id: str
    rule_name: str
    matched_text: str
    line_content: str


# Règles d'audit (ID, Nom explicite, Expression régulière compilée)
_RULES = [
    # --- Affaiblissements et précautions oratoires inutiles (Hedging) ---
    (
        "hedge_fr",
        "Précautions oratoires ou remplissage creux (FR)",
        re.compile(
            r"\b(il convient de noter|il est (important|essentiel|crucial) de (noter|souligner|rappeler)|"
            r"force est de constater|il va sans dire que|au bout du compte|dans une certaine mesure)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "hedge_en",
        "Empty hedging stem (EN)",
        re.compile(
            r"\b((it'?s|it is) (worth noting|important to (note|remember|understand))|"
            r"that said|needless to say|as we all know|at the end of the day)\b",
            re.IGNORECASE,
        ),
    ),
    # --- Enjeux artificiels et emphase dramatique (Manufactured stakes) ---
    (
        "stakes_fr",
        "Enjeux artificiels ou emphase d'époque (FR)",
        re.compile(
            r"\b(dans le monde d'aujourd'hui|dans un monde en (constante|perpétuelle) évolution|"
            r"à l'ère du numérique|aujourd'hui plus que jamais|"
            r"les enjeux n'ont jamais été aussi (élevés|cruciaux))\b",
            re.IGNORECASE,
        ),
    ),
    (
        "stakes_en",
        "Manufactured stakes (EN)",
        re.compile(
            r"\b(in today'?s (fast-paced |digital |modern )?(world|landscape|era)|"
            r"now more than ever|more important than ever|"
            r"the stakes have never been higher)\b",
            re.IGNORECASE,
        ),
    ),
    # --- Fausses confidences et candeur jouée (Performed candor) ---
    (
        "candor_fr",
        "Fausses confidences ou connivence artificielle (FR)",
        re.compile(
            r"\b(soyons honnêtes|soyons réalistes|la vérité est que|"
            r"pour être (tout à fait )?franc|voilà le truc)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "candor_en",
        "Performed candor (EN)",
        re.compile(
            r"\b(let'?s be honest|let'?s be real|here'?s the thing|"
            r"truth be told|i'?ll be honest)\b",
            re.IGNORECASE,
        ),
    ),
    # --- Quantificateurs flous et gonflés (Weasel quantifiers) ---
    (
        "weasel_fr",
        "Quantificateur flou ou enflure verbale (FR)",
        re.compile(
            r"\b(une pléthore de|une multitude de|un large éventail de|d'innombrables)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "weasel_en",
        "Weasel quantifier (EN)",
        re.compile(
            r"\b(a (wide|broad) (variety|range|array) of|a plethora of|a myriad of|"
            r"a host of|countless)\b",
            re.IGNORECASE,
        ),
    ),
    # --- Transitions mécaniques redondantes (Dead transitions) ---
    (
        "transition_fr",
        "Transition mécanique d'en-tête (FR)",
        re.compile(
            r"(?m)^\s*(de plus|en outre|par ailleurs|qui plus est)\b\s*,",
            re.IGNORECASE,
        ),
    ),
    (
        "transition_en",
        "Dead transition opener (EN)",
        re.compile(
            r"(?m)^\s*(moreover|furthermore|in addition|additionally)\b\s*,",
            re.IGNORECASE,
        ),
    ),
    # --- Faux contrastes négatifs / Parallélismes artificiels ---
    (
        "negparallel_fr",
        "Faux contraste binaire (FR)",
        re.compile(
            r"\b(ce n'est pas (seulement|simplement)\b.*\bc'est\b|"
            r"il ne s'agit pas (seulement|simplement)\b.*\bil s'agit de\b)",
            re.IGNORECASE,
        ),
    ),
    (
        "negparallel_en",
        "Negative-parallel cadence (EN)",
        re.compile(
            r"\b(it'?s not (just|merely|only)\b.*\bit'?s\b|"
            r"this isn'?t (just )?about\b.*\bit'?s about\b)",
            re.IGNORECASE,
        ),
    ),
    # --- Tics de vocabulaire et clôtures IA récurrentes ---
    (
        "cliche_fr",
        "Cliché ou clôture IA stéréotypée (FR)",
        re.compile(
            r"\b(plongeons dans|un véritable témoignage de|"
            r"naviguer dans la complexité|en conclusion\s*,)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "cliche_en",
        "LLM filler and faux kickers (EN)",
        re.compile(
            r"\b(delve into|delving into|a testament to|"
            r"in the realm of|navigating the intricacies|in conclusion\s*,)\b",
            re.IGNORECASE,
        ),
    ),
    # --- Formules passives lourdes et tournures évasives ---
    (
        "passive_fr",
        "Formule passive lourde ou déresponsabilisante (FR)",
        re.compile(
            r"\b(il a été décidé que|il doit être gardé à l'esprit que|"
            r"il est généralement admis que|il est préconisé d'utiliser)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "passive_en",
        "Heavy passive or impersonal evasion (EN)",
        re.compile(
            r"\b(it has been determined that|it should be noted that|"
            r"it is widely acknowledged that|it is recommended to be used)\b",
            re.IGNORECASE,
        ),
    ),
    # --- Répétitions et échos mécaniques de l'IA ---
    (
        "repetition_fr",
        "Répétition mécanique ou écho IA (FR)",
        re.compile(
            r"\b(non seulement cela permet de\b.*\bmais cela assure également\b|"
            r"en d['’]autres termes\b\s*,?|comme mentionné précédemment\b\s*,?)",
            re.IGNORECASE,
        ),
    ),
    (
        "repetition_en",
        "Mechanical repetition or echo tell (EN)",
        re.compile(
            r"\b(in other words\b\s*,?|as previously mentioned\b\s*,?|"
            r"not only does this allow\b.*\bbut it also ensures\b)",
            re.IGNORECASE,
        ),
    ),
]


def strip_code_blocks(text: str) -> list[tuple[int, str]]:
    """Retourne la liste des lignes (1-indexées, contenu) en ignorant les blocs de code et le code inline."""
    lines = text.splitlines()
    in_code_block = False
    filtered_lines: list[tuple[int, str]] = []

    for index, line in enumerate(lines, start=1):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue

        if not in_code_block:
            # Éliminer le code inline `...` pour ne pas lever de faux positifs sur les citations de code/règles
            clean_line = re.sub(r"`[^`]*`", lambda m: " " * len(m.group(0)), line)
            filtered_lines.append((index, clean_line))

    return filtered_lines


def audit_text(text: str, file_path: str = "<stdin>") -> list[SlopHit]:
    """Analyse un texte et retourne les correspondances trouvées hors blocs de code."""
    hits: list[SlopHit] = []
    lines = strip_code_blocks(text)

    for line_num, line_str in lines:
        for rule_id, rule_name, pattern in _RULES:
            for match in pattern.finditer(line_str):
                hits.append(
                    SlopHit(
                        file_path=file_path,
                        line_number=line_num,
                        rule_id=rule_id,
                        rule_name=rule_name,
                        matched_text=match.group(0),
                        line_content=line_str.strip(),
                    )
                )

    return hits


def audit_files(paths: list[Path]) -> list[SlopHit]:
    """Exécute l'audit sur l'ensemble des fichiers spécifiés."""
    all_hits: list[SlopHit] = []
    for path in paths:
        if not path.is_file():
            continue
        try:
            content = path.read_text(encoding="utf-8", errors="replace")
            hits = audit_text(content, str(path))
            all_hits.extend(hits)
        except Exception as err:
            print(f"Erreur lors de la lecture de {path} : {err}", file=sys.stderr)

    return all_hits


def run_selftest() -> bool:
    """Exécute les tests de détection unitaires internes."""
    samples = [
        ("Il convient de noter que le caching est actif.", "hedge_fr"),
        ("Dans le monde d'aujourd'hui, la sécurité est clé.", "stakes_fr"),
        ("Soyons honnêtes, cette fonction est lente.", "candor_fr"),
        ("Le système offre une pléthore de fonctionnalités.", "weasel_fr"),
        ("It's worth noting that Redis is required.", "hedge_en"),
        ("In today's fast-paced world, microservices rule.", "stakes_en"),
        ("Let's be honest, tests are necessary.", "candor_en"),
        ("There is a wide variety of tools.", "weasel_en"),
        ("It's not just a cache, it's a proxy.", "negparallel_en"),
        ("Let's delve into the architecture.", "cliche_en"),
        ("Il a été décidé que la base serait migrée.", "passive_fr"),
        ("It has been determined that the server failed.", "passive_en"),
        ("En d'autres termes, l'architecture est robuste.", "repetition_fr"),
        ("In other words, the architecture is decoupled.", "repetition_en"),
    ]

    for text, expected_rule in samples:
        hits = audit_text(text)
        matched_rules = [h.rule_id for h in hits]
        if expected_rule not in matched_rules:
            print(f"ÉCHEC SELFTEST : '{text}' attendait la règle '{expected_rule}', trouvé : {matched_rules}")
            return False

    # Vérification que les blocs de code markdown sont bien ignorés
    code_sample = "```bash\n# Il convient de noter\necho 'delve into'\n```\nTexte propre."
    hits_code = audit_text(code_sample)
    if len(hits_code) > 0:
        print(f"ÉCHEC SELFTEST : Du code dans un bloc markdown a été analysé : {hits_code}")
        return False

    print("Selftest réussi : l'ensemble des règles et filtres fonctionnent correctement.")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit déterministe anti-slop IA pour prose technique sobre."
    )
    parser.add_argument("files", nargs="*", help="Fichiers ou dossiers à analyser")
    parser.add_argument(
        "--json", action="store_true", help="Sortie au format JSON pour pipelines CI"
    )
    parser.add_argument(
        "--selftest", action="store_true", help="Exécuter les tests internes"
    )
    args = parser.parse_args()

    if args.selftest:
        success = run_selftest()
        return 0 if success else 1

    target_paths: list[Path] = []
    if args.files:
        for f in args.files:
            p = Path(f)
            if p.is_dir():
                target_paths.extend(p.glob("**/*.md"))
            elif p.is_file():
                target_paths.append(p)
    else:
        # Lecture depuis stdin
        content = sys.stdin.read()
        hits = audit_text(content, "<stdin>")
        if args.json:
            print(json.dumps([h._asdict() for h in hits], indent=2))
        else:
            for hit in hits:
                print(f"[Ligne {hit.line_number}] [{hit.rule_name}] Trouvé : '{hit.matched_text}'")
                print(f"   > {hit.line_content}\n")
        return 1 if hits else 0

    hits = audit_files(target_paths)

    if args.json:
        print(json.dumps([h._asdict() for h in hits], indent=2, ensure_ascii=False))
    else:
        if not hits:
            print("Audit anti-slop terminé : aucun tic d'écriture détecté.")
            return 0

        print(f"Audit anti-slop : {len(hits)} formulation(s) suspecte(s) détectée(s) :\n")
        for hit in hits:
            print(f"- {hit.file_path}:{hit.line_number} [{hit.rule_name}]")
            print(f"  Extrait  : \"{hit.matched_text}\"")
            print(f"  Contexte : {hit.line_content}\n")

    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
