# 1. run mafft to align sequences
./1.mafft.cmd FNA FNA_mafft
parallel -j 20 :::: mafft.sh

# 2. run trimal to trim alignments
./2.trimal.cmd FNA_mafft FNA_trimal
parallel -j 20 :::: trimal.sh

# 3. run filtering_alignments.py to filter gap longer than than 50% of the alignment length, alignment length shorter than 300bp, and missing indiviuals less than 20% (keep 54 indiviuals of 67 indiviuals)
mkdir FNA_filtered
python 3.filtering_alignments.py FNA_trimal FNA_filtered 54

# 4. run iqtree to build maximum-likelihood (ML) trees per gene
./4.iqtree.cmd FNA_filtered iqtree

# 5. run astral to build species tree
mkdir astral
cd astral
cat ../iqtree/*.treefile >iq.trees
java -jar /data/soft/Astral/Astral/astral.5.6.3.jar -i iq.trees -o astral.tre

