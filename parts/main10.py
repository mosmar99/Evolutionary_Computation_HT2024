"""
This file contains the main file used to compare the genetic algorithm with genocide, and static or dynamic mutation / recombination rates.
Authors: Mahmut Osmanovic (mosmar99), Sebastian Tuura (tuura01), Isac Paulsson (isacpaulsson), Emil Wagman (Neobyte01), Mohammad Al Khaled (MohamadAlkhaled)
Last updated: 2024-10-02
"""

import config
import time
from init_pop import Init_Pop
from fitness import Fitness_Function
from mutation import Mutation
from recombination import Recombination
from survival_selection import Survival_Selection
from parent_selection import Parent_Selection
from termination import Termination
from visuals import Visualization
from destroy import Destroy

# Genetic Algorithm class
class Genetic_Algorithm:
    # init function for Genetic_Algorithm class
    # input: **kwargs , contains the information about the setup we want to run.
    # output: None
    def __init__(self, **kwargs):
        
        # Some intializations and assignments
        self.GENOME_SIZE = kwargs['GENOME_SIZE'] 
        self.MAX_FITNESS_EVALUATIONS = kwargs['MAX_FITNESS_EVALUATIONS']
        self.fitness_function = Fitness_Function(kwargs['fitness_strategy'])
        self.fitness = lambda population: self.fitness_function(population, self.GENOME_SIZE)
        self.termination = Termination(kwargs['termination_strategy'])
        self.POPULATION_SIZE = kwargs['POPULATION_SIZE']
        self.NUM_OFFSPRING_RATE = kwargs['NUM_OFFSPRING_RATE']
        self.RECOMBINATION_RATE = kwargs['RECOMBINATION_RATE']
        self.MUTATION_RATE = kwargs['MUTATION_RATE']
        self.TOURNAMENT_GROUP_SIZE = kwargs['TOURNAMENT_GROUP_SIZE']
        self.init = Init_Pop(kwargs['initialization_strategy'])
        self.parent_selection = Parent_Selection(kwargs['parent_selection_strategy'])
        self.recombination = Recombination(kwargs['recombination_strategy'])
        self.mutation = Mutation(kwargs['mutation_strategy'])
        self.survival_selection = Survival_Selection(kwargs['survival_selection_strategy'])
        self.WEIGHTING_EXPONENT = kwargs['WEIGHTING_EXPONENT']
        self.visual = Visualization(kwargs['visualization_strategy'])

        self.MAX_STAGNANT_GENERATIONS = kwargs['MAX_STAGNANT_GENERATIONS']
        self.TOLERANCE = kwargs['TOLERANCE']
        self.GENOCIDE_PERC = kwargs['GENOCIDE_PERC']
        self.destroy = Destroy(max_stagnant_generations=self.MAX_STAGNANT_GENERATIONS, tolerance=self.TOLERANCE)

        self.curr_fitness_evaluations = 0
        self.curr_most_fit_individual = 0
        self.generations = 0
        self.iters = 500
        self.iters = 1

    # create the initial population
    # input: None
    # output: population: numpy array
    def get_population(self):
        return self.init(self.GENOME_SIZE, self.POPULATION_SIZE)
 
    # solve function for Genetic_Algorithm class.
    # input: population: numpy array
    # output: fitness_evals: int
    def solve(self, population):
        is_solution = False
        self.curr_fitness_evaluations = 0
        self.curr_most_fit_individual = 0
        self.generations = 100

        max_history = []
        average_history = [] 
        min_history = [] 

        max_history.append(max(self.fitness(population)))
        average_history.append(sum(self.fitness(population))/len(population))
        min_history.append(min(self.fitness(population)))

        # WITH GENOCIDE
        # while termination condition is not met
        # will terminate if:
        # - max fitness evaluations reached
        # - max iterations reached
        # - solution is found
        while( not(self.termination( curr_fitness_evaluations=self.curr_fitness_evaluations,
                                     max_fitness_evaluations=self.MAX_FITNESS_EVALUATIONS,
                                     curr_iterations=0,  
                                     max_iterations=10000, 
                                     is_solution=is_solution )) ):
            
            # calculate exploration and exploitation factors
            # set both at expected infimum to begin with
            exploration_factor = max(0.1, (self.GENOME_SIZE / (self.GENOME_SIZE + self.generations**(3/4)))) # declines to its min: 1.0 -> 0.1
            exploitation_factor = max(0.1, 1-exploration_factor) # grows to its max: 0.1 -> 1.0

            # calculate dynamic recombination and mutation rates
            dynamic_recombination_rate = self.RECOMBINATION_RATE * exploration_factor 
            dynamic_mutation_rate = self.MUTATION_RATE * exploitation_factor
            
            # apply genetic operators & calculate fitness
            selected_parents = self.parent_selection(population, self.NUM_OFFSPRING_RATE, self.TOURNAMENT_GROUP_SIZE, self.fitness)
            offspring = self.recombination(selected_parents, dynamic_recombination_rate, self.GENOME_SIZE)
            mutated_offspring = self.mutation(offspring, dynamic_mutation_rate, self.GENOME_SIZE)
            offspring_fitness = self.fitness(mutated_offspring) 
            population = self.survival_selection(population, mutated_offspring, self.fitness, self.WEIGHTING_EXPONENT)
            self.curr_fitness_evaluations += (len(offspring_fitness) + len(population))

            max_history.append(max(self.fitness(population)))
            average_history.append(sum(self.fitness(population))/len(population))
            min_history.append(min(self.fitness(population)))

            if (max(self.fitness(population)) == 1):
                return self.curr_fitness_evaluations, max_history, average_history, min_history

            self.curr_most_fit_individual = max(self.fitness(population))
            genocide_factor = max(1/6, 1 - (self.GENOME_SIZE / (self.GENOME_SIZE + self.generations**(3/4)))) # declines to its min: 1.0 -> 0.1
            dynamic_genocide_perc = self.GENOCIDE_PERC * genocide_factor
            if self.destroy.check_stagnation(self.curr_most_fit_individual):
                population = self.destroy.apply_genocide(population, dynamic_genocide_perc, self.fitness)

            self.generations += 1
        return self.curr_fitness_evaluations, max_history, average_history, min_history
    
    # Worker function for running a genetic algorithm over multiple iterations
    # input: iters: int - the number of iterations to run the algorithm
    # output: tuple: (float, List[float], List[float], List[float]) 
    def worker(self, iters):
        tot_max_history = []
        tot_average_history = []
        tot_min_history = []
        avg_gens = 0
        for _ in range(iters):
            curr_fitness_evaluations, max_history, average_history, min_history = self.solve(self.get_population())
            tot_max_history.append(max_history)
            tot_average_history.append(average_history)
            tot_min_history.append(min_history)
            avg_gens += curr_fitness_evaluations
        return round(avg_gens / iters, 2), pad_and_average(tot_max_history), pad_and_average(tot_average_history), pad_and_average(tot_min_history)

