# from jaejong paper;
# Then, to find hubs connecting regions within the SBSN, we computed the betweenness centralities of each region of the SBSN which represent the fraction of all shortest paths that contain a specific node. The top three hubs based on BC were ACC, PAG, and amygdala, and the BC of VMPFC was 0 which means this region does not contain any shortest path that connects other regions.  Interestingly, the hypothalamus was connected with the top three hubs (Fig 4C&D), which is consistent with previous animal studies showing hypothalamic interaction with the PAG and amygdala. These results also suggest a possibility that the hypothalamus might have communication with regions of the SBSN through these hubs.


import numpy as np
import os
import networkx as nx
from scipy.io import loadmat

# Function to load .mat file and extract binary matrix and ROI names
def load_data_from_mat(file_path):
    data = loadmat(file_path)
    binary_matrix = data['binary_connection_matrix']
    binary_matrix_simple = data['binary_connection_matrix_simple']  # Adjust the key name if necessary
    binary_matrix_animal = data['binary_connection_matrix_animal']
    binary_matrix_danger = data['binary_connection_matrix_danger']

    roi_names = [str(name[0]) for name in data['roi_names'][0]]
    return binary_matrix, binary_matrix_simple, binary_matrix_animal, binary_matrix_danger, roi_names

# Path to the .mat file
# file_path = '/Users/joecussen/Documents/Jobs/unimelb/adaptive_safety_coding/informational_conn/data/IC_results.mat'
#
# # Load the data
# binary_matrix, binary_matrix_simple, binary_matrix_animal, binary_matrix_danger, roi_names = load_data_from_mat(file_path)
results_dir = '/Users/joecussen/Documents/Jobs/unimelb/adaptive_safety_coding/data/IC/spartan/results_first_zstat_240524_new_ROIs'
# file_path = '/Users/joecussen/Documents/Jobs/unimelb/adaptive_safety_coding/informational_conn/data/IC_results.mat'

# Load the data
# binary_matrix, binary_matrix_simple, binary_matrix_animal, binary_matrix_danger, roi_names = load_data_from_mat(file_path)
binary_matrix = loadmat(os.path.join(results_dir, 'binary_matrix_all.mat'))['binary_connection_matrix']
binary_matrix_simple = loadmat(os.path.join(results_dir, 'binary_matrix_simple.mat'))['binary_connection_matrix']
binary_matrix_animal = loadmat(os.path.join(results_dir, 'binary_matrix_animal.mat'))['binary_connection_matrix']
binary_matrix_danger = loadmat(os.path.join(results_dir, 'binary_matrix_danger.mat'))['binary_connection_matrix']
roi_names = ['ACC', 'AMY', 'DLPFC_L', 'DLPFC_R', 'HC', 'PAG', 'T', 'antvmpfc', 'postvmpfc', 'HO_insula', 'striatum_1', 'striatum_2', 'striatum_3']

# Function to convert binary matrix to NetworkX graph
def binary_matrix_to_graph(binary_matrix, roi_names):
    G = nx.Graph()
    for i, roi in enumerate(roi_names):
        G.add_node(i, label=roi)
    for i in range(len(binary_matrix)):
        for j in range(len(binary_matrix)):
            if binary_matrix[i][j] == 1:
                G.add_edge(i, j)
    return G

# Convert the binary matrix to a graph
G = binary_matrix_to_graph(binary_matrix, roi_names)

# Calculate betweenness centrality
betweenness_centrality = nx.betweenness_centrality(G)

# Map the betweenness centrality back to the ROI names
betweenness_centrality_with_names = {roi_names[node]: centrality for node, centrality in betweenness_centrality.items()}

# Print betweenness centrality for each node
for roi, centrality in betweenness_centrality_with_names.items():
    print(f'{roi}: {centrality}')