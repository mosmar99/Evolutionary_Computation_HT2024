# CONSTANTS
GENOME_SIZE = 8 # N-QUEENS (EX: 'every Queen has a genome size of 8')
POPULATION_SIZE = 100
NUM_OFFSPRING = 2
RECOMBINATION_RATE = 0.70  
MUTATION_RATE = 0.8
MAX_FITNESS_EVALUATIONS = 10000
FILENAME = 'log.csv'
FILE_DIR = 'logs/'

setup = { 'GENOME_SIZE':                  8,
            'POPULATION_SIZE':            100,
            'NUM_OFFSPRING':              20,
            'RECOMBINATION_RATE':         0.80,
            'MUTATION_RATE':              0.10,
            'MAX_FITNESS_EVALUATIONS':    10000,
            'TOURNAMENT_GROUP_SIZE':      0.2, 
            'initialization_strategy':    'random',
            'fitness_strategy':           'conflict_based',
            'parent_selection_strategy':  'tournament',
            'survival_selection_strategy':'prob_survival',
            'recombination_strategy':     'partially_mapped_crossover',
            'mutation_strategy':          'inversion_mutation',
            'termination_strategy':       'evaluation_count',
            'visualization_strategy':     'terminal',
            'metric_strategy':            'avg_similarity',
            'logging_strategy':           'logger',
            'print_type':                 'csv_file'
    }

