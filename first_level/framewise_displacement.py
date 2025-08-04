#%%

import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

def load_and_fill(path, sep="\t"):
    cols = pd.read_csv(path, sep=sep, nrows=0).columns           # grab header
    return (pd.read_csv(path, sep=sep, engine="python",
                        names=cols, header=0, on_bad_lines="warn")  # tolerate ragged rows
            .bfill())                                    # back- then forward-fill

base = Path("/Users/joecussen/Documents/Jobs/unimelb/projects/panda/data")
df_fear1 = load_and_fill(base / "fear1_framewise_displacement.tsv")
df_fear2 = load_and_fill(base / "fear2_framewise_displacement.tsv")

#%%
# mean framewise‐displacement per subject, returned as a tidy DataFrame
df_fear1_fd = (df_fear1
               .groupby('subject', as_index=False)['framewise_displacement']
               .mean()                                   # now keeps 'subject' as a column
               .rename(columns={'framewise_displacement': 'mean_fd'}))  # optional rename

df_fear2_fd = (df_fear2
               .groupby('subject', as_index=False)['framewise_displacement']
               .mean()
               .rename(columns={'framewise_displacement': 'mean_fd'}))

#%%

# --- combine the two summaries ------------------------------------------------
fd = (
    df_fear1_fd.merge(df_fear2_fd, how="outer", on="subject",
                      suffixes=("_fear1", "_fear2"))  # keep every subject
        .set_index("subject")                         # subjects on x-axis
)

# --- quick grouped-bar plot ----------------------------------------------------
ax = fd.plot(kind="bar", width=0.8, figsize=(15, 5))  # one bar per task/subject
ax.set_ylabel("Mean framewise displacement")
ax.set_title("Mean framewise displacement per subject\n(fear 1 vs fear 2)")
ax.legend(["fear 1", "fear 2"], title="Task")
plt.tight_layout()
plt.show()

#%%
import numpy

fd_= df_fear1_fd.merge(df_fear2_fd, how="outer", on="subject",
                      suffixes=("_fear1", "_fear2"))

fear1_excluded = fd_[(fd_['mean_fd_fear1']>0.3)]
fear2_excluded = fd_[(fd_['mean_fd_fear2']>0.3)|fd_['mean_fd_fear2'].isnull()]

list(fear1_excluded['subject'])

list(fear2_excluded['subject'])