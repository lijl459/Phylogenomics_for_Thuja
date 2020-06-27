#!/bin/bash
indir=$1
outdir=$2

if [ ! -d "$outdir" ]; then
mkdir -p $outdir
fi


for i in $indir/*.fas
do
a=${i##*/}
b=${a%%.*}
echo "/data/soft/iqtree/iqtree-2.0.4-Linux/bin/iqtree2 -s $i -pre $outdir/$b -st DNA -o 19850753AA  -nt 5 -bb 1000 -m MFP  -quiet -redo && rm $outdir/$b.bionj $outdir/$b*.gz $outdir/$b.log $outdir/$b.mldist $outdir/$b.splits.nex" >>iqtree.sh
done
