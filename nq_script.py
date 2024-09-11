import numpy as np
import random as rd
import csv
import os

class Nq_evolution:
    def __init__(self, num_queens, population_size, crossover_rate, mutation_prob, max_iters, **kwargs) -> None:
        init_strategies = { 'strategy1': self.init_population_random }

        selection_strategies = { 'strategy1': self.selection1,
                                 'tournament': self.selection_tournament }

        recombination_strategies = { 'strategy1': self.recombination1}

        mutation_strategies = { 'strategy1': self.mutation1 }

        eval_strategies = { 'strategy1': self.eval_fitness1 }

        evolution_strategies = { 'strategy1': self.evolution1 }

        self.num_queens      = num_queens
        self.population_size = population_size
        self.max_iters       = max_iters
        self.crossover_rate  = crossover_rate
        self.mutation_prob   = mutation_prob

        self.init_population_generation = init_strategies[kwargs['init_strategy']]
        self.selection                  = selection_strategies[kwargs['selection_strategy']]
        self.recombination              = recombination_strategies[kwargs['recombination_strategy']]
        self.mutation                   = mutation_strategies[kwargs['mutation_strategy']]
        self.eval_fitness               = eval_strategies[kwargs['eval_strategy']]
        self.evolve                     = evolution_strategies[kwargs['evolution_strategy']]
        self.csv_file                   = 'evolution_log.csv'

        #in case csv file doesn't exist create one & add the headers.
        if not os.path.exists(self.csv_file):
            with open(self.csv_file, "w", newline="") as csvfile:
                csv.writer(csvfile).writerow([
                    'Stage', 'Iteration', 'Average Fitness',
                    'Init Strategy', 'Selection Strategy', 'Recombination Strategy',
                    'Mutation Strategy', 'Eval Strategy', 'Evolution Strategy',
                    'Num Queens', 'Population Size', 'Crossover Rate',
                    'Mutation Probability', 'Max Iterations'
                ])

    #region init strategies

    def init_population_random(self):
        # low while is included, however, high value is excluded in the calcs
        return np.random.randint(low=1, high=self.num_queens+1, size=(self.population_size, self.num_queens))
    
    #endregion

    #region recombination strategies

    # state = current boards after selection
    # probability = probability of mutation, usually between 70-90%
    def recombination1(self, selected_individuals):
        new_population = []
        copy_selected_individuals = selected_individuals.copy()

        while len(new_population) < self.population_size:
            crossover_point = np.random.randint(1, self.num_queens)
            dad_idx = np.random.randint(0, len(copy_selected_individuals))
            mom_idx = dad_idx
            while(dad_idx == mom_idx):
                mom_idx = np.random.randint(0, len(copy_selected_individuals))
            dad = copy_selected_individuals[dad_idx]
            mom = copy_selected_individuals[mom_idx]

            if(np.random.rand() < self.crossover_rate):
                child_one = [0] * self.num_queens
                child_two = [0] * self.num_queens
                for j in range(self.num_queens):
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

        return np.array(new_population[:self.population_size])
    
    #endregion

    #region Selection strategies

    def selection1(self, population):
        fitness_evals = self.eval_fitness(population)
        selected_individuals = []
        copy_population = population
        copy_fitness_evals = fitness_evals
        while(len(selected_individuals) < self.population_size):
            if (copy_population.shape[0] == 0):
                copy_population = population
                copy_fitness_evals = fitness_evals
            i = np.random.randint(low=0, high=len(copy_population))
            if rd.random() < copy_fitness_evals[i]:
                selected_individuals.append(copy_population[i])
                copy_population = np.delete(arr=copy_population, obj=i, axis=0)
                copy_fitness_evals = np.delete(arr=copy_fitness_evals, obj=i, axis=0)
        
        return np.array(selected_individuals)
    
    def selection_tournament(self, population):
        selected_individuals = []
        while(len(selected_individuals) < self.population_size):
            i = np.random.randint(low=0, high=len(population))
            idxs = np.random.choice(self.population_size, 5, replace=False)
            nr1_individual = nr2_individual = 0
            for i in range(idxs.size):
                if(i == 0):
                    if(self.eval_fitness(population[idxs[0]]) > self.eval_fitness(population[idxs[1]])):
                        nr1_individual = population[idxs[0]].copy()
                        nr2_individual = population[idxs[1]].copy()
                        continue
                    else:
                        nr1_individual = population[idxs[1]].copy()
                        nr2_individual = population[idxs[0]].copy()
                        continue
                if(i == 1):
                    continue
                if(self.eval_fitness(population[idxs[i]]) > self.eval_fitness(nr1_individual)):
                    nr2_individual = nr1_individual.copy()
                    nr1_individual = population[idxs[i]].copy()
                if(self.eval_fitness(population[idxs[i]]) > self.eval_fitness(nr2_individual)):
                    nr2_individual = population[idxs[i]].copy()
            selected_individuals.extend([nr1_individual, nr2_individual])
        return np.array(selected_individuals)
    
    #endregion
    
    #region mutation strategies

    def mutation1(self, population):
        for board in population:
            if(np.random.rand() < self.mutation_prob):
                new_gene = np.random.randint(1, self.num_queens + 1)
                insert_idx = np.random.randint(0, self.num_queens)
                board[insert_idx] = new_gene
        return population
    
    #endregion

    #region fitness functions

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
    
    #endregion

    #region evaluation strategies

    def eval_fitness1(self, population):
        fitness_evals = []
        denominator = (self.num_queens * (self.num_queens - 1)) / 2
        if(population.ndim == 1):
                fitness_evals.append(1 - Nq_evolution.fitness_function(population) / denominator) 
        elif(population.ndim == 2):
            for i in range(len(population)):
                fitness_evals.append(1 - Nq_evolution.fitness_function(population[i]) / denominator) 
        return np.array(fitness_evals)
    
    #endregion

    #region evolution strategies

    def evolution1(self, population, iteration):

        selected_state = self.selection(population)
        if (iteration + 1) % 10 == 0 and (iteration+1) >= 10:
            avg_fitness = np.average(self.eval_fitness(selected_state))
            print("SELECTION: ", (iteration+1), " | ", "Current Best Fitness:", np.average(self.eval_fitness(selected_state)))
            self.log_iteration("SELECTION", iteration+1, avg_fitness)

        recombined_state = self.recombination(selected_state)
        if (iteration + 1) % 10 == 0 and (iteration+1) >= 10:
            avg_fitness = np.average(self.eval_fitness(recombined_state))
            print("RECOMBINATION: ", (iteration+1), " | ", "Current Best Fitness:", avg_fitness)
            self.log_iteration("RECOMBINATION", iteration+1, avg_fitness)

        mutated_state = self.mutation(recombined_state)
        if (iteration + 1) % 10 == 0 and (iteration+1) >= 10:
            avg_fitness = np.average(self.eval_fitness(mutated_state))
            print("MUTATION: ", (iteration+1), " | ", "Current Best Fitness:", avg_fitness)
            print("")
            self.log_iteration("MUTATION", iteration+1, avg_fitness)

        return mutated_state
    
    #endregion

    #region utility Functions
    @staticmethod
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
    
    def log_iteration(self, stage, iteration, avg_fitness):
        #Logging each stage with the fitness value to CSV
        with open(self.csv_file, 'a', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow([
                stage, iteration, avg_fitness,
                self.init_population_generation.__name__,
                self.selection.__name__,
                self.recombination.__name__,
                self.mutation.__name__,
                self.eval_fitness.__name__,
                self.evolve.__name__,
                self.num_queens, self.population_size, self.crossover_rate,
                self.mutation_prob, self.max_iters
            ])

    #endregion
    
    def solve(self):
        population = self.init_population_generation()
        for i in range(self.max_iters):
            fitness_evals = self.eval_fitness(population)

            if(np.any(fitness_evals == 1)):
                best_individual = population[np.argmax(fitness_evals)]
                Nq_evolution.visualize_board(best_individual)
                print(f"Solution found at iteration {i}")
                break
            
            population = self.evolve(population, i)


def nq_solve_standard():
    strategies = { 'init_strategy':             'strategy1',
                   'selection_strategy':        'tournament',
                   'recombination_strategy':    'strategy1',
                   'mutation_strategy':         'strategy1',
                   'eval_strategy':             'strategy1',
                   'evolution_strategy':        'strategy1'}
    

    nq_evolution = Nq_evolution(10, 100, 0.8, 0.05, 1000, **strategies)
    nq_evolution.solve()

if __name__ == '__main__':
    nq_solve_standard()
