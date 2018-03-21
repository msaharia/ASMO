#!/bin/bash -u
#PBS -A P48500028
#PBS -N ASMO
#PBS -m ea
#PBS -q regular
#PBS -l walltime=00:05:00
#PBS -l select=1:ncpus=36:mpiprocs=1
#PBS -o ./log/asmo.out
#PBS -e ./log/asmo.err
mkdir -p /glade/scratch/manab/temp
export TMPDIR=/glade/scratch/manab/temp
export MPI_SHEPHERD=true
/glade/u/home/manab/anaconda3/envs/py27/bin/python summa_ASMO.py > asmolog.txt
