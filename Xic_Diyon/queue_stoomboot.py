"""
This script is used to run the BDT python script on the stoomboot cluster

Author: Maris Koopmans
"""

import os, sys

# Indicate which run we're testing
run = 22

# Boost the tree with some different amount of trees
ntrees = [100]#, 200, 400, 650, 800, 1200, 2000]
# ntrees = [200, 400, 650]

# Define and create the output directory
output_dir = f'/data/bfys/dwickrem/bdt_train_outputs/BDT_run{run}'

try:
	os.mkdir(output_dir)
except OSError:
	print(f'creation of directory {output_dir} failed')

for ntree in ntrees:

	# Define the command we want to use
	test_cmd = f'python /user/dwickrem/documents/XiC_analysis/load_and_train.py {run} {ntree} {output_dir}'

	# Define the script we want to use to execute this command
	submit_script = 'execute_stoomboot.sh'

	# Add the command to the submit file
	os.system(f'echo "#!/bin/sh" >> {submit_script}')

	# Move into the directory for the current run
	os.system(f'echo cd {output_dir} >> {submit_script}')
	os.system(f'echo {test_cmd} >> {submit_script}')

	# Define the command to run the script on the cluster and run it
	# Run on the gpu queue as the script needs to be allocated a lot of RAM
	run_command = f"qsub -q gpu -j oe -o /data/bfys/dwickrem/bdt_train_outputs/BDT_run{run}/run_{run}_{ntree}trees.out {submit_script}"
	os.system(run_command)

	# Delete the file to execute the script to keep the directory clean
	os.system(f"rm -f {submit_script}")
