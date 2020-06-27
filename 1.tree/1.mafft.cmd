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
echo "mafft --auto --quiet $i >$outdir/$b.mafft.cds.fas" >>maff.sh
done
