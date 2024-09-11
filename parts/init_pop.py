import numpy as np

# random init of individuals in population of size POPULATION_SIZE
class Init_Random():
    def exec(self, GENOME_SIZE, POPULATION_SIZE):
    # low while is included, however, high value is excluded in the calcs
        return np.random.randint(low=1, high=8+1, size=(POPULATION_SIZE, GENOME_SIZE))

class Init_Pop(object):
    def __init__(self, initialization_strategy):
        self.initialization_strategy = initialization_strategy
    
    def initialize_population(self, GENOME_SIZE, POPULATION_SIZE):
        return self.initialization_strategy.exec(GENOME_SIZE, POPULATION_SIZE)