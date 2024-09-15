import numpy as np
import random as rd

# Constants
GENOME_SIZE = 10 # N-QUEENS (EX: 'every Queen has a genome size of 8')
POPULATION_SIZE = 100
NUM_OFFSPRING = 2
RECOMBINATION_RATE = 0.70  
MUTATION_RATE = 0.8
MAX_FITNESS_EVALUATIONS = 10000


# random init of individuals in population of size POPULATION_SIZE
def init_population(GENOME_SIZE, POPULATION_SIZE):
    # low while is included, however, high value is excluded in the calcs
    return np.random.randint(low=1, high=8+1, size=(POPULATION_SIZE, GENOME_SIZE))

def conflict_counter(individual):
    # To Check: 
    # 1] Queens can't be in the same row (due to individual representation, no need to check for conflicting columns)
    # 2] Queens can't be in the same diagonal
    # Fitness Functions returns: '#(Conflicting Pairs of Queens)'
    n = len(individual)
    conflict_counter = 0
    for Q1 in range(n):
        for Q2 in range(Q1+1, n):
            # counts conflicts row-wise
            if(individual[Q1] == individual[Q2]):
                conflict_counter += 1
            # counts conflicts diag-wise
            # EX: [_,1,_,_,_,_,6,_] -> (2,1) & (7,6) => DIAG: (2-7)=(1-6) <=> (-5)=(-5)
            # DIFF_X = DIFF_Y => DIAG 
            if abs(individual[Q1] - individual[Q2]) == abs(Q1 - Q2):
                conflict_counter += 1
    return conflict_counter

# returns an fitness array of current population (may be 1 individual in population or more) 
def eval_fitness(population):
    fitness_evals = []
    if(np.array(population).ndim == 1):
            fitness_evals.append(1 - conflict_counter(population) / 28) 
    elif(np.array(population).ndim == 2):
        for i in range(len(population)):
            fitness_evals.append(1 - conflict_counter(population[i]) / 28) 
    return fitness_evals

# Select the best 2 selected_parents from a random group of 5 individuals
def parent_selection(population, group_size):
    candidates = rd.sample(list(population), group_size)
    candidates.sort(key=eval_fitness, reverse=True)
    return candidates[0], candidates[1]

# at crossover point (cut_index), cutt both parents DNA and crossfill
def cut_and_crossfill(dad, mom, GENOME_SIZE):
    child_one = []
    child_two = []
    cut_index = GENOME_SIZE/2
    for i in range(GENOME_SIZE):
        if(i < cut_index):
            child_one.append(dad[i])
            child_two.append(mom[i])
        else:
            child_one.append(mom[i])
            child_two.append(dad[i])
    return [child_one, child_two]

# with prob recombination_rate, do cut_and_crossfill
def recombination(selected_parents, recombination_rate):
    if (np.random.rand() <= recombination_rate):
        dad = selected_parents[0]
        mom = selected_parents[1]
        children = cut_and_crossfill(dad, mom, GENOME_SIZE)
        return children
    else:
        return selected_parents

# [_,_,3,_,_,_,8,_] -> (with prob mutation_rate, will become) -> [_,_,8,_,_,_,3,_]
def swap_mutation(individual, mutation_rate, GENOME_SIZE):
    if (np.random.rand() <= mutation_rate):
        # get indices of 2 random genes in the genome
        gene_idx1, gene_idx2 = np.random.choice(GENOME_SIZE, 2, replace=False)

        # return the genes at specified indices
        gene1, gene2 = individual[gene_idx1].copy(), individual[gene_idx2].copy()

        # swap the genes contents of the two genes at the specified indices
        individual[gene_idx1] = gene2
        individual[gene_idx2] = gene1
    return individual

# replace the currently, two worst individuals in the population
# worst is defined in terms of fitness evalutation, the lower the worse
def survival_selection(population, offspring):
    population_list = population.tolist()
    population_list.sort(key=eval_fitness, reverse=False)        
    population_list[0], population_list[1] = offspring[0], offspring[1]
    return np.array(population_list)

def termination_condition(curr_fitness_evaluations, max_fitness_evaluations, is_solution):
    if((curr_fitness_evaluations >= max_fitness_evaluations) or (is_solution)):
        return True
    return False    

def visualize_board(individual):
    n = len(individual)
    columns = "abcdefgh"
    print("\n")
    print("   " + "  ".join(columns[:n]))
    for row in range(n):
        line = f"{row + 1}  "
        for col in range(n):
            line += "Q  " if individual[col] == row + 1 else ".  "
        line += f"{row + 1}"
        print(line)
    print("   " + "  ".join(columns[:n]))
    print("\nFitness Evaluation: %8f" % (round(eval_fitness(individual)[0], 2)))
    print("Solution: ", individual)
    print("\n")

    #rebalancing_mutation
def rebalancing_mutation(individual, mutation_rate):
    if np.random.rand() <= mutation_rate:
        n = len(individual)
        for i in range(n):
            for j in range(i+1, n):
                # Check for diagonal conflict
                if abs(individual[i] - individual[j]) == abs(i - j):
                    # Resolve conflict by randomly reassigning one of the queens
                    individual[i] = np.random.randint(1, n + 1)
    return individual



def genetic_algorithm():
    is_solution = False
    CURR_FITNESS_EVALUATIONS  = 0
    tournament_group_size = 10

    population = init_population(GENOME_SIZE, POPULATION_SIZE)

    print(population[0])

    if CURR_FITNESS_EVALUATIONS == 0:
        curr_most_fit_individual = max(eval_fitness(population))
        print("\nEvaluation Count: %8d  |  %8f" % (CURR_FITNESS_EVALUATIONS, curr_most_fit_individual))
        print("")

    while( not(termination_condition(CURR_FITNESS_EVALUATIONS, MAX_FITNESS_EVALUATIONS, is_solution)) ):
        selected_parents = parent_selection(population, tournament_group_size)
        offspring = recombination(selected_parents, RECOMBINATION_RATE)
        mutated_offspring = [swap_mutation(child, MUTATION_RATE, GENOME_SIZE) for child in offspring]
        mutated_offspring = [rebalancing_mutation(child, MUTATION_RATE) for child in mutated_offspring]
        offspring_fitness = eval_fitness(mutated_offspring)
        CURR_FITNESS_EVALUATIONS += len(offspring_fitness)
        population = survival_selection(population, mutated_offspring)

        if CURR_FITNESS_EVALUATIONS % 500 == 0:
            curr_most_fit_individual = max(eval_fitness(population))
            print("Evaluation Count: %8d  |  %8f" % (CURR_FITNESS_EVALUATIONS, curr_most_fit_individual))

        if (max(eval_fitness(population)) == 1):
            is_solution = True

    best_individual = max(population, key=eval_fitness)
    visualize_board(best_individual)
    
genetic_algorithm()

