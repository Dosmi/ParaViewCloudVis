#!/bin/bash

#ADAPTED FROM SOURCE: https://docs.archer2.ac.uk/user-guide/scheduler/
#SEARCH FOR: Example: job submission script for MPI parallel job


# Slurm job options (job-name, compute nodes, job time)
#SBATCH --job-name=Example_MPI_Job
#SBATCH --time=0:20:0
#SBATCH --nodes=1
#SBATCH --tasks-per-node=32
#SBATCH --cpus-per-task=4

# Replace [budget code] below with your budget code (e.g. t01)
#SBATCH --account=[budget code]
#SBATCH --partition=standard #or highmem
#SBATCH --qos=standard # or highmem

# Set the number of threads to 1
#   This prevents any threaded system libraries from automatically
#   using threading.
export OMP_NUM_THREADS=1

# Launch the parallel job
#   Using 32*1 MPI processes and 32 MPI processes per node
#   srun picks up the distribution from the sbatch options


module load epcc-setup-env
module load load-epcc-module


module load paraview/5.10.1


srun --distribution=block:block --hint=nomultithread pvbatch pvbatchscript.py
~
