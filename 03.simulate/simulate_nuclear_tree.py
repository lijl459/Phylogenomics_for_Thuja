#! /usr/bin/env python3.6
# -*- coding: utf-8 -*-

import dendropy
from dendropy.simulate import treesim


sp_tree_str = """\
[&R] (Tdol:8.196921,((Tsut:1.052324,Tst:1.052324):0.144597,(Tpli:1.085143,(Tko:1,Toc2:1):0.085143):0.111778):7.000000);
"""

sp_tree = dendropy.Tree.get(data=sp_tree_str, schema="newick")
gene_to_species_map = dendropy.TaxonNamespaceMapping.create_contained_taxon_mapping(
        containing_taxon_namespace=sp_tree.taxon_namespace,
    num_contained=1)
with open("simulated.trees", "w") as f:
    for i in range(2969):
        gene_tree = treesim.contained_coalescent_tree(containing_tree=sp_tree, gene_to_containing_taxon_map=gene_to_species_map)
        outtre = str(gene_tree.as_string(schema='newick'))
        outtre = outtre.replace("[&R] ", "")
        outtre = outtre.replace("_1:", ":")
        f.write(outtre)


#print(gene_tree.as_ascii_plot())
