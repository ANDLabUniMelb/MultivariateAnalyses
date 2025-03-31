import os
import numpy as np
import matplotlib.pyplot as plt
import mat73
from scipy.sparse import issparse
from collections import defaultdict

specs = ["four"]
results_dir = f"/Users/joecussen/Documents/Jobs/unimelb/projects/dcm/results/"
save_dir = os.path.join(results_dir, "plots")
os.makedirs(save_dir, exist_ok=True)

version = '0120'
dcm_names = ['ANIWEAP', 'SAFETY', 'EXTINT']

# Define the ROI mapping based on the index order.
roi_names = {1: 'antvmpfc', 2: 'postvmpfc', 3: 'amy', 4: 'striatum'}

# Define the condition names (in order) for each DCM type.
condition_names = {
    "ANIWEAP": ['task', 'animals', 'weapons'],
    "SAFETY": ['task', 'high_safety', 'low_safety'],
    "EXTINT": ['task', 'high_external_safety', 'low_external_safety', 'high_internal_safety', 'low_internal_safety']
}

dcm_name = dcm_names[0]
spec = specs[0]
dcm_version = f'{dcm_name}_{version}'

# Load the PEB data.
peb_path = os.path.join(results_dir, f'PEB_{dcm_version}_{spec}.mat')
data = mat73.loadmat(peb_path)
bmr = data.get('BMR')

print(bmr)

#%%
posterior_probs = list(bmr['P'])
print(max(posterior_probs))

#%%

# Suppose each row in BMR.P is a model, and each column is a subject/family/etc.
# You might need to pick a column or average across them, depending on your analysis.
# For instance, picking the first column:
import numpy as np

# bmr is presumably a dictionary with keys: 'P', 'F', 'K', 'name', etc.
# Check shapes first:
print("Shapes:")
print("  bmr['P'].shape =", bmr['P'].shape)
print("  bmr['F'].shape =", bmr['F'].shape)
print("  bmr['K'].shape =", bmr['K'].shape)
print("  len(bmr['name']) =", len(bmr['name']))

# 1) Identify the posterior probabilities array
post_probs = bmr['P']

# If post_probs is shape (256,), we just do:
winning_model_idx = np.argmax(post_probs)
winning_model_postprob = post_probs[winning_model_idx]

print(f"Winning model index: {winning_model_idx}")
print(f"Winning model posterior probability: {winning_model_postprob}")

# 2) Identify which parameters are 'on' in that model
# bmr['K'] often has shape (nModels, nParams).
# If it is a sparse matrix, convert it:
K_array = bmr['K']
if hasattr(K_array, "toarray"):  # check if it's sparse
    K_array = K_array.toarray()

included_params = np.where(K_array[winning_model_idx, :] == 1)[0]

# 3) Get parameter names for those included connections
param_names = bmr['name']  # a list of strings, each param name
print("Parameters included in the winning model:")
for ip in included_params:
    print("  ", param_names[ip])