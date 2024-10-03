"""
This file contains the parent selection class which is responsible for selecting the parents that will be used to create offspring.
Authors: Mahmut Osmanovic (mosmar99), Sebastian Tuura (tuura01), Isac Paulsson (isacpaulsson), Emil Wagman (Neobyte01), Mohammad Al Khaled (MohamadAlkhaled)
Last updated: 2024-10-02
"""

import numpy as np

# Parent selection class
class Parent_Selection:
    # init function for Parent_Selection class
    # input: parent_selection_strategy: string
    # output: None
    def __init__(self, parent_selection_strategy):
        parent_selection_strategies = { 'tournament': self.tournament }
        self.parent_strategy = parent_selection_strategies[parent_selection_strategy]
        self.strategy_name = parent_selection_strategy

    # call function for Parent_Selection class
    # input: *args, **kwargs
    # output: self.parent_strategy(*args, **kwargs)
    def __call__(self, *args, **kwargs):
        return self.parent_strategy(*args, **kwargs)

    # Selects the parents that will be used to create offspring based on their fitness
    # input: population: numpy array, NUM_OFFSPRING_RATE: float, TOURNAMENT_GROUP_SIZE: float, fitness_function: function
    # output: parents: list
    # https://en.wikipedia.org/wiki/Tournament_selection
    def tournament(self, population, NUM_OFFSPRING_RATE, TOURNAMENT_GROUP_SIZE, fitness_function):
        #Tournament selection, selects the best two individuals from a random group of individuals
        parents = []
        for _ in range(round(NUM_OFFSPRING_RATE*population.shape[0]/2)):
            np.arange(len(population))
            random_indecies = np.random.choice(np.arange(len(population)), int(population.shape[0]*TOURNAMENT_GROUP_SIZE), replace=False)
            fitness_values = fitness_function(population[random_indecies])
            sorted_indices = np.argsort(fitness_values)

            parents.append((population[sorted_indices[0]], population[sorted_indices[1]]))

        return parents
    