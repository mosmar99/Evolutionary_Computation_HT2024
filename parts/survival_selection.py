import numpy as np
import random as rd

class Survival_Selection():
    def __init__(self, survival_strategy):
        survival_strategies = { 'del_rep_2': self.del_rep_2 }
        self.survival_strategy = survival_strategies[survival_strategy]

    def __call__(self, *args, **kwargs):
        return self.survival_strategy(*args, **kwargs)
    
    def del_rep_2(self, population, offspring, fitness_function):
        population_list = population.tolist()
        population_list.sort(key=fitness_function, reverse=False)        
        population_list[0], population_list[1] = offspring[0], offspring[1]
        return np.array(population_list)