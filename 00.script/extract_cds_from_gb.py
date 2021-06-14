#!/usr/bin/env python
import os, sys
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.Alphabet import IUPAC

if len(sys.argv) != 4:
    print("Usage: <Script> <gb_dir> <outroot> <number of species>")
    exit()

gb_dir = str(sys.argv[1])
outroot = sys.argv[2]
nsp = int(sys.argv[3])

specieslist = []
cds_dic = {}
pep_dic = {}
multicopy = []
gene_set = set()
d = {}

for gb_name in os.listdir(gb_dir):
    if gb_name.endswith('.gb'):
        species = gb_name[:-3]
        d[species] = []
        specieslist.append(species)
        gb_file = os.path.join(gb_dir, gb_name)
        gb_seq = SeqIO.read(gb_file, "genbank")
        complete_seq = gb_seq.seq
        genelist = []
        for ele in gb_seq.features:
            if ele.type == "CDS":
                cds_seq = ""
                gene = ele.qualifiers['gene'][0]
                for ele1 in ele.location.parts:
                    if ele1.strand == -1:
                        cds_seq += complete_seq[ele1.start:ele1.end].reverse_complement()
                    else:
                        cds_seq += complete_seq[ele1.start:ele1.end]
                pep_seq = cds_seq.translate()
                #translation = ele.qualifiers['translation'][0]
                if gene in genelist:
                    multicopy.append(gene)
                if gene not in cds_dic.keys():
                    cds_dic[gene] = []
                    pep_dic[gene] = []
                cds = ">%s\n%s" % (species, str(cds_seq))
                pep = ">%s\n%s" % (species, str(pep_seq))
                cds_dic[gene].append(cds)
                pep_dic[gene].append(pep)
                d[species].append(gene)
                genelist.append(gene)

L = []

for i in  sorted(d.keys()):
    L.append(sorted(d[i]))
    if len(d[i]) == 0:
        print(i)


from functools import reduce
lset = reduce(lambda x,y:set(x) & set(y), L)

n = 0
for i in lset:
    if i not in multicopy:
        n += 1

print("N of shared gene is: ", len(lset))
print("N of shared single copy gene is: ", n)

pepdir = os.path.join(outroot, "pep")
cdsdir = os.path.join(outroot, "cds")

if not os.path.exists(pepdir):
    os.mkdir(pepdir)
if not os.path.exists(cdsdir):
    os.mkdir(cdsdir)


for gene in sorted(cds_dic.keys()):
    if len(cds_dic[gene]) == nsp:
        cdsfile = open(os.path.join(cdsdir, gene + ".cds.fas"), "w")
        pepfile = open(os.path.join(pepdir, gene + ".pep.fas"), "w")
        cdsfile.write("\n".join(cds_dic[gene]))
        pepfile.write("\n".join(pep_dic[gene]))
        cdsfile.close()
        pepfile.close()

