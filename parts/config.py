# paths
FILENAME = 'log.csv'
FILE_DIR = 'logs/'
log_path = 'logs/fit_eval.log'
log_path2 = 'logs/eval_count_by_strategy.log'
log_path3 = 'logs/LHS_Setups.log'
log_path4 = 'logs/LHS_Setups_evals.log'
log_path5 = 'logs/heatmap_data.log'
curr_setups_loc = 'logs/curr_setups.log'
log_path6 = 'logs/diversity_vs_n.log'
log_path_geno5 = 'logs/geno_plot5.log'
log_path_geno6 = 'logs/geno_plot6.log' 
log_path_geno7 = 'logs/geno_plot7.log' 
log_path_geno8 = 'logs/geno_plot8.log' 
log_path_geno9 = 'logs/geno_plot9.log' 
log_path_geno10 = 'logs/geno_plot10.log' 
max_vs_mean_geno = 'logs/max_vs_mean_geno.log'
dynamic_vs_static = 'logs/dynamic_vs_static.log'
dyn_vs_static_stagn = 'logs/dyn_vs_static_stagn.log'

# setups
setup = {   'GENOME_SIZE':                  8,
            'POPULATION_SIZE':            100,
            'NUM_OFFSPRING_RATE':          0.2,
            'RECOMBINATION_RATE':         0.80,
            'MUTATION_RATE':              0.10,
            'MAX_FITNESS_EVALUATIONS':    10000,
            'TOURNAMENT_GROUP_SIZE':      0.2, 
            'initialization_strategy':    'random',
            'fitness_strategy':           'conflict_based',
            'parent_selection_strategy':  'tournament',
            'survival_selection_strategy':'prob_survival',
            'recombination_strategy':     'ordered_crossover',
            'mutation_strategy':          'inversion_mutation',
            'termination_strategy':       'evaluation_count',
            'visualization_strategy':     'terminal',
            'metric_strategy':            'avg_similarity',
            'logging_strategy':           'logger',
            'print_type':                 'csv_file'
    }

setup1 = { 'GENOME_SIZE':                  8,
            'POPULATION_SIZE':            100,
            'NUM_OFFSPRING_RATE':          0.2,
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
}

setup2 = { 'GENOME_SIZE':                  8,
            'POPULATION_SIZE':            100,
            'NUM_OFFSPRING_RATE':          0.1,
            'RECOMBINATION_RATE':         0.90,
            'MUTATION_RATE':              0.28,
            'MAX_FITNESS_EVALUATIONS':    10000,
            'TOURNAMENT_GROUP_SIZE':      0.28, 
            'initialization_strategy':    'random',
            'fitness_strategy':           'conflict_based',
            'parent_selection_strategy':  'tournament',
            'survival_selection_strategy':'prob_survival',
            'recombination_strategy':     'partially_mapped_crossover',
            'mutation_strategy':          'swap_mutation',
            'termination_strategy':       'evaluation_count',
}

setup3 = { 'GENOME_SIZE':                  8,
            'POPULATION_SIZE':            100,
            'NUM_OFFSPRING_RATE':          0.3,
            'RECOMBINATION_RATE':         0.7,
            'MUTATION_RATE':              0.05,
            'MAX_FITNESS_EVALUATIONS':    10000,
            'TOURNAMENT_GROUP_SIZE':      0.5, 
            'initialization_strategy':    'random',
            'fitness_strategy':           'conflict_based',
            'parent_selection_strategy':  'tournament',
            'survival_selection_strategy':'prob_survival',
            'recombination_strategy':     'two_point_crossover',
            'mutation_strategy':          'duplicate_replacement',
            'termination_strategy':       'evaluation_count',
}

setup4 = { 'GENOME_SIZE':                  8,
            'POPULATION_SIZE':            100,
            'NUM_OFFSPRING_RATE':          0.15,
            'RECOMBINATION_RATE':         0.88,
            'MUTATION_RATE':              0.83,
            'MAX_FITNESS_EVALUATIONS':    10000,
            'TOURNAMENT_GROUP_SIZE':      0.33, 
            'initialization_strategy':    'random',
            'fitness_strategy':           'conflict_based',
            'parent_selection_strategy':  'tournament',
            'survival_selection_strategy':'prob_survival',
            'recombination_strategy':     'even_cut_and_crossfill',
            'mutation_strategy':          'inversion_mutation',
            'termination_strategy':       'evaluation_count',
}

