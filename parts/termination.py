"""
This file contains the Terminations class which is responsible for checking if the termination criteria are met.
Authors: Mahmut Osmanovic (mosmar99), Sebastian Tuura (tuura01), Isac Paulsson (isacpaulsson), Emil Wagman (Neobyte01), Mohammad Al Khaled (MohamadAlkhaled)
Last updated: 2024-10-02
"""

# Terminations class
class Termination:
    # init function for Termination class
    # input: termination_strategy: string
    # output: None
    def __init__(self, termination_strategy):
        termination_strategies = { 'iteration_count': self.iteration_count,
                                   'evaluation_count': self.evaluation_count}
        self.termination_strategy = termination_strategies[termination_strategy]

    # call function for Termination class
    # input: *args, **kwargs
    # output: self.termination_strategy(*args, **kwargs)
    def __call__(self, *args, **kwargs):
        return self.termination_strategy(*args, **kwargs)
    
    # checks if the current iteration count is equal to the maximum iteration count
    # input: curr_fitness_evaluations: int, max_fitness_evaluations: int, curr_iterations: int, max_iterations: int, is_solution: bool
    # output: True if the current iteration count is equal to the maximum iteration count, False otherwise
    def iteration_count(self, curr_fitness_evaluations=None, max_fitness_evaluations=None, curr_iterations=0, max_iterations=10000, is_solution=False):
        if((curr_iterations >= max_iterations) or (is_solution)):
            return True
        return False 
    
    # checks if the current fitness evaluation count is equal to the maximum fitness evaluation count
    # input: curr_fitness_evaluations: int, max_fitness_evaluations: int, curr_iterations: int, max_iterations: int, is_solution: bool
    # output: True if the current fitness evaluation count is equal to the maximum fitness evaluation count, False otherwise
    def evaluation_count(self, curr_fitness_evaluations=0, max_fitness_evaluations=10000, curr_iterations=None, max_iterations=None, is_solution=False):
        if((curr_fitness_evaluations >= max_fitness_evaluations) or (is_solution)):
            return True
        return False 