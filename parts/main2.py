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

class Genetic_Algorithm_Avg:
    def __init__(self, **kwargs):
        self.GENOME_SIZE = kwargs['GENOME_SIZE'] # N-QUEENS (EX: 'every Queen has a genome size of 8')
        self.POPULATION_SIZE = kwargs['POPULATION_SIZE']
        self.NUM_OFFSPRING = kwargs['NUM_OFFSPRING']
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
        self.termination = Termination(kwargs['termination_strategy'])

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
    
    def avg_sol(self, iters):
        total = 0
        for _ in range(iters):
            total += self.solve()
        avg = total / iters
        print(f"Avg. Eval-Count. after {iters} is {avg}")
        return avg

if __name__ == '__main__':
    iters = 100
    ga = Genetic_Algorithm_Avg(**config.setup1)
    eval_count_1 = ga.avg_sol(iters)
    ga = Genetic_Algorithm_Avg(**config.setup2)
    eval_count_2 = ga.avg_sol(iters)
    ga = Genetic_Algorithm_Avg(**config.setup3)
    eval_count_3 = ga.avg_sol(iters)
    ga = Genetic_Algorithm_Avg(**config.setup4)
    eval_count_4 = ga.avg_sol(iters)
    ga = Genetic_Algorithm_Avg(**config.setup5)
    eval_count_5 = ga.avg_sol(iters)
    ga = Genetic_Algorithm_Avg(**config.setup6)
    eval_count_6 = ga.avg_sol(iters)

    with open('logs/eval_count_by_strategy.log', 'w') as log_file:
        log_file.write(f"setup_1,{eval_count_1}\n")
        log_file.write(f"setup_2,{eval_count_2}\n")
        log_file.write(f"setup_3,{eval_count_3}\n")
        log_file.write(f"setup_4,{eval_count_4}\n")
        log_file.write(f"setup_5,{eval_count_5}\n")
        log_file.write(f"setup_6,{eval_count_6}\n")
    
    Visualization('terminal').strategy_plot(config.log_path2)