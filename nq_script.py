import numpy as np
import random as rd

def init_population_generation(n):
    # low while is included, however, high value is excluded in the calcs
    return np.random.randint(low=1, high=8+1, size=(n, 8))

def fitness_function(state):
    # To Check: 
    # 1] Queens can't be in the same row (due to state representation, no need to check for conflicting columns)
    # 2] Queens can't be in the same diagonal
    # Fitness Functions returns: '#(Conflicting Pairs of Queens)'
    n = len(state)
    conflict_counter = 0
    for Q1 in range(n):
        for Q2 in range(Q1 + 1, n):
            # counts conflicts row-wise
            if(state[Q1] == state[Q2]):
                conflict_counter += 1
              # counts conflicts diag-wise
            # EX: [_,1,_,_,_,_,6,_] -> (2,1) & (7,6) => DIAG: (2-7)=(1-6) <=> (-5)=(-5)
            if(state[Q1] - state[Q2] == Q1 - Q2 or state[Q1] - state[Q2] == Q2 - Q1):
                conflict_counter += 1
    return conflict_counter

def eval_curr_fitness(state, population_size):
    fitness_evals = []
    for i in range(population_size):
        fitness_evals.append(1 - fitness_function(state[i]) / 28) 
    return np.array(fitness_evals)

def selection(state, fitness_evals, population_size):
    selected_individuals = []
    copy_state = state
    copy_fitness_evals = fitness_evals
    while(len(selected_individuals) < population_size):
        if (copy_state.shape[0] == 0):
            copy_state = state
            copy_fitness_evals = fitness_evals
        i = np.random.randint(low=0, high=len(copy_state))
        if rd.random() < copy_fitness_evals[i]:
            selected_individuals.append(copy_state[i])
            copy_state = np.delete(arr=copy_state, obj=i, axis=0)
            copy_fitness_evals = np.delete(arr=copy_fitness_evals, obj=i, axis=0)
        
    return np.array(selected_individuals)

# state = current boards after selection
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
population_size = 1000
crossover_rate = 0.8
mutation_prob = 0.3

init_state = init_population_generation(population_size)

iters = 1000
for i in range(iters):
    if(i == 0):
        fitness_evals = eval_curr_fitness(init_state, population_size)
    else:
        fitness_evals = eval_curr_fitness(mutated_state, population_size)

    if(np.any(fitness_evals == 1)):
        best_individual = mutated_state[np.argmax(fitness_evals)]
        visualize_board(best_individual)
        print(f"Solution found at iteration {i}")
        break

    selected_state = selection(init_state, fitness_evals, population_size)
    recombined_state = recombination(selected_state, population_size, crossover_rate)
    mutated_state = mutation(recombined_state, mutation_prob)

    if (i + 1) % 10 == 0 and (i+1) >= 10:
        print("Iteration: ", (i+1), " | ", "Current Best Fitness:", np.max(fitness_evals))
