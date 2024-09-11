import numpy as np
import random as rd
from fitness import Fitness_Function, Conflict_Based

class Delete_Replace():
    # replace the currently, two worst individuals in the population
    # worst is defined in terms of fitness evalutation, the lower the worse
    def del_rep_2(self, population, offspring):
        population_list = population.tolist()
        population_list.sort(key=Fitness_Function(Conflict_Based()).evaluate, reverse=False)        
        population_list[0], population_list[1] = offspring[0], offspring[1]
        return np.array(population_list)

class Survival_Selection(object):
    def __init__(self, parent_strategy, survival_strategy):
        self.survival_strategy = survival_strategy

    def del_rep_2(self, population, offspring):
        return self.survival_strategy.del_rep_2(population, offspring)