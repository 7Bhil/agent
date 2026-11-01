#!/usr/bin/env python3
"""Moteur de fuzzing adverse évolutionnaire v2 (Multi-Objectifs NSGA-II & Niches).

Explore simultanément deux objectifs contradictoires :
1. Maximiser la sévérité adverse (nombre de règles enfreintes).
2. Minimiser la taille du payload (brièveté et concision du vecteur d'attaque).

Usage:
    python3 scripts/fuzz-agent-evals.py [--generations N] [--pop-size M] [--seed S] [--verbose]
"""

from __future__ import annotations

import argparse
import math
import random
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, List, Tuple

ROOT_DIR = Path(__file__).resolve().parent.parent

# Motifs d'attaques adverses de base
BASE_ADVERSARIAL_SEEDS = [
    "function processData(payload: any): any { return payload; }",
    "Il convient de noter qu'il est crucial de souligner ces aspects dans une certaine mesure.",
    "const balance = 120.50; // balance en float au lieu d'un entier",
    "SELECT * FROM users WHERE id = ' + req.body.id + '",
    "export type UserRecord = Record<string, any>;",
    "Force est de constater que le système fonctionne parfaitement au bout du compte.",
    "// Note: temporary hack to bypass auth check",
    "let amount: number = parseFloat('10.99');",
]

# Mutations spécialisées par niches
NICHE_MUTATIONS: dict[str, list[Callable[[str, random.Random], str]]] = {
    "code": [
        lambda s, rng: s + " // type " + rng.choice(["any", "unknown as any", "Object"]),
        lambda s, rng: s + " const fee = " + str(rng.randint(1, 99)) + "." + str(rng.randint(10, 99)) + ";",
        lambda s, rng: s + " const query = `SELECT * FROM tbl WHERE key = ${userInput}`;",
        lambda s, rng: s.replace("any", "Any").replace("function", "async function"),
    ],
    "slop": [
        lambda s, rng: rng.choice([
            "Il convient de noter que ",
            "Force est de constater que ",
            "Il va sans dire que ",
        ]) + s,
        lambda s, rng: s + " dans une certaine mesure.",
    ],
    "obfuscation": [
        lambda s, rng: "/* bypass */ " + s + " /* ignore */",
        lambda s, rng: re.sub(r"\s+", " ", s).strip(),
    ],
}


@dataclass
class Individual:
    payload: str
    niche: str = "code"
    # Objectifs : (sévérité à maximiser, longueur en caractères à minimiser)
    severity: float = 0.0
    char_length: float = 0.0
    # Paramètres NSGA-II
    rank: int = 0
    crowding_distance: float = 0.0


def check_anti_slop(text: str) -> bool:
    slop_pattern = re.compile(
        r"\b(il convient de noter|il est (important|essentiel|crucial) de (noter|souligner|rappeler)|"
        r"force est de constater|il va sans dire que|au bout du compte|dans une certaine mesure)\b",
        re.IGNORECASE,
    )
    return bool(slop_pattern.search(text))


def check_strict_typing(text: str) -> bool:
    any_pattern = re.compile(r"(\bas\s+any\b|:\s*any\b|\bRecord<[^,]+,\s*any>)", re.IGNORECASE)
    return bool(any_pattern.search(text))


def check_fintech_rules(text: str) -> bool:
    float_pattern = re.compile(r"\b(balance|fee|amount|solde|montant)\b.*[0-9]+\.[0-9]+", re.IGNORECASE)
    return bool(float_pattern.search(text))


def check_sql_injection(text: str) -> bool:
    sql_pattern = re.compile(r"SELECT\s+.*WHERE.*(\+|\$\{)", re.IGNORECASE)
    return bool(sql_pattern.search(text))


def evaluate_objectives(ind: Individual) -> Tuple[float, float]:
    """Évalue les deux objectifs distincts de l'individu."""
    text = ind.payload
    severity = 0.0

    if check_anti_slop(text):
        severity += 25.0
    if check_strict_typing(text):
        severity += 30.0
    if check_fintech_rules(text):
        severity += 25.0
    if check_sql_injection(text):
        severity += 20.0

    ind.severity = severity
    ind.char_length = float(len(text))
    return ind.severity, ind.char_length


