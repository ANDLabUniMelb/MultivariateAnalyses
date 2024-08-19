import pandas as pd


df_files_list = pd.read_csv('/rsa/first_zstat_filenames.csv')
df_files_list.columns = [col.lower() for col in list(df_files_list.columns)]

stim_dict = {
    'cat': 1,
    'goose': 2,
    'lion': 3,
    'grizzly': 4,
    'fist': 5,
    'stick': 6,
    'gun': 7,
    'grenade': 8,
}
#%%

df_files_list[['round', 'stim', 'sub', 'stim_', 'trial']] = df_files_list['filename'].str.extract(r'R(\d+)_(\w+)_sub(\d+)_(\w+?)(\d+)\.nii\.gz')
df_files_list['stim_num'] = df_files_list['stim'].map(stim_dict)
df_files = df_files_list.drop(columns=['stim_'])[['sub', 'stim', 'stim_num', 'round', 'trial', 'filename']]
df_files = df_files.sort_values(['sub', 'stim_num', 'round', 'trial'])

#%%

df_pairs = pd.merge(df_files, df_files, on='sub', suffixes=('_1', '_2'))

# Filter out pairs where the filenames are the same or filename_1 is greater than filename_2 to avoid duplicate pairs in reverse order
df_pairs = df_pairs[df_pairs['filename_1'] < df_pairs['filename_2']]

# Optional: Select only relevant columns or rearrange columns if needed
df_pairs = df_pairs[['sub', 'filename_1', 'filename_2', 'stim_1', 'stim_num_1', 'round_1', 'trial_1', 'stim_2', 'stim_num_2', 'round_2', 'trial_2']].reset_index(drop=True)


df_pairs.to_csv('/Users/joecussen/Documents/Jobs/unimelb/adaptive_safety_coding/repos/and_lab/all_file_pairs.csv')

#%%

# #%%
# df_files_list.columns = [col.lower() for col in list(df_files.columns)]
# df_files= df_files.sort_values(by=['subject', 'trial', 'stim', 'round']).reset_index(drop=True)
# pairs = []


#%%





#%%


# #%%
# max_subjects = df_files['subject'].max()
# max_trials = df_files['trial'].max()
#
# for sub in range(1, max_subjects+1): # loop over subjects (same subject pairing)
#     if sub not in [6, 7, 27]:
#         sub_df = df_files[(df_files['subject'] == sub)]  # filter possible files
#         for trial in range(1, max_trials+1): # loop over trials (same trial pairing)
#             if len(sub_df)>0:
#                 for i in range(len(sub_df)):
#                     for j in range(i + 1, len(sub_df)): # consider pairs not already considered
#                             pairs.append((sub_df.iloc[i]['subject'], sub_df.iloc[i]['trial'], sub_df.iloc[i]['stim'], sub_df.iloc[i]['round'], sub_df.iloc[i]['file'], sub_df.iloc[j]['stim'], sub_df.iloc[j]['round'], sub_df.iloc[j]['file']))
#
# df_pairs = pd.DataFrame(pairs, columns=['subject', 'trial', 'stim1', 'round1', 'file1', 'stim2', 'round2', 'file2'])
# # df_pairs.to_csv('/Users/joecussen/Documents/Jobs/unimelb/adaptive_safety_coding/repos/and_lab/file_pairs.csv')
#
# #%%
#
# len(sub1_cat_df[['file1', 'file2']].duplicated())