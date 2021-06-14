#!/usr/bin/python
# by Lijl

import sys, os
if len(sys.argv) != 2:
    print('Usage: <Script> <inroot> > output')
    exit()
inroot = sys.argv[1]
#outroot = sys.argv[2]

lst1 = []
lst2 = []
dic = {}
for name in os.listdir(inroot):
    if name.endswith(".txt") or name.endswith(".out"):
        inpath = os.path.join(inroot, name)
        with open(inpath) as f:
            for line in f:
                if "Total log probability:" in line:
                    lst1.append(name)
                    lst2.append(float(line.split(":")[1]))
                    dic[name] = float(line.split(":")[1])
                    break


print(lst2)
max_value = max(lst2)
#i = lst2.index(max_value)

for value in sorted(lst2)[::-1]:
    i = lst2.index(value)
    print(lst1[i], value)
