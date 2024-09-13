import numpy as np
import random as rd

class Parent_Selection:
    def __init__(self, parent_selection_strategy):
        parent_selection_strategies = { 'tournament': self.tournament }
        self.parent_strategy = parent_selection_strategies[parent_selection_strategy]

    def __call__(self, *args, **kwargs):
        return self.parent_strategy(*args, **kwargs)

    def tournament(self, population, NUM_OFFSPRING, TOURNAMENT_GROUP_SIZE, fitness_function):
        parents = []
        for i in range(round(NUM_OFFSPRING/2)):
            candidate_indecies = np.random.choice(population.shape[0], int(population.shape[0]*TOURNAMENT_GROUP_SIZE), replace=True)
            sorted_candidates = sorted(population[candidate_indecies], key=lambda idx: fitness_function(population[idx]), reverse=True)

            parents.append((sorted_candidates[0], sorted_candidates[1]))

        return parents
    