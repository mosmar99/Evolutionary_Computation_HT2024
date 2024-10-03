"""
This file contains the main file used to compare different setups of the genetic algorithm using parameter tuning & threading, visualised using a density heatmap.
Authors: Mahmut Osmanovic (mosmar99), Sebastian Tuura (tuura01), Isac Paulsson (isacpaulsson), Emil Wagman (Neobyte01), Mohammad Al Khaled (MohamadAlkhaled)
Last updated: 2024-10-02
"""

# IMPORTS
import config
import time
import concurrent.futures, multiprocessing
import numpy as np
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


# Genetic Algorithm class
class Genetic_Algorithm_Avg:
    # init function for Genetic_Algorithm class
    # input: **kwargs , contains the information about the setup we want to run.
    # output: None
    def __init__(self, **kwargs):
        # Not included in Parameter Search
        self.GENOME_SIZE = config.constants['GENOME_SIZE'] # N-QUEENS (EX: 'every Queen has a genome size of 8')
        self.MAX_FITNESS_EVALUATIONS = 10000
        self.fitness_function = Fitness_Function('conflict_based')
        self.termination = Termination('evaluation_count')
        self.TOURNAMENT_GROUP_SIZE = config.constants['TOURNAMENT_GROUP_SIZE']
        # self.TOURNAMENT_GROUP_SIZE = kwargs['TOURNAMENT_GROUP_SIZE']
        self.POPULATION_SIZE = config.constants['POPULATION_SIZE']
        # self.POPULATION_SIZE = kwargs['POPULATION_SIZE']
        self.NUM_OFFSPRING_RATE = config.constants['NUM_OFFSPRING_RATE']
        # self.NUM_OFFSPRING_RATE = kwargs['NUM_OFFSPRING_RATE']

        # Included in Parameter Search
        self.MUTATION_RATE = kwargs['MUTATION_RATE']
        self.RECOMBINATION_RATE = kwargs['RECOMBINATION_RATE']
        self.init = Init_Pop(kwargs['initialization_strategy'])
        self.parent_selection = Parent_Selection(kwargs['parent_selection_strategy'])
        self.recombination = Recombination(kwargs['recombination_strategy'])
        self.mutation = Mutation(kwargs['mutation_strategy'])
        self.survival_selection = Survival_Selection(kwargs['survival_selection_strategy'])

        self.fitness = self.calculate_fitness

        self.curr_fitness_evaluations = 0
        self.curr_most_fit_individual = 0

    # calculate fitness function
    # input: population: numpy array
    # output: fitness scores: numpy array
    def calculate_fitness(self, population):
        return self.fitness_function(population, self.GENOME_SIZE)
    
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
        return (setup_idx, setup_eval_count, genetic_algorithm)
    
    # get the topX setups
    # input: topX: int
    # output: None
    @staticmethod
    def get_topX_setups(topX):
        evals_file_loc = config.final_2000x10
        setups_file_loc = config.final_2000_setups
        output_file_loc = 'topX_setups.py'
        pt.extract_topX_setups(evals_file_loc, setups_file_loc, output_file_loc, topX)

# Main function
if __name__ == '__main__':
    # get the configurations from the config file
    iters = config.iters
    setup_count = config.setup_count
    pt = Parameter_Tuning('LHS')
    setups = pt.tuning_strategy(setup_count)

    # save the setups to a file
    with open(config.test_setups, 'w') as log_setup:
        log_setup.write(f"Iterations per setup: {iters}.\nAmount of Setups: {setup_count}.\n\n{setups}")
    print("\n... created and saved setups")
    

    # run the Genetic Algorithm for each setup using threading and max available cores
    file_lock = Lock()
    counter = 0
    with concurrent.futures.ProcessPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
        with open(config.test_results, 'w') as log:
            # print headers to file.
            log.write("setup_id,mutation_strategy,recombination_strategy,parent_selection_strategy,initialization_strategy,POPULATION_SIZE,NUM_OFFSPRING_RATE,RECOMBINATION_RATE,MUTATION_RATE,TOURNAMENT_GROUP_SIZE,evaluation_count\n")

            start_time = time.time()
            futures = []
            
            # run the Genetic Algorithm for each setup
            for setup_idx, setup in enumerate(setups):
                future = executor.submit(Genetic_Algorithm_Avg.worker, setup_idx, setup, iters)
                futures.append(future)
            
            # write the results to the file
            for future in concurrent.futures.as_completed(futures):
                setup_idx, setup_eval_count, genetic_algorithm = future.result()

                # strings
                mutation_strategy = genetic_algorithm.mutation.strategy_name
                recombination_strategy = genetic_algorithm.recombination.strategy_name
                parent_selection_strategy = genetic_algorithm.parent_selection.strategy_name
                initialization_strategy = genetic_algorithm.init.strategy_name

                # numbers
                population_size = config.constants['POPULATION_SIZE']
                num_offspring_rate = config.constants['NUM_OFFSPRING_RATE']
                recombination_rate = genetic_algorithm.RECOMBINATION_RATE
                mutation_rate = genetic_algorithm.MUTATION_RATE
                tournament_group_size = config.constants['TOURNAMENT_GROUP_SIZE']
                
                with file_lock:
                    log.write(f"s_{setup_idx + 1},{mutation_strategy},{recombination_strategy},{parent_selection_strategy},{initialization_strategy},{population_size},{num_offspring_rate},{recombination_rate},{mutation_rate},{tournament_group_size},{setup_eval_count}\n")
                    counter = counter + 1
                    print(f"Loading {(counter * 100 / setup_count)}%  --({(time.time() - start_time):.2f}sec)")
    
    # create a density heatmap of the results
    folder = config.test_results
    n = config.constants['GENOME_SIZE']
    iters = config.iters
    setup_count = config.setup_count
    Visualization('px_density_hp').create_density_heatmap(folder, iters, n, setup_count)