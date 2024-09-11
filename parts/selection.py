import numpy as np
import random as rd
from fitness import Fitness_Function, Conflict_Based

class Tournament():
    # Select the best 2 selected_parents from a random group of 5 individuals
    def pick_2_5(self, population):
        candidates = rd.sample(list(population), 5)
        candidates.sort(key=Fitness_Function(Conflict_Based()).evaluate, reverse=True)
        return candidates[0], candidates[1]

class Delete_Replace():
    # replace the currently, two worst individuals in the population
    # worst is defined in terms of fitness evalutation, the lower the worse
    def del_rep_2(self, population, offspring):
        population_list = population.tolist()
        population_list.sort(key=Fitness_Function(Conflict_Based()).evaluate, reverse=False)        
        population_list[0], population_list[1] = offspring[0], offspring[1]
        return np.array(population_list)

class Selection(object):
    def __init__(self, parent_strategy, survival_strategy):
        self.parent_strategy = parent_strategy
        self.survival_strategy = survival_strategy

    def pick_2_5(self, population):
        return self.parent_strategy.pick_2_5(population)
    
    def del_rep_2(self, population, offspring):
        return self.survival_strategy.del_rep_2(population, offspring)