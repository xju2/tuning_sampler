#!/bin/bash

for INDIR in submit/*
do
	if [ -d $INDIR ];then
		echo $INDIR
		pythia8-main93 -c $INDIR/runPythia.cmnd -n 10000 -o $INDIR/combined
	fi
done
