# Multivariate Analyses

This repository contains code for various multivariate analyses on neuroimaging data, used for research within the AND Lab.
The code is mostly written in matlab and python, and it serves as examples can be re-applied to new analyses.

For each type of analysis, more specific information and instructions on the files and how to run them can be found in the README.md of the corresponding folder.

### Spartan (unimelb HPC):

You will probably want to run your analyses on Melbourne's HPC system, Spartan, since this can handle large processes and amounts of data...

So here are a few useful snippets of bash code:


__SSH login from terminal:__

```ssh yourusername@spartan.hpc.unimelb.edu.au```

__Change directory:__

```cd /data/gpfs/projects/punim****```


__Start interactive session:__

```sinteractive -p interactive --time=05:00:00 --cpus-per-task=8 --mem=32G```

__Load matlab:__

```module load MATLAB/2023a_Update_1```

__Run matlab script__
```matlab -nodisplay -nosplash -nodesktop -r "run('your_script.m'); exit;"```

__Secure copy files:__

To copy from spartan cluster to your local machine:

```scp -r yourlogin@spartan.hpc.unimelb.edu.au:/data/gpfs/projects/punim****/your/files /your/local/file/path```

To copy from your local machine to spartan, switch the order of the filepaths i.e. put the local path first, and spartan path second.

__Compare files:__

```cmp -s /path/to/first/file /path/to/second/file```

__Batch processing:__

The easiest way to run long processes on Spartan is to set them running as batch jobs, disconnected from the terminal. That way the job will complete by itself and you can logout/ leave your computer.

To do this, you need to create a bash script with commands referencing your matlab/python scripts. You can then run the batch job with:

```sbatch yourbashscript.sh```

Check the job queue for your account:

```squeue -u yourusername```

```sprio -u yourusername```

Cancel a job using the job number:

```scancel yourjobnumber```


__Bash script example:__

Here is an example bash script. The #SBATCH parameters define the settings for your batch job, such as number of tasks, CPUs, memory, time etc... Replace punim**** and yourjobname with your assigned project resource and a job name.

```
#!/bin/sh
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=48G
#SBATCH --account=punim****
#SBATCH --job-name='yourjobname'
#SBATCH --time=0-24:00:00
#SBATCH -o /data/gpfs/projects/punim****/scripts/logs/slurm.%N.%j.out
#SBATCH -e /data/gpfs/projects/punim****/scripts/logs/slurm.%N.%j.err

module load MATLAB/2023a_Update_1
# Define the directory containing your MATLAB scripts
SCRIPT_DIR="/data/gpfs/projects/punim****/scripts"

# Navigate to the directory containing your MATLAB scripts
cd "${SCRIPT_DIR}"

run_condition="first_zstat"

echo "Processing with run_condition=${run_condition}
matlab -nosplash -nodesktop -r "addpath(genpath('${SCRIPT_DIR}')); your_matlab_script; exit;"
```
