class Stagnation:
    def __init__(self, stagnation_strategy):
        stagnation_strategies = { 'static': self.static,
                                    'dynamic': self.dynamic }
        
        self.stagnation_strategy = stagnation_strategies[stagnation_strategy]
        self.strategy_name = stagnation_strategy

    def __call__(self, *args, **kwargs):
        return self.stagnation_strategy(*args, **kwargs)

    def static(self, *args, **kwargs):
        return self.solve_static_stagnation(*args, **kwargs)
    
    def dynamic(self, *args, **kwargs):
        return self.solve_dynamic_stagnation(*args, **kwargs)