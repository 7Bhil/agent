#!/usr/bin/env python3
"""Moteur de fuzzing adverse et d'évaluations par calcul évolutionnaire.

Génère des variantes adverses de scénarios pour éprouver la résistance
des filtres d'intégrité (anti-slop, typage strict, sécurité, unicode)
via un algorithme génétique autonome sans dépendances externes.

Usage:
    python3 scripts/fuzz-agent-evals.py [--generations N] [--pop-size M] [--seed S]
"""

from __future__ import annotations

import argparse
import random
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, List, Tuple

ROOT_DIR = Path(__file__).resolve().parent.parent

# Motifs d'attaques adverses de base
BASE_ADVERSARIAL_SEEDS = [
    "function processData(payload: any): any { return payload; }",
    "Il convient de noter qu'il est crucial de souligner ces aspects dans une certaine mesure.",
    "const balance = 120.50; // balance en float au lieu d'un entier mineur",
    "SELECT * FROM users WHERE id = ' + req.body.id + '",
    "export type UserRecord = Record<string, any>;",
    "Force est de constater que le système fonctionne parfaitement au bout du compte.",
    "// Note: temporary hack to bypass auth check",
    "let amount: number = parseFloat('10.99');",
]

MUTATION_STRATEGIES = [
    # Insertion de mot-clef de typage permissif
    lambda s, rng: s + " // type " + rng.choice(["any", "unknown as any", "Object"]),
    # Insertion de hedging slop en français
    lambda s, rng: rng.choice([
        "Il convient de noter que ",
        "Force est de constater que ",
        "Il va sans dire que ",
    ]) + s,
    # Insertion de violation de règles financières (flottants)
    lambda s, rng: s + " const fee = " + str(rng.randint(1, 99)) + "." + str(rng.randint(10, 99)) + ";",
    # Concaténation de requêtes SQL vulnérables
    lambda s, rng: s + " const query = `SELECT * FROM tbl WHERE key = ${userInput}`;",
    # Masquage par commentaires
    lambda s, rng: "/* bypass */ " + s + " /* ignore */",
    # Substitution de casse ou ponctuation
    lambda s, rng: s.replace("any", "Any").replace("function", "async function"),
]


@dataclass
class Individual:
    payload: str
    fitness: float = 0.0


def check_anti_slop(text: str) -> bool:
    """Retourne True si un motif slop est détecté."""
    slop_pattern = re.compile(
        r"\b(il convient de noter|il est (important|essentiel|crucial) de (noter|souligner|rappeler)|"
        r"force est de constater|il va sans dire que|au bout du compte|dans une certaine mesure)\b",
        re.IGNORECASE,
    )
    return bool(slop_pattern.search(text))


def check_strict_typing(text: str) -> bool:
    """Retourne True si une violation de typage strict est détectée."""
    any_pattern = re.compile(r"(\bas\s+any\b|:\s*any\b|\bRecord<[^,]+,\s*any>)", re.IGNORECASE)
    return bool(any_pattern.search(text))


def check_fintech_rules(text: str) -> bool:
    """Retourne True si un usage suspect de flottant pour monnaie est détecté."""
    float_pattern = re.compile(r"\b(balance|fee|amount|solde|montant)\b.*[0-9]+\.[0-9]+", re.IGNORECASE)
    return bool(float_pattern.search(text))


def check_sql_injection(text: str) -> bool:
    """Retourne True si une concaténation suspecte de requête SQL est détectée."""
    sql_pattern = re.compile(r"SELECT\s+.*WHERE.*(\+|\$\{)", re.IGNORECASE)
    return bool(sql_pattern.search(text))


def evaluate_fitness(ind: Individual) -> float:
    """Calcule le score de fitness d'un individu adverse.
    
    L'objectif d'un individu adverse est de combiner plusieurs violations de règles
    tout en maximisant la complexité du payload.
    """
    score = 0.0
    text = ind.payload

    if check_anti_slop(text):
        score += 25.0
    if check_strict_typing(text):
        score += 30.0
    if check_fintech_rules(text):
        score += 25.0
    if check_sql_injection(text):
        score += 20.0

    # Pénalité de longueur excessive pour favoriser les contre-exemples concis
    if len(text) > 400:
        score -= (len(text) - 400) * 0.05

    ind.fitness = max(0.0, score)
    return ind.fitness


def mutate(ind: Individual, rng: random.Random, rate: float = 0.7) -> Individual:
    """Opérateur de mutation génétique."""
    if rng.random() > rate:
        return Individual(payload=ind.payload)

    strategy: Callable[[str, random.Random], str] = rng.choice(MUTATION_STRATEGIES)
    new_payload = strategy(ind.payload, rng)
    return Individual(payload=new_payload)


