import os, csv, config

class File_Handler:
    def __init__(self, print_type):
        print_types = { "csv_file": self.csv_file}
        self.fitness_strategy = print_types[print_type]
        self.strategy_name = print_type
        self.filenameAndPath = "./" + config.FILE_DIR + "/" + config.FILENAME

    def __call__(self, *args, **kwargs):
        return self.fitness_strategy(*args, **kwargs)

    def check_dir(self):
        if not os.path.exists(config.FILE_DIR):
            os.makedirs(config.FILE_DIR)

    def check_file(self):
        if not os.path.exists(self.filenameAndPath):
            with open(self.filenameAndPath, "w", newline="") as csvfile:
                csv.writer(csvfile).writerow([
                    'EVALUATIONS','MOST_FIT','GENOME_SIZE', 'POPULATION_SIZE', 'NUM_OFFSPRING',
                    'RECOMBINATION_RATE', 'MUTATION_RATE', 'MAX_FITNESS_EVALUATIONS',
                    'Init Strategy', 'Fitness Function', 'Parent Selection',
                    'Survival Selection', 'Recombination', 'Mutation',
                    'Evolution Strategy'
                ])

    # For logging information to file in csv format.
    def csv_file(self, **kwargs):

        self.check_dir()
        self.check_file()

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
                kwargs.get('mutation_strategy', ''),
                kwargs.get('evolution_strategy', '')
            ])