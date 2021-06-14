#!/usr/bin/python
import sys, os, re
from ete3 import Tree

if len(sys.argv) != 4:
    print("Usage: <script> <intrees> <namelist.txt> <outfile>")
    exit()

inroot = sys.argv[1]
outroot = sys.argv[-1]

dic = {}

k = re.compile("\s+")
with open(sys.argv[2]) as f:
    for line in f:
        l = k.split(line)
        dic[l[0]] = l[1]


st = set()
with open(outroot, "w") as outfile:
    with open(inroot) as infile:
        for line in infile:
            tree = Tree(line)
            leaves = tree.get_leaf_names()
            for leaf in leaves:
                st.add(leaf)

    for name in sorted(st):
        sp = name.split("@")[0]
        outfile.write(name + "\t" + dic[sp] + "\n")
