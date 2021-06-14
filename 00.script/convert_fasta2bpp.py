#!/usr/bin/env python
import sys, re, os
from Bio import SeqIO

if len(sys.argv) != 3:
    print("Usage: <Script> <in_root> <out_nex>")
    exit()

k = re.compile("\s+")

inroot = sys.argv[1]
outroot = sys.argv[-1]
splist = []

outfile = open(outroot, "w")

for i in sorted(os.listdir(inroot)):
    if i.endswith(".fas"):
        inpath = os.path.join(inroot, i)
        geneName = i.split(".")[0]
        dic = {}
        count = 0
        s = ""
        for seq_record in SeqIO.parse(inpath, "fasta"):
            sp = str(seq_record.id)
            count += 1
            sequences = str(seq_record.seq)
            seqLen = len(sequences)
            spinfo = geneName + "^" + sp
            spinfo = spinfo + " "*(50-len(spinfo))
            outline = spinfo + sequences + "\n"
            s += outline
        s = "\n" + s + "\n"
        outfile.write("%d %d\n" % (count, seqLen))
        outfile.write(s)
outfile.close()
