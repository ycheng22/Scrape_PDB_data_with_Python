#!/bin/bash 
#SBATCH -J py_job 
#SBATCH -n 4 -N 1 
#SBATCH -t 8:00:00
#SBATCH --mem=10gb 
#SBATCH -o mat_%A.out 
#SBATCH -e mat_%A.err 
#SBATCH -J matjob
#SBATCH --mail-type=all 
#SBATCH -A WSU

##set up your environment 
module load python/3.7

## run python program
python scrap_pdb_improv_thread_mem.py
