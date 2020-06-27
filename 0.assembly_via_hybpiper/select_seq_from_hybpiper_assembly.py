#!/usr/bin/python
# This script was used to extract FNA file and FAA file from reluts of HybPiper
# input the dir of HybPiper results file
# output FNA and FAA sequence per gene
# By LiJL

import sys, os, re
from Bio import SeqIO



k = re.compile("\s+")

if len(sys.argv) != 4:
    print("Usage: <Script> <indir> <genes_with_paralog_warnings.txt> <outdir>")
    exit()

outdir = sys.argv[-1]
indir = sys.argv[1]

paralog = set()
with open(sys.argv[2]) as f:
    for line in f:
        line = line.strip()
        paralog.add(line)




#namelist = []
#with open(sys.argv[2]) as f:
#    for line in f: namelist.append(k.split(line)[0])

paralog = set()


dicN = {}
dicA = {}
shortgene = []
indset = set()

for i in os.listdir(indir):
    inpath = os.path.join(indir, i)
    if os.path.exists(inpath):
        for root, path, names in os.walk(inpath):
            if root.endswith("FNA") and len(names) == 1:
                genepath = os.path.join(root, names[0])
                gene = names[0].split(".")[0]
                if gene not in dicN.keys():
                    dicN[gene] = []
                if gene not in paralog:
                    for seq_record in SeqIO.parse(genepath, "fasta"):
                        indname = seq_record.id
                        indset.add(indname)
                        length = len(seq_record.seq)
                        if length < 300:
                            shortgene.append(gene)
                        dicN[gene].append(seq_record)
            elif root.endswith("FAA") and len(names) == 1:
                genepath = os.path.join(root, names[0])
                gene = names[0].split(".")[0]
                if gene not in dicA.keys():
                    dicA[gene] = []
                if gene not in paralog:
                    for seq_record in SeqIO.parse(genepath, "fasta"):
                        indname = seq_record.id
                        indset.add(indname)
                        length = len(seq_record.seq)
                        if length < 100:
                            shortgene.append(gene)
                        dicA[gene].append(seq_record)


os.chdir(outdir)

if not os.path.exists("FNA"):
    os.mkdir("FNA")
if not os.path.exists("FAA"):
    os.mkdir("FAA")



for key in dicN.keys():
    if key not in shortgene:
        outname = key + ".FNA"
        outroot = os.path.join("FNA", outname)
        SeqIO.write(dicN[key], outroot, "fasta")

for key in dicA.keys():
    if key not in shortgene:
        outname = key + ".FAA"
        outroot = os.path.join("FAA", outname)
        SeqIO.write(dicA[key], outroot, "fasta")

                        
                        
                    
                
    



