#!/bin/bash

#SBATCH --job-name=$jobname
#SBATCH --nodes=$node
#SBATCH --ntasks-per-node=$ncore
#SBATCH -t $usetime:00:00
#SBATCH --partition=$partition

python mpi_run.py $index

EOF
chmod +x $subScript
errcode=$?
if [ $errcode -eq 0 ]; then
  sbatch $subScript
fi

