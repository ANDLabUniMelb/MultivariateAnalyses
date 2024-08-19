# RSA Python

__Dependencies:__
- Python 3.10.14
- Packages in requirements.txt

__File descriptions:__
- ```create_all_pairs.py``` - creates a list of all possible pairs of filenames from a list of files (for pairwise correlation calculations in RSA)
- ```create_pairs.py``` - creates a list of possible pairs of filenames, with some conditions
- ```plot_rdms.py``` -  visualising RDMs as plots
- ```rsa.py``` - main RSA calculation script
- ```rsa_all_pairs.py``` -  runs RSA using pairwise correlation method
- ```rsa_binary.py``` -  binary RSA calculation script
- ```sanity_checks.py``` -  loads data files for basic sanity checks

__How to run:__
- Set all variables to your specific project, and make all modificatons needed
- Set up virtual environment with python 3.10.14 (conda works well)
- Install dependencies into virtual environment from requirements.txt file
- Run files from command line or Python IDE

__To run on Spartan HPC:__
- Rename input and output filepaths to spartan paths
- Move all files and dependencies to spartan, and run via bash script

