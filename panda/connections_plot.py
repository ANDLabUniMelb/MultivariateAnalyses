import itertools as it
from typing import Dict, Iterable
from pathlib import Path                       # ← NEW


import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import networkx as nx
import pandas as pd
import numpy as np


# Default pastel node palette
NODE_COLOURS: Dict[str, str] = {
    "Hipp":      "#b1e6c2",
    "p-vmPFC": "#d8c3ff",
    "Amygdala":  "#fff6b3",
    # "Striatum":  "#ffd4b8",
}

name_dict = {
    "hipp": "Hipp",
    "postvmpfc": "p-vmPFC",
    "amygdala": "Amygdala",
    # "striatum":  "Striatum",
}

anchor_xy = {
    "Hipp":      (-0.5,  -0.5),   # left
    "p-vmPFC": ( 0.5,  -0.5),   # right
    "Amygdala":  ( 0.0,  0.5),   # top
    # "striatum":  ( 0.0, -1.0),   # bottom
}


def plot_ep_graph(
    df: pd.DataFrame,
    path: str,
    shell_layout: bool = True,
    scale_labels: float = 1.25,
    width_scale: float = 20.0,
    node_size: int = 500,
    arrowsize: int = 25,
    title: str | None = None,
    pad: float = 0.25,
    *,
    node_colours: Dict[str, str] = NODE_COLOURS,
    fixed_pos: Dict[str, tuple[float, float]] | None = anchor_xy,   # ← NEW
    ep_attr: str = "Ep",
    pp_attr: str = "Pp",
    source_col: str = "source",
    target_col: str = "target",
    legend: str = 'main',
) -> None:

    # Build graph
    G = nx.from_pandas_edgelist(
        df,
        source=source_col,
        target=target_col,
        edge_attr=[ep_attr, pp_attr],
        create_using=nx.MultiDiGraph()
    )

    # Positions
    pos = nx.shell_layout(G) if shell_layout else nx.spring_layout(G)
    if fixed_pos:
        pos.update({n: fixed_pos[n] for n in fixed_pos if n in G})
    pos_lbl = {n: (x * scale_labels, y * scale_labels) for n, (x, y) in pos.items()}

    # Node drawing
    nx.draw_networkx_nodes(
        G, pos,
        node_size=node_size,
        node_color=[node_colours.get(n, "#d3d3d3") for n in G.nodes()]
    )
    nx.draw_networkx_labels(G, pos_lbl, font_size=20)

    # Edge colours & widths
    edges = G.edges(keys=True, data=True)
    colours = ['#ff9999' if d[ep_attr] >= 0 else '#9999ff' for *_, d in edges]
    widths  = [abs(d[ep_attr]) * width_scale for *_, d in edges]

    nx.draw_networkx_edges(
        G, pos,
        edge_color=colours,
        width=widths,
        connectionstyle="arc3,rad=0.15",
        arrowsize=arrowsize
    )

    # Edge labels
    connectionstyle = [f"arc3,rad={r}" for r in it.accumulate([0.15] * 4)]
    labels = {tuple(e): f"{ep_attr}={d[ep_attr]}, {pp_attr}>{min(np.floor(d[pp_attr] * 100) / 100, 0.99)}" for *e, d in edges}
    nx.draw_networkx_edge_labels(
        G, pos,
        labels,
        connectionstyle=connectionstyle,
        label_pos=0.5,
        font_color="black"
    )

    # Layout tweaks
    plt.margins(pad)
    plt.axis('off')  # ← hides axes, ticks, frame
    plt.gca().set_frame_on(False)  # ← double-check: no box drawn

    if legend == 'main':
        legend_elements = [
            Line2D([0], [0], color='#ff9999', lw=3, label='Excitatory (Ep ≥ 0)'),
            Line2D([0], [0], color='#9999ff', lw=3, label='Inhibitory (Ep < 0)')
        ]
    else:
        legend_elements = [
            Line2D([0], [0], color='#ff9999', lw=3, label='Increased Ep'),
            Line2D([0], [0], color='#9999ff', lw=3, label='Decreased Ep')
        ]

    plt.legend(
        handles=legend_elements,
        loc='upper center',  # anchor point of the legend
        bbox_to_anchor=(0.95, 0.8),  # (x=centre, y=5% below the plot)
        frameon=False,
        fontsize=10
    )
    if title:
        plt.title(title, fontsize=16)
    plt.tight_layout()

    # -------- new, minimal save block --------
    fig = plt.gcf()                                   # ← NEW (grab *this* figure)
    out_dir = Path(path)                              # ← NEW
    out_dir.mkdir(parents=True, exist_ok=True)        # ← NEW
    fname = f"{title or 'plot'}.png"                  # ← NEW
    fig.savefig(out_dir / fname,
                dpi=300,
                bbox_inches="tight")                  # ← NEW
    # -----------------------------------------

    plt.show()
    plt.close(fig)                                    # ← NEW (keeps memory down)


spec = 'GCM_0707_unsmooth_fear_1_combined_peb_fit_amyg_no_striatum'
path = f"/Users/joecussen/Documents/Jobs/unimelb/projects/panda/scripts/peb_results/0707/{spec}"
connections_csv = f"{path}/connections.csv"
class_connections_csv = f"{path}/class_connections.csv"

df = pd.read_csv(connections_csv)
df['source']=df['source'].replace(name_dict)
df['target']=df['target'].replace(name_dict)
df['Ep'] =df['Ep'].round(2)
df_A = df[df['matrix']=='A'][['source', 'target', 'Ep', 'Pp']].reset_index(drop = True)
df_B = df[df['matrix']=='B'][['condition', 'source', 'target', 'Ep', 'Pp']].reset_index(drop = True)
plot_ep_graph(df_A, title = 'A Matrix: Intrinsic connections', width_scale=5, path = path)



condition_dict={
    1.0: 'Task',
    2.0: 'Early conditioning CS+',
    3.0: 'Early conditioning CS-',
    4.0: 'Early extinction CS+',
    5.0: 'Early extinction CS-',
}

for con in [2.0, 3.0, 4.0, 5.0]:
    df_con = df_B[df_B['condition']==con]
    df_con=df_con[df_con['Pp']>0.95].reset_index(drop=True)
    plot_ep_graph(df_con, title=f'B Matrix: {condition_dict[con]}', width_scale=3.5, path = path)

#%%
df_class = pd.read_csv(class_connections_csv)
df_class['source']=df_class['source'].replace(name_dict)
df_class['target']=df_class['target'].replace(name_dict)
df_class['Ep'] =df_class['Ep'].round(2)
df_class = df_class[['condition', 'source', 'target', 'Ep', 'Pp']].reset_index(drop = True)
for con in [2.0, 3.0, 4.0, 5.0]:
    df_class_con = df_class[df_class['condition']==con]
    df_class_con=df_class_con[df_class_con['Pp']>0.95].reset_index(drop=True)
    if df_class_con.shape[0]>0:
        plot_ep_graph(df_class_con, title = f'{condition_dict[con]}: Predictive of Trait Anxiety', width_scale=5, path = path, legend='')

