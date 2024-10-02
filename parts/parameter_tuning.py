"""
This file contains the parameter tuning class which is responsible for tuning the parameters of the genetic algorithm.
Authors: Mahmut Osmanovic (mosmar99), Sebastian Tuura (tuura01), Isac Paulsson (isacpaulsson), Emil Wagman (Neobyte01), Mohammad Al Khaled (MohamadAlkhaled)
Last updated: 2024-10-02
"""

import numpy as np
from scipy.stats import qmc
import config
import ast
import json
import itertools

# Parameter tuning class
class Parameter_Tuning():
    # init function for Parameter_Tuning class
    # input: tuning_strategy: string
    # output: None
    def __init__(self, tuning_strategy):
        tuning_strategies = { 'LHS': self.pt_LHS,
                            'Halton': self.pt_Halton,
                            'Sobol': self.pt_Sobol,
                            'Grid': self.pt_Grid
                            }
        
        self.tuning_strategy = tuning_strategies[tuning_strategy]
        self.strategy_name = tuning_strategy
    
    # call function for Parameter_Tuning class
    # input: *args, **kwargs
    # output: self.tuning_strategy(*args, **kwargs)
    def __call__(self, *args, **kwargs):
        return self.tuning_strategy(*args, **kwargs)

    # Latin Hypercube Sampling
    # input: n_samples: int
    # output: setups: list
    # https://en.wikipedia.org/wiki/Latin_hypercube_sampling
    def pt_LHS(self, n_samples=100):
        # Create a Latin Hypercube sampler
        sampler = qmc.LatinHypercube(d=len(config.param_ranges))
        samples = sampler.random(n=n_samples)

        # Generate setups based on the samples
        setups = []
        for sample in samples:
            setup = {}
            for i, (param, (low, high)) in enumerate(config.param_ranges.items()):
                if (param == "POPULATION_SIZE"):
                    setup[param] = round(low + (high - low) * sample[i])
                else:
                    setup[param] = round(low + (high - low) * sample[i], 3)

            for strategy, options in config.strategy_options.items():
                setup[strategy] = np.random.choice(options)

            setups.append(setup)
        
        return setups

    # Halton sequence
    # input: n_samples: int
    # output: setups: list
    # https://en.wikipedia.org/wiki/Halton_sequence
    def pt_Halton(self, n_samples=100):
        # Create a Halton sequence sampler
        sampler = qmc.Halton(d=len(config.param_ranges))
        samples = sampler.random(n=n_samples)

        # Generate setups based on the samples
        setups = []
        for sample in samples:
            setup = {}
            for i, (param, (low, high)) in enumerate(config.param_ranges.items()):
                if (param == "POPULATION_SIZE"):
                    setup[param] = round(low + (high - low) * sample[i])
                else:
                    setup[param] = round(low + (high - low) * sample[i], 3)

            for strategy, options in config.strategy_options.items():
                setup[strategy] = np.random.choice(options)

            setups.append(setup)
        
        return setups

    # Sobol sequence
    # input: n_samples: int
    # output: setups: list
    # https://en.wikipedia.org/wiki/Sobol_sequence
    def pt_Sobol(self, n_samples=100):
        # Create a Sobol sequence sampler
        sampler = qmc.Sobol(d=len(config.param_ranges), scramble=False)
        samples = sampler.random_base2(m=int(np.log2(n_samples)))

        # Generate setups based on the samples
        setups = []
        for sample in samples:
            setup = {}
            for i, (param, (low, high)) in enumerate(config.param_ranges.items()):
                if param == "POPULATION_SIZE":
                    setup[param] = round(low + (high - low) * sample[i])
                else:
                    setup[param] = round(low + (high - low) * sample[i], 3)

            # Randomly choose strategy options
            for strategy, options in config.strategy_options.items():
                setup[strategy] = np.random.choice(options)

            setups.append(setup)

        return setups

    # Grid sampling
    # input: n_samples: int
    # output: setups: list
    def pt_Grid(self, n_samples=100):
        # Create a grid of samples
        grid_size = int(np.round(np.sqrt(n_samples)))
        x_values = np.linspace(0, 1, grid_size)
        y_values = np.linspace(0, 1, grid_size)
        x_grid, y_grid = np.meshgrid(x_values, y_values)
        samples = np.vstack([np.round(x_grid.ravel(), 3), np.round(y_grid.ravel(), 2)]).T

        # Generate setups based on the samples
        setups = []
        for sample in samples:
            setup = {}
            for i, (param, (low, high)) in enumerate(config.param_ranges.items()):
                if param == "POPULATION_SIZE":
                    setup[param] = round(low + (high - low) * sample[i])
                else:
                    setup[param] = round(low + (high - low) * sample[i], 3)

            # Randomly choose strategy options
            for strategy, options in config.strategy_options.items():
                setup[strategy] = np.random.choice(options)

            setups.append(setup)

        return setups
    
    # Extract the top X setups from the evaluations file & store them in a new file
    # input: evals_file_loc: string, setups_file_loc: string, output_file_loc: string, topX: int
    # output: None
    def extract_topX_setups(self,evals_file_loc, setups_file_loc, output_file_loc, topX):
        with open(evals_file_loc, 'r') as eval_file:
            eval_lines = eval_file.readlines()[1:]  # Skip header

        evals = []
        setup_ids = []

        # Extract the setup_id and evaluation_count from each line
        for line in eval_lines:
            parts = line.strip().split(',')
            setup_id = parts[0]  
            evaluation_count = int(parts[-1])  
            setup_ids.append(setup_id)
            evals.append(evaluation_count)

        # Get top X setups (lowest eval score)
        evals = np.array(evals)
        sorted_arr_indices = np.argsort(evals)[:topX]  # Indices of the top X setups

        with open(setups_file_loc, 'r') as setups_file:
            setups = ast.literal_eval(''.join(setups_file.readlines()[3:]))  # Skip first 3 lines

        topX_setups = [setups[idx] for idx in sorted_arr_indices]  

        # Write the top X setups to the output file
        with open(output_file_loc, 'w') as output_file:
            for idx in range(topX):
                sorted_idx = sorted_arr_indices[idx]  
                setup = topX_setups[idx]  
                setup_id = setup_ids[sorted_idx]  

                output_file.write(f"{setup_id} = {{\n")
                for key, value in config.constants.items():
                    output_file.write(f"    '{key}': {repr(value)},\n")
                for key, value in setup.items():
                    output_file.write(f"    '{key}': {repr(value)},\n")
                output_file.write("}\n\n")

# Example usage, make sure you have the correct log files
if __name__ == '__main__':
    pt = Parameter_Tuning('LHS')
    evals_file_loc = 'logs/LHS_Setups_evals.log'
    setups_file_loc = 'logs/LHS_Setups.log'
    output_file_loc = 'topX_setups.py'
    topX = 10
    pt.extract_topX_setups(evals_file_loc, setups_file_loc, output_file_loc, topX)