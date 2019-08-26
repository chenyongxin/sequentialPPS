# sequentialPPS
> Postprocessing for sequential output data

## Introduction
This repository tries to collect data from sequential output from a mimic-multiprocessors program and generate visualization for paraview/visIt.

Two scripts are included in this repository: sequential.f90 and visu.py.

* sequential.f90: generates only one output data file from mimic-multiprocessors program.
* visu.py: generates hdf5 file and XDMF file for paraview/visIt.

## Usage
1. To compile and run sequential.f90:
```
gfortran sequential.f90
./a.out
```
2. To run visu.py:
```
python visu.py
```
