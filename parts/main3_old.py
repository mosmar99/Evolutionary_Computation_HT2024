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

class Genetic_Algorithm_Avg:
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


    def solve(self):
        is_solution = False
        self.curr_fitness_evaluations = 0
        self.curr_most_fit_individual = 0

        population = self.init(self.GENOME_SIZE, self.POPULATION_SIZE)

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
    def worker(setup_idx, setup, iters):
        genetic_algorithm = Genetic_Algorithm_Avg(**setup)
        setup_eval_count = round(genetic_algorithm.exp_evals(iters))
        return (setup_idx, setup_eval_count)
    
    @staticmethod
    def get_topX_setups(topX):
        evals_file_loc = 'logs/LHS_Setups_evals.log'
        setups_file_loc = 'logs/LHS_Setups.log'
        output_file_loc = 'topX_setups.py'
        pt.extract_topX_setups(evals_file_loc, setups_file_loc, output_file_loc, topX)
    
if __name__ == '__main__':
    iters = 10
    setup_count = 100
    topX = 15
    pt = Parameter_Tuning('LHS')
    setups = pt.tuning_strategy(setup_count)
    
    with open(config.log_path3, 'w') as log_setup:
        log_setup.write(f"iterations per setup: {iters}\namount of setups: {setup_count}\n\n{setups}")
    print("\n... created and saved setups")
    
    file_lock = Lock()
    counter = 0
    with concurrent.futures.ProcessPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
        with open(config.log_path4, 'w') as log_evals:
            start_time = time.time()
            futures = []
            
            for setup_idx, setup in enumerate(setups):
                future = executor.submit(Genetic_Algorithm_Avg.worker, setup_idx, setup, iters)
                futures.append(future)
            
            for future in concurrent.futures.as_completed(futures):
                setup_idx, setup_eval_count = future.result()
                
                with file_lock:
                    log_evals.write(f"s_{setup_idx + 1},{setup_eval_count}\n")
                    counter = counter + 1
                    print(f"Loading {(counter * 100 / setup_count)}%  --({(time.time() - start_time):.2f}sec)")

    Genetic_Algorithm_Avg.get_topX_setups(topX)
    Visualization('strategy_plot').strategy_plot(file_loc=config.log_path4, runs=iters)