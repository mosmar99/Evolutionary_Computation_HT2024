import config
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

class Visualization:
    def __init__(self, visualization_strategy):
        visualization_strategies = { 'terminal': self.terminal,
                                     'html_sim_eval': self.html_sim_eval,
                                     'strategy_plot': self.strategy_plot,
                                     'graph_space_vs_solutions': self.graph_space_vs_solutions,
                                     'heatmap': self.heatmap,
                                     'scatter': self.scatter}
        self.visualization_strategy = visualization_strategies[visualization_strategy]

    def __call__(self, *args, **kwargs):
        self.visualization_strategy(*args, **kwargs)
    
    def terminal(self, individual, fitness_function):
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
    
    def html_sim_eval(self, file_loc):
        fig = make_subplots(rows=1, cols=2)
        df = pd.read_csv(file_loc)

        fig.add_trace(
            go.Scatter(x=df['evaluation_count'], y=df['avg_similarity_score'], name='Average Similarity Score'),
            row=1, col=1
        )

        fig.add_trace(
            go.Scatter(x=df['evaluation_count'], y=df['fitness_score'], name='Fitness Score'),
            row=1, col=2
        )

        fig.update_xaxes(title_text='Evaluation Count', row=1, col=1)
        fig.update_yaxes(title_text='Average Similarity Score', row=1, col=1)
        fig.update_xaxes(title_text='Evaluation Count', row=1, col=2)
        fig.update_yaxes(title_text='Fitness Score', row=1, col=2)

        fig.update_layout(height=600, width=1200, title_text="Group 9: Scatter Plots of Genetic Algorithm Metrics")
        fig.show()

    def strategy_plot(self, file_loc, runs):
        strategies = []
        eval_counts = []
        
        with open(file_loc, 'r') as file:
            for line in file:
                strategy, count = line.strip().split(',')
                strategies.append(strategy)
                eval_counts.append(float(count))

        sorted_data = sorted(zip(strategies, eval_counts), key=lambda x: x[1])
        sorted_strategies, sorted_eval_counts = zip(*sorted_data)

        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=sorted_strategies,
            y=sorted_eval_counts,
            marker=dict(
                color=sorted_eval_counts,  
                colorscale='rdbu', 
                showscale=False 
            )
        ))

        fig.update_layout(
            title=f'Evaluation Count by Strategy ({runs} Runs/Strategy)',
            xaxis_title='Strategy',
            yaxis_title='Evaluation Count',
            xaxis_tickangle=-45,
            template='plotly_white'
        )

        fig.show()

    def graph_space_vs_solutions(self, data_fil_loc):
        data = pd.read_csv(data_fil_loc)

        n_values = data['n']
        fractions = data['Fractions']

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

    def heatmap(self, datafile_loc):
        df = pd.read_csv(datafile_loc, header=0)
        fig, axes = plt.subplots(1, 2, figsize=(12, 6))
        sns.heatmap(df.corr(), annot=True, fmt=".2f", ax=axes[0])
        axes[0].set_title("Correlation Heatmap of Population Size and Evaluation Count")
        sns.scatterplot(x="population_size", y="setup_eval_count", data=df, ax=axes[1])
        axes[1].set_title("Population Size vs Evaluation Count")
        plt.tight_layout()
        plt.show()

    def scatter(self, datafile_loc, x_axis, y_axis):
        df = pd.read_csv(datafile_loc, header=0)
        df_sorted = df.sort_values(by=y_axis)
        threshold = df_sorted[y_axis].quantile(0.05)
        df_blue = df_sorted[df_sorted[y_axis] > threshold]
        df_pink = df_sorted[df_sorted[y_axis] <= threshold]
        
        plt.scatter(df_blue[x_axis], df_blue[y_axis], color='lightblue', label='bottom 0.95 eval_score')
        plt.scatter(df_pink[x_axis], df_pink[y_axis], color='pink', label='top 0.05 eval_score')
        
        plt.xlabel(x_axis)
        plt.ylabel(y_axis)
        plt.title(f"{y_axis} vs. {x_axis}")
        plt.legend()
        plt.tight_layout()
        plt.show()
    
    def lineplot_2col(self, datafile_loc):
        df = pd.read_csv(datafile_loc, header=None, names=['y1', 'y2'])
        iters = np.arange(1, len(df.y1)+1)
        fig, axs = plt.subplots(1, 2, figsize=(10, 4))
        axs[0].plot(iters, df.y1, label='Without Genocide', color='blue')
        axs[0].axhline(y=np.mean(df.y2), color='red', linestyle='--', label='Avg No-Genocide Count', zorder=1)
        axs[0].set_xlabel('Iteration')
        axs[0].set_ylabel('Final Generation Count')
        axs[0].legend()

        axs[1].plot(iters, df.y2, label='With Genocide', color='green', zorder=0)
        axs[1].axhline(y=np.mean(df.y2), color='red', linestyle='--', label='Avg Genocide Count', zorder=1)
        axs[1].set_xlabel('Iteration')
        axs[1].set_ylabel('Final Generation Count')
        axs[1].legend()

        # Display the plots
        plt.tight_layout()
        plt.show()

if __name__ == '__main__':
    # GET NQUEENS SPACE/SOL GRAPH
    # view_obj = Visualization('graph_space_vs_solutions')
    # view_obj('logs/nqueens_data.log')
    
    # # Get Heatmap
    # view_obj = Visualization('heatmap')
    # view_obj('logs/heatmap_data.log')
    
    # Get Trendline
    view_obj = Visualization('scatter')
    view_obj(config.log_path6, 'recombination_rate', 'setup_eval_count')
