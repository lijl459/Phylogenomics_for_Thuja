#!/usr/bin/env python
import re, sys, os
from Bio import SeqIO
from ete3 import Tree

if len(sys.argv) != 6:
    print("Usage: <script> <in fasta> <sptree> <indlist> <outgroup> <out_root>")
    exit()

inpath = sys.argv[1]
outroot = sys.argv[-1]

k = re.compile("\s+")
sp2ind = {}
ind2sp = {}
splist = []
O = sys.argv[4]

with open(sys.argv[2]) as f:
    sptree = Tree(f.read())
root_point = sptree.get_leaves_by_name(O)[0]
sptree.set_outgroup(root_point)

with open(sys.argv[3]) as f:
    for line in f:
        l = k.split(line)
        name = l[0]
        sp = l[1]
        if sp not in sp2ind:
            sp2ind[sp] = []
            splist.append(sp)
        sp2ind[sp].append(name)
        ind2sp[name] = sp

splist.remove(O)

dic = {}
for sp in splist:
    dic[sp] = []
dic[O] = []
for seq_record in SeqIO.parse(inpath, "fasta"):
    name = str(seq_record.id)
    sp = ind2sp[name]
    sequences = str(seq_record.seq)
    seq_record.id = ind2sp[name]
    dic[sp].append(seq_record)

n = len(splist)
lst = []

for a in range(n):
    for b in range(n):
        for c in range(n):
            if c > b and b > a:
                sp1 = splist[a]
                sp2 = splist[b]
                sp3 = splist[c]
                anc12 = sptree.get_common_ancestor([sp1, sp2])
                anc13 = sptree.get_common_ancestor([sp1, sp3])
                anc23 = sptree.get_common_ancestor([sp2, sp3])
                if sp3 not in anc12:
                    lst.append([sp1, sp2, sp3])
                if sp2 not in anc13:
                    lst.append([sp1, sp3, sp2])
                if sp1 not in anc23:
                    lst.append([sp2, sp3, sp1])


for triple in lst:
    outname = "-".join(triple) + ".fas"
    outpath = os.path.join(outroot, outname)
    seqlist = []
    p1 = triple[0]
    p2 = triple[1]
    p3 = triple[2]
    seqlist = dic[p1] + dic[p2] + dic[p3] + dic[O]
    SeqIO.write(seqlist, outpath, "fasta")


    
    
