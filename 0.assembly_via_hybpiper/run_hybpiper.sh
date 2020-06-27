#!/bin/bash



#Remove any previous runs
#parallel rm -r {} :::: namelist.txt


#Run main HybPiper script with all available CPUs
#while read i
#do
#python /data/soft/HybPiper/reads_first.py -r $i*.fq -b 26sp.target.fasta  --prefix $i --bwa --cpu 30
#done < namelist.txt

#Get the seq_lengths.txt file
python /data/soft/HybPiper/get_seq_lengths.py 26sp.target.fasta  namelist.txt dna > test_seq_lengths.txt

#Test for paralogs
while read i
do
python  /data/soft/HybPiper/paralog_investigator.py $i
done < namelist.txt

#Run intronerate
while read i
do
python  /data/soft/HybPiper/intronerate.py --prefix $i
done < namelist.txt
