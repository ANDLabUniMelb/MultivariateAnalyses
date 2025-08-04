import pandas as pd
from pathlib import Path

taskname = 'fear2'
tsv = Path(f'/Users/joecussen/Documents/Jobs/unimelb/projects/panda/data/task-{taskname}_events.tsv')
out_dir = f'/Users/joecussen/Documents/Jobs/unimelb/projects/panda/data/{taskname}_onsets'

df = pd.read_csv(tsv, sep='\t')
df= df[~df['trial_type'].isin(['Fixation', 'Question', 'Scream'])]
df['trial_type'] = 1
fname = Path(out_dir,'Task.txt')

df.to_csv(fname, sep='\t', header=False, index=False, columns=['onset', 'duration', 'trial_type'])

# for condition, g in df.groupby('trial_type'):
#     fname = out_dir / (''.join(c if c.isalnum() or c in '_+-' else '_' for c in condition) + '.txt')
#     g.assign(trial_type=1).to_csv(
#         fname, sep='\t', header=False, index=False, columns=['onset', 'duration', 'trial_type']
#     )
#     print(f'Wrote {fname} ({len(g)} rows)')
