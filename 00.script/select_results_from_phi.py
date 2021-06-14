#!/usr/bin/python
import sys, os
if len(sys.argv) != 5:
    print("Usage: <script> <pi_root> <seq_root> <tree_root> <work_dir>")
    exit()

inroot = sys.argv[1]
seqroot = sys.argv[2]
treeroot = sys.argv[3]
workdir = sys.argv[4]


os.chdir(workdir)

if not os.path.exists("sequences"):
    os.mkdir("sequences")
if not os.path.exists("trees"):
    os.mkdir("trees")
 
outline = "%s\t%f\n"
genelist = []
with open("phi.results", "w") as outfile:
    for name in os.listdir(sys.argv[1]):
        if name.endswith(".result"):
            inpath = os.path.join(inroot, name)
            gene = name.split(".")[0]
            with open(inpath) as f:
                s = f.read()
                p = s.split(":")[-1]
                if "--" in p:
                    pass
                else:
                    p = float(p)
                    if p > 0.05:
                        genelist.append(gene)
                        outfile.write(outline % (gene, p))

for name in os.listdir(seqroot):
    gene = name.split(".")[0]
    if gene in genelist:
        seqpath = os.path.join(seqroot, name)
        outpath = os.path.join("sequences", name)
        with open(outpath, "w") as outfile:
            with open(seqpath) as infile:
                f = infile.read()
                outfile.write(f)

for name in os.listdir(treeroot):
    gene = name.split(".")[0]
    if gene in genelist and name.endswith("treefile"):
        treepath = os.path.join(treeroot, name)
        outpath = os.path.join("trees", name)
        with open(outpath, "w") as outfile:
            with open(treepath) as infile:
                f = infile.read()
                outfile.write(f)

    
