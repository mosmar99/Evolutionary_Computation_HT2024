import numpy as np
import random

class Recombination:
    def __init__(self, recombination_strategy):
        recombination_strategies = { 'even_cut_and_crossfill': self.even_cut_and_crossfill,
                                    'one_point_crossover': self.one_point_crossover,
                                    'two_point_crossover': self.two_point_crossover,
                                    'partially_mapped_crossover': self.partially_mapped_crossover,
                                    'pmx_dp_rm': self.pmx_dp_rm,
                                    'ordered_crossover': self.ordered_crossover}

        self.recombination_strategy = recombination_strategies[recombination_strategy]
        self.strategy_name = recombination_strategy

    def __call__(self, *args, **kwargs):
        return self.recombine(*args, **kwargs)
    
    def recombine(self, selected_parents, recombination_rate, GENOME_SIZE):
        offspring = []
        for parents in selected_parents:
            offspring.extend(self.generate_offspring(parents, recombination_rate, GENOME_SIZE))
        
        return np.array(offspring)
    
    def generate_offspring(self, parents, recombination_rate, GENOME_SIZE):
        dad = parents[0]
        mom = parents[1]
        if (np.random.rand() <= recombination_rate):  
            children = self.recombination_strategy(dad, mom, GENOME_SIZE)
            return children
        else:
            return parents
    
    # at crossover point (cut_index), cutt both parents DNA and crossfill
    def even_cut_and_crossfill(self, dad, mom, GENOME_SIZE):
        child_one = []
        child_two = []
        cut_index = GENOME_SIZE/2
        for i in range(GENOME_SIZE):
            if(i < cut_index):
                child_one.append(dad[i])
                child_two.append(mom[i])
            else:
                child_one.append(mom[i])
                child_two.append(dad[i])
        return [child_one, child_two]

    # at crossover point (cut_index), cutt both parents DNA and crossfill
    def one_point_crossover(self, dad, mom, GENOME_SIZE):
        child_one = []
        child_two = []
        cut_index = np.random.randint(1, GENOME_SIZE - 1)
        for i in range(GENOME_SIZE):
            if(i < cut_index):
                child_one.append(dad[i])
                child_two.append(mom[i])
            else:
                child_one.append(mom[i])
                child_two.append(dad[i])
        return [child_one, child_two]
    
    def two_point_crossover(self, dad, mom, GENOME_SIZE):
        
        child_one = [0] * GENOME_SIZE
        child_two = [0] * GENOME_SIZE

        #choose two crossover points A & B
        crossover_point_A = np.random.randint(1, GENOME_SIZE - 1)
        crossover_point_B = np.random.randint(crossover_point_A + 1, GENOME_SIZE) # +1 to ensure they are never equal
        
        for idx in range(GENOME_SIZE):
            if crossover_point_A <= idx <= crossover_point_B:
                child_one[idx] = dad[idx]
                child_two[idx] = mom[idx]
            else:
                child_one[idx] = mom[idx]
                child_two[idx] = dad[idx]

        return [child_one, child_two]
    
    def partially_mapped_crossover(self, dad, mom, GENOME_SIZE):
        child_one = [0] * GENOME_SIZE
        child_two = [0] * GENOME_SIZE

        random_indecies = np.random.choice(GENOME_SIZE, 2, replace=False) + 1
        startidx, stopidx = np.sort(random_indecies)
        mapping = {}

        for idx in range(GENOME_SIZE):
            if startidx <= idx <= stopidx:
                child_one[idx] = dad[idx]
                child_two[idx] = mom[idx]
                mapping[dad[idx]] = mom[idx]
            else:
                child_one[idx] = mom[idx]
                child_two[idx] = dad[idx]

        for dmap, mmap in mapping.items():
            if dmap != mmap:
                indexc1 = np.where(child_one==dmap)[0][0]
                indexc2 = np.where(child_two==mmap)[0][0]
                child_one[indexc1] = mmap
                child_two[indexc2] = dmap

        return np.array([child_one, child_two])
    
    def pmx_dp_rm(self, dad, mom, GENOME_SIZE):
        child_one, child_two = self.partially_mapped_crossover(dad, mom, GENOME_SIZE)
        return np.array([self.duplicate_replacement(child_one, GENOME_SIZE), self.duplicate_replacement(child_two, GENOME_SIZE)])

    def duplicate_replacement(self, individual, GENOME_SIZE):
        valid_permutation = np.arange(1, GENOME_SIZE + 1)
        unique, counts = np.unique(individual, return_counts=True)

        duplicates = unique[counts > 1]
        missing_values = np.setdiff1d(valid_permutation, individual)

        for duplicate, missing in zip(duplicates, missing_values):
            duplicate_indices = np.where(individual == duplicate)[0]
            individual[duplicate_indices[np.random.randint(len(duplicate_indices))]] = missing

        return individual
    
    def ordered_crossover(self, dad, mom, GENOME_SIZE):

        genome_pool = np.arange(1, GENOME_SIZE + 1)

        child_one = [-1] * GENOME_SIZE
        child_two = [-1] * GENOME_SIZE

        #choose two crossover points A & B
        crossover_point_A = random.choice(genome_pool[:len(genome_pool)-1])
        crossover_point_B = random.choice(genome_pool)

        while crossover_point_A >= crossover_point_B:
            crossover_point_B = random.choice(genome_pool)

        dad_copy = dad.copy()
        mom_copy = mom.copy()

        dad_subset = dad_copy[crossover_point_A:crossover_point_B]
        mom_subset = mom_copy[crossover_point_A:crossover_point_B]
        
        dad_uniques = []
        mom_uniques = []

        [dad_uniques.append(x) for x in dad_subset if x not in dad_uniques]
        [mom_uniques.append(x) for x in mom_subset if x not in mom_uniques]

        for idx in range(crossover_point_A,crossover_point_B):
            if(idx - crossover_point_A < len(dad_uniques)):
                child_one[idx] = dad_uniques[idx - crossover_point_A]
            if(idx - crossover_point_A < len(mom_uniques)):
                child_two[idx] = mom_uniques[idx - crossover_point_A]


        for idx in range(GENOME_SIZE):
            if idx < crossover_point_A or idx >= crossover_point_B:
                if dad_copy[idx] not in child_one:
                    child_one[idx] = dad_copy[idx]
                if mom_copy[idx] not in child_two:
                    child_two[idx] = mom_copy[idx]

        missing_values_child_one = np.setdiff1d(genome_pool, child_one)
        missing_values_child_two = np.setdiff1d(genome_pool, child_two)

        
        for idx in range(len(missing_values_child_one)):
            if -1 in child_one:
                child_one[child_one.index(-1)] = int(missing_values_child_one[idx])
        
        for idx in range(len(missing_values_child_two)):
            if -1 in child_two:
                child_two[child_two.index(-1)] = int(missing_values_child_two[idx])

        return [child_one, child_two]