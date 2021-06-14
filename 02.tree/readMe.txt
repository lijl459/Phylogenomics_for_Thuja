# 1. Run phyloneny_mafft.cmd to align sequences and filter gap longer than than 50% of the alignment length, alignment length shorter than 300bp, and missing indiviuals less than ./phyloneny_mafft.cmd 00.FAA 00.FNA 30 20

# 2. run iqtree to build maximum-likelihood (ML) trees per gene
./iqtree.command FNA_filtered iqtree 4 10

# 3. run astral to build species tree
mkdir astral
cd astral
cat ../iqtree/*.treefile >iq.trees
java -jar /data/soft/Astral/Astral/astral.5.6.3.jar -i iq.trees -o astral.tre

# 4. run mpest to build species tree
/data/soft/MP-EST/mp-est/src/mpest mpest.ctl
