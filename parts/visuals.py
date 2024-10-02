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
        axs[0].plot(iters, df.y1, label='Static', color='blue')
        axs[0].set_title(f"Without: n={n}")
        axs[0].axhline(y=np.mean(df.y1), color='darkblue', linestyle='--', label=f'Avg. {np.mean(df.y1)}', zorder=1)
        axs[0].set_xlabel('Iteration')
        axs[0].set_ylabel('Final Generation Count')
        axs[0].legend()

        # create column 2 & add the values
        axs[1].plot(iters, df.y2, label='Dynamic', color='green', zorder=0)
        axs[1].set_title(f"With: n={n}")
        axs[1].axhline(y=np.mean(df.y2), color='darkgreen', linestyle='--', label=f'Avg. {np.mean(df.y2)}', zorder=1)
        axs[1].set_xlabel('Iteration')
        axs[1].set_ylabel('Final Generation Count')
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
    folder = config.test_results
    n = config.constants['GENOME_SIZE']
    iters = config.iters
    setup_count = config.setup_count
    Visualization('px_density_hp').create_numeric_heatmap(folder, iters, n, setup_count)