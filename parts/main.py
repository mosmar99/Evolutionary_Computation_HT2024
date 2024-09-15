# IMPORTS
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

class Genetic_Algorithm:
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
        self.visual = Visualization(kwargs['visualization_strategy'])
        self.termination = Termination(kwargs['termination_strategy'])
        self.metric = Metric(kwargs['metric_strategy'])
        self.logger = Log(kwargs['logging_strategy'])

        self.fileprinter = File_Handler(kwargs['print_type'])

        self.curr_fitness_evaluations = 0
        self.curr_most_fit_individual = 0


    def solve(self):
        is_solution = False
        curr_fitness_evaluations = 0
        similarity_threshold = 0.4

        population = self.init(self.GENOME_SIZE, self.POPULATION_SIZE)

        if curr_fitness_evaluations == 0:
            curr_most_fit_individual = max(self.fitness(population))
            print("\nEvaluation Count: %8d  |  %8f" % (curr_fitness_evaluations, curr_most_fit_individual))
            print("")
            self.print(curr_fitness_evaluations, curr_most_fit_individual)

        while( not(self.termination( curr_fitness_evaluations=curr_fitness_evaluations,
                                     max_fitness_evaluations=self.MAX_FITNESS_EVALUATIONS,
                                     curr_iterations=0,  
                                     max_iterations=10000, 
                                     is_solution=is_solution )) ):
            
            selected_parents = self.parent_selection(population, self.NUM_OFFSPRING, self.TOURNAMENT_GROUP_SIZE, self.fitness)
            offspring = self.recombination(selected_parents, self.RECOMBINATION_RATE, self.GENOME_SIZE)
            mutated_offspring = self.mutation(offspring, self.MUTATION_RATE, self.GENOME_SIZE)

            avg_sim = self.metric(mutated_offspring, population)
            offspring_fitness = self.fitness(mutated_offspring) 
            self.logger(curr_fitness_evaluations, avg_sim, offspring_fitness)
            
            if (avg_sim < similarity_threshold):
                curr_fitness_evaluations += len(offspring_fitness)
                population = self.survival_selection(population, mutated_offspring, self.fitness)

            if (curr_fitness_evaluations % 500 == 0):
                curr_most_fit_individual = max(self.fitness(population))
                print("Evaluation Count: %8d  |  %8f" % (curr_fitness_evaluations, curr_most_fit_individual))
                self.print(curr_fitness_evaluations, curr_most_fit_individual)

            if (max(self.fitness(population)) == 1):
                is_solution = True

        best_individual = max(population, key=self.fitness)
        self.visual(best_individual, self.fitness)
        self.visual.HTML_Plots('avg_similarity_log.log')

    def print(self, evals, most_fit):
        to_print = {
            'CURR_FITNESS_EVALUATIONS': evals,
            'CURR_MOST_FIT_INDIVIDUAL': most_fit,
            'GENOME_SIZE': self.GENOME_SIZE,
            'POPULATION_SIZE': self.POPULATION_SIZE,
            'NUM_OFFSPRING': self.NUM_OFFSPRING,
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


if __name__ == '__main__':
    setup = { 'GENOME_SIZE':                15,
              'POPULATION_SIZE':            1000,
              'NUM_OFFSPRING':              20,
              'RECOMBINATION_RATE':         0.80,
              'MUTATION_RATE':              0.10,
              'MAX_FITNESS_EVALUATIONS':    10000,
              'TOURNAMENT_GROUP_SIZE':      0.2, 
              'initialization_strategy':    'random',
              'fitness_strategy':           'conflict_based',
              'parent_selection_strategy':  'tournament',
              'survival_selection_strategy':'prob_survival',
              'recombination_strategy':     'two_point_crossover',
              'mutation_strategy':          'inversion_mutation',
              'termination_strategy':       'evaluation_count',
              'visualization_strategy':     'terminal',
              'metric_strategy':            'avg_similarity',
              'logging_strategy':           'logger',
              'print_type':                 'csv_file'
            }
    
    ga = Genetic_Algorithm(**setup)
    ga.solve()