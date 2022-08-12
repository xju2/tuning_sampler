# Introduction

This generates the $Z\to\mu\mu$ events in the $pp$ collision at $\sqrt s = 13$ TeV.


# Instructions

* Create DIY configuration
```bash
docker run -it --rm -v $PWD:$PWD -w $PWD docexoty/py8hdf-cori:1.3.1 create_diy_configs py8_zmumu_13TeV_A14.cmnd parameters_MPI.json --pythia-cmd-name runPythia.cmnd
```
* Generate events
The data analysis is [ATLAS_2019_I1736531](https://rivet.hepforge.org/analyses/ATLAS_2019_I1736531).

Start the docker container:
```bash
docker run -it --rm -v $PWD:$PWD -w $PWD hepstore/rivet-pythia bash
```

```bash
pythia8-main93 -c runPythia.cmnd -n 10000 -o combined
```
The `runPythia.cmnd` looks like the following:
```text
Beams:idA = 2212                   ! first beam, p = 2212, pbar = -2212
Beams:idB = 2212                   ! second beam, p = 2212, pbar = -2212
Beams:eCM = 13000.                 ! CM energy of collision

WeakBosonAndParton:qqbar2gmZg = on              ! q qbar --> gamma*/Z0 g
WeakBosonAndParton:qg2gmZq = on                 ! q g --> gamma/Z0 q

23:onMode       = off                                   ! turn off all decay modes
23:onIfAny      = 13 -13                            ! turn on mumu decay mode

Tune:ee = 7                         ! use Monash 2013 Tune by Peter Skands
Tune:pp = 21                        ! use ATLAS A14 central tune with NNPDF2.3LO
PDF:pSet = 13                       ! use NNPDF23LO as the PDF set

UncertaintyBands:doVariations = on
UncertaintyBands:List = {
    MUR0.5_MUF1 isr:muRfac=0.5, 
    MUR2_MUF_1 isr:muRfac=2.0,
        PDFup isr:PDF:plus=1.0,
        PDFdn isr:PDF:minus=1.0
}
Main:runRivet = on
Main:analyses = ATLAS_2019_I1736531
MultipartonInteractions:alphaSvalue      = 0.1          ! alpha_s value for MPI
```
<!-- then generate the events:
```bash
mpirun -n 6 pythia8-diy -i submit -n 30000 -a ATLAS_2019_I1736531 --evts-per-block 5000 -o combined.yoda
``` -->