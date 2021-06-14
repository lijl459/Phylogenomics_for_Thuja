import sys, os
#inroot = sys.argv[1]
#outroot = sys.argv[2]

dname = {}
dprob = {}
dic1 = {}
dic2 = {}
for ret in os.listdir("."):
    if ret.startswith("H"):
        dname[ret] = []
        dprob[ret] = []
        if ret not in dic1:
            dic1[ret] = {}
        if ret not in dic2:
            dic2[ret] = {}
        for name in os.listdir(ret):
            if name.endswith(".txt") or name.endswith(".out"):
                inpath = os.path.join(ret, name)
                dname[ret].append(name)
                with open(inpath) as f:
                    count = 0
                    a = 0
                    for line in f:
                        count += 1
                        if "Inferred Network #1:" in line:
                            a = count
                        if a != 0:
                            n1 = a + 1
                            n2 = a + 2
                            n3 = a + 3
                            if count == n1:
                                dic1[ret][name] = line
                            elif count == n2:
                                dprob[ret].append(float(line.split(":")[1]))
                            elif count == n3:
                                tree = line.split(": ")[1]
                                dic2[ret][name] = tree

# ret, name, prob
d = {}
if not os.path.exists("results"):
    os.mkdir("results")
os.chdir("results")

for ret in dname.keys():
    max_value = max(dprob[ret])
    i = dprob[ret].index(max_value)
    name = dname[ret][i]
    d[ret] = [name, max_value]
    with open("phylonet." + ret+".bl.tre", "w") as f:
        f.write(dic1[ret][name].strip(" "))
    with open("phylonet." +ret+".Dendroscope.tre", "w") as f:
        f.write(dic2[ret][name].strip(" "))

with open("best_run.txt", "w") as f:
    f.write("ret\trunName\tlog_prob\n")
    for ret in sorted(d):
        line = "%s\t%s\t%f\n"
        f.write(line % (ret, d[ret][0], d[ret][1]))
