#!/usr/bin/env python
import os, sys, re
from Bio import SeqIO
from Bio.Seq import Seq

if len(sys.argv) != 4:
    print("Usage: <Script> <input_fna_dir> <out_fna_dir> <out_faa_dir>")
    exit()

inroot = sys.argv[1]
fnadir = sys.argv[2]
faadir = sys.argv[3]
stop_codon = ["TAG", "TAA", "TCA"]
k = re.compile("\*")


try:
    os.mkdir(fnadir)
    os.mkdir(faadir)
except:
    pass

for name in os.listdir(inroot):
    if name.endswith(".FNA") or name.endswith(".fas"):
        inpath = os.path.join(inroot, name)
        lst = []
        lst2 = []
        gene = "_".join(name.split(".")[:-1])
        dnafile = open(os.path.join(fnadir, gene + ".fas"), "w")
        aafile = open(os.path.join(faadir, gene + ".fas"), "w")

        for seq_record in SeqIO.parse(inpath, "fasta"):
            seqname = seq_record.id
            cds_seq = seq_record.seq
            if len(cds_seq) % 3 != 0:
                print(name, seqname)
                continue
            pep_seq = cds_seq.translate(table=11)
            sites = []
            results = re.finditer(k, str(pep_seq)[:-1])
            m = 0
            n = 0
            dnaseq = ""
            aaseq = ""
            check = [i for i in results]
            if len(check) == 0:
                dnaseq = cds_seq
                aaseq = pep_seq
            else:
                for result in check:
                    a = result.span()
                    dnaseq += cds_seq[m:a[0]*3]
                    aaseq += pep_seq[n:a[0]]
                    n = a[1]
                    m = a[1]*3
                dnaseq += cds_seq[m:len(cds_seq)]
                aaseq += pep_seq[n:len(pep_seq)]
            dnafile.write(">%s\n%s\n" % (seqname, dnaseq))
            aafile.write(">%s\n%s\n" % (seqname, aaseq))
        dnafile.close()
        aafile.close()
            
                    
                
            
