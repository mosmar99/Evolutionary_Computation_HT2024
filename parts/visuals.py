"""
This file contains the Visualization class which is responsible for creating visualizations of the data.
Authors: Mahmut Osmanovic (mosmar99), Sebastian Tuura (tuura01), Isac Paulsson (isacpaulsson), Emil Wagman (Neobyte01), Mohammad Al Khaled (MohamadAlkhaled)
Last updated: 2024-10-02
"""

import config
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Class for creating visualizations
class Visualization:
    # init function for Visualization class
    # input: visualization_strategy: string
    # output: None
    def __init__(self, visualization_strategy):
        visualization_strategies = { 
            'terminal': self.terminal,
            'html_sim_eval': self.html_sim_eval,
            'strategy_plot': self.strategy_plot,
            'graph_space_vs_solutions': self.graph_space_vs_solutions,
            'heatmap': self.heatmap,
            'scatter': self.scatter,
            'bar': self.create_bar_plot,  
            'box': self.create_box_plot,  
            'px_heatmap': self.create_heatmap,  
            'px_scatter': self.create_scatter_plot,
            'px_numeric_heatmap': self.create_numeric_heatmap,
            'px_density': self.create_density_plot,
            'px_density_hp': self.create_density_heatmap
        }
        self.visualization_strategy = visualization_strategies[visualization_strategy]

    # call function for Visualization class
    def __call__(self, *args, **kwargs):
        self.visualization_strategy(*args, **kwargs)
    
    # terminal visualization
    # input: individual: numpy array, fitness_function: Fitness_Function
    # output: None
    def terminal(self, individual, fitness_function):
        # Prints the board to the terminal

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
        print("\nFitness Evaluation: %8f" % (round(fitness_function(individual)[0], 2)))
        print("Solution: ", individual)
        print("\n")
    
    # html_sim_eval visualization
    # input: file_loc: string
    # output: None
    def html_sim_eval(self, file_loc):
        # creates two scatter plots in one figure
        fig = make_subplots(rows=1, cols=2)
        df = pd.read_csv(file_loc)

        # Scatter plot of average similarity score and fitness score
        fig.add_trace(
            go.Scatter(x=df['evaluation_count'], y=df['avg_similarity_score'], name='Average Similarity Score'),
            row=1, col=1
        )

        # Scatter plot of evaluation count and fitness score
        fig.add_trace(
            go.Scatter(x=df['evaluation_count'], y=df['fitness_score'], name='Fitness Score'),
            row=1, col=2
        )

        # Update xaxis properties
        fig.update_xaxes(title_text='Evaluation Count', row=1, col=1)
        fig.update_yaxes(title_text='Average Similarity Score', row=1, col=1)
        fig.update_xaxes(title_text='Evaluation Count', row=1, col=2)
        fig.update_yaxes(title_text='Fitness Score', row=1, col=2)

        # Update title and size & show the figure
        fig.update_layout(height=600, width=1200, title_text="Group 9: Scatter Plots of Genetic Algorithm Metrics")
        fig.show()

    # strategy_plot visualization
    # input: file_loc: string, runs: int
    # output: None
    def strategy_plot(self, file_loc, runs):
        strategies = []
        eval_counts = []
        
        # Read the data from the file
        with open(file_loc, 'r') as file:
            for line in file:
                strategy, count = line.strip().split(',')
                strategies.append(strategy)
                eval_counts.append(float(count))

        # Sort the data, with regards to the evaluation count
        sorted_data = sorted(zip(strategies, eval_counts), key=lambda x: x[1])
        sorted_strategies, sorted_eval_counts = zip(*sorted_data)

        # Create the bar plot
        fig = go.Figure()

        # Add the data to the plot
        fig.add_trace(go.Bar(
            x=sorted_strategies,
            y=sorted_eval_counts,
            marker=dict(
                color=sorted_eval_counts,  
                colorscale='rdbu', 
                showscale=False 
            )
        ))

        # Update the layout of the plot
        fig.update_layout(
            title=f'Evaluation Count by Strategy ({runs} Runs/Strategy)',
            xaxis_title='Strategy',
            yaxis_title='Evaluation Count',
            xaxis_tickangle=-45,
            template='plotly_white'
        )
        # Show the plot
        fig.show()


    # Exponent plot visualization
    # input: file_loc: string, runs: int 
    # output: None
    def exponent_plot(self, file_loc, runs):
        exponents = []
        eval_counts = []

        # open fild in read mode
        with open(file_loc, 'r') as file:
            for line in file:
                # append the values
                exponent, count = line.strip().split(',')
                exponents.append(exponent)
                eval_counts.append(float(count))

        # create and display plot
        fig, axs = plt.subplots(1, 1, figsize=(10, 4)) 
        axs.plot(exponents, eval_counts, label='Exponents', color='blue')
        axs.set_title(f"Evaluation count by survival exponent ({runs} runs/exponent)")
        axs.set_xlabel(f'Exponent')
        axs.set_ylabel('Average evalualtions')
        axs.legend()
        
        plt.grid()
        plt.tight_layout()
        plt.show()

    # Convergence plot visualization for population fitness over generations
    # input: file_loc: string, runs: int
    # output: None
    def exponent_convergance_plot(self, file_loc, runs):
        evals = []
        max_evals = []
        avg_evals = []
        min_evals = []

        # open file in read mode
        with open(file_loc, 'r') as file:
            for line in file:
                # append values from file
                max_eval, avg_eval, min_eval = line.strip().split(',,')
                max_evals.append([float(val) for val in max_eval.strip('[]').split(',')])
                avg_evals.append([float(val) for val in avg_eval.strip('[]').split(',')])
                min_evals.append([float(val) for val in min_eval.strip('[]').split(',')])   

        # create and show plot
        fig, axs = plt.subplots(1, 1, figsize=(10, 4)) 

        axs.plot(np.arange(1, len(max_evals[2])+1), max_evals[2], label='50 max', color='red')
        axs.plot(np.arange(1, len(avg_evals[2])+1), avg_evals[2], label='50 average', color='red', ls='--')
        axs.plot(np.arange(1, len(min_evals[2])+1), min_evals[2], label='50 min', color='red', ls=':')

        axs.plot(np.arange(1, len(max_evals[1])+1), max_evals[1], label='15 max', color='green')
        axs.plot(np.arange(1, len(avg_evals[1])+1), avg_evals[1], label='15 average', color='green', ls='--')
        axs.plot(np.arange(1, len(min_evals[1])+1), min_evals[1], label='15 min', color='green', ls=':')

        axs.plot(np.arange(1, len(max_evals[0])+1), max_evals[0], label='0 max', color='blue')
        axs.plot(np.arange(1, len(avg_evals[0])+1), avg_evals[0], label='0 average', color='blue', ls='--')
        axs.plot(np.arange(1, len(min_evals[0])+1), min_evals[0], label='0 min', color='blue', ls=':')

        axs.set_title(f"Population convergence by exponent ({runs} runs/exponent)")
        axs.set_xlabel(f'Generations')
        axs.set_ylabel('Fitness')
        axs.legend()
        
        plt.grid()
        plt.tight_layout()
        plt.show()

    # graph_space_vs_solutions visualization
    # input: data_fil_loc: string
    # output: None
    def graph_space_vs_solutions(self, data_fil_loc):
        # Read the data from the file
        data = pd.read_csv(data_fil_loc)
    
        # get the values from the data
        n_values = data['n']
        fractions = data['Fractions']

        # Create the plot
        plt.figure(figsize=(10, 6))
        plt.plot(n_values, fractions, marker='o', linestyle='-', color='b')

        plt.yscale('log')
        plt.gca().yaxis.set_major_formatter(plt.FormatStrFormatter('%.2e'))

        plt.title('N-Queens Problem: Fraction of Solutions vs N')
        plt.xlabel('N (Genome Size)')
        plt.ylabel('# Solution/Space')

        plt.grid(True)
        plt.tight_layout()
        plt.show()

    # heatmap visualization
    # input: datafile_loc: string
    # output: None
    def heatmap(self, datafile_loc):

        # Read the data from the file
        df = pd.read_csv(datafile_loc, header=0)

        # Create the heatmap
        fig, axes = plt.subplots(1, 2, figsize=(12, 6))
        sns.heatmap(df.corr(), annot=True, fmt=".2f", ax=axes[0])
        axes[0].set_title("Correlation Heatmap of Population Size and Evaluation Count")
        sns.scatterplot(x="population_size", y="setup_eval_count", data=df, ax=axes[1])
        axes[1].set_title("Population Size vs Evaluation Count")
        plt.tight_layout()
        plt.show()

    # scatter visualization
    # input: datafile_loc: string, x_axis: string, y_axis: string
    # output: None
    # https://en.wikipedia.org/wiki/Scatter_plot
    def scatter(self, datafile_loc, x_axis, y_axis):
        # read the data from the file & sort values
        df = pd.read_csv(datafile_loc, header=0)
        df_sorted = df.sort_values(by=y_axis)
        threshold = df_sorted[y_axis].quantile(0.05)
        df_blue = df_sorted[df_sorted[y_axis] > threshold]
        df_pink = df_sorted[df_sorted[y_axis] <= threshold]
        
        # Create the scatter plot, with the data & add coloring for the top 5% and bottom 95%
        plt.scatter(df_blue[x_axis], df_blue[y_axis], color='lightblue', label='bottom 0.95 eval_score')
        plt.scatter(df_pink[x_axis], df_pink[y_axis], color='pink', label='top 0.05 eval_score')
        
        plt.xlabel(x_axis)
        plt.ylabel(y_axis)
        plt.title(f"{y_axis} vs. {x_axis}")
        plt.legend()
        plt.tight_layout()
        plt.show()
    
    # 2 column lineplot visualization
    # input: datafile_loc: string, n: int
    # output: None
    def lineplot_2col(self, datafile_loc, n):
        # read the data from the file
        df = pd.read_csv(datafile_loc, header=None, names=['y1', 'y2'])
        iters = np.arange(1, len(df.y1)+1)
        fig, axs = plt.subplots(1, 2, figsize=(10, 4))

        # create column 1 & add the values
        axs[0].plot(iters, df.y1, color='blue')
        # axs[0].set_title(f"Trigger Gen: Stagnation of Max. Fit Individual | n={n}")
        # axs[0].set_title(f"Without Genocide | n={n}")
        # axs[0].set_title(f"Static Recombination & Mutation Rate | n={n}")
        axs[0].set_title(f"Static Genocide Rates | n={n}")
        axs[0].axhline(y=np.mean(df.y1), color='darkblue', linestyle='--', label=f'Avg. {round(np.mean(df.y1), 2)}', zorder=1)
        axs[0].set_xlabel('Setup')
        axs[0].set_ylabel('Generation Count')
        axs[0].legend()
        
        # create column 2 & add the values
        axs[1].plot(iters, df.y2, color='green', zorder=0)
        # axs[1].set_title(f"Trigger Gen: Stagnation of Population Mean | n={n}")
        # axs[1].set_title(f"With Genocide | n={n}")
        # axs[1].set_title(f"Dynamic Recombination & Mutation Rate | n={n}")
        axs[1].set_title(f"Dynamic Genocide Rates | n={n}")
        axs[1].axhline(y=np.mean(df.y2), color='darkgreen', linestyle='--', label=f'Avg. {round(np.mean(df.y2),2)}', zorder=1)
        axs[1].set_xlabel('Setup')
        axs[1].set_ylabel('Generation Count')
        axs[1].legend()

        # Display the plots
        plt.tight_layout()
        plt.show()

    # 1 column lineplot visualization
    # input: datafile_loc: string, n: int, runs: int
    # output: None
    def lineplot_1col(self, datafile_loc, n, runs):
        # read the data from the file
        df = pd.read_csv(datafile_loc, header=None, names=['y'])
        iters = np.arange(1, len(df.y)+1)
        fig, axs = plt.subplots(1, 1, figsize=(10, 4))

        # create the line plot
        axs.plot(iters, df.y, label='Final Configuration', color='blue')
        axs.set_title(f"Final Generation Count per Generated Population (n={n} | runs_per_population={runs})")
        axs.axhline(y=np.mean(df.y), color='darkblue', linestyle='--', label=f'Avg. {round(np.mean(df.y), 2)}', zorder=1)
        axs.set_xlabel(f'Population')
        axs.set_ylabel('Generation Count')
        axs.legend()
        
        # show the plot
        plt.tight_layout()
        plt.show()

    # bar plot visualization
    # input: file_loc: string, runs: int, n: int, setup_count: int
    # output: None
    def create_bar_plot(self, file_loc, runs, n, setup_count):
        # read the data from the file & create the bar plot
        df = pd.read_csv(file_loc)
        fig = px.bar(df, x='mutation_strategy', y='evaluation_count', color='evaluation_count', title=f'Bar Plot of Evaluation Count by Mutation Strategy (n={n} | setup_count = {setup_count} | {runs} Runs)')
        fig.show()

    # create_box_plot visualization
    # input: file_loc: string, runs: int, n: int, setup_count: int
    # output: None
    def create_box_plot(self, file_loc, runs, n, setup_count):
        # read the data from the file & create the box plot
        df = pd.read_csv(file_loc)
        fig = px.box(df, x='mutation_strategy', y='evaluation_count', points='all', title=f'Box Plot of Evaluation Count by Mutation Strategy (n={n} | setup_count = {setup_count} | {runs} Runs)')
        fig.show()

    # create_heatmap visualization
    # input: file_loc: string, runs: int, n: int, setup_count: int
    # output: None
    def create_heatmap(self, file_loc, runs, n, setup_count):
        # read the data from the file & create the heatmap
        df = pd.read_csv(file_loc)
        heatmap_data = df.pivot_table(values='evaluation_count', index='mutation_strategy', columns='recombination_strategy', aggfunc='mean')
        fig = go.Figure(data=go.Heatmap(z=heatmap_data.values, x=heatmap_data.columns, y=heatmap_data.index))
        fig.update_layout(title=f'Heatmap of Evaluation Count by Strategies (n={n} | setup_count = {setup_count} | {runs} Runs)', xaxis_title='Recombination Strategy', yaxis_title='Mutation Strategy')
        fig.show()

    # create_scatter_plot visualization
    # input: file_loc: string, runs: int, n: int, setup_count: int
    # output: None
    def create_scatter_plot(self, file_loc, runs, n, setup_count):
        # read the data from the file & create the scatter plot
        df = pd.read_csv(file_loc)
        fig = px.scatter(df, x='RECOMBINATION_RATE', y='evaluation_count', color='evaluation_count', size='MUTATION_RATE', title=f'Scatter Plot: TOURNAMENT_GROUP_SIZE vs Evaluation Count (n={n} | setup_count = {setup_count} | {runs} Runs)')
        fig.update_traces(marker=dict(size=10))
        fig.show()

    # create_numeric_heatmap visualization
    # input: file_loc: string, runs: int, n: int, setup_count: int
    # output: None
    def create_numeric_heatmap(self, file_loc, runs, n, setup_count):
        # read the data from the file
        df = pd.read_csv(file_loc)
        numerical_columns = ['POPULATION_SIZE', 'NUM_OFFSPRING_RATE', 'RECOMBINATION_RATE', 'MUTATION_RATE', 'TOURNAMENT_GROUP_SIZE']

        # create the heatmap
        y = 'MUTATION_RATE'
        x = 'RECOMBINATION_RATE'
        heatmap_data = df.pivot_table(
            values='evaluation_count', 
            index=y,  
            columns=x,
            aggfunc='mean' 
        )
        
        fig = go.Figure(data=go.Heatmap(
            z=heatmap_data.values,  
            x=heatmap_data.columns,  
            y=heatmap_data.index,    
            colorscale='Viridis'  
        ))
        
        fig.update_layout(
            title=f'Heatmap of Evaluation Count by Mutation & Recombination Rates (n={n} | setup_count = {setup_count} | {runs} Runs)',
            xaxis_title=x,
            yaxis_title=y
        )
        
        fig.show()
    
    # create_density_plot visualization
    # input: file_loc: string, runs: int, n: int, setup_count: int
    # output: None
    def create_density_plot(self, file_loc, runs, n, setup_count):
        # read the data from the file & create the density plot
        df = pd.read_csv(file_loc)
        fig = px.density_contour(df, 
                                x='RECOMBINATION_RATE', 
                                y='MUTATION_RATE', 
                                z='evaluation_count',
                                title=f'Density Plot of Evaluation Count by Mutation & Recombination Rates (n={n} | setup_count = {setup_count} | {runs} Runs)')
        fig.show()

    # create_density_heatmap visualization
    # input: file_loc: string, runs: int, n: int, setup_count: int
    # output: None
    def create_density_heatmap(self, file_loc, runs, n, setup_count):
        # read the data from the file & create the density heatmap
        df = pd.read_csv(file_loc)
        fig = px.density_heatmap(df, 
                                x='RECOMBINATION_RATE', 
                                y='MUTATION_RATE', 
                                z='evaluation_count', 
                                title=f'Density Heatmap of Evaluation Count (n={n} | setup_count = {setup_count} | {runs} Runs)')
        fig.show()

# "main function" used for testing purposes & should NOT be ran as is.
# input: None
# output: None
if __name__ == '__main__':
    vis = Visualization('strategy_plot')
    
    # visualization of the best setup
    vis.lineplot_1col(datafile_loc="sample logs/final_out.log", n=8, runs=10)

    # setup comparison visualization (bar chart)
    vis.strategy_plot(file_loc="sample logs/LHS_Setups_evals.log", runs=50)

    # setup comparison visualization (heatmap)
    Visualization('px_density_hp').create_density_heatmap("sample logs/test_results.log", 10, 8, 100)

    # stagnation mean vs max
    vis.lineplot_2col(datafile_loc="sample logs/max_vs_mean_geno.log", n=8)

    # static vs dynamic stagnation
    vis.lineplot_2col("sample logs/dyn_vs_static_stagn.log", 8)

    # with and without genocide
    vis.lineplot_2col("sample logs/geno_plot8.log", 8)

    # with static genocide comparing static vs dynamic mutation and recombination rates
    vis.lineplot_2col("sample logs/dynamic_vs_static.log", 8)