# IMPORTS
import config
import numpy as np
import random as rd
from init_pop import Init_Pop, Init_Random
from fitness import Fitness_Function, Conflict_Based
from mutation import Mutation, Swap_Mutation
from recombination import Recombination, Cut_And_Crossfill
from selection import Selection, Tournament, Delete_Replace
from termination import Termination, Evaluation_Count
from visuals import Visualization, Terminal

def genetic_algorithm_1():
    is_solution = False
    CURR_FITNESS_EVALUATIONS  = 0

    init_obj = Init_Pop(Init_Random())
    fitness_obj = Fitness_Function(Conflict_Based())
    selection_obj = Selection(parent_strategy=Tournament(), survival_strategy=Delete_Replace())
    recombination_obj = Recombination(Cut_And_Crossfill())
    mutation_obj = Mutation(Swap_Mutation())
    visual_obj = Visualization(Terminal())

    population = init_obj.initialize_population(config.GENOME_SIZE, config.POPULATION_SIZE)

    if CURR_FITNESS_EVALUATIONS == 0:
        curr_most_fit_individual = max(fitness_obj.evaluate(population))
        print("\nEvaluation Count: %8d  |  %8f" % (CURR_FITNESS_EVALUATIONS, curr_most_fit_individual))
        print("")

    while( not(Termination(Evaluation_Count()).is_terminate(
            curr_fitness_evaluations=CURR_FITNESS_EVALUATIONS,
            max_fitness_evaluations=config.MAX_FITNESS_EVALUATIONS,
            curr_iterations=0,  
            max_iterations=10000, 
            is_solution=is_solution )) ):
        
        selected_parents = selection_obj.pick_2_5(population)
        offspring = recombination_obj.recombine(selected_parents, config.RECOMBINATION_RATE, config.GENOME_SIZE)
        mutated_offspring = [mutation_obj.mutate(child, config.MUTATION_RATE, config.GENOME_SIZE) for child in offspring]
        offspring_fitness = fitness_obj.evaluate(mutated_offspring)
        CURR_FITNESS_EVALUATIONS += len(offspring_fitness)
        population = selection_obj.del_rep_2(population, mutated_offspring)

        if CURR_FITNESS_EVALUATIONS % 500 == 0:
            curr_most_fit_individual = max(fitness_obj.evaluate(population))
            print("Evaluation Count: %8d  |  %8f" % (CURR_FITNESS_EVALUATIONS, curr_most_fit_individual))

        if (max(fitness_obj.evaluate(population)) == 1):
            is_solution = True

    best_individual = max(population, key=fitness_obj.evaluate)
    visual_obj.view(best_individual)

genetic_algorithm_1()