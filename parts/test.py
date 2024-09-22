import marimo

__generated_with = "0.8.17"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    import numpy as np
    import concurrent.futures
    return concurrent, mo, np


@app.cell
def __():
    futures = [(0,512),(1,411),(2,7222),(3,1241),(4,821),(5,3442)]
    return futures,


@app.cell
def __(np):
    avg_offspring = [0.342, 0.383, 0.497, 0.449, 0.402, 0.211, 0.359,  0.322,  0.374, 0.479]
    print(np.mean(avg_offspring))
    return avg_offspring,


@app.cell
def __(np):
    avg_rec = [0.748, 0.856, 0.806, 0.623, 0.862, 0.817, 0.7, 0.619, 0.755, 0.759]
    print(np.mean(avg_rec))
    return avg_rec,


@app.cell
def __(np):
    avg_mut = [0.319,  0.342, 0.387, 0.106, 0.132, 0.018, 0.441, 0.456, 0.372, 0.485]
    print(np.mean(avg_mut))
    return avg_mut,


@app.cell
def __(np):
    avg_tourn = [0.312, 0.135, 0.693, 0.227, 0.109, 0.221, 0.397, 0.101,  0.746,  0.782]
    print(np.mean(avg_tourn))
    return avg_tourn,


if __name__ == "__main__":
    app.run()
