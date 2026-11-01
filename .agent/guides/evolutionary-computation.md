# Guide d'Ingénierie : Calcul Évolutionnaire & Métaheuristiques

Ce guide standardise la conception et l'implémentation d'algorithmes évolutionnaires déterministes, typés et testables.

---

## 1. Principes Fondamentaux d'Ingénierie

1. **Déterminisme et Reproductibilité** : Tout algorithme évolutionnaire doit accepter une graine pseudo-aléatoire (`seed` / PRNG) explicite. Deux exécutions avec la même graine doivent produire strictement les mêmes résultats.
2. **Typage Strict et Séparation Génotype / Phénotype** :
   - Le **génotype** est la structure interne de codage (vecteur binaire, vecteur réel, graphe de décision).
   - Le **phénotype** est l'expression de la solution dans le domaine problème.
   - Ne jamais utiliser le type `any` ou des objets anonymes lâches.
3. **Fonction de Fitness Découplée et Pure** : La fonction d'évaluation doit être sans effet de bord imprévu (*pure function* lorsque possible).
4. **Gestion du Budget d'Évaluation** : Préciser obligatoirement les critères d'arrêt : nombre d'évaluations maximal, nombre de générations sans amélioration (stagnation), fitness seuil atteinte.

---

## 2. Patron d'Implémentation TypeScript

```typescript
export interface GeneticAlgorithmConfig<TGenotype> {
  readonly populationSize: number;
  readonly maxGenerations: number;
  readonly mutationRate: number;
  readonly crossoverRate: number;
  readonly eliteCount: number;
  readonly seed: number;
}

export interface Candidate<TGenotype> {
  readonly genotype: TGenotype;
  readonly fitness: number;
}

export interface EvolutionaryEngine<TGenotype, TSolution> {
  decode(genotype: TGenotype): TSolution;
  evaluate(phenotype: TSolution): number;
  mutate(genotype: TGenotype, rng: () => number): TGenotype;
  crossover(parentA: TGenotype, parentB: TGenotype, rng: () => number): [TGenotype, TGenotype];
  initializePopulation(size: number, rng: () => number): TGenotype[];
}

// PRNG linéaire congruentiel simple et déterministe pour tests reproductibles
export function createPrng(seed: number): () => number {
  let s = seed % 2147483647;
  if (s <= 0) s += 2147483646;
  return () => {
    s = (s * 16807) % 2147483647;
    return (s - 1) / 2147483646;
  };
}

export function runGeneticAlgorithm<TGenotype, TSolution>(
  engine: EvolutionaryEngine<TGenotype, TSolution>,
  config: GeneticAlgorithmConfig<TGenotype>
): Candidate<TGenotype> {
  const rng = createPrng(config.seed);
  let population: Candidate<TGenotype>[] = engine
    .initializePopulation(config.populationSize, rng)
    .map((genotype) => {
      const phenotype = engine.decode(genotype);
      return { genotype, fitness: engine.evaluate(phenotype) };
    });

  for (let gen = 0; gen < config.maxGenerations; gen++) {
    population.sort((a, b) => b.fitness - a.fitness);

    const nextGeneration: Candidate<TGenotype>[] = population.slice(0, config.eliteCount);

    while (nextGeneration.length < config.populationSize) {
      // Sélection par tournoi
      const parentA = tournamentSelect(population, 3, rng);
      const parentB = tournamentSelect(population, 3, rng);

      let [childA, childB] = rng() < config.crossoverRate
        ? engine.crossover(parentA.genotype, parentB.genotype, rng)
        : [parentA.genotype, parentB.genotype];

      if (rng() < config.mutationRate) childA = engine.mutate(childA, rng);
      if (rng() < config.mutationRate) childB = engine.mutate(childB, rng);

      nextGeneration.push({
        genotype: childA,
        fitness: engine.evaluate(engine.decode(childA)),
      });

      if (nextGeneration.length < config.populationSize) {
        nextGeneration.push({
          genotype: childB,
          fitness: engine.evaluate(engine.decode(childB)),
        });
      }
    }

    population = nextGeneration;
  }

  population.sort((a, b) => b.fitness - a.fitness);
  return population[0];
}

function tournamentSelect<T>(pop: Candidate<T>[], k: number, rng: () => number): Candidate<T> {
  let best = pop[Math.floor(rng() * pop.length)];
  for (let i = 1; i < k; i++) {
    const contestant = pop[Math.floor(rng() * pop.length)];
    if (contestant.fitness > best.fitness) {
      best = contestant;
    }
  }
  return best;
}
```

