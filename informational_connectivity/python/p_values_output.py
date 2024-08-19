import os
import pandas as pd
import numpy as np
from scipy.io import loadmat
import os
import numpy as np
from scipy.io import loadmat
from scipy.stats import norm

def stouffer_method(pvalues_all):
    # Get the shape of the p-values array
    num_subjects, numRows, numCols = pvalues_all.shape

    # Initialize matrix to store group-level p-values
    stouffer_pvalues = np.zeros((numRows, numCols))

    # Loop through each element in the matrices
    for row in range(numRows):
        for col in range(numCols):
            # Extract p-values for the current element across all subjects
            pvals = pvalues_all[:, row, col]

            # Stouffer's Z-score method
            z_scores = norm.ppf(1 - pvals)
            mean_z = np.mean(z_scores)
            stouffer_pvalues[row, col] = 1 - norm.cdf(mean_z)

    return stouffer_pvalues

roi_set_2 = ['ACC caudodorsal', 'Amygdala', 'Insula', 'Anterior VMPFC', 'Hippocampus', 'PAG', 'Posterior VMPFC', 'Ventral striatum', 'Dorsal striatum', 'Thalamus']
roi_set_2_ordered = ['ACC caudodorsal', 'Amygdala', 'Insula', 'Dorsal striatum', 'Posterior VMPFC',
                     'Anterior VMPFC', 'Hippocampus', 'Ventral striatum', 'PAG', 'Thalamus']

def set_lower_triangular_to_zero(matrix):
    matrix = matrix.copy()
    rows, cols = np.tril_indices_from(matrix, -1)
    matrix[rows, cols] = 0
    return matrix

p_values_path = '/Users/joecussen/Documents/Jobs/unimelb/adaptive_safety_coding/repos/and_lab/informational_connectivity/p_values'

def read_mat(suffix, results_dir, name):
    matrix = loadmat(os.path.join(results_dir, f'pvalues_{suffix}.mat'))['pvalues_save']
    matrix = stouffer_method(matrix)
    matrix = set_lower_triangular_to_zero(matrix)
    matrix_df = pd.DataFrame(matrix, index=roi_set_2, columns=roi_set_2)
    matrix_df = matrix_df[roi_set_2_ordered].copy()
    matrix_df = matrix_df.reindex(roi_set_2_ordered)
    matrix_df.to_csv(f'{p_values_path}/{name}.csv')


results_root = '/Users/joecussen/Documents/Jobs/unimelb/adaptive_safety_coding/data/IC/results/results_final'


read_mat('danger', os.path.join(results_root,'results_rois2_clean_first_zstat_210624'), 'Safe vs. Danger ROI Set 2')
read_mat('simple', os.path.join(results_root,'results_rois2_animal_first_zstat_210624'),'Safe vs. Danger (Animals Only) ROI Set 2')
read_mat('simple', os.path.join(results_root,'results_rois2_weapon_first_zstat_210624'), 'Safe vs. Danger (Weapons Only) ROI Set 2')
read_mat('direction', os.path.join(results_root,'results_rois2_second_zstat_210624'), 'Second Stim ROI Set 2')
read_mat('direction', os.path.join(results_root,'results_rois2_animal_second_zstat_210624'), 'Second Stim (Animals Only) ROI Set 2')
read_mat('direction', os.path.join(results_root,'results_rois2_weapon_second_zstat_210624'), 'Second Stim (Weapons Only) ROI Set 2')
