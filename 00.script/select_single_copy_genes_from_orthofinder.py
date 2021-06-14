#!/usr/bin/env python
import sys, re, os
from Bio import SeqIO

if len(sys.argv) != 6:
    print("Usage: <Script> <OrthoGroup.csv> <SingleCopyFile> <incds_root> <cds or pep> <out_root>")
    exit()

k = re.compile("\s+")

if sys.argv[4] == "pep":
    suffix = ".pep.fas"
    minlen = 100
else:
    suffix = ".cds.fas"
    minlen = 300
print(suffix)
print(minlen)

lst1 = []

with open(sys.argv[2]) as f:
    for line in f:
        line = line.strip()
        lst1.append(line)


dic = {}

with open(sys.argv[1]) as f:
    count = 0
    for line in f:
        count += 1
        if count == 1:
            a = k.split(line)
            id_list = [""]
            for name in a[1:-1]:
#                if "-" in name:
#                    sp = name.split("-")[0]
#                else:
#                    sp = name.split(".")[0]
                sp = name.split(".")[0]
                id_list.append(sp)
                dic[sp] = {}        
        elif line.startswith("OG"):
            line = line.strip()
            l = line.split("\t")
            if l[0] in lst1:
                for i in range(1, len(id_list)):
                    trans = k.split(l[i])[0]
                    if "|" in trans:
                        trans = trans.split("|")[0]

                    dic[id_list[i]][trans] = l[0]
        else:
            pass


# dic,  {sp1: {'TRINITY_DN14697_c0_g1_i1.p1': 'OG0009594'}}

cdsroot = sys.argv[3]


dic2 = {}
short = set()
for i in sorted(os.listdir(cdsroot)):
    if not i.endswith(".fa"):
        continue
    inpath = os.path.join(cdsroot, i)
    sp = i.split(".")[0]
    if sp in dic.keys():
        print(sp)
        for seq_record in SeqIO.parse(inpath, "fasta"):
            name = str(seq_record.id)
            if "|" in name:
                name = name.split("|")[0]
            length = len(seq_record.seq)
            sequences = str(seq_record.seq)
            if name in dic[sp].keys():
                gene = dic[sp][name]
                if length < minlen:
                    short.add(gene)
                seq = ">%s\n%s\n" % (sp, sequences)
                if gene not in dic2.keys():
                    dic2[gene] = [seq]
                else:
                    dic2[gene].append(seq)


for gene in dic2.keys():
    if gene not in short:
        outroot = os.path.join(sys.argv[-1], gene + suffix)
        with open(outroot, "w") as f:
            for line in dic2[gene]:
                f.write(line)
        

    
