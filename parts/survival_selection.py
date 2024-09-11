import numpy as np
import random as rd

class Delete_Replace():
    # replace the currently, two worst individuals in the population
    # worst is defined in terms of fitness evalutation, the lower the worse
    def del_rep_2(self, population, offspring, fitness_evals):
        pop_with_evals = [(list(population[i]), fitness_evals[i]) for i in range(0, len(population))]
        pop_with_evals.sort(key=pop_with_evals[1], reverse=False) 
        pop_with_evals[0], pop_with_evals[1] = offspring[0], offspring[1]
        return np.array(population_list)

class Survival_Selection(object):
    def __init__(self, survival_strategy):
        self.survival_strategy = survival_strategy

    def del_rep_2(self, population, offspring):
        return self.survival_strategy.del_rep_2(population, offspring)