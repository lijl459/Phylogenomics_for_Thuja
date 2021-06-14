#!/usr/bin/env python
import sys, re, os
from Bio import SeqIO

if len(sys.argv) != 4:
    print("Usage: <Script> <in_root> <out_root> <minimum_sp>")
    exit()

k = re.compile("\s+")

inroot = sys.argv[1]
outroot = sys.argv[2]
nsp = int(sys.argv[3])

for i in sorted(os.listdir(inroot)):
    inpath = os.path.join(inroot, i)
    lst = []
    a = 0
    b = 0
    c = 0
    if i.endswith(".fasta") or i.endswith(".fa") or  i.endswith(".fas"):
        count = 0
        for seq_record in SeqIO.parse(inpath, "fasta"):
            name = str(seq_record.id)
            length = len(seq_record.seq)
            sequences = str(seq_record.seq)
            missing = sequences.count("-")
            n = length - missing 
            if missing > length/2:
                pass
            elif n < 300:
                pass
            else:
                a += 1
                lst.append(seq_record)
        if a > nsp:
            outname = i.split(".")[0] + ".filtered.fas"
            outname =  os.path.join(outroot, outname)
            SeqIO.write(lst, outname, "fasta")

        

    
