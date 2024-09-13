import numpy as np

class Survival_Selection:
    def __init__(self, survival_selection_strategy):
        survival_strategies = { 'del_rep_2': self.del_rep_2,
                                'prob_survival': self.prob_survival }
        self.survival_strategy = survival_strategies[survival_selection_strategy]

    def __call__(self, *args, **kwargs):
        return self.survival_strategy(*args, **kwargs)
    
    def del_rep_2(self, population, offspring, fitness_function):
        fitness_values = fitness_function(population)
        sorted_indices = np.argsort(fitness_values)
        sorted_population = population[sorted_indices]
        sorted_population[0] = offspring[0]
        sorted_population[1] = offspring[1]   
        return sorted_population
    
    def prob_survival(self, population, offspring, fitness_function):
        total_population = np.concatenate([population, offspring])
        total_population_evals = np.array(fitness_function(np.concatenate([population, offspring])))

        normalized_weights = total_population_evals**5 / np.sum(total_population_evals**5)
        
        selected_indecies = np.random.choice(np.arange(len(total_population)), len(population), p=normalized_weights, replace=False)
        return total_population[selected_indecies]

