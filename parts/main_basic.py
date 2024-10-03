"""
This file contains a basic implementation of a genetic algorithm for solving the N-Queens problem.
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
from metric import Metric
from log import Log
from visuals import Visualization
from filehandler import File_Handler

# Genetic Algorithm class
class Genetic_Algorithm_FE:
    # init function for Genetic_Algorithm class
    # input: **kwargs , contains the information about the setup we want to run.
    # output: None
    def __init__(self, **kwargs):
        # Initializations and assignments

        self.GENOME_SIZE = kwargs['GENOME_SIZE']
        self.POPULATION_SIZE = kwargs['POPULATION_SIZE']
        self.NUM_OFFSPRING_RATE = kwargs['NUM_OFFSPRING_RATE']
        self.RECOMBINATION_RATE = kwargs['RECOMBINATION_RATE']
        self.MUTATION_RATE = kwargs['MUTATION_RATE']
        self.MAX_FITNESS_EVALUATIONS = kwargs['MAX_FITNESS_EVALUATIONS']
        self.TOURNAMENT_GROUP_SIZE = kwargs['TOURNAMENT_GROUP_SIZE']

        self.init = Init_Pop(kwargs['initialization_strategy'])

        self.fitness_function = Fitness_Function(kwargs['fitness_strategy'])
        self.fitness = lambda population: self.fitness_function(population, self.GENOME_SIZE)
        self.parent_selection = Parent_Selection(kwargs['parent_selection_strategy'])
        self.survival_selection = Survival_Selection(kwargs['survival_selection_strategy'])
        self.recombination = Recombination(kwargs['recombination_strategy'])
        self.mutation = Mutation(kwargs['mutation_strategy'])
        self.visual = Visualization(kwargs['visualization_strategy'])
        self.termination = Termination(kwargs['termination_strategy'])
        self.metric = Metric(kwargs['metric_strategy'])
        self.logger = Log(kwargs['logging_strategy'])

        self.fileprinter = File_Handler(kwargs['print_type'])

        self.curr_fitness_evaluations = 0
        self.curr_most_fit_individual = 0

    # solve function for Genetic_Algorithm class, with dynamic genocide
    # input: population: numpy array
    # output: None
    def solve(self):
        is_solution = False
        self.curr_fitness_evaluations = 0
        self.curr_most_fit_individual = 0
        similarity_threshold = 0.4

        population = self.init(self.GENOME_SIZE, self.POPULATION_SIZE) # Create initial population

        # first evaluation
        if self.curr_fitness_evaluations == 0:
            self.curr_most_fit_individual = max(self.fitness(population))
            print("\nEvaluation Count: %8d  |  %8f" % (self.curr_fitness_evaluations, self.curr_most_fit_individual))
            print("")
            self.print(self.curr_fitness_evaluations, self.curr_most_fit_individual)

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
            
            # Selection, recombination, mutation, and survival selection
            selected_parents = self.parent_selection(population, self.NUM_OFFSPRING_RATE, self.TOURNAMENT_GROUP_SIZE, self.fitness)
            offspring = self.recombination(selected_parents, self.RECOMBINATION_RATE, self.GENOME_SIZE)
            mutated_offspring = self.mutation(offspring, self.MUTATION_RATE, self.GENOME_SIZE)

            # Evaluation
            avg_sim = self.metric(mutated_offspring, population)
            offspring_fitness = self.fitness(mutated_offspring) 
            self.logger(self.curr_fitness_evaluations, avg_sim, offspring_fitness)
            self.curr_fitness_evaluations += (len(offspring_fitness) +  len(population))
            
            # Survival selection based on similarity
            if (avg_sim < similarity_threshold):
                population = self.survival_selection(population, mutated_offspring, self.fitness)

            # print current evaluation count and most fit individual every 500 evaluations
            if (self.curr_fitness_evaluations % 500 == 0):
                self.curr_most_fit_individual = max(self.fitness(population))
                print("Evaluation Count: %8d  |  %8f" % (self.curr_fitness_evaluations, self.curr_most_fit_individual))
                self.print(self.curr_fitness_evaluations, self.curr_most_fit_individual)

            # check if solution is found
            if (max(self.fitness(population)) == 1):
                avg_sim = self.metric(mutated_offspring, population)
                sol_fitness = max(self.fitness(population))
                self.logger(self.curr_fitness_evaluations, avg_sim, sol_fitness)
                is_solution = True

        # create a visualization of the best individual
        best_individual = max(population, key=self.fitness)
        self.visual(best_individual, self.fitness)
        self.visual.html_sim_eval(config.log_path)

    # print function for Genetic_Algorithm class
    # input: evals: int, most_fit: float
    # output: None
    def print(self, evals, most_fit):
        to_print = {
            'CURR_FITNESS_EVALUATIONS': evals,
            'CURR_MOST_FIT_INDIVIDUAL': most_fit,
            'GENOME_SIZE': self.GENOME_SIZE,
            'POPULATION_SIZE': self.POPULATION_SIZE,
            'NUM_OFFSPRING_RATE': self.NUM_OFFSPRING_RATE,
            'RECOMBINATION_RATE': self.RECOMBINATION_RATE,
            'MUTATION_RATE': self.MUTATION_RATE,
            'MAX_FITNESS_EVALUATIONS': self.MAX_FITNESS_EVALUATIONS,

            'initialization_strategy': self.init.strategy_name,
            'fitness_strategy': self.fitness_function.strategy_name,
            'parent_selection_strategy': self.parent_selection.strategy_name,
            'survival_selection_strategy': self.survival_selection.strategy_name,
            'recombination_strategy': self.recombination.strategy_name,
            'mutation_strategy': self.mutation.strategy_name,
        }
        self.fileprinter.csv_file(**to_print)

# "main function"
# input: None
# output: None
if __name__ == '__main__':
    # Initialize the Genetic Algorithm class with the setup from the config file
    ga = Genetic_Algorithm_FE(**config.setup) # FE = y = Fitness. E = Evals.
    ga.solve()