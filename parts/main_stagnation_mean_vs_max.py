"""
This file contains the main file used to compare the genetic algorithm with regards to average / mean fitness score and maximum fitness score.
Authors: Mahmut Osmanovic (mosmar99), Sebastian Tuura (tuura01), Isac Paulsson (isacpaulsson), Emil Wagman (Neobyte01), Mohammad Al Khaled (MohamadAlkhaled)
Last updated: 2024-10-02
"""

# IMPORTS
import config
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

        # Initializations and assignments
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
        self.visual = Visualization(kwargs['visualization_strategy'])

        self.MAX_STAGNANT_GENERATIONS = kwargs['MAX_STAGNANT_GENERATIONS']
        self.TOLERANCE = kwargs['TOLERANCE']
        self.GENOCIDE_PERC = kwargs['GENOCIDE_PERC']
        self.destroy = Destroy(max_stagnant_generations=self.MAX_STAGNANT_GENERATIONS, tolerance=self.TOLERANCE)

        self.curr_fitness_evaluations = 0
        self.curr_most_fit_individual = 0
        self.generations = 0
        self.iters = 100+1
    
    # create the initial population
    # input: None
    # output: population: numpy array
    def get_population(self):
        return self.init(self.GENOME_SIZE, self.POPULATION_SIZE)

    # solve function for Genetic_Algorithm with regards to max fitness score.
    # input: population: numpy array
    # output: generations: int
    def solve_max(self, population):

        is_solution = False
        self.curr_fitness_evaluations = 0
        self.curr_most_fit_individual = 0
        self.generations = 0

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
            
            # apply genetic operators & calculate fitness
            selected_parents = self.parent_selection(population, self.NUM_OFFSPRING_RATE, self.TOURNAMENT_GROUP_SIZE, self.fitness)
            offspring = self.recombination(selected_parents, self.RECOMBINATION_RATE, self.GENOME_SIZE)
            mutated_offspring = self.mutation(offspring, self.MUTATION_RATE, self.GENOME_SIZE)
            offspring_fitness = self.fitness(mutated_offspring) 
            population = self.survival_selection(population, mutated_offspring, self.fitness)
            self.curr_fitness_evaluations += (len(offspring_fitness) + len(population))

            # check if solution is found
            if (max(self.fitness(population)) == 1):
                return self.generations

            # if the best fitness score doesn't improve / stagnates we will apply genocide
            self.curr_most_fit_individual = max(self.fitness(population))
            if self.destroy.check_stagnation(self.curr_most_fit_individual):
                population = self.destroy.apply_genocide(population, self.GENOCIDE_PERC, self.fitness)

            self.generations += 1
        return self.generations
    
    # solve function for Genetic_Algorithm with regards to mean fitness score.
    # input: population: numpy array
    # output: generations: int
    def solve_mean(self, population):
        is_solution = False
        self.curr_fitness_evaluations = 0
        self.curr_most_fit_individual = 0
        self.generations = 0

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
            
            # apply genetic operators & calculate fitness
            selected_parents = self.parent_selection(population, self.NUM_OFFSPRING_RATE, self.TOURNAMENT_GROUP_SIZE, self.fitness)
            offspring = self.recombination(selected_parents, self.RECOMBINATION_RATE, self.GENOME_SIZE)
            mutated_offspring = self.mutation(offspring, self.MUTATION_RATE, self.GENOME_SIZE)
            offspring_fitness = self.fitness(mutated_offspring) 
            population = self.survival_selection(population, mutated_offspring, self.fitness)
            self.curr_fitness_evaluations += (len(offspring_fitness) + len(population))

            # check if solution is found
            if (max(self.fitness(population)) == 1):
                return self.generations

            # if the mean fitness score doesn't improve / stagnates we will apply genocide
            fitness_evals = self.fitness(population)
            if self.destroy.check_stagnation((sum(fitness_evals) / len(fitness_evals))):
                population = self.destroy.apply_genocide(population, self.GENOCIDE_PERC, self.fitness)

            self.generations += 1
        return self.generations

# "main function" comparing the genetic algorithm with regards to average / mean fitness score and maximum fitness score.
# creates a two-column lineplot visualisation of the results.
if __name__ == '__main__':
    gen_algo = Genetic_Algorithm(**config.setup_mean_or_max)
    path = config.max_vs_mean_geno
    with open(path, 'w') as logfile:
        for _ in range(gen_algo.iters-1):
            population = gen_algo.get_population()
            logfile.write(f"{gen_algo.solve_max(population)},{gen_algo.solve_mean(population)}\n")
    gen_algo.visual.lineplot_2col(path, gen_algo.GENOME_SIZE)
