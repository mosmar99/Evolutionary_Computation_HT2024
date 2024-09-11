import numpy as np
import random as rd
from fitness import Fitness_Function, Conflict_Based

class Parent_Selection(object):
    def __init__(self, parent_selection_strategy):
        parent_selection_strategies = { 'tournament_2_5': self.tournament_2_5 }
        self.parent_strategy = parent_selection_strategies(parent_selection_strategy)

    def tournament_2_5(self, population, fittness_evals):
        pop_with_evals = [(list(population[i]), fittness_evals[i]) for i in range(0, len(population))]
        candidates = rd.sample(pop_with_evals, 5) # Only selects two parents from the entire population !?
        candidates.sort(key=pop_with_evals[1], reverse=True)
        return [(candidates[0], candidates[1])]
    