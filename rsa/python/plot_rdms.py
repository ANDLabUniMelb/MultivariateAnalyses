import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

working_dir = '//'

#%% read into df
df_pairs_results = pd.read_csv(f'{working_dir}all_pairs_corr_6mm_smooth.csv', index_col=None)

#%% filter out na values
df_pairs = df_pairs_results.dropna()
# df_pairs = df_pairs[(df_pairs['round_1'].isin([1, 3]))&(df_pairs['round_1'].isin([1, 3]))]
condition = 'round' # 'stim' or 'round'

#%%
if condition == 'stim':
    labels = ['cat', 'goose', 'lion', 'grizzly', 'fist', 'stick', 'gun', 'grenade']
    gby_col_1 = 'stim_num_1'
    gby_col_2 = 'stim_num_2'
    df_pairs = df_pairs[(df_pairs['round_1'] != df_pairs['round_2'])] #change this line
elif condition == 'round':
    labels = ['R1', 'R2', 'R3', 'R4']
    gby_col_1 = 'round_1'
    gby_col_2 = 'round_2'
else:
    print('enter condition: stim or round')

df_pairs['min_gby_col'] =  df_pairs[[gby_col_1, gby_col_2]].min(axis=1)
df_pairs['max_gby_col'] = df_pairs[[gby_col_1, gby_col_2]].max(axis=1)
df_pairs['combo'] = df_pairs['min_gby_col'].astype(str) + df_pairs['max_gby_col'].astype(str)

#%% group by pairings to get RDM, and plot
corr_cols = ['corr_win_lose', 'corr_amygdala', 'corr_insula', 'corr_antvmPFC', 'corr_vmpfc']
df_gby = df_pairs.groupby(['combo'])[corr_cols].mean().reset_index()
df_gby['x'] = df_gby['combo'].str[0]
df_gby['y'] = df_gby['combo'].str[1]
for corr in corr_cols:
    matrix = df_gby.pivot(index='x', columns='y', values=corr)
    matrix_np = matrix.to_numpy()
    upper_tri = np.triu(matrix_np)
    matrix_symmetric = upper_tri + upper_tri.T - np.diag(np.diag(upper_tri))
    symmetric_matrix = pd.DataFrame(matrix_symmetric, index=matrix.index, columns=matrix.columns)
    symmetric_matrix.index = labels
    symmetric_matrix.columns = labels
    plt.figure(figsize=(10, 8))
    ax = sns.heatmap(symmetric_matrix, cmap='viridis', annot=True)
    ax.set_title(f'{condition} RDM, ROI: {corr}')
    cbar = ax.collections[0].colorbar
    cbar.set_label('Correlation Coefficient', labelpad=10)  # Increase the padding here
    plt.savefig(f"{working_dir}figures/RDM_{condition}_{corr}.png")  # Save the figure to a file
    plt.show()
    plt.close()



# #%% group by pairings to get RDM, and plot SUBJECT RDMS
# corr_cols = ['corr_win_lose', 'corr_amygdala', 'corr_insula', 'corr_antvmPFC', 'corr_vmpfc']
# for subject in sorted(list(df_pairs['sub'].unique())):
#     df_pairs_sub = df_pairs[df_pairs['sub']== subject]
#     df_gby = df_pairs_sub.groupby(['combo'])[corr_cols].mean().reset_index()
#     df_gby['x'] = df_gby['combo'].str[0]
#     df_gby['y'] = df_gby['combo'].str[1]
#     for corr in corr_cols:
#         matrix = df_gby.pivot(index='x', columns='y', values=corr)
#         matrix_np = matrix.to_numpy()
#         upper_tri = np.triu(matrix_np)
#         matrix_symmetric = upper_tri + upper_tri.T - np.diag(np.diag(upper_tri))
#         symmetric_matrix = pd.DataFrame(matrix_symmetric, index=matrix.index, columns=matrix.columns)
#         symmetric_matrix.index = labels
#         symmetric_matrix.columns = labels
#         plt.figure(figsize=(10, 8),  dpi=100)
#         ax = sns.heatmap(symmetric_matrix, cmap='viridis', annot=True)
#         ax.set_title(f'{condition} RDM, ROI: {corr}, sub: {subject}')
#         cbar = ax.collections[0].colorbar
#         cbar.set_label('Correlation Coefficient', labelpad=10)  # Increase the padding here
#         plt.show()
#         plt.close()
