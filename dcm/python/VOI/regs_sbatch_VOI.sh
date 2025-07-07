#!/bin/bash

#SBATCH -p cascade
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --mem-per-cpu=32G
#SBATCH --time=00:30:00
#SBATCH --array=140,142,151,153

#SBATCH --job-name=VOI_regs

#Load Matlab 
module load MATLAB/2023a_Update_1

#specify where your matlab function and SPM12 are located
func_path='/data/scratch/projects/punim1471/NeuroWIRED/scripts/CNBT/VOI'
SPM_path='/data/scratch/projects/punim1471/spm12'

#threshold is specified after 'TASK ID' and region # goes last
matlab -nodisplay -nodesktop -r "addpath '$matlab_path', addpath '$SPM_path', regs_function_VOI(${SLURM_ARRAY_TASK_ID},12,1)"