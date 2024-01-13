import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap

output_path = "./Output/"
def plotUtilityMatrix(utility_matrix, drivers, title):
    cmap = ListedColormap(['lightblue', 'green'])

    fig, ax = plt.subplots(figsize=(20, 15))
    ax.set_aspect('equal')

    for i, row in enumerate(utility_matrix):
        driver_name = drivers[i]
        for j, value in enumerate(row):
            if value is not None:
                ax.add_patch(plt.Rectangle((j, -i - 1), 1, 1, color=cmap(value > 0), alpha=0.7))
                ax.text(j + 0.5, -i - 0.5, f'{value:.2f}', color='black', ha='center', va='center', fontsize=8)
            else:
                ax.add_patch(plt.Rectangle((j, -i - 1), 1, 1, color='lightblue', alpha=0.7))

        ax.text(-0.5, -i - 0.5, f'{driver_name}', color='black', ha='right', va='center', fontsize=10,
                fontweight='bold')

    ax.set_title(title, fontsize=20)

    ax.set_xlim(0, len(utility_matrix[0])+1)

    ax.set_xticks(np.arange(len(utility_matrix[0])) + 0.5)
    ax.set_yticks(-np.arange(len(utility_matrix)+1) - 0.5)
    ax.set_xticklabels([f's{i}' for i in range(len(utility_matrix[0]))])
    ax.set_yticklabels([])

    plt.savefig(f"{output_path}{title}.png")

def plotUtilityMatrix2(utility_matrix, drivers, title):
    """
    :param utility_matrix: utility matrix with content based approach
    :type utility_matrix: dict
    :param drivers: list of drivers
    :param title: title of the plot
    :return: None
    """
    cmap = ListedColormap(['lightblue', 'green'])

    fig, ax = plt.subplots(figsize=(20, 15))
    ax.set_aspect('equal')

    for i, row in enumerate(utility_matrix):
        driver_name = drivers[i]
        for j, value in enumerate(row):
            if value is not None:
                ax.add_patch(plt.Rectangle((j, -i - 1), 1, 1, color=cmap(value > 0), alpha=0.7))
                ax.text(j + 0.5, -i - 0.5, f'{value:.2f}', color='black', ha='center', va='center', fontsize=8)
            else:
                ax.add_patch(plt.Rectangle((j, -i - 1), 1, 1, color='lightblue', alpha=0.7))

        ax.text(-0.5, -i - 0.5, f'{driver_name}', color='black', ha='right', va='center', fontsize=10,
                fontweight='bold')

    ax.set_title(title, fontsize=20)

    ax.set_xlim(0, len(utility_matrix[0])+1)

    ax.set_xticks(np.arange(len(utility_matrix[0])) + 0.5)
    ax.set_yticks(-np.arange(len(utility_matrix)+1) - 0.5)
    ax.set_xticklabels([f's{i}' for i in range(len(utility_matrix[0]))])
    ax.set_yticklabels([])

    plt.savefig(f"{output_path}{title}.png")