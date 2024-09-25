import src.genetic_algorithm as ga
import src.config as config
import src.utils.visuals as visuals
import src.parameter_tuning as Parameter_Tuning
import time
import concurrent.futures, multiprocessing
from threading import Lock

def main(**kwargs):
    tuner = Parameter_Tuning.Parameter_Tuning
    use_threading   = kwargs.get('use_threading', config.default_setup['use_threading'])    
    pt              = tuner(kwargs.get('tuning_strategy', config.default_setup['tuning_strategy']))
    iters           = kwargs.get('iters', config.default_setup['iters'])
    setup_count     = kwargs.get('setup_count', config.default_setup['setup_count'])
    log_to_file     = kwargs.get('log_to_file', config.default_setup['log_to_file'])
    log_file        = kwargs.get('log_file', config.default_setup['log_file'])
    visual          = kwargs.get('visualization_strategy', config.default_setup['visualization_strategy'])
    output_log_path = kwargs.get('output_log_path', config.default_setup['output_log_path'])
    log_file_X      = str(kwargs.get('log_file_X', config.default_setup['log_file_X']))
    log_file_Y      = str(kwargs.get('log_file_Y', config.default_setup['log_file_Y']))
    topX            = kwargs.get('topX', config.default_setup['topX'])

    solver = ga.Genetic_Algorithm(**kwargs)

    if(not use_threading):
        solver.solve()
    else:
        setups = []
        if pt is not None:
            setups = pt.tuning_strategy(setup_count)
            with open(config.curr_setups_loc, 'w') as curr_setups:
                curr_setups.write(f"{setups}")
            print(" --- CREATED SETUPS --- \n")

        file_lock = Lock()
        counter = 0
        with concurrent.futures.ProcessPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
            with open(output_log_path, 'w') as log_evals:
                log_evals.write(f"{log_file_X},{log_file_Y}\n")
                start_time = time.time()
                futures = []
                
                for setup_idx, setup in enumerate(setups):
                    future = executor.submit(solver.worker, setup_idx, setup, attribute=log_file_X.upper(), iters = iters)
                    futures.append(future)
                
                for future in concurrent.futures.as_completed(futures):
                    setup_idx, setup_eval_count, recieved_attribute = future.result()
                    
                    with file_lock:
                        if recieved_attribute is None:
                            recieved_attribute = f"s_{setup_idx + 1}"
                        log_evals.write(f"{recieved_attribute},{setup_eval_count}\n")
                        counter = counter + 1
                        print(f"Loading {(counter * 100 / setup_count)}%  --({(time.time() - start_time):.2f}sec)")

    if visual is not None and output_log_path is not None:
        view_obj = visuals.Visualization(visual)
        if log_file_Y is not None:
            view_obj(output_log_path, log_file_X, log_file_Y)
        elif log_file_X is not None:
            view_obj(output_log_path, log_file_X)
        else:
            view_obj(output_log_path)
        print("--- VISUALIZATION CREATED ---")



if __name__ == "__main__":
    main(**config.example_old_main5)