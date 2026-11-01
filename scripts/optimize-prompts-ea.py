#!/usr/bin/env python3
"""Moteur évolutionnaire d'optimisation de prompts et d'instructions système (Prompt Breeder).

Applique un algorithme génétique pour optimiser la concision, la densité sémantique
et le respect des limites de budget de contexte sur les templates d'instructions.

Usage:
    python3 scripts/optimize-prompts-ea.py [--generations N] [--pop-size M] [--seed S]
"""

from __future__ import annotations

import argparse
import random
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple

ROOT_DIR = Path(__file__).resolve().parent.parent

# Mutations textuelles contrôlées pour optimiser les prompts
MUTATIONS = [
    # Suppression de remplissages et affaiblissements
    lambda text, rng: re.sub(r"\b(il convient de noter que|force est de constater que|il va sans dire que)\s*", "", text, flags=re.IGNORECASE),
    # Remplacement de formulations verbeuses par des formulations directes
    lambda text, rng: text.replace("est dans l'obligation de", "doit").replace("a la responsabilité de", "doit"),
    # Nettoyage des espaces multiples
    lambda text, rng: re.sub(r" +", " ", text),
    # Permutation de directives indépendantes
    lambda text, rng: _permute_bullet_points(text, rng),
    # Compression de listes à puces
    lambda text, rng: text.replace("\n\n- ", "\n- "),
]


def _permute_bullet_points(text: str, rng: random.Random) -> str:
    lines = text.split("\n")
    bullet_indices = [i for i, line in enumerate(lines) if line.strip().startswith("- ")]
    if len(bullet_indices) >= 2:
        i1, i2 = rng.sample(bullet_indices, 2)
        lines[i1], lines[i2] = lines[i2], lines[i1]
    return "\n".join(lines)


@dataclass
class PromptCandidate:
    content: str
    fitness: float = 0.0


def evaluate_prompt_fitness(candidate: PromptCandidate, target_rules: List[str]) -> float:
    """Évalue un prompt selon :
    1. Présence de tous les mots-clés/concepts obligatoires (exhaustivité).
    2. Concision et économie de tokens (brièveté).
    3. Absence totale de slop / hedging.
    """
    text = candidate.content
    score = 0.0

    # 1. Vérification de la présence des règles cibles
    matched_rules = 0
    for rule in target_rules:
        if re.search(r"\b" + re.escape(rule) + r"\b", text, re.IGNORECASE):
            matched_rules += 1

    coverage_ratio = matched_rules / max(1, len(target_rules))
    score += coverage_ratio * 70.0  # 70% du score sur la complétude

    # 2. Absence de slop (pénalité sévère en cas de présence)
    slop_pattern = re.compile(
        r"\b(il convient de noter|il est (important|essentiel|crucial) de (noter|souligner|rappeler)|"
        r"force est de constater|il va sans dire que|au bout du compte|dans une certaine mesure)\b",
        re.IGNORECASE,
    )
    if slop_pattern.search(text):
        score -= 40.0

    # 3. Économie de tokens (longueur idéale bornée)
    char_count = len(text.strip())
    if 100 <= char_count <= 800:
        # Bonus pour la compacité sans perte
        score += max(0.0, 30.0 - (char_count / 800.0) * 15.0)
    else:
        score += 5.0

    candidate.fitness = max(0.0, score)
    return candidate.fitness


def crossover_prompts(p1: PromptCandidate, p2: PromptCandidate, rng: random.Random) -> Tuple[PromptCandidate, PromptCandidate]:
    """Croisement de sections ou lignes de prompts."""
    lines1 = [line for line in p1.content.split("\n") if line.strip()]
    lines2 = [line for line in p2.content.split("\n") if line.strip()]

    if len(lines1) > 2 and len(lines2) > 2:
        cut1 = rng.randint(1, len(lines1) - 1)
        cut2 = rng.randint(1, len(lines2) - 1)
        c1 = "\n".join(lines1[:cut1] + lines2[cut2:])
        c2 = "\n".join(lines2[:cut2] + lines1[cut1:])
    else:
        c1, c2 = p1.content, p2.content

    return PromptCandidate(content=c1), PromptCandidate(content=c2)


