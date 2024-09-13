import numpy as np

class Parent_Selection:
    def __init__(self, parent_selection_strategy):
        parent_selection_strategies = { 'tournament': self.tournament }
        self.parent_strategy = parent_selection_strategies[parent_selection_strategy]

    def __call__(self, *args, **kwargs):
        return self.parent_strategy(*args, **kwargs)

    def tournament(self, population, NUM_OFFSPRING, TOURNAMENT_GROUP_SIZE, fitness_function):
        parents = []
        for _ in range(round(NUM_OFFSPRING/2)):
            np.arange(len(population))
            random_indecies = np.random.choice(np.arange(len(population)), int(population.shape[0]*TOURNAMENT_GROUP_SIZE), replace=False)
            fitness_values = fitness_function(population[random_indecies])
            sorted_indices = np.argsort(fitness_values)

            parents.append((population[sorted_indices[0]], population[sorted_indices[1]]))

        return parents
    