---

## 3. Patron d'Implémentation Python

```python
from __future__ import annotations
import random
from dataclasses import dataclass
from typing import Callable, Generic, List, Tuple, TypeVar

G = TypeVar("G")  # Type du Génotype
P = TypeVar("P")  # Type du Phénotype

@dataclass(frozen=True)
class Individual(Generic[G]):
    genotype: G
    fitness: float

class EvolutionarySolver(Generic[G, P]):
    def __init__(
        self,
        decode_fn: Callable[[G], P],
        evaluate_fn: Callable[[P], float],
        mutate_fn: Callable[[G, random.Random], G],
        crossover_fn: Callable[[G, G, random.Random], Tuple[G, G]],
        init_fn: Callable[[random.Random], G],
    ) -> None:
        self.decode = decode_fn
        self.evaluate = evaluate_fn
        self.mutate = mutate_fn
        self.crossover = crossover_fn
        self.init_individual = init_fn

    def solve(
        self,
        pop_size: int,
        generations: int,
        mutation_rate: float,
        seed: int,
        tournament_size: int = 3,
    ) -> Individual[G]:
        rng = random.Random(seed)
        
        # Initialisation
        population: List[Individual[G]] = []
        for _ in range(pop_size):
            g = self.init_individual(rng)
            fit = self.evaluate(self.decode(g))
            population.append(Individual(genotype=g, fitness=fit))

        for _ in range(generations):
            population.sort(key=lambda ind: ind.fitness, reverse=True)
            new_pop: List[Individual[G]] = [population[0]]  # Élitism

            while len(new_pop) < pop_size:
                p1 = self._tournament(population, tournament_size, rng)
                p2 = self._tournament(population, tournament_size, rng)

                c1_g, c2_g = self.crossover(p1.genotype, p2.genotype, rng)
                if rng.random() < mutation_rate:
                    c1_g = self.mutate(c1_g, rng)
                if rng.random() < mutation_rate:
                    c2_g = self.mutate(c2_g, rng)

                new_pop.append(Individual(genotype=c1_g, fitness=self.evaluate(self.decode(c1_g))))
                if len(new_pop) < pop_size:
                    new_pop.append(Individual(genotype=c2_g, fitness=self.evaluate(self.decode(c2_g))))

            population = new_pop

        population.sort(key=lambda ind: ind.fitness, reverse=True)
        return population[0]

    def _tournament(self, pop: List[Individual[G]], k: int, rng: random.Random) -> Individual[G]:
        chosen = rng.sample(pop, k)
        return max(chosen, key=lambda ind: ind.fitness)
```

---

## 4. Règles d'Optimisation Multi-Objectifs (NSGA-II)

Lorsqu'un problème comporte plusieurs fonctions objectifs contradictoires (ex: latence vs coût vs couverture) :
- Ne pas agréger arbitrairement les critères en une somme pondérée naive.
- Calculer le front de Pareto via la dominance au sens de Pareto.
- Maintenir la diversité de la population le long du front à l'aide de la distance de crowding (*Crowding Distance*).

---

## 5. Checklist de Validation

- [ ] L'algorithme fournit un comportement 100% déterministe avec une graine fixe.
- [ ] Aucun type vague (`any`, `Object` non typé) n'est employé.
- [ ] La fonction de fitness est protégée contre les divisions par zéro et les valeurs infinies.
- [ ] Les opérateurs de mutation et croisement préservent la validité structurelle du génotype.
- [ ] Le budget d'évaluation (générations, taille population) est plafonné pour éviter les boucles infinies.
