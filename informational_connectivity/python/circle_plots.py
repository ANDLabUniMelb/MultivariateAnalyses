import os
from pycirclize import Circos
import pandas as pd
import numpy as np
from scipy.io import loadmat
import matplotlib.pyplot as plt
from matplotlib.colors import to_hex

# Function to load .mat file and extract binary matrix and ROI names
def load_data_from_mat(file_path):
    data = loadmat(file_path)
    binary_matrix = data['binary_connection_matrix']
    binary_matrix_simple = data['binary_connection_matrix_simple']  # Adjust the key name if necessary
    binary_matrix_animal = data['binary_connection_matrix_animal']
    binary_matrix_danger = data['binary_connection_matrix_danger']

    roi_names = [str(name[0]) for name in data['roi_names'][0]]
    return binary_matrix, binary_matrix_simple, binary_matrix_animal, binary_matrix_danger, roi_names

# Function to set the lower triangular part of a matrix to NaN
def set_lower_triangular_to_zero(matrix):
    matrix = matrix.copy()
    rows, cols = np.tril_indices_from(matrix, -1)
    matrix[rows, cols] = 0
    return matrix

# Path to the .mat file

results_dir = '/Users/joecussen/Documents/Jobs/unimelb/adaptive_safety_coding/data/IC/spartan/results_first_zstat_270524_weapons'
# file_path = '/Users/joecussen/Documents/Jobs/unimelb/adaptive_safety_coding/informational_conn/data/IC_results.mat'

# Load the data
# binary_matrix, binary_matrix_simple, binary_matrix_animal, binary_matrix_danger, roi_names = load_data_from_mat(file_path)
binary_matrix = loadmat(os.path.join(results_dir, 'binary_matrix_all.mat'))['binary_connection_matrix']
binary_matrix_simple = loadmat(os.path.join(results_dir, 'binary_matrix_simple.mat'))['binary_connection_matrix']
# binary_matrix_animal = loadmat(os.path.join(results_dir, 'binary_matrix_animal.mat'))['binary_connection_matrix']
# binary_matrix_danger = loadmat(os.path.join(results_dir, 'binary_matrix_danger.mat'))['binary_connection_matrix']
roi_set_1 = ['ACC_caudodorsal', 'ACC_pregenual', 'AMY', 'anterior_insula', 'antvmpfc_10mm', 'HC', 'PAG', 'postvmpfc_10mm', 'striatum_1', 'striatum_3', 'T',]
roi_set_2 = ['ACC_caudodorsal', 'ACC_pregenual', 'AMY', 'anterior_insula', 'HO_antvmpfc', 'HC', 'PAG', 'HO_postvmpfc', 'striatum_1', 'striatum_3', 'T', ]

roi_names= roi_set_1
cmap = plt.get_cmap("tab10")
colour_mapping = {roi: to_hex(cmap(i % 10)) for i, roi in enumerate(roi_names)}

def plot_ic_circle(matrix, name, condition= ''):
    # Set the lower triangular part of the matrix to zero
    binary_matrix = set_lower_triangular_to_zero(matrix)
    matrix_df = pd.DataFrame(binary_matrix, index=roi_names, columns=roi_names)
    matrix_df = matrix_df.loc[~(matrix_df == 0).all(axis=1), ~(matrix_df == 0).all(axis=0)]
    circos = Circos.initialize_from_matrix(
        matrix_df,
        space=5,
        cmap=colour_mapping,
        label_kws=dict(size=12),
        link_kws=dict(ec="black", lw=0.5, direction=0),
    )
    circos.savefig(f"{results_dir}/IC_plot_{name}{condition}.png")

for mat, name in [(binary_matrix, 'all'), (binary_matrix_simple, 'simplified')]:#, (binary_matrix_animal, 'animal'), (binary_matrix_danger, 'danger')]:
    plot_ic_circle(mat, name, condition= '_weapons_only')
