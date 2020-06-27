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
echo "/data/soft/trimal/trimal-trimAl/source/trimal -in $i -out $outdir/$b.gt80.cds.fas -htmlout $outdir/$b.gt80.html -gt 0.8">>gt80.sh
done
