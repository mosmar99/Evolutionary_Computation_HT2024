import numpy as np

class Metric():
    def __init__(self, metric_strategy):
        metric_strategies = { 'avg_similarity': self.avg_similarity }
        self.metric_strategy = metric_strategies[metric_strategy]

    def __call__(self, *args, **kwargs):
        return self.metric_strategy(*args, **kwargs)   

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
    def avg_similarity(self, offspring, population):
        total_similarity = 0
        population_sample = population[np.random.choice(population.shape[0], int(population.shape[0]*0.5), replace=False)]
        for ind in population_sample:
            for child in offspring:
                total_similarity += self.element_wise_similarity(child, ind)
        
        return total_similarity / (len(offspring) * len(population_sample))