setup5 = { 'GENOME_SIZE':                  8,
            'POPULATION_SIZE':            100,
            'NUM_OFFSPRING_RATE':          0.4,
            'RECOMBINATION_RATE':         0.90,
            'MUTATION_RATE':              0.05,
            'MAX_FITNESS_EVALUATIONS':    10000,
            'TOURNAMENT_GROUP_SIZE':      0.16, 
            'initialization_strategy':    'random',
            'fitness_strategy':           'conflict_based',
            'parent_selection_strategy':  'tournament',
            'survival_selection_strategy':'prob_survival',
            'recombination_strategy':     'pmx_dp_rm',
            'mutation_strategy':          'inversion_mutation',
            'termination_strategy':       'evaluation_count',
}

setup6 = { 'GENOME_SIZE':                  8,
            'POPULATION_SIZE':            100,
            'NUM_OFFSPRING_RATE':          0.4,
            'RECOMBINATION_RATE':         0.90,
            'MUTATION_RATE':              0.05,
            'MAX_FITNESS_EVALUATIONS':    10000,
            'TOURNAMENT_GROUP_SIZE':      0.16, 
            'initialization_strategy':    'random',
            'fitness_strategy':           'conflict_based',
            'parent_selection_strategy':  'tournament',
            'survival_selection_strategy':'prob_survival',
            'recombination_strategy':     'pmx_dp_rm',
            'mutation_strategy':          'inversion_mutation',
            'termination_strategy':       'evaluation_count',
}

# # MAIN3
# param_ranges = {
#     'POPULATION_SIZE': (50, 200),
#     'NUM_OFFSPRING_RATE': (0.1, 0.5),   
#     'RECOMBINATION_RATE': (0.6, 0.9),
#     'MUTATION_RATE': (0.01, 0.5),
#     'TOURNAMENT_GROUP_SIZE': (0.1, 0.8),
# }

# strategy_options = {
#     'initialization_strategy': ['random_permutations'],
#     'parent_selection_strategy': ['tournament'],
#     'recombination_strategy': ['partially_mapped_crossover', 'pmx_dp_rm', 'ordered_crossover'],
#     'mutation_strategy': ['swap_mutation', 'inversion_mutation', 'duplicate_replacement'],
#     'survival_selection_strategy': ['prob_survival'],
# }

# constants = { 
#     'GENOME_SIZE': 8,
#     'MAX_FITNESS_EVALUATIONS': 10000,
#     'fitness_strategy': 'conflict_based',
#     'termination_strategy': 'evaluation_count',
#     'visualization_strategy': 'terminal',
#     'metric_strategy': 'avg_similarity',
#     'logging_strategy': 'logger',
#     'print_type': 'csv_file',
# }

# MAIN3
param_ranges = {
    'POPULATION_SIZE': (99, 101),
    'NUM_OFFSPRING_RATE': (0.18, 0.72),   
    'RECOMBINATION_RATE': (0.6, 0.9),
    'MUTATION_RATE': (0.01, 0.28),
    'TOURNAMENT_GROUP_SIZE': (0.3, 0.6),
}

strategy_options = {
    'initialization_strategy': ['random'],
    'parent_selection_strategy': ['tournament'],
    'recombination_strategy': ['ordered_crossover'],
    'mutation_strategy': ['creep_mutation', 'scramble_mutation'],
    'survival_selection_strategy': ['prob_survival'],
}

constants = { 
    'GENOME_SIZE': 8,
    'MAX_FITNESS_EVALUATIONS': 10000,
    'fitness_strategy': 'conflict_based',
    'termination_strategy': 'evaluation_count',
    'visualization_strategy': 'terminal',
    'metric_strategy': 'avg_similarity',
    'logging_strategy': 'logger',
    'print_type': 'csv_file',
}

# param_ranges = {
#     'RECOMBINATION_RATE': (0.05, 0.95),
# }

# strategy_options = {
# }

# # for the sake of printing topX
# constants = { 
#     'GENOME_SIZE': 7,
#     'POPULATION_SIZE': 100,
#     'MAX_FITNESS_EVALUATIONS': 10000,
#     'fitness_strategy': 'conflict_based',
#     'termination_strategy': 'evaluation_count',
#     'visualization_strategy': 'terminal',
#     'metric_strategy': 'avg_similarity',
#     'logging_strategy': 'logger',
#     'print_type': 'csv_file',
#     'NUM_OFFSPRING_RATE': 0.381,
#     'MUTATION_RATE': 0.306,
#     'TOURNAMENT_GROUP_SIZE': 0.372,
#     'initialization_strategy': ['random_permutations'],
#     'parent_selection_strategy': ['tournament'],
#     'recombination_strategy': ['partially_mapped_crossover'],
#     'mutation_strategy': ['duplicate_replacement'],
#     'survival_selection_strategy': ['prob_survival']
# }

