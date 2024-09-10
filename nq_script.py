import numpy as np
import random as rd

def init_population(POPULATION_SIZE):
    # low while is included, however, high value is excluded in the calcs
    return np.random.randint(low=1, high=8+1, size=(POPULATION_SIZE, 8))

def fitness_function(state):
    # To Check: 
    # 1] Queens can't be in the same row (due to state representation, no need to check for conflicting columns)
    # 2] Queens can't be in the same diagonal
    # Fitness Functions returns: '#(Conflicting Pairs of Queens)'
    n = len(state)
    conflict_counter = 0
    for Q1 in range(n):
        for Q2 in range(Q1+1, n):
            # counts conflicts row-wise
            if(state[Q1] == state[Q2]):
                conflict_counter += 1
            # counts conflicts diag-wise
            # EX: [_,1,_,_,_,_,6,_] -> (2,1) & (7,6) => DIAG: (2-7)=(1-6) <=> (-5)=(-5)
            if abs(state[Q1] - state[Q2]) == abs(Q1 - Q2):
                conflict_counter += 1
    return conflict_counter

def eval_fitness(state):
    fitness_evals = []
    if(state.ndim == 1):
            fitness_evals.append(1 - fitness_function(state) / 28) 
    elif(state.ndim == 2):
        for i in range(len(state)):
            fitness_evals.append(1 - fitness_function(state[i]) / 28) 
    return np.array(fitness_evals)

# Tournament Strategy: "Best 2 out of Random 5"
def parent_selection(state, population_size):
    selected_individuals = []
    while(len(selected_individuals) < population_size):
        i = np.random.randint(low=0, high=len(state))
        idxs = np.random.choice(population_size, 5, replace=False)
        nr1_individual = nr2_individual = 0
        for i in range(idxs.size):
            if(i == 0):
                if(eval_fitness(state[idxs[0]]) > eval_fitness(state[idxs[1]])):
                    nr1_individual = state[idxs[0]].copy()
                    nr2_individual = state[idxs[1]].copy()
                    continue
                else:
                    nr1_individual = state[idxs[1]].copy()
                    nr2_individual = state[idxs[0]].copy()
                    continue
            if(i == 1):
                continue
            if(eval_fitness(state[idxs[i]]) > eval_fitness(nr1_individual)):
                nr2_individual = nr1_individual.copy()
                nr1_individual = state[idxs[i]].copy()
            if(eval_fitness(state[idxs[i]]) > eval_fitness(nr2_individual)):
                nr2_individual = state[idxs[i]].copy()
        selected_individuals.extend([nr1_individual, nr2_individual])
    return np.array(selected_individuals)

# state = current boards after parent_selection
# probability = probability of mutation, usually between 70-90%
def recombination(selected_individuals, population_size, crossover_rate):
    new_population = []
    copy_selected_individuals = selected_individuals.copy()

    while len(new_population) < population_size:
        crossover_point = np.random.randint(3, 6)
        dad_idx = np.random.randint(0, len(copy_selected_individuals))
        mom_idx = dad_idx
        while(dad_idx == mom_idx):
            mom_idx = np.random.randint(0, len(copy_selected_individuals))
        dad = copy_selected_individuals[dad_idx]
        mom = copy_selected_individuals[mom_idx]

        if(np.random.rand() < crossover_rate):
            child_one = child_two = [0] * 8
            for j in range(8):
                if(j < crossover_point):
                    child_one[j] = dad[j]
                    child_two[j] = mom[j]
                else:
                    child_one[j] = mom[j]
                    child_two[j] = dad[j]
            new_population.append(child_one)
            new_population.append(child_two)
        else:
            new_population.append(dad)
            new_population.append(mom)
    return np.array(new_population[:population_size])

def mutation(state, mutation_prob):
    for board in state:
        if(np.random.rand() < mutation_prob):
            new_gene = np.random.randint(1, 9)
            insert_idx = np.random.randint(0, 8)
            board[insert_idx] = new_gene
    return state

def visualize_board(state):
    n = len(state)
    columns = "abcdefgh"
    print("\n")
    print("   " + "  ".join(columns[:n]))
    for row in range(n):
        line = f"{row + 1}  "
        for col in range(n):
            line += "Q  " if state[col] == row + 1 else ".  "
        line += f"{row + 1}"
        print(line)
    print("   " + "  ".join(columns[:n]))
    print("\n")

# Main EC-Loop
POPULATION_SIZE = 100
NUM_OFFSPRING = 2
CROSSOVER_RATE = 1.0  
MUTATION_RATE = 0.8  
ITERS = 10000

init_state = init_population(POPULATION_SIZE)

for i in range(ITERS):
    if(i == 0):
        fitness_evals = eval_fitness(init_state)
        print("START EVAL", np.average(fitness_evals), "\n")
    else:
        fitness_evals = eval_fitness(mutated_state)

    if(np.any(fitness_evals == 1)):
        best_individual = mutated_state[np.argmax(fitness_evals)]
        visualize_board(best_individual)
        print(best_individual)
        print(f"Solution found at iteration {i}")
        break

    selected_state = parent_selection(init_state, POPULATION_SIZE)
    if (i + 1) % 10 == 0 and (i+1) >= 10:
        print("SELECTION:    %5d | Current Best Fitness: %.5f" % ((i+1), np.average(eval_fitness(selected_state))))
   
    recombined_state = recombination(selected_state, POPULATION_SIZE, CROSSOVER_RATE)
    if (i + 1) % 10 == 0 and (i+1) >= 10:
        print("RECOMBINATION:%5d | Current Best Fitness: %.5f" % ((i+1), np.average(eval_fitness(recombined_state))))
   
    mutated_state = mutation(recombined_state, MUTATION_RATE)
    if (i + 1) % 10 == 0 and (i+1) >= 10:
        print("MUTATION:     %5d | Current Best Fitness: %.5f" % ((i+1), np.average(eval_fitness(mutated_state))))
        print("")

def ec_algorithm():
    pass