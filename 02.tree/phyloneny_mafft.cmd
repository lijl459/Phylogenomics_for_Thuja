#!/usr/bin/bash


if [ $# != 4 ] ; then 
echo "USAGE: $0 <pep_dir> <cds_dir> <parallel_jobs> <number of individuals>" 
echo " e.g.: $0 00.FAA 00.FNA 30 8" 
exit 1; 
fi


pepdir=$1
cdsdir=$2
n=$3
nsp=$4


out1=01.pep_aln
out2=02.cds_aln
out3=03.gt50
out4=04.ind50


#Step 1 using mafft to align pep sequences
echo "Step 1 align pep using mafft"

if [ -d $out1 ]; then
    rm -r $out1
fi

mkdir $out1

if [ -e "mafft.sh" ]; then
rm mafft.sh
fi

for i in $pepdir/*.fas
do
basename=$(basename ${i} .fas)
echo "mafft --genafpair --maxiterate 1000 --quiet $i >$out1/${basename}.aln.pep.fas" >>mafft.sh
done

parallel  -j $n :::: mafft.sh

#Step 2 using pal2nal to align cds sequences
echo "Step 2 using pal2nal to align cds sequences"


if [  -d $out2 ]; then
    rm -r $out2
fi

mkdir -p $out2

if [ -e "pal.sh" ]; then
rm pal.sh
fi


for i in $out1/*.fas
do
basename=$(basename ${i} .aln.pep.fas)
echo "perl /data/soft/pal2nal/pal2nal.v14/pal2nal.pl $i $cdsdir/${basename}.fas  -output fasta > $out2/${basename}.align.cds.fas" >>pal.sh
done

parallel -j $n :::: pal.sh

#Step 3 using perl script to retain gene types rate greater than 80% with 3 windows.
#Perl script was download from https://github.com/yongzhiyang2012/Euryale_ferox_and_Ceratophyllum_demersum_genome_analysis, Yang et al., 2020, Nature Plants, https://doi.org/10.1038/s41477-020-0594-6.
echo "Step 3 using perl script to retain gene types rate greater than 80% with 3 windows"


if [  -d $out3 ]; then
    rm -r $out3
fi

mkdir -p $out3

if [ -e "gt.sh" ]; then
rm gt.sh
fi


for i in $out2/*.fas
do
basename=$(basename ${i} .align.cds.fas)
echo "/home/user001/script/perl/fasta-missing.pl $i 80 3 >$out3/${basename}.fas" >>gt.sh
done

parallel  -j $n :::: gt.sh



#Step 4 using python script to removed length of gaps more than half of aligment sequences
echo "Step 4 using python script to removed length of gaps more than halp of aligment sequences"

if [ -d $out4 ]; then
    rm -r $out4
fi  

mkdir -p $out4

python filtering_alignment_missing.py $out3 $out4  $nsp

