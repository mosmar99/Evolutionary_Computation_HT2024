"""
This file contains the initialization population class which is responsible for generating the initial population & subsequent populations.
Authors: Mahmut Osmanovic (mosmar99), Sebastian Tuura (tuura01), Isac Paulsson (isacpaulsson), Emil Wagman (Neobyte01), Mohammad Al Khaled (MohamadAlkhaled)
Last updated: 2024-10-02
"""

import numpy as np

class Init_Pop:
    # init function for Init_Pop class
    # input: initialization_strategy: string
    # output: None
    def __init__(self, initialization_strategy):
        init_strategies = { 'random': self.init_random,
                            'random_permutations': self.init_random_permutations }
        
        self.initialization_strategy = init_strategies[initialization_strategy]
        self.strategy_name = initialization_strategy
    
    # call function for Init_Pop class
    # input: *args, **kwargs
    # output: self.initialization_strategy(*args, **kwargs)
    def __call__(self, *args, **kwargs):
        return self.initialization_strategy(*args, **kwargs)

    # random init of individuals in population of size POPULATION_SIZE
    # input: GENOME_SIZE: int, POPULATION_SIZE: int
    # output: numpy array of shape (POPULATION_SIZE, GENOME_SIZE) containing random integers from 1 to GENOME_SIZE
    def init_random(self, GENOME_SIZE, POPULATION_SIZE):
        # low while is included, however, high value is excluded in the calcs
        return np.random.randint(low=1, high=GENOME_SIZE+1, size=(POPULATION_SIZE, GENOME_SIZE))
    
    # creates a permutation of integers from 1 to GENOME_SIZE for each individual in the population (no two indexes will be the same)
    # input: GENOME_SIZE: int, POPULATION_SIZE: int
    # output: numpy array of shape (POPULATION_SIZE, GENOME_SIZE) containing random permutations of integers from 1 to GENOME_SIZE
    def init_random_permutations(self, GENOME_SIZE, POPULATION_SIZE):
        # Removes the possibility for horizontal conflicts
        base = np.arange(1, GENOME_SIZE + 1)
        permutations = np.empty((POPULATION_SIZE, GENOME_SIZE), dtype=int)

        for i in range(POPULATION_SIZE):
            permutations[i] = np.random.permutation(base)

        return permutations
