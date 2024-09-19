# IMPORTS
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
from parameter_tuning import Parameter_Tuning

class Genetic_Algorithm_Avg:
    def __init__(self, **kwargs):
        self.GENOME_SIZE = 8 # N-QUEENS (EX: 'every Queen has a genome size of 8')
        self.MAX_FITNESS_EVALUATIONS = 10000

        self.POPULATION_SIZE = kwargs['POPULATION_SIZE']
        self.NUM_OFFSPRING = kwargs['NUM_OFFSPRING']
        self.RECOMBINATION_RATE = kwargs['RECOMBINATION_RATE']
        self.MUTATION_RATE = kwargs['MUTATION_RATE']
        self.TOURNAMENT_GROUP_SIZE = kwargs['TOURNAMENT_GROUP_SIZE']

        self.fitness_function = Fitness_Function('conflict_based')
        self.fitness = lambda population: self.fitness_function(population, self.GENOME_SIZE)
        self.termination = Termination('evaluation_count')
        
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
            
            selected_parents = self.parent_selection(population, self.NUM_OFFSPRING, self.TOURNAMENT_GROUP_SIZE, self.fitness)
            offspring = self.recombination(selected_parents, self.RECOMBINATION_RATE, self.GENOME_SIZE)
            mutated_offspring = self.mutation(offspring, self.MUTATION_RATE, self.GENOME_SIZE)
            offspring_fitness = self.fitness(mutated_offspring) 
            self.curr_fitness_evaluations += len(offspring_fitness)
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
    
if __name__ == '__main__':
    # Generate Setups
    iters = 100
    setup_count = 100
    setups = Parameter_Tuning('LHS').tuning_strategy(setup_count)
    with open(config.log_path3, 'w') as log_setup:
        log_setup.write(f"iterations per setup: {iters}\namount of setups: {setup_count}\n\n{setups}")
    print("\n... created and saved setups")

    # generate evals for all setups and print to file
    with open(config.log_path4, 'w') as log_evals:
        setup_evals = []
        start_time = time.time()
        for setup_idx, setup in enumerate(setups):
            genetic_algorithm = Genetic_Algorithm_Avg(**setup)
            setup_eval_count = genetic_algorithm.exp_evals(iters)
            log_evals.write(f"s_{setup_idx + 1},{setup_eval_count}\n")
            print(f"Loading {((setup_idx * 100) + 1) / setup_count:.0f}%  --({(time.time() - start_time):.2f}sec)")

    Visualization('terminal').strategy_plot(file_loc=config.log_path4, runs=iters)
    