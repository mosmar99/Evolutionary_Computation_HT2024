"""
Idea is to benchmark our evolutionary algorithm.
Algorithm is ripped from: https://medium.com/@tech_future/n-queen-genetic-algorithm-approach-ec1a9299eeed
"""

def is_safe(board, row, col, n):
    # Check if there is a queen in the same column
    for i in range(row):
        if board[i] == col or \
           board[i] - i == col - row or \
           board[i] + i == col + row:
            return False
    return True

def solve_n_queens_util(board, row, n, solutions, num_solutions):
    if len(solutions) == num_solutions:
        return

    if row == n:
        solutions.append(board.copy())
    else:
        for col in range(n):
            if is_safe(board, row, col, n):
                board[row] = col
                solve_n_queens_util(board, row + 1, n, solutions, num_solutions)

def get_n_queens_solutions(n, num_solutions):
    board = [-1] * n
    solutions = []
    solve_n_queens_util(board, 0, n, solutions, num_solutions)
    return solutions

def print_solutions(solutions):
    for solution in solutions:
        for row in solution:
            line = ['Q' if i == row else '.' for i in range(len(solution))]
            print(" ".join(line))
        print("\n")

# Example usage for getting 2 solutions for the 8-queens problem
def solve_n_queens_wirth(n, num_solutions=1):
    solutions = get_n_queens_solutions(n, num_solutions)
    print_solutions(solutions)

