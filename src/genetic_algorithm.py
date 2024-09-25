"""
Need to break out dynamic genocide
Need to break out stagnation
"""

# IMPORTS
import src.config as config
import time
import concurrent.futures, multiprocessing
from threading import Lock
from src.init_pop import Init_Pop
from src.fitness import Fitness_Function
from src.mutation import Mutation
from src.recombination import Recombination
from src.survival_selection import Survival_Selection
from src.parent_selection import Parent_Selection
from src.utils.termination import Termination
from src.utils.visuals import Visualization
from src.parameter_tuning import Parameter_Tuning

class Genetic_Algorithm:
    def __init__(self, **kwargs):
        # Strategies
        self.init                    =              Init_Pop(kwargs.get('initialization_strategy', config.default_setup['initialization_strategy']))
        self.parent_selection        =              Parent_Selection(kwargs.get('parent_selection_strategy', config.default_setup['parent_selection_strategy']))
        self.recombination           =              Recombination(kwargs.get('recombination_strategy', config.default_setup['recombination_strategy']))
        self.mutation                =              Mutation(kwargs.get('mutation_strategy', config.default_setup['mutation_strategy']))
        self.survival_selection      =              Survival_Selection(kwargs.get('survival_selection_strategy', config.default_setup['survival_selection_strategy']))
        self.termination             =              Termination(kwargs.get('termination_strategy', config.default_setup['termination_strategy']))
        self.fitness_function        =              Fitness_Function(kwargs.get('fitness_strategy', config.default_setup['fitness_strategy']))

        # Parameters
        self.POPULATION_SIZE         =              kwargs.get('POPULATION_SIZE', config.default_setup['POPULATION_SIZE'])
        self.GENOME_SIZE             =              kwargs.get('GENOME_SIZE', config.default_setup['GENOME_SIZE'])
        self.MAX_FITNESS_EVALUATIONS =              kwargs.get('MAX_FITNESS_EVALUATIONS', config.default_setup['MAX_FITNESS_EVALUATIONS'])
        self.fitness                 =              lambda population: self.fitness_function(population, self.GENOME_SIZE)
        self.NUM_OFFSPRING_RATE      =              kwargs.get('NUM_OFFSPRING_RATE', config.default_setup['NUM_OFFSPRING_RATE'])
        self.MUTATION_RATE           =              kwargs.get('MUTATION_RATE', config.default_setup['MUTATION_RATE'])
        self.TOURNAMENT_GROUP_SIZE   =              kwargs.get('TOURNAMENT_GROUP_SIZE', config.default_setup['TOURNAMENT_GROUP_SIZE'])
        self.RECOMBINATION_RATE      =              kwargs.get('RECOMBINATION_RATE', config.default_setup['RECOMBINATION_RATE'])

        self.curr_fitness_evaluations = 0
        self.curr_most_fit_individual = 0
        self.generations = 0
        self.iters = kwargs.get('ITERS', 100+1)

    def get_population(self):
        return self.init(self.GENOME_SIZE, self.POPULATION_SIZE)

    def solve(self, population = None):
        is_solution = False
        self.curr_fitness_evaluations = 0
        self.curr_most_fit_individual = 0

        if population is None:
            population = self.get_population()

        while( not(self.termination( curr_fitness_evaluations=self.curr_fitness_evaluations,
                                     max_fitness_evaluations=self.MAX_FITNESS_EVALUATIONS,
                                     curr_iterations=0,  
                                     max_iterations=10000, 
                                     is_solution=is_solution )) ):
            
            selected_parents = self.parent_selection(population, self.NUM_OFFSPRING_RATE, self.TOURNAMENT_GROUP_SIZE, self.fitness)
            offspring = self.recombination(selected_parents, self.RECOMBINATION_RATE, self.GENOME_SIZE)
            mutated_offspring = self.mutation(offspring, self.MUTATION_RATE, self.GENOME_SIZE)
            offspring_fitness = self.fitness(mutated_offspring) 
            self.curr_fitness_evaluations += (len(offspring_fitness) + len(population))
            population = self.survival_selection(population, mutated_offspring, self.fitness)

            if (max(self.fitness(population)) == 1):
                return self.curr_fitness_evaluations
        return self.curr_fitness_evaluations
    
    def exp_evals(self, iters):
        total = 0
        for _ in range(iters):
            total += self.solve()
        avg = total / iters
        return avg

    @staticmethod
    def worker(setup_idx, setup, attribute, iters):
        genetic_algorithm = Genetic_Algorithm(**setup)
        setup_eval_count = round(genetic_algorithm.exp_evals(iters))
        return_attribute = None
        try:
            return_attribute = setup[attribute]
        except:
            return_attribute = None
        return (setup_idx, setup_eval_count, return_attribute)
    
    @staticmethod
    def get_topX_setups(topX, pt):
        evals_file_loc = 'logs/LHS_Setups_evals.log'
        setups_file_loc = 'logs/LHS_Setups.log'
        output_file_loc = 'topX_setups.py'
        pt.extract_topX_setups(evals_file_loc, setups_file_loc, output_file_loc, topX)