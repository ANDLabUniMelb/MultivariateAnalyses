from pathlib import Path
import pandas as pd, re

df_scans = pd.read_csv("/Users/joecussen/Documents/Jobs/unimelb/projects/dcm_7t/data/onsets/scan_counts.csv")
df_scans["subject"] = df_scans["file"].str.extract(r'sub-(\d+)').astype(int)
df_scans["run"] = df_scans["file"].str.extract(r'[_-]run-?(\d+)', flags=re.I).astype(int)
df_scans = df_scans.sort_values(["subject", "run"]).reset_index(drop=True)
df_scans['tr']=0.8
df_scans["scans_before"] = (
    df_scans.groupby("subject")["n_scans"].cumsum() - df_scans["n_scans"]
)
df_scans['onset_offset']= df_scans['tr']*df_scans['scans_before']
df_scans = df_scans[['subject', 'run', 'tr', 'n_scans', 'scans_before', 'onset_offset']]


#%%

parent = Path("/Users/joecussen/Documents/Jobs/unimelb/projects/dcm_7t/data/onsets_2507/onsets")           # change to your parent directory
paths = [p for p in parent.rglob('*_safety_run-*.txt')        # include only *_safety_run-*.txt
         if "safety_interaction" not in p.name]

df = pd.DataFrame({"filepath": [str(p) for p in paths]})
df["subject"]    = df["filepath"].str.extract(r'sub-(\d+)').astype(int)
df["run"]        = df["filepath"].str.extract(r'_run-(\d+)').astype(int)
df["onset_name"] = df["filepath"].str.extract(r'_run-\d+_(.+)\.txt$')[0]

df = df.sort_values(["subject", "run", "onset_name"]).reset_index(drop=True)

records = []
for _, row in df.iterrows():
    tmp = pd.read_csv(row.filepath, sep=r"\s+", header=None,
                      names=["onset", "duration", "value"])
    tmp["subject"]    = row.subject
    tmp["run"]        = row.run
    tmp["onset_name"] = row.onset_name
    records.append(tmp)

all_events = pd.concat(records, ignore_index=True)   # outer-join style union

#%%
df_full = pd.merge(all_events, df_scans, on = ['subject', 'run'], how= 'left')

#%%
df_full['onset_new']= df_full['onset']+df_full['onset_offset']


#%%
df_full=df_full.sort_values(by = ['subject', 'onset_name', 'run'])

#%%

# directory in which to save the new files
out_dir = Path("/Users/joecussen/Documents/Jobs/unimelb/projects/dcm_7t/data/onsets_2507/concatenated")
out_dir.mkdir(parents=True, exist_ok=True)

for (sub, onset_name), g in (
        df_full.sort_values(['run', 'onset_new'])
               .groupby(['subject', 'onset_name'], sort=False)):

    out_path = out_dir / f"sub-{sub:02d}_safety_{onset_name}.txt"
    g[["onset_new", "duration", "value"]] \
        .to_csv(out_path,
                sep=' ',
                header=False,
                index=False,
                float_format='%.8f')   # adjust precision if needed
    print(f"wrote {out_path}")

#%%

task_categories = ['FirstStim_animals', 'FirstStim_weapons', 'SecondStim_animals', 'SecondStim_weapons', 'Outcome_lost', 'Outcome_won']
df_task = df_full[df_full['onset_name'].isin(task_categories)]
df_task['onset_name']='Task'
df_task=df_task.sort_values(by = ['subject','onset_new'])

for (sub, onset_name), g in (
        df_task.sort_values(['run', 'onset_new'])
               .groupby(['subject', 'onset_name'], sort=False)):

    out_path = out_dir / f"sub-{sub:02d}_safety_{onset_name}.txt"
    g[["onset_new", "duration", "value"]] \
        .to_csv(out_path,
                sep=' ',
                header=False,
                index=False,
                float_format='%.8f')   # adjust precision if needed
    print(f"wrote {out_path}")