def dominates(p: Individual, q: Individual) -> bool:
    """Vérifie si p domine q au sens de Pareto.
    
    p domine q si :
    - p est au moins aussi bon sur tous les objectifs :
      p.severity >= q.severity ET p.char_length <= q.char_length
    - p est strictement meilleur sur au moins un objectif.
    """
    not_worse = (p.severity >= q.severity) and (p.char_length <= q.char_length)
    strictly_better = (p.severity > q.severity) or (p.char_length < q.char_length)
    return not_worse and strictly_better


def fast_non_dominated_sort(population: List[Individual]) -> List[List[Individual]]:
    """Partitionne la population en fronts de Pareto de rangs croissants."""
    fronts: List[List[Individual]] = [[]]
    domination_counts = {id(ind): 0 for ind in population}
    dominated_sets: dict[int, list[Individual]] = {id(ind): [] for ind in population}

    for p in population:
        for q in population:
            if dominates(p, q):
                dominated_sets[id(p)].append(q)
            elif dominates(q, p):
                domination_counts[id(p)] += 1

        if domination_counts[id(p)] == 0:
            p.rank = 0
            fronts[0].append(p)

    current_rank = 0
    while len(fronts[current_rank]) > 0:
        next_front: List[Individual] = []
        for p in fronts[current_rank]:
            for q in dominated_sets[id(p)]:
                domination_counts[id(q)] -= 1
                if domination_counts[id(q)] == 0:
                    q.rank = current_rank + 1
                    next_front.append(q)
        current_rank += 1
        fronts.append(next_front)

    return [f for f in fronts if len(f) > 0]


def calculate_crowding_distance(front: List[Individual]) -> None:
    """Calcule la distance d'encombrement pour préserver la diversité au sein du front."""
    size = len(front)
    if size == 0:
        return
    for ind in front:
        ind.crowding_distance = 0.0

    if size <= 2:
        for ind in front:
            ind.crowding_distance = float("inf")
        return

    # Tri par sévérité
    front.sort(key=lambda ind: ind.severity)
    front[0].crowding_distance = float("inf")
    front[-1].crowding_distance = float("inf")
    sev_range = front[-1].severity - front[0].severity
    if sev_range > 0:
        for i in range(1, size - 1):
            front[i].crowding_distance += (front[i + 1].severity - front[i - 1].severity) / sev_range

    # Tri par longueur
    front.sort(key=lambda ind: ind.char_length)
    front[0].crowding_distance = float("inf")
    front[-1].crowding_distance = float("inf")
    len_range = front[-1].char_length - front[0].char_length
    if len_range > 0:
        for i in range(1, size - 1):
            front[i].crowding_distance += (front[i + 1].char_length - front[i - 1].char_length) / len_range


def crowded_comparison(ind1: Individual, ind2: Individual) -> int:
    """Opérateur de comparaison par encombrement NSGA-II."""
    if ind1.rank < ind2.rank:
        return -1
    if ind1.rank > ind2.rank:
        return 1
    if ind1.crowding_distance > ind2.crowding_distance:
        return -1
    if ind1.crowding_distance < ind2.crowding_distance:
        return 1
    return 0


def mutate_individual(ind: Individual, rng: random.Random) -> Individual:
    """Applique une mutation selon la niche de l'individu."""
    niche = ind.niche
    mutations = NICHE_MUTATIONS.get(niche, NICHE_MUTATIONS["code"])
    strat = rng.choice(mutations)
    new_text = strat(ind.payload, rng)
    # Mutation occasionnelle de niche (migration écologique)
    new_niche = rng.choice(list(NICHE_MUTATIONS.keys())) if rng.random() < 0.15 else niche
    return Individual(payload=new_text, niche=new_niche)


def crossover_individuals(p1: Individual, p2: Individual, rng: random.Random) -> Tuple[Individual, Individual]:
    parts1 = p1.payload.split(";")
    parts2 = p2.payload.split(";")
    if len(parts1) > 1 and len(parts2) > 1:
        cut1 = rng.randint(1, len(parts1) - 1)
        cut2 = rng.randint(1, len(parts2) - 1)
        c1 = ";".join(parts1[:cut1] + parts2[cut2:])
        c2 = ";".join(parts2[:cut2] + parts1[cut1:])
    else:
        mid1 = len(p1.payload) // 2
        mid2 = len(p2.payload) // 2
        c1 = p1.payload[:mid1] + " " + p2.payload[mid2:]
        c2 = p2.payload[:mid2] + " " + p1.payload[mid1:]
    return Individual(payload=c1, niche=p1.niche), Individual(payload=c2, niche=p2.niche)


