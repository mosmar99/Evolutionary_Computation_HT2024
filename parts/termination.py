import numpy as np

class Evaluation_Count():
    def exec(self, curr_fitness_evaluations=0, max_fitness_evaluations=10000, curr_iterations=None, max_iterations=None, is_solution=False):
        if((curr_fitness_evaluations >= max_fitness_evaluations) or (is_solution)):
            return True
        return False 
       
class Iteration_Count():
    def exec(self, curr_fitness_evaluations=None, max_fitness_evaluations=None, curr_iterations=0, max_iterations=10000, is_solution=False):
        if((curr_iterations >= max_iterations) or (is_solution)):
            return True
        return False    

class Termination(object):
    def __init__(self, termination_strategy):
        self.termination_strategy = termination_strategy
    
    def is_terminate(self, curr_fitness_evaluations=0, max_fitness_evaluations=10000, 
                     curr_iterations=0, max_iterations=10000, is_solution=False):
        return self.termination_strategy.exec(curr_fitness_evaluations, max_fitness_evaluations, 
                                              curr_iterations, max_iterations,
                                              is_solution)