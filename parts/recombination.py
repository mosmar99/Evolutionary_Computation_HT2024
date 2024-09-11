import numpy as np

# at crossover point (cut_index), cutt both parents DNA and crossfill
def cut_and_crossfill(dad, mom, GENOME_SIZE):
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

class Cut_And_Crossfill():
    def exec(self, selected_parents, recombination_rate, GENOME_SIZE):
        if (np.random.rand() <= recombination_rate):
            dad = selected_parents[0]
            mom = selected_parents[1]
            children = cut_and_crossfill(dad, mom, GENOME_SIZE)
            return children
        else:
            return selected_parents

class Recombination(object):
    def __init__(self, recombination_strategy):
        self.recombination_strategy = recombination_strategy
    
    def recombine(self, selected_parents, recombination_rate, GENOME_SIZE):
        return self.recombination_strategy.exec(selected_parents, recombination_rate, GENOME_SIZE)