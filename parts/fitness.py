import numpy as np

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

class Conflict_Based():
    # returns an fitness array of current population (may be 1 individual in population or more) 
    def exec(self, population):
        fitness_evals = []
        if(np.array(population).ndim == 1):
                fitness_evals.append(1 - conflict_counter(population) / 28) 
        elif(np.array(population).ndim == 2):
            for i in range(len(population)):
                fitness_evals.append(1 - conflict_counter(population[i]) / 28) 
        return fitness_evals

class Fitness_Function(object):
    def __init__(self, fitness_strategy):
        self.fitness_strategy = fitness_strategy
    
    def evaluate(self, population):
        return self.fitness_strategy.exec(population) 