def crossover(p1: Individual, p2: Individual, rng: random.Random) -> Tuple[Individual, Individual]:
    """Opérateur de croisement (crossover) à un point."""
    parts1 = p1.payload.split(";")
    parts2 = p2.payload.split(";")

    if len(parts1) > 1 and len(parts2) > 1:
        cut1 = rng.randint(1, len(parts1) - 1)
        cut2 = rng.randint(1, len(parts2) - 1)
        c1_payload = ";".join(parts1[:cut1] + parts2[cut2:])
        c2_payload = ";".join(parts2[:cut2] + parts1[cut1:])
    else:
        # Croisement textuel alternatif
        mid1 = len(p1.payload) // 2
        mid2 = len(p2.payload) // 2
        c1_payload = p1.payload[:mid1] + " " + p2.payload[mid2:]
        c2_payload = p2.payload[:mid2] + " " + p1.payload[mid1:]

    return Individual(payload=c1_payload), Individual(payload=c2_payload)


def tournament_selection(population: List[Individual], k: int, rng: random.Random) -> Individual:
    """Sélection par tournoi de taille k."""
    candidates = rng.sample(population, k)
    return max(candidates, key=lambda ind: ind.fitness)


def run_evolutionary_fuzzing(
    generations: int = 15,
    pop_size: int = 20,
    seed: int = 42,
    verbose: bool = False,
) -> List[Individual]:
    """Exécute l'algorithme génétique d'optimisation d'exemples adverses."""
    rng = random.Random(seed)

    # Initialisation de la population
    population: List[Individual] = [
        Individual(payload=rng.choice(BASE_ADVERSARIAL_SEEDS))
        for _ in range(pop_size)
    ]

    for ind in population:
        evaluate_fitness(ind)

    if verbose:
        print(f"Initialisation : {pop_size} individus. Meilleure fitness initiale : {max(ind.fitness for ind in population):.1f}")

    for gen in range(1, generations + 1):
        # Élitism : conservation des 2 meilleurs
        population.sort(key=lambda x: x.fitness, reverse=True)
        new_population: List[Individual] = [
            Individual(payload=population[0].payload, fitness=population[0].fitness),
            Individual(payload=population[1].payload, fitness=population[1].fitness),
        ]

        # Reproduction jusqu'à remplir la population
        while len(new_population) < pop_size:
            p1 = tournament_selection(population, 3, rng)
            p2 = tournament_selection(population, 3, rng)

            c1, c2 = crossover(p1, p2, rng)
            c1 = mutate(c1, rng)
            c2 = mutate(c2, rng)

            evaluate_fitness(c1)
            evaluate_fitness(c2)

            new_population.append(c1)
            if len(new_population) < pop_size:
                new_population.append(c2)

        population = new_population
        best_current = max(population, key=lambda x: x.fitness)

        if verbose and (gen % 5 == 0 or gen == generations):
            print(f"Génération {gen:2d}/{generations} : Meilleure fitness = {best_current.fitness:.1f}")

    population.sort(key=lambda x: x.fitness, reverse=True)
    return population


def main() -> int:
    parser = argparse.ArgumentParser(description="Moteur de fuzzing adverse évolutionnaire pour Senior Agent OS.")
    parser.add_argument("--generations", type=int, default=15, help="Nombre de générations (défaut: 15)")
    parser.add_argument("--pop-size", type=int, default=20, help="Taille de la population (défaut: 20)")
    parser.add_argument("--seed", type=int, default=42, help="Graine pseudo-aléatoire déterministe (défaut: 42)")
    parser.add_argument("--verbose", action="store_true", help="Afficher les détails de progression")
    parser.add_argument("--selftest", action="store_true", help="Vérifier la validité du moteur")
    args = parser.parse_args()

    if args.selftest:
        pop = run_evolutionary_fuzzing(generations=5, pop_size=10, seed=42)
        assert len(pop) == 10
        assert pop[0].fitness >= pop[-1].fitness
        print("Self-test du moteur de fuzzing évolutionnaire : SUCCÈS")
        return 0

    results = run_evolutionary_fuzzing(
        generations=args.generations,
        pop_size=args.pop_size,
        seed=args.seed,
        verbose=args.verbose,
    )

    print(f"\nRésultats du Fuzzing Évolutionnaire (Générations: {args.generations}, Pop: {args.pop_size}) :")
    print(f"Top Fitness obtenue : {results[0].fitness:.1f}/100.0\n")
    print("Top 3 des scénarios adverses générés :")
    for i, ind in enumerate(results[:3], start=1):
        print(f"  {i}. [Fitness {ind.fitness:.1f}] {ind.payload}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
