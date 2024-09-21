import numpy as np
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt

class Visualization:
    def __init__(self, visualization_strategy):
        visualization_strategies = { 'terminal': self.terminal }
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
    
    def HTML_Plots(self, file_loc):
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
        
        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=strategies,
            y=eval_counts,
            marker=dict(
                color=eval_counts,  
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

if __name__ == '__main__':
    view_obj = Visualization('terminal')
    view_obj.graph_space_vs_solutions('logs/nqueens_data.log')

