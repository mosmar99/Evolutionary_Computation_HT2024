import numpy as np
from scipy.stats import qmc
import config
import ast
import json
    
class Parameter_Tuning():
    def __init__(self, tuning_strategy):
        tuning_strategies = { 'LHS': self.pt_LHS }
        
        self.tuning_strategy = tuning_strategies[tuning_strategy]
        self.strategy_name = tuning_strategy
    
    def __call__(self, *args, **kwargs):
        return self.tuning_strategy(*args, **kwargs)

    def pt_LHS(self, n_samples=100):
        sampler = qmc.LatinHypercube(d=len(config.param_ranges))
        samples = sampler.random(n=n_samples)
    
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
    
    def extract_topX_setups(self,evals_file_loc, setups_file_loc, output_file_loc, topX):
        eval_file = open(evals_file_loc, 'r')
        eval_file = sorted(eval_file, key=lambda x: int(x.split('_')[1].split(',')[0]))
        evals = []
        char_eval = []
        is_comma = False
        for line in eval_file:
            is_comma = False
            char_eval.clear()
            for char in line:
                if(is_comma == False):
                    if(char == ','):
                        is_comma = True
                else:
                    if(char == '.' or char == ','):
                        break
                    char_eval.append(char)
            evals.append(int(''.join(char_eval)))
        # get topX evals (lowest eval score)
        evals = np.array(evals)
        sorted_arr_indicies = np.argsort(np.array(evals))[:topX]
        setups = np.array(ast.literal_eval(''.join(open(setups_file_loc).readlines()[3:])))
        topX_setups = setups[sorted_arr_indicies]

        output_file = open(output_file_loc, 'w')
        for idx in range(topX):
            sorted_idx = sorted_arr_indicies[idx]
            setup = topX_setups[idx]
            output_file.write(f"setup{sorted_idx + 1} = {{\n")
            for key, value in config.constants.items():
                output_file.write(f"    '{key}': {repr(value)},\n")
            for key, value in setup.items():
                output_file.write(f"    '{key}': {repr(value)},\n")
            output_file.write("}\n\n")

if __name__ == '__main__':
    pt = Parameter_Tuning('LHS')
    evals_file_loc = 'logs/LHS_Setups_evals.log'
    setups_file_loc = 'logs/LHS_Setups.log'
    output_file_loc = 'topX_setups.py'
    topX = 10
    pt.extract_topX_setups(evals_file_loc, setups_file_loc, output_file_loc, topX)