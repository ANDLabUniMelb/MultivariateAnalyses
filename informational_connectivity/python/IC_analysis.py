import os
from pycirclize import Circos
import pandas as pd
import numpy as np
import networkx as nx
from scipy.io import loadmat
import matplotlib.pyplot as plt
from matplotlib.colors import to_hex

def set_lower_triangular_to_zero(matrix):
    matrix = matrix.copy()
    rows, cols = np.tril_indices_from(matrix, -1)
    matrix[rows, cols] = 0
    return matrix

def plot_ic_circle(matrix, results_suffix, roi_names, figures_dir, name= ''):
    roi_set_2_ordered = ['ACC caudodorsal', 'Amygdala', 'Insula', 'Dorsal striatum', 'Posterior VMPFC',
                         'Anterior VMPFC', 'Hippocampus', 'Ventral striatum', 'PAG', 'Thalamus']
    colour_dict = {
        '1': '#1f77b4',  # Blue
        '2': '#ff7f0e',  # Orange
        '3': '#2ca02c',  # Green
    }
    roi_colour_dict = {
        'ACC caudodorsal': '1',
        'Amygdala': '1',
        'Insula': '1',
        'Dorsal striatum': '1',
        'Posterior VMPFC': '1',
        'Anterior VMPFC': '2',
        'Hippocampus': '2',
        'Ventral striatum': '2',
        'PAG': '3',
        'Thalamus': '3',
    }

    # Map ROI names to colours
    colour_mapping = {roi: colour_dict[roi_colour_dict[roi]] for roi in roi_set_2_ordered}

    binary_matrix = set_lower_triangular_to_zero(matrix)
    matrix_df = pd.DataFrame(binary_matrix, index=roi_names, columns=roi_names)
    matrix_df = matrix_df[roi_set_2_ordered].copy()
    matrix_df = matrix_df.reindex(roi_set_2_ordered)
    matrix_df = matrix_df.loc[~(matrix_df == 0).all(axis=1), ~(matrix_df == 0).all(axis=0)]
    circos = Circos.initialize_from_matrix(
        matrix_df,
        space=5,
        cmap=colour_mapping,
        label_kws=dict(size=12),
        link_kws=dict(ec="black", lw=0.5, direction=0),
    )
    circos.savefig(f"{figures_dir}/{name}.png")

def binary_matrix_to_graph(binary_matrix, roi_names):
    G = nx.Graph()
    for i, roi in enumerate(roi_names):
        G.add_node(i, label=roi)
    for i in range(len(binary_matrix)):
        for j in range(len(binary_matrix)):
            if binary_matrix[i][j] == 1:
                G.add_edge(i, j)
    return G


def run_analysis(results_suffix, results_dir, figures_dir, roi_names, name=''):
    # load data
    binary_matrix = loadmat(os.path.join(results_dir, f'binary_matrix_{results_suffix}.mat'))['binary_connection_matrix']
    # plot IC chord figure
    plot_ic_circle(binary_matrix, results_suffix, roi_names, figures_dir, name)
    # calculate betweenness centrality
    G = binary_matrix_to_graph(binary_matrix, roi_names)
    betweenness_centrality = nx.betweenness_centrality(G)
    betweenness_centrality_names = {roi_names[node]: centrality for node, centrality in
                                         betweenness_centrality.items()}
    print(f'Betweenness centrality for condition: {name}')
    for roi, centrality in betweenness_centrality_names.items():
        print(f'{roi}: {centrality}')


roi_set_2 = ['ACC caudodorsal', 'Amygdala', 'Insula', 'Anterior VMPFC', 'Hippocampus', 'PAG', 'Posterior VMPFC', 'Ventral striatum', 'Dorsal striatum', 'Thalamus']

results_root = '/Users/joecussen/Documents/Jobs/unimelb/adaptive_safety_coding/data/IC/results/results_final'

figures_root = '/Users/joecussen/Documents/Jobs/unimelb/adaptive_safety_coding/repos/and_lab/informational_connectivity/figures_final_2'



run_analysis('danger', os.path.join(results_root,'results_rois2_clean_first_zstat_210624'), figures_root, roi_set_2, name = 'Safe vs. Danger ROI Set 2')
run_analysis('simple', os.path.join(results_root,'results_rois2_animal_first_zstat_210624'), figures_root, roi_set_2, 'Safe vs. Danger (Animals Only) ROI Set 2')
run_analysis('simple', os.path.join(results_root,'results_rois2_weapon_first_zstat_210624'), figures_root, roi_set_2, 'Safe vs. Danger (Weapons Only) ROI Set 2')
run_analysis('direction', os.path.join(results_root,'results_rois2_second_zstat_210624'), figures_root, roi_set_2, 'Second Stim ROI Set 2')
run_analysis('direction', os.path.join(results_root,'results_rois2_animal_second_zstat_210624'), figures_root, roi_set_2, 'Second Stim (Animals Only) ROI Set 2')
run_analysis('direction', os.path.join(results_root,'results_rois2_weapon_second_zstat_210624'), figures_root, roi_set_2, 'Second Stim (Weapons Only) ROI Set 2')
