# IC Matlab

__Dependencies__:
- CoSMoMVPA-master (download and add to matlab path)
- latest_IC_toolbox (download and add to matlab path)

__File descriptions__:
- ```IC_clean.m``` - main script for IC analysis
- ```IC_setup.m``` - setup helper function for defining initial variables
- ```nanzscore.m``` - custom function for calculating zscores as part of IC
- ```plot_ICM.m``` - plotting function for creating and saving ICM output figures
- ```stouffer_method.m``` - stouffer statistical method for computing z scores across all subjects
- ```sig_testing.m``` - script to calculate significance (not needed as this is also in IC_clean) 
- ```count_voxels.m``` - utility function to count the number of voxels in ROI masks
- ```roi_overlap.m``` - utility function to determine the overlapping voxels in a set of ROI masks.


__How to run:__
- Set all variables to your specific project, and make all modificatons needed
- Add dependencies to matlab path
- Run files in matlab

__To run on Spartan HPC:__
- Rename input and output filepaths to spartan paths
- Move all files and dependencies to spartan, and run via bash script