import numpy as np

class Init_Pop():
    def __init__(self, initialization_strategy):
        init_strategies = { 'random': self.init_random,
                            'random_permutations': self.init_random_permutations }
        
        self.initialization_strategy = init_strategies[initialization_strategy]
    
    def __call__(self, *args, **kwargs):
        return self.initialization_strategy(*args, **kwargs)

    # random init of individuals in population of size POPULATION_SIZE
    def init_random(self, GENOME_SIZE, POPULATION_SIZE):
        # low while is included, however, high value is excluded in the calcs
        return np.random.randint(low=1, high=GENOME_SIZE+1, size=(POPULATION_SIZE, GENOME_SIZE))
    
    def init_random_permutations(self, GENOME_SIZE, POPULATION_SIZE):
        # Removes the possibility for horizontal conflicts
        base = np.arange(GENOME_SIZE)
        permutations = np.empty((POPULATION_SIZE, GENOME_SIZE), dtype=int)

        for i in range(self.population_size):
            permutations[i] = np.random.permutation(base)

        return permutations

if __name__ == '__main__':
    population = Init_Pop('random')()
