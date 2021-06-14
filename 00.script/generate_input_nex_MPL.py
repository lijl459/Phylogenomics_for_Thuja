#!/usr/bin/env python
import os, sys, re

if len(sys.argv) != 4:
    print("Usage: <Script> <intree> <out_nexus> <num of reticulations>")
    exit()
n = int(sys.argv[-1])

with open(sys.argv[2], "w") as outfile:
    s = "#NEXUS\n\nBEGIN TREES;\n"
    outfile.write(s)
    title = "Tree gt%d = %s"
    count = -1
    with open(sys.argv[1]) as f:
        for line in f:
            count += 1
            outfile.write(title % (count, line))
    outfile.write("\nEND;\n\n")
    outfile.write("BEGIN PHYLONET;\nInferNetwork_MPL (all) %d -pl 5  -di;\nEND;" % n)

print("java -jar /data/soft/PhyloNet/PhyloNet_3.8.2.jar %s >%s.out" % (sys.argv[2], sys.argv[2]))    
