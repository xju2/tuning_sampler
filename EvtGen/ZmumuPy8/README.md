# Introduction

This generates the $Z\to\mu\mu$ events in the $pp$ collision at $\sqrt s = 13$ TeV.


# Instructions

* Create DIY configuration
```bash
docker run -it --rm -v $PWD:$PWD -w $PWD docexoty/py8hdf-cori:1.3.1 create_diy_configs py8_zmumu_13TeV_A14.cmd parameters_MPI.json
```
* Generate events
The data analysis is [ATLAS_2019_I1736531](https://rivet.hepforge.org/analyses/ATLAS_2019_I1736531).

Start the docker container:
```bash
docker run -it --rm -v $PWD:$PWD -w $PWD docexoty/mctuning:1.0.0 bash
```
then generate the events:
```bash
mpirun -n 6 pythia8-diy -i submit -n 30000 -a ATLAS_2019_I1736531 --evts-per-block 5000 -o combined.yoda
```