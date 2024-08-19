# IC Python

__Dependencies:__
- Python 3.10.14
- Packages in requirements.txt

__File descriptions:__
- ```IC_analysis.py``` - main script for creating chord plots and calculating betweenness centrality
- ```betweenness_centrality.py``` - calculates betweenness centrality between connected nodes (ROIs)
- ```category_mapping.py``` - set new labels and values to filenames for use as input for IC analysis 
- ```circle_plots.py``` -  visualising IC analysis output as chord plot
- ```p_values_output.py``` -  runs RSA using pairwise correlation method


__How to run:__
- Set all variables to your specific project, and make all modificatons needed
- Set up virtual environment with python 3.10.14 (conda works well)
- Install dependencies into virtual environment from requirements.txt file
- Run files from command line or Python IDE

__To run on Spartan HPC:__
- Rename input and output filepaths to spartan paths
- Move all files and dependencies to spartan, and run via bash script
