# IMPORTS
from init_pop import Init_Pop
from fitness import Fitness_Function
from mutation import Mutation
from recombination import Recombination
from survival_selection import Survival_Selection
from parent_selection import Parent_Selection
from termination import Termination
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

        self.init = Init_Pop(kwargs['initialization_strategy'])

        self.fitness_function = Fitness_Function(kwargs['fitness_strategy'])
        self.fitness = lambda population: self.fitness_function(population, self.GENOME_SIZE)
        self.parent_selection = Parent_Selection(kwargs['parent_selection_strategy'])
        self.survival_selection = Survival_Selection(kwargs['survival_selection_strategy'])
        self.recombination = Recombination(kwargs['recombination_strategy'])
        self.mutation = Mutation(kwargs['mutation_strategy'])
        self.visual = Visualization(kwargs['visualization_strategy'])
        self.termination = Termination(kwargs['termination_strategy'])
        self.fileprinter = File_Handler(kwargs['print_type'])

        evolution_strategies = { 'standard_evolve': self.standard_evolve }
        self.evolution_strategy = evolution_strategies[kwargs['evolution_strategy']]

        self.curr_fitness_evaluations = 0
        self.curr_most_fit_individual = 0

    def evolve(self, population):
        self.evolution_strategy(population)

    def standard_evolve(self, population):
        selected_parents = self.parent_selection(population, self.NUM_OFFSPRING, self.fitness)
        offspring = self.recombination(selected_parents, self.RECOMBINATION_RATE, self.GENOME_SIZE)
        mutated_offspring = self.mutation(offspring, self.MUTATION_RATE, self.GENOME_SIZE)
        offspring_fitness = self.fitness(mutated_offspring)
        self.curr_fitness_evaluations += len(offspring_fitness)
        population = self.survival_selection(population, mutated_offspring, self.fitness)

    def solve(self):
        is_solution = False
        self.curr_fitness_evaluations = 0

        population = self.init(self.GENOME_SIZE, self.POPULATION_SIZE)

        if self.curr_fitness_evaluations == 0:
            self.curr_most_fit_individual = max(self.fitness(population))
            print("\nEvaluation Count: %8d  |  %8f" % (self.curr_fitness_evaluations, self.curr_most_fit_individual))
            print("")
            self.print()

        while( not(self.termination( self.curr_fitness_evaluations,
                                     max_fitness_evaluations=self.MAX_FITNESS_EVALUATIONS,
                                     curr_iterations=0,  
                                     max_iterations=10000, 
                                     is_solution=is_solution )) ):
            
            self.evolve(population)

            if self.curr_fitness_evaluations % 500 == 0:
                self.curr_most_fit_individual = max(self.fitness(population))
                print("Evaluation Count: %8d  |  %8f" % (self.curr_fitness_evaluations, self.curr_most_fit_individual))
                self.print()

            if (max(self.fitness(population)) == 1):
                is_solution = True

        best_individual = max(population, key=self.fitness)
        self.visual(best_individual, self.fitness)

    def print(self):
        to_print = {
            'CURR_FITNESS_EVALUATIONS': self.curr_fitness_evaluations,
            'CURR_MOST_FIT_INDIVIDUAL': self.curr_most_fit_individual,
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
            'evolution_strategy': self.evolution_strategy.__name__
        }
        self.fileprinter(**to_print)

if __name__ == '__main__':
    setup = { 'GENOME_SIZE':                8,
              'POPULATION_SIZE':            100,
              'NUM_OFFSPRING':              2,
              'RECOMBINATION_RATE':         0.70,
              'MUTATION_RATE':              0.8,
              'MAX_FITNESS_EVALUATIONS':    10000,
              'initialization_strategy':    'random_permutations',
              'fitness_strategy':           'conflict_based',
              'parent_selection_strategy':  'tournament_2_5',
              'survival_selection_strategy':'del_rep_2',
              'recombination_strategy':     'cut_and_crossfill',
              'mutation_strategy':          'swap_mutation',
              'termination_strategy':       'evaluation_count',
              'visualization_strategy':     'terminal',
              'evolution_strategy':         'standard_evolve',
              'print_type':                 'csv_file'}
    
    ga = Genetic_Algorithm(**setup)
    ga.solve()