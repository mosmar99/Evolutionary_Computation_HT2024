import numpy as np

class Mutation:
    def __init__(self, mutation_strategy):
        mutation_strategies = {'swap_mutation': self.swap_mutation,
                               'inversion_mutation': self.inversion_mutation,
                               'duplicate_replacement': self.duplicate_replacement,
                               'creep_mutation': self.creep_mutation,
                               'scramble_mutation': self.scramble_mutation}
        
        self.mutation_strategy = mutation_strategies[mutation_strategy]
        self.strategy_name = mutation_strategy
    
    def __call__(self, *args, **kwargs):
        return self.mutate(*args, **kwargs)
    
    def mutate(self, offspring, mutation_rate, GENOME_SIZE):
        for i in range(len(offspring)):
            if (np.random.rand() <= mutation_rate):
                offspring[i] = self.mutation_strategy(offspring[i], GENOME_SIZE)
        return offspring
    
    # [_,_,3,_,_,_,8,_] -> (with prob mutation_rate, will become) -> [_,_,8,_,_,_,3,_]
    def swap_mutation(self, individual, GENOME_SIZE):
        # get indices of 2 random genes in the genome
        gene_idx1, gene_idx2 = np.random.choice(GENOME_SIZE, 2, replace=False)

        # return the genes at specified indices
        gene1, gene2 = individual[gene_idx1].copy(), individual[gene_idx2].copy()

        # swap the genes contents of the two genes at the specified indices
        individual[gene_idx1] = gene2
        individual[gene_idx2] = gene1
        return individual

    def inversion_mutation(self, individual, GENOME_SIZE):
        # get indices of 2 random genes in the genome not including the edges
        random_indecies = np.random.choice(GENOME_SIZE-2, 2, replace=False) + 1
        startidx, stopidx = np.sort(random_indecies)
        individual_copy = individual.copy()
        # Inverse between selected indecies
        for i in range(stopidx - startidx + 1):
            individual[startidx+i] = individual_copy[stopidx-i]

        return individual
    
    # Replaces one duplicate value with missing ones.
    def duplicate_replacement(self, individual, GENOME_SIZE):
        valid_permutation = np.arange(1, GENOME_SIZE + 1)
        unique, counts = np.unique(individual, return_counts=True)

        duplicates = unique[counts > 1]
        missing_values = np.setdiff1d(valid_permutation, individual)

        for duplicate, missing in zip(duplicates, missing_values):
            duplicate_indices = np.where(individual == duplicate)[0]
            individual[duplicate_indices[np.random.randint(len(duplicate_indices))]] = missing

        return individual
    
    def creep_mutation(self, individual, GENOME_SIZE):
        rd_col_idx = np.random.choice(GENOME_SIZE)

        if individual[rd_col_idx] > 0 and individual[rd_col_idx] < GENOME_SIZE:
            up_or_down = np.random.choice([-1, 1])
            individual[rd_col_idx] += up_or_down
        elif individual[rd_col_idx] == 0:
            individual[rd_col_idx] += 1
        elif individual[rd_col_idx] == GENOME_SIZE:
            individual[rd_col_idx] -= 1
        else:
            raise ValueError(f"Unexpected value in '{individual[rd_col_idx]}'")
        
        return individual
        
    def scramble_mutation(self, individual, GENOME_SIZE):
        random_size = np.random.randint(1, GENOME_SIZE+1)
        random_genetical_subset = np.random.choice(GENOME_SIZE, size=random_size, replace=False)
        for i in range(len(random_genetical_subset)):
            gene_idx = random_genetical_subset[i]
            individual[gene_idx] = np.random.choice(GENOME_SIZE) + 1
        return individual
    
if __name__ == '__main__':
    GENOME_SIZE = 8
    individual = np.random.randint(1, GENOME_SIZE+1, size=GENOME_SIZE)
    mut_obj = Mutation('creep_mutation')
    print(individual)
    mut_obj.scramble_mutation(individual, GENOME_SIZE)
    print(individual)