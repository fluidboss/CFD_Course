##
## This is a bash programme
## Please add extrudeMeshDict to the system directory
## add creating2D.sh to the main directory
## then run
## chmod 777 creating2D.sh
## ./creating2D.sh

rm -r postProcessing
foamListTimes -rm
blockMesh
snappyHexMesh -overwrite
extrudeMesh
pimpleFoam
