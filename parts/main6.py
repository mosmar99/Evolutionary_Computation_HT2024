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
from destroy import Destroy

class Genetic_Algorithm:
    def __init__(self, **kwargs):

        self.GENOME_SIZE = kwargs['GENOME_SIZE'] 
        self.MAX_FITNESS_EVALUATIONS = kwargs['MAX_FITNESS_EVALUATIONS']
        self.fitness_function = Fitness_Function(kwargs['fitness_strategy'])
        self.fitness = lambda population: self.fitness_function(population, self.GENOME_SIZE)
        self.termination = Termination(kwargs['termination_strategy'])
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
        self.visual = Visualization(kwargs['visualization_strategy'])

        self.MAX_STAGNANT_GENERATIONS = kwargs['MAX_STAGNANT_GENERATIONS']
        self.TOLERANCE = kwargs['TOLERANCE']
        self.GENOCIDE_PERC = kwargs['GENOCIDE_PERC']
        self.destroy = Destroy(max_stagnant_generations=self.MAX_STAGNANT_GENERATIONS, tolerance=self.TOLERANCE, 
                               genocide_perc=self.GENOCIDE_PERC)

        self.curr_fitness_evaluations = 0
        self.curr_most_fit_individual = 0
        self.generations = 0

    def solve(self):
        is_solution = False
        self.curr_fitness_evaluations = 0
        self.curr_most_fit_individual = 0
        self.generations = 0

        population = self.init(self.GENOME_SIZE, self.POPULATION_SIZE)
        population_copy = population.copy()

        # WITH GENOCIDE
        while( not(self.termination( curr_fitness_evaluations=self.curr_fitness_evaluations,
                                     max_fitness_evaluations=self.MAX_FITNESS_EVALUATIONS,
                                     curr_iterations=0,  
                                     max_iterations=10000, 
                                     is_solution=is_solution )) ):
            
            selected_parents = self.parent_selection(population, self.NUM_OFFSPRING_RATE, self.TOURNAMENT_GROUP_SIZE, self.fitness)
            offspring = self.recombination(selected_parents, self.RECOMBINATION_RATE, self.GENOME_SIZE)
            mutated_offspring = self.mutation(offspring, self.MUTATION_RATE, self.GENOME_SIZE)
            offspring_fitness = self.fitness(mutated_offspring) 
            population = self.survival_selection(population, mutated_offspring, self.fitness)
            self.curr_fitness_evaluations += (len(offspring_fitness) + len(population))

            if (max(self.fitness(population)) == 1):
                print(f"\n --- GENERATION: {self.generations} --- ", end="")
                self.visual(max(population, key=self.fitness), self.fitness)
                break

            self.curr_most_fit_individual = max(self.fitness(population))
            if self.destroy.check_stagnation(self.curr_most_fit_individual):
                # print(" --- GENOCIDE APPLIED --- ")
                population = self.destroy.apply_genocide(population, self.fitness)

            self.generations += 1
            # print(f" --- GENERATION: {self.generations} --- ")

        is_solution = False
        self.curr_fitness_evaluations = 0
        self.curr_most_fit_individual = 0
        self.generations = 0
        # WITHOUT GENOCIDE (SAME INITIAL POPULATION)
        while( not(self.termination( curr_fitness_evaluations=self.curr_fitness_evaluations,
                                     max_fitness_evaluations=self.MAX_FITNESS_EVALUATIONS,
                                     curr_iterations=0,  
                                     max_iterations=10000, 
                                     is_solution=is_solution )) ):
            
            selected_parents = self.parent_selection(population_copy, self.NUM_OFFSPRING_RATE, self.TOURNAMENT_GROUP_SIZE, self.fitness)
            offspring = self.recombination(selected_parents, self.RECOMBINATION_RATE, self.GENOME_SIZE)
            mutated_offspring = self.mutation(offspring, self.MUTATION_RATE, self.GENOME_SIZE)
            offspring_fitness = self.fitness(mutated_offspring) 
            population_copy = self.survival_selection(population_copy, mutated_offspring, self.fitness)
            self.curr_fitness_evaluations += (len(offspring_fitness) + len(population_copy))

            if (max(self.fitness(population_copy)) == 1):
                self.visual(max(population_copy, key=self.fitness), self.fitness)
                print(f" --- GENERATION: {self.generations} --- ")
                break

            self.generations += 1
            if(self.generations % 5 == 0):
                print(f" --- FITNESS: {self.curr_fitness_evaluations} --- ")

    
if __name__ == '__main__':
    Genetic_Algorithm(**config.setup_genocide).solve()