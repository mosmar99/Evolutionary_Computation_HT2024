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
                if (param == "POPULATION_SIZE" or param == "NUM_OFFSPRING"):
                    setup[param] = round(low + (high - low) * sample[i])
                else:
                    setup[param] = round(low + (high - low) * sample[i], 3)

            for strategy, options in config.strategy_options.items():
                setup[strategy] = np.random.choice(options)

            setups.append(setup)
        
        return setups
    
    def extract_topX_setups(self,evals_file, setups_file, output_file, top_x):
        pass


if __name__ == '__main__':
    pt = Parameter_Tuning('LHS')
    evals_file = 'logs/LHS_Setups_evals_copy.log'
    setups_file = 'logs/LHS_Setups_copy.log'
    output_file = 'topX_configs.py'
    top_x = 10
    pt.extract_topX_setups(evals_file, setups_file, output_file, top_x)