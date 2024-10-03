import config
import time
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
        self.WEIGHTING_EXPONENT = kwargs['WEIGHTING_EXPONENT']
        self.visual = Visualization(kwargs['visualization_strategy'])

        self.MAX_STAGNANT_GENERATIONS = kwargs['MAX_STAGNANT_GENERATIONS']
        self.TOLERANCE = kwargs['TOLERANCE']
        self.GENOCIDE_PERC = kwargs['GENOCIDE_PERC']
        self.destroy = Destroy(max_stagnant_generations=self.MAX_STAGNANT_GENERATIONS, tolerance=self.TOLERANCE)

        self.curr_fitness_evaluations = 0
        self.curr_most_fit_individual = 0
        self.generations = 0
        self.iters = 500

    def get_population(self):
        return self.init(self.GENOME_SIZE, self.POPULATION_SIZE)
 
    def solve(self, population):
        is_solution = False
        self.curr_fitness_evaluations = 0
        self.curr_most_fit_individual = 0
        self.generations = 100

        max_history = []
        average_history = [] 
        min_history = [] 

        max_history.append(max(self.fitness(population)))
        average_history.append(sum(self.fitness(population))/len(population))
        min_history.append(min(self.fitness(population)))

        # WITH GENOCIDE
        while( not(self.termination( curr_fitness_evaluations=self.curr_fitness_evaluations,
                                     max_fitness_evaluations=self.MAX_FITNESS_EVALUATIONS,
                                     curr_iterations=0,  
                                     max_iterations=10000, 
                                     is_solution=is_solution )) ):
            
            # set both at expected infimum to begin with
            exploration_factor = max(0.1, (self.GENOME_SIZE / (self.GENOME_SIZE + self.generations**(3/4)))) # declines to its min: 1.0 -> 0.1
            exploitation_factor = max(0.1, 1-exploration_factor) # grows to its max: 0.1 -> 1.0

            dynamic_recombination_rate = self.RECOMBINATION_RATE * exploration_factor 
            dynamic_mutation_rate = self.MUTATION_RATE * exploitation_factor
            
            selected_parents = self.parent_selection(population, self.NUM_OFFSPRING_RATE, self.TOURNAMENT_GROUP_SIZE, self.fitness)
            offspring = self.recombination(selected_parents, dynamic_recombination_rate, self.GENOME_SIZE)
            mutated_offspring = self.mutation(offspring, dynamic_mutation_rate, self.GENOME_SIZE)
            offspring_fitness = self.fitness(mutated_offspring) 
            population = self.survival_selection(population, mutated_offspring, self.fitness, self.WEIGHTING_EXPONENT)
            self.curr_fitness_evaluations += (len(offspring_fitness) + len(population))

            max_history.append(max(self.fitness(population)))
            average_history.append(sum(self.fitness(population))/len(population))
            min_history.append(min(self.fitness(population)))

            if (max(self.fitness(population)) == 1):
                return self.curr_fitness_evaluations, max_history, average_history, min_history

            self.curr_most_fit_individual = max(self.fitness(population))
            genocide_factor = max(1/6, 1 - (self.GENOME_SIZE / (self.GENOME_SIZE + self.generations**(3/4)))) # declines to its min: 1.0 -> 0.1
            dynamic_genocide_perc = self.GENOCIDE_PERC * genocide_factor
            if self.destroy.check_stagnation(self.curr_most_fit_individual):
                population = self.destroy.apply_genocide(population, dynamic_genocide_perc, self.fitness)

            self.generations += 1
        return self.curr_fitness_evaluations, max_history, average_history, min_history
    
    def worker(self, iters):
        tot_max_history = []
        tot_average_history = []
        tot_min_history = []
        avg_gens = 0
        for _ in range(iters):
            curr_fitness_evaluations, max_history, average_history, min_history = self.solve(self.get_population())
            tot_max_history.append(max_history)
            tot_average_history.append(average_history)
            tot_min_history.append(min_history)
            avg_gens += curr_fitness_evaluations
        return round(avg_gens / iters, 2), pad_and_average(tot_max_history), pad_and_average(tot_average_history), pad_and_average(tot_min_history)

def pad_and_average(lists):
    max_len = max([len(ls) for ls in lists])
    averages = []
    for x in range(max_len):
        num = 0
        tot = 0
        for y in range(len(lists)):
            num += 1
            if len(lists[y]) > x:
                tot += lists[y][x]
            else:
                tot += lists[y][-1]
        averages.append(tot/num)

    return averages

if __name__ == '__main__':
    eval_counts = []

    exponent = 0
    ga = Genetic_Algorithm(WEIGHTING_EXPONENT=exponent,**config.setup_final)
    eval_counts.append(ga.worker(ga.iters))
    print(f"progress {1}%")

    exponent = 15
    ga = Genetic_Algorithm(WEIGHTING_EXPONENT=exponent,**config.setup_final)
    eval_counts.append(ga.worker(ga.iters))
    print(f"progress {2}%")

    exponent = 50
    ga = Genetic_Algorithm(WEIGHTING_EXPONENT=exponent,**config.setup_final)
    eval_counts.append(ga.worker(ga.iters))
    print(f"progress {3}%")

    with open(config.exponent_out, 'w') as log_file:
        for res in eval_counts:
            log_file.write(f"{res[1]},,{res[2]},,{res[3]}\n")
    
    Visualization('terminal').exponent_convergance_plot(config.exponent_out, ga.iters)
