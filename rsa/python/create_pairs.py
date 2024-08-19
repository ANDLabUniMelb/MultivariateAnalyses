import pandas as pd

df_files = pd.read_csv('/rsa/file_names.csv')

#%%
df_files.columns = [col.lower() for col in list(df_files.columns)]
df_files= df_files.sort_values(by=['subject', 'trial', 'stim', 'round']).reset_index(drop=True)
pairs = []

#%%
max_subjects = df_files['subject'].max()
max_trials = df_files['trial'].max()

for sub in range(1, max_subjects+1): # loop over subjects (same subject pairing)
    if sub not in [6, 7, 27]:
        for trial in range(1, max_trials+1): # loop over trials (same trial pairing)
            sub_df = df_files[(df_files['subject']==sub)&(df_files['trial']==trial)] # filter possible files
            if len(sub_df)>0:
                for i in range(len(sub_df)):
                    for j in range(i + 1, len(sub_df)): # consider pairs not already considered
                        if sub_df.iloc[i]['round'] != sub_df.iloc[j]['round']: # if from different rounds (different round pairing)
                            pairs.append((sub_df.iloc[i]['subject'], sub_df.iloc[i]['trial'], sub_df.iloc[i]['stim'], sub_df.iloc[i]['round'], sub_df.iloc[i]['file'], sub_df.iloc[j]['trial'], sub_df.iloc[j]['stim'], sub_df.iloc[j]['round'], sub_df.iloc[j]['file']))

df_pairs = pd.DataFrame(pairs, columns=['subject', 'trial1', 'stim1', 'round1', 'file1', 'trial2', 'stim2', 'round2', 'file2'])

#%%
df_pairs.to_csv('/Users/joecussen/Documents/Jobs/unimelb/adaptive_safety_coding/repos/and_lab/file_pairs_all.csv')

#%%
sub1_df = df_pairs[df_pairs['subject']==1]

#%%

sub1_cat_df = sub1_df[(sub1_df['stim1']=='cat')&(sub1_df['stim2']=='cat')]