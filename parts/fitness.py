"""
This file contains the fitness function class which is responsible for calculating the fitness of an individual in the population.
Authors: Mahmut Osmanovic (mosmar99), Sebastian Tuura (tuura01), Isac Paulsson (isacpaulsson), Emil Wagman (Neobyte01), Mohammad Al Khaled (MohamadAlkhaled)
Last updated: 2024-10-02
"""

import numpy as np

class Fitness_Function:
    # init function for Fitness_Function class
    # input: fitness_strategy: string
    # output: None
    def __init__(self, fitness_strategy):
        fitness_strategies = { "conflict_based": self.conflict_based}
        self.fitness_strategy = fitness_strategies[fitness_strategy]
        self.fitness_lookup_table = {} # Cache for fitness evaluations
        self.strategy_name = fitness_strategy

    # call function for Fitness_Function class
    # input: *args, **kwargs
    # output: self.fitness_strategy(*args, **kwargs)
    def __call__(self, *args, **kwargs):
        return self.fitness_strategy(*args, **kwargs)
    
    # attempts to look up the fitness of an individual in the cache
    # if the individual is not found in the cache, it is evaluated and added to the cache
    # input: individual: numpy array
    # output: fitness: float
    def trylookup(self, individual):
        try:
            return self.fitness_lookup_table[hash(individual.tobytes())]
        except KeyError:
            fitness = conflict_counter(individual)
            self.fitness_lookup_table[hash(individual.tobytes())] = fitness
            return fitness
        
    # returns an fitness array of current population (may be 1 individual in population or more)
    # input: population: numpy array, genome_size: int
    # output: fitness_evals: numpy array
    def conflict_based(self, population, genome_size):
        fitness_evals = []
        denominator = (genome_size * (genome_size - 1)) / 2 # Maximum number of conflicts for a given genome size
        if(np.array(population).ndim == 1):
                fitness_evals.append(1 - self.trylookup(population) / denominator) 
        elif(np.array(population).ndim == 2):
            for i in range(len(population)):
                fitness_evals.append(1 - self.trylookup(population[i]) / denominator) 
        return fitness_evals

# Fitness Function returns: '#(Conflicting Pairs of Queens)'
# input: individual: numpy array
# output: conflict_counter: int
# information about valid moves for a queen: https://en.wikipedia.org/wiki/Queen_(chess)#Placement_and_movement 
def conflict_counter(individual):
    # To Check: 
    # 1] Queens can't be in the same row (due to individual representation, no need to check for conflicting columns)
    # 2] Queens can't be in the same diagonal
    # Fitness Functions returns: '#(Conflicting Pairs of Queens)'
    n = len(individual)
    conflict_counter = 0
    for Q1 in range(n):
        for Q2 in range(Q1+1, n):
            # counts conflicts row-wise
            if(individual[Q1] == individual[Q2]):
                conflict_counter += 1
            # counts conflicts diag-wise
            # EX: [_,1,_,_,_,_,6,_] -> (2,1) & (7,6) => DIAG: (2-7)=(1-6) <=> (-5)=(-5)
            # DIFF_X = DIFF_Y => DIAG 
            if abs(individual[Q1] - individual[Q2]) == abs(Q1 - Q2):
                conflict_counter += 1
    return conflict_counter
