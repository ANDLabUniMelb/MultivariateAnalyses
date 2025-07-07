#!/bin/bash
#SBATCH -p cascade
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --mem-per-cpu=32G
#SBATCH --time=00:30:00
#SBATCH --array=100,101,102,103,104,106,107,108,109,111,112,113,114,116,117,118,119,120,121,122,123,125,126,127,128,130,131,132,133,134,135,137,138,139,140,142,143,145,146,147,148,149,150,151,152,153,154,156

#SBATCH --job-name=VOI

#Load Matlab 
module load MATLAB/2023a_Update_1

#specify where your matlab function and SPM12 are located
func_path='/data/scratch/projects/punim1471/NeuroWIRED/scripts/CNBT/VOI'
SPM_path='/data/scratch/projects/punim1471/spm12'

#threshold is specified after 'TASK ID' and region # goes last
matlab -nodisplay -nodesktop -r "addpath '$matlab_path', addpath '$SPM_path', Function_VOI(${SLURM_ARRAY_TASK_ID},3,99)"