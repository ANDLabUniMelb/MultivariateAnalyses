import os
import numpy as np
import matplotlib.pyplot as plt
import mat73
from scipy.sparse import issparse
from collections import defaultdict

specs = ["final"]
results_dir = f"/Users/joecussen/Documents/Jobs/unimelb/projects/dcm/results/final/"
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

for dcm_name in dcm_names:
    dcm_version = f'{dcm_name}_{version}'
    for spec in specs:
        # Load the PEB data.
        peb_path = os.path.join(results_dir, f'PEB_{dcm_version}_{spec}.mat')
        data = mat73.loadmat(peb_path)
        peb = data.get('PEB')
        if isinstance(peb, list):
            peb = peb[0]
        print("Pnames:", peb['Pnames'])

        # Determine number of A-matrix parameters based on number of regions.
        regions = ['antvmpfc', 'postvmpfc', 'amy', 'striatum']
        a_matrix_len = len(regions) ** 2

        # Process Ep and Cp.
        Ep = peb['Ep']
        if issparse(Ep):
            Ep = Ep.toarray()
        Ep = np.array(Ep).flatten()

        # The first a_matrix_len values are for the A matrix;
        # the remaining ones are for the condition-specific B matrices.
        B_params = Ep[a_matrix_len:]
        Cp = np.array(peb['Cp'])
        Cp = Cp[a_matrix_len:, a_matrix_len:]
        ci_vals = 1.96 * np.sqrt(np.diag(Cp))

        # Get the B parameter names.
        # Note: In the provided Pnames these are stored as lists like [['B(2,1,2)'], ...]
        b_param_names = [p[0] if isinstance(p, list) else p for p in peb['Pnames'][a_matrix_len:]]

        # Function to parse a B parameter name.
        def parse_b_name(bname):
            # Expected format: "B(i,j,k)"
            inner = bname.strip()[2:-1]  # remove the "B(" prefix and ")" suffix
            parts = inner.split(',')
            if len(parts) != 3:
                raise ValueError(f"Unexpected B parameter format: {bname}")
            target = int(parts[0])
            source = int(parts[1])
            cond = int(parts[2])
            return target, source, cond

        # Function to generate a connection label given target and source indices.
        def connection_label(target, source):
            # The effect is from the source region to the target region.
            return f"{roi_names[source]}→{roi_names[target]}"

        # Group B parameters by condition.
        # For each parameter we store its Ep value, its error (ci), and its connection label.
        condition_data = defaultdict(lambda: {"Ep": [], "ci": [], "labels": []})
        for idx, bname in enumerate(b_param_names):
            target, source, cond = parse_b_name(bname)
            label = connection_label(target, source)
            condition_data[cond]["Ep"].append(B_params[idx])
            condition_data[cond]["ci"].append(ci_vals[idx])
            condition_data[cond]["labels"].append(label)

        # Sort conditions numerically (assuming the condition number k starts at 1).
        sorted_conditions = sorted(condition_data.keys())
        num_conditions = len(sorted_conditions)

        # Verify that all conditions have the same number of connections.
        connection_counts = [len(condition_data[cond]["Ep"]) for cond in sorted_conditions]
        if len(set(connection_counts)) != 1:
            print("Warning: Conditions have differing numbers of connections:", connection_counts)
        num_connections = connection_counts[0]

        # Create subplots (one per condition).
        fig, axs = plt.subplots(num_conditions, 1, sharex=True, figsize=(8, 4 * num_conditions))
        if num_conditions == 1:
            axs = [axs]

        # (Assuming the connection order is the same across conditions, we use the first condition's labels.)
        x_labels = condition_data[sorted_conditions[0]]["labels"]

        # Loop over conditions and plot.
        for i, cond in enumerate(sorted_conditions):
            ep_values = condition_data[cond]["Ep"]
            ci_errors = condition_data[cond]["ci"]
            # Map condition number to condition name using the dictionary.
            cond_name = condition_names[dcm_name][cond - 1] if cond - 1 < len(condition_names[dcm_name]) else f"Condition {cond}"
            axs[i].axhline(0, color='black', linestyle='--', linewidth=1)
            axs[i].bar(range(num_connections), ep_values, color='skyblue', edgecolor='black')
            axs[i].errorbar(range(num_connections), ep_values, yerr=ci_errors, fmt='k.',
                            linewidth=1.5, capsize=5)
            axs[i].set_title(cond_name)
            axs[i].set_ylabel("Parameter Estimate")
            axs[i].set_ylim(-1.5, 1.5)  # fixed y-axis limits

        axs[-1].set_xticks(range(num_connections))
        axs[-1].set_xticklabels(x_labels, rotation=45, ha='right')
        axs[-1].set_xlabel("Connection")
        plt.tight_layout()
        save_path = os.path.join(save_dir, f"{dcm_name}_{spec}_PEB_plot.png")
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()