import numpy as np
import logging
import config

class Log():
    def __init__(self, logging_strategy):
        logging_strategies = { 'logger' : self.log }
        self.logging_strategy = logging_strategies[logging_strategy]

    def __call__(self, *args, **kwargs):
        self.logging_strategy(*args, **kwargs)

    def log(self, curr_fitness_evaluations, avg_sim, offspring_fitness):
        offspring_fitness = round(np.mean(offspring_fitness), 2)
        logging.basicConfig(filename=config.log_path, level=logging.INFO, 
                    format='%(message)s', filemode='w')
        log_obj = logging.getLogger()
        if(curr_fitness_evaluations == 0):
            log_obj.info(f"evaluation_count,avg_similarity_score,fitness_score")
        log_obj.info("%d, %f, %f" % (curr_fitness_evaluations, avg_sim, round(np.mean(offspring_fitness), 2)))

