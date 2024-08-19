# IC Matlab

__Dependencies__:

This can be a bit of a pain to set up on Mac Silicon chip machines, make sure you download and install latest GitHub versions of dependencies.
- decoding_toolbox (download, install and add to matlab path)
- lib_svm (download, install and add to matlab path)
- spm_main (download, install and add to matlab path)

__File descriptions__:
- ```decoding_final.m``` - main decoding script
- ```decoding_readable.m``` - main decoding script, also checks that files are readable

__How to run:__
- Set all variables to your specific project, and make all modificatons needed
- Add dependencies to matlab path
- Run files in matlab

__To run on Spartan HPC:__
- Rename input and output filepaths to spartan paths
- Move all files and dependencies to spartan, and run via bash script