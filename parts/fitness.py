import numpy as np

class Fitness_Function:
    def __init__(self, fitness_strategy):
        fitness_strategies = { "conflict_based": self.conflict_based}
        self.fitness_strategy = fitness_strategies[fitness_strategy]
        self.fitness_lookup_table = {}

    def __call__(self, *args, **kwargs):
        return self.fitness_strategy(*args, **kwargs)
    
    def trylookup(self, individual):
        try:
            return self.fitness_lookup_table[hash(individual.tobytes())]
        except KeyError:
            fitness = conflict_counter(individual)
            self.fitness_lookup_table[hash(individual.tobytes())] = fitness
            return fitness
        
    # returns an fitness array of current population (may be 1 individual in population or more) 
    def conflict_based(self, population, genome_size):
        fitness_evals = []
        denominator = (genome_size * (genome_size - 1)) / 2
        if(np.array(population).ndim == 1):
                fitness_evals.append(1 - self.trylookup(population) / denominator) 
        elif(np.array(population).ndim == 2):
            for i in range(len(population)):
                fitness_evals.append(1 - self.trylookup(population[i]) / denominator) 
        return fitness_evals

    # Function to calculate element-wise similarity between two individuals
    def element_wise_similarity(self, individual_A, individual_B):
        individual_A = np.array(individual_A)
        individual_B = np.array(individual_B)
        if individual_A.size != individual_B.size and individual_A.shape[0] == individual_B.shape[0]:
            raise ValueError("Arrays must have the same shape")
        matches = np.sum(individual_A == individual_B)
        total = individual_A.size
        return matches / total

    # Compute average similarity of offspring compared to a sample of the population
    def avg_similarity(self, offspring, population_sample):
        total_similarity = 0
        for ind in population_sample:
            for child in offspring:
                total_similarity += self.element_wise_similarity(child, ind)
        
        return total_similarity / (len(offspring) * len(population_sample))
    
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
