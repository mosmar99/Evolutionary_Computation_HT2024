import time

from nqAlgorithm import solve_n_queens_wirth

n = 20 #nxn squares


def main():
    start_time = time.time()
    solve_n_queens_wirth(n)
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
    main()