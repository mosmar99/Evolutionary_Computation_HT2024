import numpy as np
from fitness import Fitness_Function, Conflict_Based

class Terminal:
    def exec(self, individual):
        n = len(individual)
        columns = "abcdefgh"
        print("\n")
        print("   " + "  ".join(columns[:n]))
        for row in range(n):
            line = f"{row + 1}  "
            for col in range(n):
                line += "Q  " if individual[col] == row + 1 else ".  "
            line += f"{row + 1}"
            print(line)
        print("   " + "  ".join(columns[:n]))
        print("\nFitness Evaluation: %8f" % (round(Fitness_Function(Conflict_Based()).evaluate(individual)[0], 2)))
        print("Solution: ", individual)
        print("\n")

class Visualization(object):
    def __init__(self, visualization_strategy):
        self.visualization_strategy = visualization_strategy

    def view(self, individual):
        return self.visualization_strategy.exec(individual)