# IMPORTS
from init_pop import Init_Pop
from fitness import Fitness_Function
from mutation import Mutation
from recombination import Recombination
from survival_selection import Survival_Selection
from parent_selection import Parent_Selection
from termination import Termination
from visuals import Visualization
import numpy as np
import logging

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

        logging.basicConfig(filename='avg_similarity_log.log', level=logging.INFO, 
                            format='%(message)s', filemode='w')
        self.logger = logging.getLogger()

    def solve(self):
        is_solution = False
        curr_fitness_evaluations = 0
        similarity_threshold = 0.4

        population = self.init(self.GENOME_SIZE, self.POPULATION_SIZE)

        if curr_fitness_evaluations == 0:
            curr_most_fit_individual = max(self.fitness(population))
            self.logger.info(f"evaluation_count,avg_similarity_score,fitness_score")
            print("\nEvaluation Count: %8d  |  %8f" % (curr_fitness_evaluations, curr_most_fit_individual))
            print("")

        while( not(self.termination( curr_fitness_evaluations=curr_fitness_evaluations,
                                     max_fitness_evaluations=self.MAX_FITNESS_EVALUATIONS,
                                     curr_iterations=0,  
                                     max_iterations=10000, 
                                     is_solution=is_solution )) ):
            
            selected_parents = self.parent_selection(population, self.NUM_OFFSPRING, self.TOURNAMENT_GROUP_SIZE, self.fitness)
            offspring = self.recombination(selected_parents, self.RECOMBINATION_RATE, self.GENOME_SIZE)
            mutated_offspring = self.mutation(offspring, self.MUTATION_RATE, self.GENOME_SIZE)

            population_sample = population[np.random.choice(self.POPULATION_SIZE, int(self.POPULATION_SIZE*0.5), replace=False)]
            avg_sim = self.fitness_function.avg_similarity(mutated_offspring, population_sample)
            offspring_fitness = self.fitness(mutated_offspring) 
            self.logger.info("%d, %f, %f" % (curr_fitness_evaluations, avg_sim, round(np.mean(offspring_fitness), 2)))
            
            if (avg_sim < similarity_threshold):
                curr_fitness_evaluations += len(offspring_fitness)
                population = self.survival_selection(population, mutated_offspring, self.fitness)


            if (curr_fitness_evaluations % 500 == 0):
                curr_most_fit_individual = max(self.fitness(population))
                print("Evaluation Count: %8d  |  %8f" % (curr_fitness_evaluations, curr_most_fit_individual))

            if (max(self.fitness(population)) == 1):
                is_solution = True

        best_individual = max(population, key=self.fitness)
        self.visual(best_individual, self.fitness)
        self.visual.HTML_Plots('avg_similarity_log.log')

if __name__ == '__main__':
    setup = { 'GENOME_SIZE':                8,
              'POPULATION_SIZE':            100,
              'NUM_OFFSPRING':              20,
              'RECOMBINATION_RATE':         0.80,
              'MUTATION_RATE':              0.80,
              'MAX_FITNESS_EVALUATIONS':    10000,
              'TOURNAMENT_GROUP_SIZE':      0.2, 
              'initialization_strategy':    'random',
              'fitness_strategy':           'conflict_based',
              'parent_selection_strategy':  'tournament',
              'survival_selection_strategy':'prob_survival',
              'recombination_strategy':     'two_point_crossover',
              'mutation_strategy':          'swap_mutation',
              'termination_strategy':       'evaluation_count',
              'visualization_strategy':     'terminal',
              'evolution_strategy':         'standard_evolve'}
    
    ga = Genetic_Algorithm(**setup)
    ga.solve()