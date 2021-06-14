#!/usr/bin/env python
import sys, re, os
from Bio import SeqIO

if len(sys.argv) != 3:
    print("Usage: <Script> <in_root> <out_root>")
    exit()

k = re.compile("\s+")

inroot = sys.argv[1]
outroot = sys.argv[2]

if not os.path.exists(os.path.join(outroot, "input")):
    os.mkdir(os.path.join(outroot, "input"))

dic = {}
info = " "*30

cfg = """## ALIGNMENT FILE ##
alignment = concatated.phy;

## BRANCHLENGTHS: linked | unlinked ##
branchlengths = linked;

## MODELS OF EVOLUTION: all | allx | mrbayes | beast | gamma | gammai | <list> ##
models = all;

# MODEL SELECCTION: AIC | AICc | BIC #
model_selection = aicc;

## DATA BLOCKS: see manual for how to define ##
[data_blocks]
%s

## SCHEMES, search: all | user | greedy | rcluster | rclusterf | kmeans ##
[schemes]
search = rcluster;"""

blocks = """%s_pos1 = %d-%d\\3;
%s_pos2 = %d-%d\\3;
%s_pos3 = %d-%d\\3;
"""

s = ""
n = 0
spset = set()

for i in sorted(os.listdir(inroot)):
    if i.endswith(".fas"):
        inpath = os.path.join(inroot, i)
        for seq_record in SeqIO.parse(inpath, "fasta"):
            name = str(seq_record.id)
            spset.add(name)

for name in spset:
    dic[name] = ""

print(len(spset))
count = 0
for i in sorted(os.listdir(inroot)):
    if i.endswith(".fas"):
        inpath = os.path.join(inroot, i)
        namelist = list(spset)
        for seq_record in SeqIO.parse(inpath, "fasta"):
            name = str(seq_record.id)
            namelist.remove(name)
            sequences = str(seq_record.seq)
            dic[name] += sequences
        gene = i.split(".")[0]
        n0 = n
        n += len(sequences)
        seqlen = len(sequences)
        for individual in namelist:
            dic[individual] += "-" * seqlen

        s += blocks % (gene, n0+1, n, gene, n0+2, n, gene, n0+3, n)

with open(os.path.join(outroot, "input", "concatated.phy"), "w") as outfile:
    for name in sorted(dic):
        nseq = len(dic[name])
        nsp = len(dic)
        outfile.write("%d\t%d\n\n" % (nsp, nseq))
        break

    for name in sorted(dic):
        #spinfo = name + " "*(30-len(name))
        outline = name + " "*10 + dic[name] + "\n"
        outfile.write(outline)

with open(os.path.join(outroot, "input", "partition_finder.cfg"), "w") as f:
    f.write(cfg % (s))
        
print("python /data/soft/partitionfinder/partitionfinder-2.1.1/PartitionFinder.py input -p 10 --raxml [--rcluster-max 100]")
    
