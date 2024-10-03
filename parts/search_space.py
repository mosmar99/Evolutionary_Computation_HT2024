"""
This file contains the recombination class which is responsible for recombining the selected parents to create offspring.
Authors: Mahmut Osmanovic (mosmar99), Sebastian Tuura (tuura01), Isac Paulsson (isacpaulsson), Emil Wagman (Neobyte01), Mohammad Al Khaled (MohamadAlkhaled)
Last updated: 2024-10-02

Plots how the fundamental solutions as a fraction of the search space decreases when the genome size N increases
"""

import math
import matplotlib.pyplot as plt

n_values = list(range(4, 21))
fundamental_solutions = [1, 2, 1, 6, 12, 46, 92, 341, 1787, 9233, 45752, 285053, 
                         1846955, 11977939, 83263591, 621012754, 4878666808]
search_space = [math.factorial(n) for n in n_values]
ratios = [fundamental_solutions[i] / search_space[i] for i in range(len(n_values))]

plt.figure(figsize=(8, 6))
plt.plot(n_values, ratios, marker='o', linestyle='-', color='b')
plt.yscale('log')

plt.title("Ratio of Fundamental Solutions to Search Space (N-Queens)", fontsize=14)
plt.xlabel("N (Genome Size)", fontsize=12)
plt.ylabel("Solutions / Search Space (log scale)", fontsize=12)

plt.grid(True, which="both", ls="--")
plt.tight_layout()
plt.show()
