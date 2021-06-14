#!/usr/bin/python
import sys, os, re
from ete3 import Tree

if len(sys.argv) != 3:
    print("Usage: <script> <inroot> <outfile>")
    exit()

inroot = sys.argv[1]
outroot = sys.argv[2]

sptree = "(Tdol:8.264,((Tpli:1.131069,(Tko:1,Toc2:1):0.131069):0.132931,(Tsut:1.069682,Tst:1.069682):0.194318):7.000000);"
sptree =  Tree(sptree)
#root_point = sptree.get_leaves_by_name(outgroup)[0]
#chltree.set_outgroup(root_point)
#print(chltree)

outfile = open(outroot, "w")
outfile.write("RF\tFrequency\n")

for name in os.listdir(inroot):
    treeroot = os.path.join(inroot, name, "simulated.rr.trees")
    if os.path.isfile(treeroot):
        dic = {}
        count = 0
        with open(treeroot) as infile:
            for line in infile:
                count += 1
                tree = Tree(line)
                rf = sptree.robinson_foulds(tree)[0]
                if rf in dic.keys():
                    dic[rf] += 1
                else:
                    dic[rf] = 1

        for rf in dic.keys():
            outfile.write("%d\t%f\n" % (rf, float(dic[rf])/count))




        
