import numpy as np

# [_,_,3,_,_,_,8,_] -> (with prob mutation_rate, will become) -> [_,_,8,_,_,_,3,_]
class Swap_Mutation():
    def exec(self, individual, mutation_rate, GENOME_SIZE):
        if (np.random.rand() <= mutation_rate):
            # get indices of 2 random genes in the genome
            gene_idx1, gene_idx2 = np.random.choice(GENOME_SIZE, 2, replace=False)

            # return the genes at specified indices
            gene1, gene2 = individual[gene_idx1].copy(), individual[gene_idx2].copy()

            # swap the genes contents of the two genes at the specified indices
            individual[gene_idx1] = gene2
            individual[gene_idx2] = gene1
        return individual

class Mutation(object):
    def __init__(self, mutation_strategy):
        self.mutation_strategy = mutation_strategy

    # set default values to some parameters, makes them "optional"
    def mutate(self, individual, mutation_rate, GENOME_SIZE):
        return self.mutation_strategy.exec(individual, mutation_rate, GENOME_SIZE)
    