# IMPORTS
import config
import numpy as np
import random as rd
from init_pop import Init_Pop
from fitness import Fitness_Function
from mutation import Mutation
from recombination import Recombination
from survival_selection import Survival_Selection
from parent_selection import Parent_Selection
from termination import Termination, Evaluation_Count
from visuals import Visualization

def genetic_algorithm_1():
    is_solution = False
    curr_fitness_evaluations = 0

    init = Init_Pop('random')
    fitness_function = Fitness_Function('conflict_based')
    fitness = lambda population: fitness_function(population, config.GENOME_SIZE)
    parent_selection = Parent_Selection('tournament_2_5')
    survival_selection = Survival_Selection('del_rep_2')
    recombination = Recombination('cut_and_crossfill')
    mutation = Mutation('swap_mutation')
    visual = Visualization('terminal')

    population = init(config.GENOME_SIZE, config.POPULATION_SIZE)

    if curr_fitness_evaluations == 0:
        curr_most_fit_individual = max(fitness(population))
        print("\nEvaluation Count: %8d  |  %8f" % (curr_fitness_evaluations, curr_most_fit_individual))
        print("")

    while( not(Termination(Evaluation_Count()).is_terminate(
            curr_fitness_evaluations=curr_fitness_evaluations,
            max_fitness_evaluations=config.MAX_FITNESS_EVALUATIONS,
            curr_iterations=0,  
            max_iterations=10000, 
            is_solution=is_solution )) ):
        
        selected_parents = parent_selection(population, fitness)
        offspring = recombination(selected_parents, config.RECOMBINATION_RATE, config.GENOME_SIZE)
        mutated_offspring = mutation(offspring, config.MUTATION_RATE, config.GENOME_SIZE)
        offspring_fitness = fitness(mutated_offspring)
        curr_fitness_evaluations += len(offspring_fitness)
        population = survival_selection(population, mutated_offspring, fitness)

        if curr_fitness_evaluations % 500 == 0:
            curr_most_fit_individual = max(fitness(population))
            print("Evaluation Count: %8d  |  %8f" % (curr_fitness_evaluations, curr_most_fit_individual))

        if (max(fitness(population)) == 1):
            is_solution = True

    best_individual = max(population, key=fitness)
    visual(best_individual, fitness)

if __name__ == '__main__':
    genetic_algorithm_1()