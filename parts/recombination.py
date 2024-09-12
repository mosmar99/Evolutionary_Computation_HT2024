import numpy as np

class Recombination:
    def __init__(self, recombination_strategy):
        recombination_strategies = { 'cut_and_crossfill': self.cut_and_crossfill}

        self.recombination_strategy = recombination_strategies[recombination_strategy]

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
    def cut_and_crossfill(self, dad, mom, GENOME_SIZE):
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