#library(phybase);
require("ape")
library("gplots")

#setwd("E:\\?????????\\project\\Thuja\\DensiTree")

genetree <- read.tree(file = "iqtree.rr.zero.tre")
#sptree <- read.tree(text = mptree1)

for (tree in genetree){
  outgroup <- match(c("Tdol"),tree$tip.label)
  tree.rooted <- root(tree,outgroup,node = NULL)
  if (is.binary(tree)) {
    tree.rooted.ultra <- chronopl(tree, 1, 
                                  age.min = 62.68, age.max = NULL,
                                  node = "root", S = 1, tol = 1e-8,
                                  CV = FALSE, eval.max = 500, iter.max = 500)
    write.tree(tree.rooted.ultra, file = "iqtrees.rr.zero.ultra.tre", append = TRUE)
  }

}

