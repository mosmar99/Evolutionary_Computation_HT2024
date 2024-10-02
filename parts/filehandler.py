"""
This file contains the file handler class which is responsible for logging information to a file in csv format.
Authors: Mahmut Osmanovic (mosmar99), Sebastian Tuura (tuura01), Isac Paulsson (isacpaulsson), Emil Wagman (Neobyte01), Mohammad Al Khaled (MohamadAlkhaled)
Last updated: 2024-10-02
"""

import os, csv, config

class File_Handler:
    # init function for File_Handler class
    # input: print_type: string
    # output: None
    def __init__(self, print_type):
        print_types = { "csv_file": self.csv_file}
        self.fitness_strategy = print_types[print_type]
        self.strategy_name = print_type
        self.filenameAndPath = "./" + config.FILE_DIR + "/" + config.FILENAME

        #check that directory and file exists
        self.check_dir()
        self.check_file()

    # call function for File_Handler class
    # input: *args, **kwargs
    # output: self.fitness_strategy(*args, **kwargs)
    def __call__(self, *args, **kwargs):
        return self.fitness_strategy(*args, **kwargs)

    # check if directory exists, if not create it
    # input: None
    # output: None
    def check_dir(self):
        if not os.path.exists(config.FILE_DIR):
            os.makedirs(config.FILE_DIR)

    # check if file exists, if not create it and add the headers
    # input: None
    # output: None
    def check_file(self):
        with open(self.filenameAndPath, "w", newline="") as csvfile:
            csv.writer(csvfile).writerow([
                'EVALUATIONS','MOST_FIT','GENOME_SIZE', 'POPULATION_SIZE', 'NUM_OFFSPRING',
                'RECOMBINATION_RATE', 'MUTATION_RATE', 'MAX_FITNESS_EVALUATIONS',
                'Init Strategy', 'Fitness Function', 'Parent Selection',
                'Survival Selection', 'Recombination', 'Mutation'
            ])

    # For logging information to file in csv format.
    # input: **kwargs
    # output: None
    def csv_file(self, **kwargs):

        # Open file and write the information contained in the Kwargs to the file
        with open(self.filenameAndPath, 'a', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow([
                kwargs.get('CURR_FITNESS_EVALUATIONS'),
                kwargs.get('CURR_MOST_FIT_INDIVIDUAL'),
                kwargs.get('GENOME_SIZE', ''),
                kwargs.get('POPULATION_SIZE', ''),
                kwargs.get('NUM_OFFSPRING', ''),
                kwargs.get('RECOMBINATION_RATE', ''),
                kwargs.get('MUTATION_RATE', ''),
                kwargs.get('MAX_FITNESS_EVALUATIONS', ''),
                kwargs.get('initialization_strategy', ''),
                kwargs.get('fitness_strategy', ''),
                kwargs.get('parent_selection_strategy', ''),
                kwargs.get('survival_selection_strategy', ''),
                kwargs.get('recombination_strategy', ''),
                kwargs.get('mutation_strategy', '')
            ])