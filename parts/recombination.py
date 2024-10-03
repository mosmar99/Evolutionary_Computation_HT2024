"""
This file contains the recombination class which is responsible for recombining the selected parents to create offspring.
Authors: Mahmut Osmanovic (mosmar99), Sebastian Tuura (tuura01), Isac Paulsson (isacpaulsson), Emil Wagman (Neobyte01), Mohammad Al Khaled (MohamadAlkhaled)
Last updated: 2024-10-02
"""

import numpy as np

# Recombination class
class Recombination:
    # init function for Recombination class
    # input: recombination_strategy: string
    # output: None
    def __init__(self, recombination_strategy):
        recombination_strategies = { 'even_cut_and_crossfill': self.even_cut_and_crossfill,
                                    'one_point_crossover': self.one_point_crossover,
                                    'two_point_crossover': self.two_point_crossover,
                                    'partially_mapped_crossover': self.partially_mapped_crossover,
                                    'pmx_dp_rm': self.pmx_dp_rm,
                                    'ordered_crossover': self.ordered_crossover}

        self.recombination_strategy = recombination_strategies[recombination_strategy]
        self.strategy_name = recombination_strategy

    # call function for Recombination class
    # input: *args, **kwargs
    # output: self.recombine(*args, **kwargs)
    def __call__(self, *args, **kwargs):
        return self.recombine(*args, **kwargs)
    
    # recombines the selected parents to create offspring
    # input: selected_parents: numpy array, recombination_rate: float, GENOME_SIZE: int
    # output: numpy array
    def recombine(self, selected_parents, recombination_rate, GENOME_SIZE):
        offspring = []
        for parents in selected_parents:
            offspring.extend(self.generate_offspring(parents, recombination_rate, GENOME_SIZE))
        
        return np.array(offspring)
    
    # generates offspring from two parents according to the recombination rate
    # input: parents: numpy array, recombination_rate: float, GENOME_SIZE: int
    # output: numpy array of parents incase of no recombination, otherwise numpy array of offspring
    def generate_offspring(self, parents, recombination_rate, GENOME_SIZE):
        dad = parents[0]
        mom = parents[1]
        if (np.random.rand() <= recombination_rate):  
            children = self.recombination_strategy(dad, mom, GENOME_SIZE)
            return children
        else:
            return parents
    
    # at crossover point (cut_index), cutt both parents DNA and crossfill
    # input: dad: numpy array, mom: numpy array, GENOME_SIZE: int
    # output: numpy array of two children
    def even_cut_and_crossfill(self, dad, mom, GENOME_SIZE):
        child_one = []
        child_two = []
        cut_index = GENOME_SIZE/2 # cut in the middle
        for i in range(GENOME_SIZE): # crossfill
            if(i < cut_index):
                child_one.append(dad[i])
                child_two.append(mom[i])
            else:
                child_one.append(mom[i])
                child_two.append(dad[i])
        return [child_one, child_two]

    # at crossover point (cut_index), cutt both parents DNA and crossfill
    # input: dad: numpy array, mom: numpy array, GENOME_SIZE: int
    # output: numpy array of two children
    # https://en.wikipedia.org/wiki/Crossover_(genetic_algorithm)#One-point_crossover
    def one_point_crossover(self, dad, mom, GENOME_SIZE):
        child_one = []
        child_two = []
        cut_index = np.random.randint(1, GENOME_SIZE - 1) # cut at random index
        for i in range(GENOME_SIZE): # crossfill
            if(i < cut_index):
                child_one.append(dad[i])
                child_two.append(mom[i])
            else:
                child_one.append(mom[i])
                child_two.append(dad[i])
        return [child_one, child_two]
    
    # at two crossover points (A & B), cutt both parents DNA and crossfill
    # input: dad: numpy array, mom: numpy array, GENOME_SIZE: int
    # output: numpy array of two children
    # https://en.wikipedia.org/wiki/Crossover_(genetic_algorithm)#Two-point_and_k-point_crossover
    def two_point_crossover(self, dad, mom, GENOME_SIZE):
        
        child_one = [0] * GENOME_SIZE
        child_two = [0] * GENOME_SIZE

        #choose two crossover points A & B
        crossover_point_A = np.random.randint(1, GENOME_SIZE - 1)
        crossover_point_B = np.random.randint(crossover_point_A + 1, GENOME_SIZE) # +1 to ensure they are never equal
        
        for idx in range(GENOME_SIZE): # crossfill
            if crossover_point_A <= idx <= crossover_point_B:
                child_one[idx] = dad[idx]
                child_two[idx] = mom[idx]
            else:
                child_one[idx] = mom[idx]
                child_two[idx] = dad[idx]

        return [child_one, child_two]
    
    # partially mapped crossover
    # input: dad: numpy array, mom: numpy array, GENOME_SIZE: int
    # output: numpy array of two children
    # https://www.baeldung.com/cs/ga-pmx-operator#partially-mapped-crossover-pmx
    def partially_mapped_crossover(self, dad, mom, GENOME_SIZE):
        child_one = [0] * GENOME_SIZE
        child_two = [0] * GENOME_SIZE

        #choose two crossover points A & B
        random_indecies = np.random.choice(GENOME_SIZE, 2, replace=False) + 1
        startidx, stopidx = np.sort(random_indecies)
        mapping = {}

        for idx in range(GENOME_SIZE): # Copy the Middle Segment
            if startidx <= idx <= stopidx:
                child_one[idx] = dad[idx]
                child_two[idx] = mom[idx]
                mapping[dad[idx]] = mom[idx]
            else:
                child_one[idx] = mom[idx]
                child_two[idx] = dad[idx]

        for dmap, mmap in mapping.items(): # Determine the Mapping
            if dmap != mmap:
                indexc1 = np.where(child_one==dmap)[0][0]
                indexc2 = np.where(child_two==mmap)[0][0]
                child_one[indexc1] = mmap
                child_two[indexc2] = dmap

        return np.array([child_one, child_two])
    
    # partially mapped crossover with duplicate replacement
    # input: dad: numpy array, mom: numpy array, GENOME_SIZE: int
    # output: numpy array of two children
    def pmx_dp_rm(self, dad, mom, GENOME_SIZE):
        # perform partially mapped crossover
        child_one, child_two = self.partially_mapped_crossover(dad, mom, GENOME_SIZE)
        # perform duplicate replacement & return children
        return np.array([self.duplicate_replacement(child_one, GENOME_SIZE), self.duplicate_replacement(child_two, GENOME_SIZE)])

    # duplicate replacement
    # input: individual: numpy array, GENOME_SIZE: int
    # output: numpy array
    def duplicate_replacement(self, individual, GENOME_SIZE):
        # create a valid permutation & find duplicates to replace

        valid_permutation = np.arange(1, GENOME_SIZE + 1)
        unique, counts = np.unique(individual, return_counts=True)

        duplicates = unique[counts > 1]
        missing_values = np.setdiff1d(valid_permutation, individual)

        for duplicate, missing in zip(duplicates, missing_values):
            duplicate_indices = np.where(individual == duplicate)[0]
            individual[duplicate_indices[np.random.randint(len(duplicate_indices))]] = missing

        return individual # return individual with duplicates replaced
    
    # ordered crossover
    # input: dad: numpy array, mom: numpy array, GENOME_SIZE: int
    # output: numpy array of two children
    def ordered_crossover(self, dad, mom, GENOME_SIZE):

        # Create a pool of all possible values
        genome_pool = np.arange(1, GENOME_SIZE + 1)

        child_one = [-1] * GENOME_SIZE
        child_two = [-1] * GENOME_SIZE

        #choose two crossover points A & B
        crossover_point_A = np.random.randint(1, GENOME_SIZE - 1)
        crossover_point_B = np.random.randint(crossover_point_A + 1, GENOME_SIZE) # +1 to ensure they are never equal

        # create copies of parents and create subsets between crossover points
        dad_copy = dad.copy()
        mom_copy = mom.copy()

        dad_subset = dad_copy[crossover_point_A:crossover_point_B]
        mom_subset = mom_copy[crossover_point_A:crossover_point_B]

        # Find unique values in subsets        
        dad_uniques = []
        mom_uniques = []

        [dad_uniques.append(x) for x in dad_subset if x not in dad_uniques]
        [mom_uniques.append(x) for x in mom_subset if x not in mom_uniques]

        # Fill in the crossover points with the unique values
        for idx in range(crossover_point_A,crossover_point_B):
            if(idx - crossover_point_A < len(dad_uniques)):
                child_one[idx] = dad_uniques[idx - crossover_point_A]
            if(idx - crossover_point_A < len(mom_uniques)):
                child_two[idx] = mom_uniques[idx - crossover_point_A]

        # Fill in the rest of the children with the remaining values
        for idx in range(GENOME_SIZE):
            if idx < crossover_point_A or idx >= crossover_point_B:
                if dad_copy[idx] not in child_one:
                    child_one[idx] = dad_copy[idx]
                if mom_copy[idx] not in child_two:
                    child_two[idx] = mom_copy[idx]

        # get the missing values from the genome pool
        missing_values_child_one = np.setdiff1d(genome_pool, child_one)
        missing_values_child_two = np.setdiff1d(genome_pool, child_two)

        # Fill in the missing values
        for idx in range(len(missing_values_child_one)):
            if -1 in child_one:
                child_one[child_one.index(-1)] = int(missing_values_child_one[idx])
        
        for idx in range(len(missing_values_child_two)):
            if -1 in child_two:
                child_two[child_two.index(-1)] = int(missing_values_child_two[idx])

        return [child_one, child_two]