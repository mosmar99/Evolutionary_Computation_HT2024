import numpy as np
from init_pop import Init_Pop

class Destroy:
    def __init__(self, max_stagnant_generations, tolerance, genocide_perc):
        self.max_stagnant_generations = max_stagnant_generations
        self.tolerance = tolerance
        self.genocide_perc = genocide_perc
        self.old_champion = None
        self.stagnant_generations = 0

    def check_stagnation(self, contender):
        if(self.old_champion is None):
            self.old_champion = contender
            return False

        if(contender - self.old_champion > self.tolerance):
            # Improvement detected, reset stagnation counter
            self.old_champion = contender
            self.stagnant_generations = 0
            return False
        else:
            # No significant improvement
            self.stagnant_generations += 1
            return self.stagnant_generations >= self.max_stagnant_generations

    def apply_genocide(self, population, fitness_function):
        genome_size = population.shape[1]
        num_to_replace = int(len(population) * self.genocide_perc)
        num_to_keep = len(population) - num_to_replace
        fitness_scores = np.array(fitness_function(population))
        normalized_weights = fitness_scores ** 5 / np.sum(fitness_scores ** 5)
        survivors_indices = np.random.choice(np.arange(len(population)), num_to_keep, p=normalized_weights, replace=False)
        survivors = population[survivors_indices]
        new_individuals = Init_Pop('random_permutations')(genome_size, num_to_replace)
        new_population = np.concatenate((survivors, new_individuals), axis=0)
        self.stagnant_generations = 0
        return new_population
