#!/bin/bash -u
#PBS -A P48500028
#PBS -N ASMO
#PBS -m ea
#PBS -q regular
#PBS -l walltime=12:00:00
#PBS -l select=1:ncpus=36:mpiprocs=36
#PBS -o ./log/asmo.out
#PBS -e ./log/asmo.err
mkdir -p /glade/scratch/manab/temp
export TMPDIR=/glade/scratch/manab/temp
export MPI_SHEPHERD=true
mpiexec_mpt launch_cf.sh /glade/p/work/manab/fcast/ASMO/summa/asmo_joblist