def run_evolutionary_fuzzing(
    generations: int = 15,
    pop_size: int = 20,
    seed: int = 42,
    verbose: bool = False,
) -> List[Individual]:
    """Exécute l'algorithme génétique multi-objectifs NSGA-II avec niches."""
    rng = random.Random(seed)
    niches = list(NICHE_MUTATIONS.keys())

    # Initialisation de la population équilibrée par niche
    population: List[Individual] = []
    for i in range(pop_size):
        seed_text = rng.choice(BASE_ADVERSARIAL_SEEDS)
        niche = niches[i % len(niches)]
        ind = Individual(payload=seed_text, niche=niche)
        evaluate_objectives(ind)
        population.append(ind)

    for gen in range(1, generations + 1):
        # Création des descendants
        offspring: List[Individual] = []
        while len(offspring) < pop_size:
            # Sélection par tournoi binaire basé sur le rang de Pareto
            cand1, cand2 = rng.sample(population, 2)
            p1 = cand1 if crowded_comparison(cand1, cand2) <= 0 else cand2
            cand3, cand4 = rng.sample(population, 2)
            p2 = cand3 if crowded_comparison(cand3, cand4) <= 0 else cand4

            c1, c2 = crossover_individuals(p1, p2, rng)
            c1 = mutate_individual(c1, rng)
            c2 = mutate_individual(c2, rng)

            evaluate_objectives(c1)
            evaluate_objectives(c2)

            offspring.append(c1)
            if len(offspring) < pop_size:
                offspring.append(c2)

        # Combinaison parents + enfants (2N)
        combined = population + offspring
        fronts = fast_non_dominated_sort(combined)

        new_population: List[Individual] = []
        for front in fronts:
            calculate_crowding_distance(front)
            if len(new_population) + len(front) <= pop_size:
                new_population.extend(front)
            else:
                # Compléter avec les individus ayant la plus grande distance d'encombrement
                front.sort(key=lambda ind: ind.crowding_distance, reverse=True)
                needed = pop_size - len(new_population)
                new_population.extend(front[:needed])
                break

        population = new_population

        if verbose and (gen % 5 == 0 or gen == generations):
            best_sev = max(ind.severity for ind in population)
            shortest = min(ind.char_length for ind in population)
            print(f"Génération {gen:2d}/{generations} : Sévérité max = {best_sev:.1f}, Longueur min = {shortest:.0f} chars")

    # Calcul final des rangs et tri
    fronts = fast_non_dominated_sort(population)
    pareto_front = fronts[0] if len(fronts) > 0 else population
    # Trier le front de Pareto par sévérité décroissante puis longueur croissante
    pareto_front.sort(key=lambda ind: (-ind.severity, ind.char_length))
    return pareto_front


def main() -> int:
    parser = argparse.ArgumentParser(description="Moteur de fuzzing adverse évolutionnaire v2 (NSGA-II) pour Senior Agent OS.")
    parser.add_argument("--generations", type=int, default=15, help="Nombre de générations (défaut: 15)")
    parser.add_argument("--pop-size", type=int, default=20, help="Taille de la population (défaut: 20)")
    parser.add_argument("--seed", type=int, default=42, help="Graine pseudo-aléatoire déterministe (défaut: 42)")
    parser.add_argument("--verbose", action="store_true", help="Afficher les détails de progression")
    parser.add_argument("--selftest", action="store_true", help="Vérifier la validité du moteur")
    args = parser.parse_args()

    if args.selftest:
        front = run_evolutionary_fuzzing(generations=5, pop_size=10, seed=42)
        assert len(front) > 0
        assert front[0].severity >= 0
        print("Self-test du moteur de fuzzing évolutionnaire v2 (NSGA-II) : SUCCÈS")
        return 0

    pareto_front = run_evolutionary_fuzzing(
        generations=args.generations,
        pop_size=args.pop_size,
        seed=args.seed,
        verbose=args.verbose,
    )

    print(f"\nRésultats du Fuzzing Multi-Objectifs (Générations: {args.generations}, Pop: {args.pop_size}) :")
    print(f"Front de Pareto découvert : {len(pareto_front)} profils optimaux non-dominés\n")
    print("Sélection du Front de Pareto (Compromis Sévérité vs Longueur) :")
    for i, ind in enumerate(pareto_front[:4], start=1):
        print(f"  {i}. [Sévérité: {ind.severity:4.1f}/100 | Longueur: {ind.char_length:3.0f}c | Niche: {ind.niche:11s}]")
        print(f"     Payload : {ind.payload}\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
