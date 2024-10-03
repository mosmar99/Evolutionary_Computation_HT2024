"""
This file contains the main file used to compare different setups of the genetic algorithm using parameter tuning & threading, visualised using a bar chart.
Authors: Mahmut Osmanovic (mosmar99), Sebastian Tuura (tuura01), Isac Paulsson (isacpaulsson), Emil Wagman (Neobyte01), Mohammad Al Khaled (MohamadAlkhaled)
Last updated: 2024-10-02
"""

# IMPORTS
import config
import time
import concurrent.futures, multiprocessing
from threading import Lock
from init_pop import Init_Pop
from fitness import Fitness_Function
from mutation import Mutation
from recombination import Recombination
from survival_selection import Survival_Selection
from parent_selection import Parent_Selection
from termination import Termination
from visuals import Visualization
from parameter_tuning import Parameter_Tuning
import numpy as np  


# Genetic Algorithm class
class Genetic_Algorithm_Avg:
    # init function for Genetic_Algorithm class
    # input: **kwargs , contains the information about the setup we want to run.
    # output: None
    def __init__(self, **kwargs):
        # Not included in Parameter Search
        self.GENOME_SIZE = 8 # N-QUEENS (EX: 'every Queen has a genome size of 8')
        self.MAX_FITNESS_EVALUATIONS = 10000
        self.fitness_function = Fitness_Function('conflict_based')
        self.fitness = lambda population: self.fitness_function(population, self.GENOME_SIZE)
        self.termination = Termination('evaluation_count')

        # Included in Parameter Search
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

        self.curr_fitness_evaluations = 0
        self.curr_most_fit_individual = 0

    # solve function for Genetic_Algorithm class
    # input: None
    # output: fitness evaluations: int
    def solve(self):
        is_solution = False
        self.curr_fitness_evaluations = 0
        self.curr_most_fit_individual = 0

        population = self.init(self.GENOME_SIZE, self.POPULATION_SIZE) # create the initial population

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
            self.curr_fitness_evaluations += (len(offspring_fitness) + len(population))
            population = self.survival_selection(population, mutated_offspring, self.fitness)

            # check if solution is found
            if (max(self.fitness(population)) == 1):
                return self.curr_fitness_evaluations
        return self.curr_fitness_evaluations
    
    # calculate the average fitness evaluations
    # input: iters: int
    # output: avg: float
    def exp_evals(self, iters):
        total = 0
        for _ in range(iters):
            total += self.solve()
        avg = total / iters
        return avg
    
    # worker function for threading
    # input: setup_idx: int, setup: dict, iters: int
    # output: tuple: (int, int)
    @staticmethod
    def worker(setup_idx, setup, iters):
        genetic_algorithm = Genetic_Algorithm_Avg(**setup)
        setup_eval_count = round(genetic_algorithm.exp_evals(iters))
        return (setup_idx, setup_eval_count)
    
    # get the topX setups
    # input: topX: int
    # output: None
    @staticmethod
    def get_topX_setups(topX):
        # file locations to read data from
        evals_file_loc = 'logs/LHS_Setups_evals.log'
        setups_file_loc = 'logs/LHS_Setups.log'
        output_file_loc = 'topX_setups.py'
        # extract the topX setups into a new file
        pt.extract_topX_setups(evals_file_loc, setups_file_loc, output_file_loc, topX)

# "main function"
# input: None
# output: None
if __name__ == '__main__':
    # some initial setup
    iters = 10
    setup_count = 2000
    topX = 50

    # create the setups using LHS
    pt = Parameter_Tuning('LHS')
    setups = pt.tuning_strategy(setup_count)
    setups = [
        {key: value.item() if isinstance(value, np.generic) else value for key, value in setup.items()}
        for setup in setups
    ]
    # save the setups to a file
    with open(config.log_path3, 'w') as log_setup:
        log_setup.write(f"iterations per setup: {iters}\namount of setups: {setup_count}\n\n{setups}")
    print("\n... created and saved setups")
    
    # run the setups using threading & max cores available
    file_lock = Lock()
    counter = 0
    with concurrent.futures.ProcessPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
        with open(config.log_path4, 'w') as log_evals:
            start_time = time.time()
            futures = []
            
            # for each setup, run the Genetic Algorithm and save the results
            for setup_idx, setup in enumerate(setups):
                future = executor.submit(Genetic_Algorithm_Avg.worker, setup_idx, setup, iters)
                futures.append(future)
            
            # save the results to a file
            for future in concurrent.futures.as_completed(futures):
                setup_idx, setup_eval_count = future.result()
                
                with file_lock:
                    log_evals.write(f"s_{setup_idx + 1},{setup_eval_count}\n")
                    counter = counter + 1
                    print(f"Loading {(counter * 100 / setup_count)}%  --({(time.time() - start_time):.2f}sec)")

    # get the topX setups and create a visualization, comparing them based on the average evaluation count
    Genetic_Algorithm_Avg.get_topX_setups(topX - 1) # crashed so added - 1
    Visualization('strategy_plot').strategy_plot(file_loc=config.log_path4, runs=iters)