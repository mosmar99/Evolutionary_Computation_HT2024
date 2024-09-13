import numpy as np
import random as rd

class Survival_Selection:
    def __init__(self, survival_selection_strategy):
        survival_strategies = { 'del_rep_2': self.del_rep_2,
                                'prob_survival': self.prob_survival }
        self.survival_strategy = survival_strategies[survival_selection_strategy]

    def __call__(self, *args, **kwargs):
        return self.survival_strategy(*args, **kwargs)
    
    def del_rep_2(self, population, offspring, fitness_function):
        population_list = population.tolist()
        population_list.sort(key=fitness_function, reverse=False)        
        population_list[0], population_list[1] = offspring[0], offspring[1]
        return np.array(population_list)
    
    def prob_survival(self, population, offspring, fitness_function):
        total_population = np.concatenate([population, offspring])
        total_population_evals = fitness_function(total_population)
        sum = np.sum(total_population_evals)
        weights = np.apply_along_axis(lambda x: x/sum, axis=0, arr=total_population_evals)
        selected_indecies = np.random.choice(np.arange(len(total_population)), len(population), p=weights)
        return total_population[selected_indecies]

