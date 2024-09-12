      
class Termination:
    def __init__(self, termination_strategy):
        termination_strategies = { 'iteration_count': self.iteration_count,
                                   'evaluation_count': self.evaluation_count}
        self.termination_strategy = termination_strategies[termination_strategy]
        self.strategy_name = termination_strategy
    
    def __call__(self, *args, **kwargs):
        return self.termination_strategy(*args, **kwargs)
    
    def iteration_count(self, curr_fitness_evaluations=None, max_fitness_evaluations=None, curr_iterations=0, max_iterations=10000, is_solution=False):
        if((curr_iterations >= max_iterations) or (is_solution)):
            return True
        return False 

    def evaluation_count(self, curr_fitness_evaluations=0, max_fitness_evaluations=10000, curr_iterations=None, max_iterations=None, is_solution=False):
        if((curr_fitness_evaluations >= max_fitness_evaluations) or (is_solution)):
            return True
        return False 