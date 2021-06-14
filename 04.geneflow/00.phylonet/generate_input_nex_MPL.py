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
    outfile.write("BEGIN PHYLONET;\nInferNetwork_MPL (all) %d  -a <Tdolabrata: RBGE-L-34, Tdol;Tsutchuenensis: Tsut, YB20-03-1, SW-ZML-201749-1; Tstandishii: RBGE-L-33, E00131707, Tst; Tplicata: RBGE-L-32, 19861190A1, Tpli, E00311657; Toccidentalis: E00312456, E00312386, 19850753AA, Toc2; Tkoraiensis: RBGE-L-31, Tko, 20150776A, E00420068>  -pl 6  -di;\nEND;" % n)

print("java -jar /data/soft/PhyloNet/PhyloNet_3.8.2.jar %s >%s.out" % (sys.argv[2], sys.argv[2]))    
