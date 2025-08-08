import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


spec = 'GCM_0707_unsmooth_fear_1_combined_peb_fit' # main run spec
path = f"/Users/joecussen/Documents/Jobs/unimelb/projects/panda/scripts/peb_results/0707/{spec}"
models_csv = f"{path}/driving_inputs_models.csv"
regions_csv = f"{path}/driving_inputs_regions.csv"

df_models = pd.read_csv(models_csv)
df_regions = pd.read_csv(regions_csv)

name_dict = {
    "hipp": "Hipp",
    "postvmpfc": "p-vmPFC",
    "amygdala": "Amygdala",
    # "striatum":  "Striatum",
    "hipp+postvmpfc": "Hipp + p-vmPFC",
    "hipp+amygdala": "Hipp + Amygdala",
    "postvmpfc+amygdala": "p-vmPFC + Amygdala",
    "all": "Hipp + p-vmPFC + Amygdala"
}
df_models = pd.concat([df_models.iloc[1:], df_models.iloc[[0]]], ignore_index=True)

df_models['region'] = df_models['region'].replace(name_dict)
# --- everything above stays the same ---

# round to 2 dp (keeps decimals)
df_models['model_probability'] = df_models['model_probability'].round(2)

fig, ax = plt.subplots(figsize=(7, 7))
bars = ax.bar(df_models['region'], df_models['model_probability'], color='#E29338')

# value labels (slight offset so they fit)
for bar in bars:
    h = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2,
            h + 0.02,                # small offset, not +1
            f'{h:.2f}',
            ha='center', va='bottom', fontsize=10)

ax.set_ylim(0, df_models['model_probability'].max() + 0.1)  # top padding
ax.set_ylabel('Posterior Probability', fontsize = 12)
# ax.set_xlabel('Model', fontsize = 12)

ax.set_title('Driving Input Bayesian Model Selection',
             fontsize=16, pad=25)

for side in ('top', 'right'):
    ax.spines[side].set_visible(False)

plt.xticks(rotation=45, ha='right')
# … your plotting code …

plt.tight_layout()
plt.savefig(f'{path}/models_bms_plot.png', dpi=300, bbox_inches='tight')  # save figure
plt.show()