setup_genocide = {  'GENOME_SIZE':                    6,
                    'POPULATION_SIZE':              100,
                    'NUM_OFFSPRING_RATE':           0.2,
                    'RECOMBINATION_RATE':          0.80,
                    'MUTATION_RATE':               0.10,
                    'MAX_FITNESS_EVALUATIONS':    12000,
                    'TOURNAMENT_GROUP_SIZE':        0.2, 
                    'MAX_STAGNANT_GENERATIONS':      3,
                    'TOLERANCE':                   1e-2,
                    'GENOCIDE_PERC':                0.2,
                    'initialization_strategy':    'random',
                    'fitness_strategy':           'conflict_based',
                    'parent_selection_strategy':  'tournament',
                    'survival_selection_strategy':'prob_survival',
                    'recombination_strategy':     'partially_mapped_crossover',
                    'mutation_strategy':          'inversion_mutation',
                    'termination_strategy':       'evaluation_count',
                    'visualization_strategy':     'terminal',
}
setup_mean_or_max = {  'GENOME_SIZE':                 6,
                    'POPULATION_SIZE':              100,
                    'NUM_OFFSPRING_RATE':           0.2,
                    'RECOMBINATION_RATE':          0.80,
                    'MUTATION_RATE':               0.1,
                    'MAX_FITNESS_EVALUATIONS':    12000,
                    'TOURNAMENT_GROUP_SIZE':        0.2, 
                    'MAX_STAGNANT_GENERATIONS':      3,
                    'TOLERANCE':                   1e-2,
                    'GENOCIDE_PERC':                0.2,
                    'initialization_strategy':    'random',
                    'fitness_strategy':           'conflict_based',
                    'parent_selection_strategy':  'tournament',
                    'survival_selection_strategy':'prob_survival',
                    'recombination_strategy':     'partially_mapped_crossover',
                    'mutation_strategy':          'inversion_mutation',
                    'termination_strategy':       'evaluation_count',
                    'visualization_strategy':     'terminal',
}

setup_dynamic = {  'GENOME_SIZE':                     6,
                    'POPULATION_SIZE':              100,
                    'NUM_OFFSPRING_RATE':           0.2,
                    'RECOMBINATION_RATE':          0.90,
                    'MUTATION_RATE':               0.20,
                    'MAX_FITNESS_EVALUATIONS':    12000,
                    'TOURNAMENT_GROUP_SIZE':        0.2, 
                    'MAX_STAGNANT_GENERATIONS':      3,
                    'TOLERANCE':                   1e-2,
                    'GENOCIDE_PERC':                0.2,
                    'initialization_strategy':    'random',
                    'fitness_strategy':           'conflict_based',
                    'parent_selection_strategy':  'tournament',
                    'survival_selection_strategy':'prob_survival',
                    'recombination_strategy':     'partially_mapped_crossover',
                    'mutation_strategy':          'inversion_mutation',
                    'termination_strategy':       'evaluation_count',
                    'visualization_strategy':     'terminal',
}

setup_dyn_stagn = {  'GENOME_SIZE':                   7,
                    'POPULATION_SIZE':              100,
                    'NUM_OFFSPRING_RATE':           0.2,
                    'RECOMBINATION_RATE':          0.90,
                    'MUTATION_RATE':               0.20,
                    'MAX_FITNESS_EVALUATIONS':    30000,
                    'TOURNAMENT_GROUP_SIZE':        0.2, 
                    'MAX_STAGNANT_GENERATIONS':      3,
                    'TOLERANCE':                   1e-2,
                    'GENOCIDE_PERC':                0.3,
                    'initialization_strategy':    'random',
                    'fitness_strategy':           'conflict_based',
                    'parent_selection_strategy':  'tournament',
                    'survival_selection_strategy':'prob_survival',
                    'recombination_strategy':     'partially_mapped_crossover',
                    'mutation_strategy':          'inversion_mutation',
                    'termination_strategy':       'evaluation_count',
                    'visualization_strategy':     'terminal',
}