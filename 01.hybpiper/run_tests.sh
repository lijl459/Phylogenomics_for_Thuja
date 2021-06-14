#!/bin/bash



#Remove any previous runs
parallel rm -r {} :::: namelist.txt


#Run main HybPiper script with all available CPUs
while read i
do
python /data/soft/HybPiper/reads_first2.py -r $i*.gz -b target.fas   --prefix $i --bwa --cpu 40
done < namelist.txt

#Get the seq_lengths.txt file
python /data/soft/HybPiper/get_seq_lengths.py target.fas  namelist.txt dna > test_seq_lengths.txt

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

#Run hybpiper_stats
python /data/soft/HybPiper/hybpiper_stats.py test_seq_lengths.txt namelist.txt >assembly_stats.txt

# Run /data/soft/HybPiper/cleanup.py
while read i
do
python  /data/soft/HybPiper/cleanup.py $i
done < namelist.txt

