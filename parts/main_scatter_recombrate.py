"""
This file contains the main file used to compare the genetic algorithm with genocide, and static or dynamic mutation / recombination rates.
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

# Genetic Algorithm class
class Genetic_Algorithm_Avg:
    # init function for Genetic_Algorithm class
    # input: **kwargs , contains the information about the setup we want to run.
    # output: None
    def __init__(self, **kwargs):
        # Not included in Parameter Search
        self.POPULATION_SIZE = 100
        self.GENOME_SIZE = 9 # N-QUEENS (EX: 'every Queen has a genome size of 8')
        self.MAX_FITNESS_EVALUATIONS = 10000
        self.fitness_function = Fitness_Function('conflict_based')
        self.fitness = lambda population: self.fitness_function(population, self.GENOME_SIZE)
        self.termination = Termination('evaluation_count')
        self.NUM_OFFSPRING_RATE = 0.381
        self.MUTATION_RATE = 0.306
        self.TOURNAMENT_GROUP_SIZE = 0.372
        self.init = Init_Pop('random_permutations')
        self.parent_selection = Parent_Selection('tournament')
        self.recombination = Recombination('partially_mapped_crossover')
        self.mutation = Mutation('duplicate_replacement')
        self.survival_selection = Survival_Selection('prob_survival')

        # Included in Parameter Search
        self.RECOMBINATION_RATE = kwargs['RECOMBINATION_RATE']

        self.curr_fitness_evaluations = 0
        self.curr_most_fit_individual = 0

    # solve function for Genetic_Algorithm class.
    # input: population: numpy array
    # output: fitness_evals: int
    def solve(self):
        is_solution = False
        self.curr_fitness_evaluations = 0
        self.curr_most_fit_individual = 0

        # Generate initial population
        population = self.init(self.GENOME_SIZE, self.POPULATION_SIZE)

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
            
            # apply genetic operations & calculate fitness
            selected_parents = self.parent_selection(population, self.NUM_OFFSPRING_RATE, self.TOURNAMENT_GROUP_SIZE, self.fitness)
            offspring = self.recombination(selected_parents, self.RECOMBINATION_RATE, self.GENOME_SIZE)
            mutated_offspring = self.mutation(offspring, self.MUTATION_RATE, self.GENOME_SIZE)
            offspring_fitness = self.fitness(mutated_offspring) 
            self.curr_fitness_evaluations += (len(offspring_fitness) + len(population))
            population = self.survival_selection(population, mutated_offspring, self.fitness)

            #check if solution is found
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
    def worker(setup_idx, setup, attribute, iters):
        genetic_algorithm = Genetic_Algorithm_Avg(**setup)
        setup_eval_count = round(genetic_algorithm.exp_evals(iters))
        return (setup_idx, setup_eval_count, setup[attribute])
    
    # get the topX setups
    # input: topX: int
    # output: None
    @staticmethod
    def get_topX_setups(topX):
        evals_file_loc = 'logs/LHS_Setups_evals.log'
        setups_file_loc = 'logs/LHS_Setups.log'
        output_file_loc = 'topX_setups.py'
        pt.extract_topX_setups(evals_file_loc, setups_file_loc, output_file_loc, topX)

# "main function"
# input: None
# output: None
# creates random setups using LHS, with threading it then evaluates them, and stores the "scores"
# lastly creates scatter plot with the results
if __name__ == '__main__':
    
    #setup the setups
    iters = 3
    setup_count = 100
    pt = Parameter_Tuning('LHS')
    setups = pt.tuning_strategy(setup_count)
    with open(config.curr_setups_loc, 'w') as curr_setups:
        curr_setups.write(f"{setups}")
    print(" --- CREATED SETUPS --- \n")
    
    #Threading runs at max availble cores!
    file_lock = Lock()
    counter = 0
    with concurrent.futures.ProcessPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
        with open(config.log_path6, 'w') as log_evals:
            log_evals.write(f"recombination_rate,setup_eval_count\n")
            start_time = time.time()
            futures = []
            
            for setup_idx, setup in enumerate(setups):
                future = executor.submit(Genetic_Algorithm_Avg.worker, setup_idx, setup, attribute='RECOMBINATION_RATE', iters = iters)
                futures.append(future)
            
            for future in concurrent.futures.as_completed(futures):
                setup_idx, setup_eval_count, recieved_attribute = future.result()
                
                with file_lock:
                    log_evals.write(f"{recieved_attribute},{setup_eval_count}\n")
                    counter = counter + 1
                    print(f"Loading {(counter * 100 / setup_count)}%  --({(time.time() - start_time):.2f}sec)")

    # visualize results with a scatter plot
    view_obj = Visualization('scatter')
    view_obj(config.log_path6, 'recombination_rate', 'setup_eval_count')