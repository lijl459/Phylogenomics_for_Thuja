#!/bin/bash

if [ $# != 4 ] ; then
echo "USAGE: $0 <fasta_dir> <out_dir> <num_cores> <num_runs>"
echo " e.g.: $0 sequence/04.length50/ iqtree 4 10"
exit 1;
fi

indir=$1
outdir=$2
num_core=$3
n_run=$4

if [ ! -d "$outdir" ]; then
mkdir -p $outdir
fi

if [ -e "iqtree.sh" ]; then
rm iqtree.sh
fi

for i in $indir/*.fas
do
a=${i##*/}
b=${a%%.*}
echo "/data/soft/iqtree/iqtree-2.1.3-Linux/bin/iqtree2 -s $i -pre $outdir/$b -st DNA  -nt auto -B 1000 -m MFP  -quiet  " >>iqtree.sh
done

parallel -j $n_run :::: iqtree.sh
