"""
This file contains the Log class which is responsible for logging information to a file in csv format.
Authors: Mahmut Osmanovic (mosmar99), Sebastian Tuura (tuura01), Isac Paulsson (isacpaulsson), Emil Wagman (Neobyte01), Mohammad Al Khaled (MohamadAlkhaled)
Last updated: 2024-10-02
"""

import numpy as np
import logging
import config

class Log():

    # init function for Log class
    # input: logging_strategy: string
    # output: None
    def __init__(self, logging_strategy):
        logging_strategies = { 'logger' : self.log }
        self.logging_strategy = logging_strategies[logging_strategy]

    # call function for Log class
    # input: *args, **kwargs
    # output: self.logging_strategy(*args, **kwargs)
    def __call__(self, *args, **kwargs):
        self.logging_strategy(*args, **kwargs)

    # log the information to the file
    # input: curr_fitness_evaluations: int, avg_sim: float, offspring_fitness: numpy array
    # output: None
    def log(self, curr_fitness_evaluations, avg_sim, offspring_fitness):
        # rounds the offspring fitness to 2 decimal places
        # logs the information to the file in the format: evaluation_count,avg_similarity_score,fitness_score
        # file name is set in the config file

        offspring_fitness = round(np.mean(offspring_fitness), 2) 
        logging.basicConfig(filename=config.log_path, level=logging.INFO,
                    format='%(message)s', filemode='w')
        log_obj = logging.getLogger()
        if(curr_fitness_evaluations == 0):
            log_obj.info(f"evaluation_count,avg_similarity_score,fitness_score")
        log_obj.info("%d, %f, %f" % (curr_fitness_evaluations, avg_sim, round(np.mean(offspring_fitness), 2)))

