import numpy as np
import random as rd

class Parent_Selection:
    def __init__(self, parent_selection_strategy):
        parent_selection_strategies = { 'tournament_2_5': self.tournament_2_5 }
        self.parent_strategy = parent_selection_strategies[parent_selection_strategy]

    def __call__(self, *args, **kwargs):
        return self.parent_strategy(*args, **kwargs)

    def tournament_2_5(self, population, fitness_function):
        parents = []
        for i in range(round(len(population)/50)):
            candidate_indecies = np.random.choice(population.shape[0], 5, replace=True)
            sorted_candidates = sorted(population[candidate_indecies], key=lambda idx: fitness_function(population[idx]), reverse=True)

            parents.append((sorted_candidates[0], sorted_candidates[1]))

        return parents
    