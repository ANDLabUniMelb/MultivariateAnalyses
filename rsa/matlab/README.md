# RSA Matlab

__Dependencies:__
- CoSMoMVPA-master (download and add to matlab path)

__File descriptions:__
- ```rsa_final.m``` - RSA main script 
- ```rsa_final_cluster.m``` - RSA main script as a function that can be run on different conditions on Spartan cluster
- ```rsa_final_demeaned.m``` - RSA main script with demeaning added
- ```rsa_setup.m``` - Utility function to set up all variables 
- ```round_means.m``` - Function to calculate mean activation per round, only needed if demeaning
- ```view_rdms.m``` - Script to load and view RDM variables in matlab

__How to run:__
- Set all variables to your specific project, and make all modificatons needed
- Add dependencies to matlab path
- Run files in matlab

__To run on Spartan HPC:__
- Rename input and output filepaths to spartan paths
- Move all files and dependencies to spartan, and run via bash script