# Function to pad lists and calculate their average values
# input: lists: List[List[float]] - a list of lists containing numerical values
# output: List[float] - a list of average values computed from the input lists
def pad_and_average(lists):
    max_len = max([len(ls) for ls in lists])
    averages = []
    for x in range(max_len):
        num = 0
        tot = 0
        for y in range(len(lists)):
            num += 1
            if len(lists[y]) > x:
                tot += lists[y][x]
            else:
                tot += lists[y][-1]
        averages.append(tot/num)

    return averages


# "main function" for genetic algorithm
# for different weighting exponents and logging the results
# output: None - results are appended to eval_counts and written to a log file
if __name__ == '__main__':
    eval_counts = []

    exponent = 0
    ga = Genetic_Algorithm(WEIGHTING_EXPONENT=exponent,**config.setup_final)
    eval_counts.append(ga.worker(ga.iters))
    print(f"progress {1}%")

    exponent = 15
    ga = Genetic_Algorithm(WEIGHTING_EXPONENT=exponent,**config.setup_final)
    eval_counts.append(ga.worker(ga.iters))
    print(f"progress {2}%")

    exponent = 50
    ga = Genetic_Algorithm(WEIGHTING_EXPONENT=exponent,**config.setup_final)
    eval_counts.append(ga.worker(ga.iters))
    print(f"progress {3}%")

    with open(config.exponent_out, 'w') as log_file:
        for res in eval_counts:
            log_file.write(f"{res[1]},,{res[2]},,{res[3]}\n")
    
    Visualization('terminal').exponent_convergance_plot(config.exponent_out, ga.iters)
