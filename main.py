import time

from nqAlgorithm import solve_n_queens_wirth
from nq_script import solve_n_queens_evolutionary

n = 20 #nxn squares


def main():
    start_time_wirth = time.time()
    solve_n_queens_wirth(n)
    time_passed_wirth = time.time() - start_time_wirth
    print("--- %s seconds ---" % time_passed_wirth)

    start_time_evolutionary = time.time()
    solve_n_queens_evolutionary(n)
    time_passed_evolutionary = time.time() - start_time_evolutionary
    print("--- %s seconds ---" % time_passed_evolutionary)

    diff = time_passed_wirth - time_passed_evolutionary

    if diff > 0:
        print("Evolutionary algorithm is %s faster :)" % (time_passed_wirth - time_passed_evolutionary))
    else:
        print("Evolutionary algorithm is %s slower :(" % (time_passed_evolutionary - time_passed_wirth))

if __name__ == "__main__":
    main()