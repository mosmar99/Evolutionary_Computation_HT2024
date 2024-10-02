"""
This file contains the Destroy class which is responsible for checking stagnation in the population and applying genocide when necessary.
Authors: Mahmut Osmanovic (mosmar99), Sebastian Tuura (tuura01), Isac Paulsson (isacpaulsson), Emil Wagman (Neobyte01), Mohammad Al Khaled (MohamadAlkhaled)
Last updated: 2024-10-02
"""
import numpy as np
from init_pop import Init_Pop

class Destroy:
    # init function for Destroy class
    # input: max_stagnant_generations: int, tolerance: float
    # output: None
    def __init__(self, max_stagnant_generations, tolerance):
        self.max_stagnant_generations = max_stagnant_generations
        self.tolerance = tolerance
        self.old_champion = None
        self.stagnant_generations = 0

    # method to check stagnation in popluation
    # input: contender: float (fitness score of the contender)
    # output: bool (True if the contender is stagnating, False otherwise)
    def check_stagnation(self, contender):

        # If no old champion, set the contender as the champion
        if(self.old_champion is None):
            self.old_champion = contender
            return False

        # check if the contender is better than the old champion according to a set tolerance value.
        if(contender - self.old_champion > self.tolerance):
            # Improvement detected, reset stagnation counter
            self.old_champion = contender
            self.stagnant_generations = 0
            return False
        else:
            # No significant improvement
            self.stagnant_generations += 1
            return self.stagnant_generations >= self.max_stagnant_generations

    # method to apply genocide to the population
    # input: population: numpy array, genocide_perc: float, fitness_function: function
    # output: new_population: numpy array
    def apply_genocide(self, population, genocide_perc, fitness_function):
        # Calculate the number of individuals to replace
        genome_size = population.shape[1]
        num_to_replace = int(len(population) * genocide_perc)
        num_to_keep = len(population) - num_to_replace

        # Calculate the fitness scores and select the survivors
        fitness_scores = np.array(fitness_function(population))
        normalized_weights = fitness_scores ** 5 / np.sum(fitness_scores ** 5)
        survivors_indices = np.random.choice(np.arange(len(population)), num_to_keep, p=normalized_weights, replace=False)
        survivors = population[survivors_indices]

        # Generate new individuals to replace the non-survivors
        new_individuals = Init_Pop('random_permutations')(genome_size, num_to_replace)
        new_population = np.concatenate((survivors, new_individuals), axis=0)
        self.stagnant_generations = 0
        return new_population
