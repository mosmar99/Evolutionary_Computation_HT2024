"""
This file contains the survival selection class which is responsible for selecting the individuals that will survive to the next generation.
Authors: Mahmut Osmanovic (mosmar99), Sebastian Tuura (tuura01), Isac Paulsson (isacpaulsson), Emil Wagman (Neobyte01), Mohammad Al Khaled (MohamadAlkhaled)
Last updated: 2024-10-02
"""

import numpy as np

# Survival_Selection class
class Survival_Selection:
    # init function for Survival_Selection class
    # input: survival_selection_strategy: string
    # output: None
    def __init__(self, survival_selection_strategy):
        survival_strategies = { 'del_rep_2': self.del_rep_2,
                                'prob_survival': self.prob_survival }
        self.survival_strategy = survival_strategies[survival_selection_strategy]
        self.strategy_name = survival_selection_strategy

    # call function for Survival_Selection class
    # input: *args, **kwargs
    # output: self.survival_strategy(*args, **kwargs)
    def __call__(self, *args, **kwargs):
        return self.survival_strategy(*args, **kwargs)
    
    # Deletes the two least fit individuals in the population and replaces them with the two offspring
    # input: population: numpy array, offspring: numpy array, fitness_function: function
    # output: sorted_population: numpy array
    def del_rep_2(self, population, offspring, fitness_function):
        fitness_values = fitness_function(population)
        sorted_indices = np.argsort(fitness_values)
        sorted_population = population[sorted_indices]
        sorted_population[0] = offspring[0]
        sorted_population[1] = offspring[1]   
        return sorted_population
    
    # Selects the individuals that will survive to the next generation based on their fitness
    # input: population: numpy array, offspring: numpy array, fitness_function: function
    # output: total_population[selected_indecies]: numpy array
    def prob_survival(self, population, offspring, fitness_function):
        total_population = np.concatenate([population, offspring])
        total_population_evals = np.array(fitness_function(np.concatenate([population, offspring])))

        normalized_weights = total_population_evals**5 / np.sum(total_population_evals**5)
        
        selected_indecies = np.random.choice(np.arange(len(total_population)), len(population), p=normalized_weights, replace=False)
        return total_population[selected_indecies]#

