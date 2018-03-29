#!/bin/bash -u
#PBS -A P48500028
#PBS -N ASMO_SUMMA
#PBS -m abe
#PBS -M manab@ucar.edu
#PBS -q regular
#PBS -l walltime=12:00:00
#PBS -l select=1:ncpus=36:mpiprocs=1
#PBS -o ./log/asmo.out
#PBS -e ./log/asmo.err
mkdir -p /glade/scratch/manab/temp
export TMPDIR=/glade/scratch/manab/temp
export MPI_SHEPHERD=true
/glade/u/home/manab/anaconda3/envs/py27/bin/python summa_ASMO.py > log4
