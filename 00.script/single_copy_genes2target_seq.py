#!/usr/bin/env python
import sys, re, os
from Bio import SeqIO

if len(sys.argv) != 3:
    print("Usage: <Script> <in_root> <out_file>")
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
            sequences = str(seq_record.seq)
            seqLen = len(sequences)
            head = ">%s-%s\t%d\n" % (sp, geneName, seqLen)
            outfile.write(head)
            outfile.write(sequences + "\n")
outfile.close()
