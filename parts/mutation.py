import numpy as np

class Mutation:
    def __init__(self, mutation_strategy):
        mutation_strategies = {'swap_mutation': self.swap_mutation}
        
        self.mutation_strategy = mutation_strategies[mutation_strategy]
    
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


if __name__ == '__main__':
    population = Mutation('random')()