def mutate_prompt(candidate: PromptCandidate, rng: random.Random, rate: float = 0.6) -> PromptCandidate:
    """Mutation ciblée d'un prompt."""
    if rng.random() > rate:
        return PromptCandidate(content=candidate.content)

    strategy = rng.choice(MUTATIONS)
    mutated_content = strategy(candidate.content, rng)
    return PromptCandidate(content=mutated_content)


def optimize_prompt(
    initial_text: str,
    target_rules: List[str],
    generations: int = 10,
    pop_size: int = 15,
    seed: int = 42,
    verbose: bool = False,
) -> PromptCandidate:
    """Exécute l'algorithme génétique d'optimisation de prompt."""
    rng = random.Random(seed)

    population = [PromptCandidate(content=initial_text)]
    # Génération d'individus initiaux variés par mutation
    for _ in range(pop_size - 1):
        ind = mutate_prompt(PromptCandidate(content=initial_text), rng, rate=1.0)
        population.append(ind)

    for ind in population:
        evaluate_prompt_fitness(ind, target_rules)

    for gen in range(1, generations + 1):
        population.sort(key=lambda x: x.fitness, reverse=True)
        new_pop = [
            PromptCandidate(content=population[0].content, fitness=population[0].fitness)
        ]

        while len(new_pop) < pop_size:
            # Tournoi
            cand1, cand2 = rng.sample(population, 2)
            p1 = cand1 if cand1.fitness >= cand2.fitness else cand2
            cand3, cand4 = rng.sample(population, 2)
            p2 = cand3 if cand3.fitness >= cand4.fitness else cand4

            c1, c2 = crossover_prompts(p1, p2, rng)
            c1 = mutate_prompt(c1, rng)
            c2 = mutate_prompt(c2, rng)

            evaluate_prompt_fitness(c1, target_rules)
            evaluate_prompt_fitness(c2, target_rules)

            new_pop.append(c1)
            if len(new_pop) < pop_size:
                new_pop.append(c2)

        population = new_pop

        if verbose:
            best = max(population, key=lambda x: x.fitness)
            print(f"Génération {gen:2d}/{generations} : Meilleure fitness = {best.fitness:.1f}")

    population.sort(key=lambda x: x.fitness, reverse=True)
    return population[0]


def main() -> int:
    parser = argparse.ArgumentParser(description="Optimiseur évolutionnaire de prompts et règles système.")
    parser.add_argument("--generations", type=int, default=10, help="Nombre de générations (défaut: 10)")
    parser.add_argument("--pop-size", type=int, default=15, help="Taille de la population (défaut: 15)")
    parser.add_argument("--seed", type=int, default=42, help="Graine aléatoire déterministe (défaut: 42)")
    parser.add_argument("--verbose", action="store_true", help="Afficher les itérations")
    parser.add_argument("--selftest", action="store_true", help="Auto-test du moteur")
    args = parser.parse_args()

    sample_input = (
        "Il convient de noter que l'agent a la responsabilité de valider les entrées. "
        "Force est de constater qu'il est crucial de respecter le typage strict. "
        "L'agent est dans l'obligation de refuser le type any. "
        "Il va sans dire que la sécurité par défaut doit être assurée."
    )
    target_rules = ["valider", "typage strict", "any", "sécurité"]

    if args.selftest:
        best = optimize_prompt(sample_input, target_rules, generations=5, pop_size=10, seed=42)
        assert best.fitness > 0
        print("Self-test de l'optimiseur évolutionnaire de prompts : SUCCÈS")
        return 0

    best = optimize_prompt(
        sample_input,
        target_rules,
        generations=args.generations,
        pop_size=args.pop_size,
        seed=args.seed,
        verbose=args.verbose,
    )

    print(f"\nRésultat de l'optimisation (Fitness: {best.fitness:.1f}) :")
    print("-" * 50)
    print(best.content)
    print("-" * 50)
    return 0


if __name__ == "__main__":
    sys.exit(main())
