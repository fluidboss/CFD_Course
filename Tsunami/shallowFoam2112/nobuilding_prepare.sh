#!/bin/bash

#$ -S /bin/bash
#$ -l h_rt=0:30:0
#$ -l mem=1G
#$ -l tmpfs=15G
#$ -t 1-1
#$ -N Teeth_cone_0.05
#$ -wd /home/ucemiea/Scratch/OpenFOAM/ucemiea-2.4.0/applications/solvers/shallowFoam

#$ -ac allow=LMNOPQSTU
module load mesa gmsh
module load python/2.7.9
module load boost/1_54_0/mpi/intel-2015-update2
module load gsl/2.4/intel-2017  
module load openfoam/2.4.0/intel-2017-update1

wclean
wmake