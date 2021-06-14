#! /usr/bin/env python3.6
# -*- coding: utf-8 -*-

import dendropy
from dendropy.simulate import treesim


sp_tree_str = """\
[&R] (Tdol:16.528,((Tpli:2.262138,(Tko:2.0,Toc2:2.0):0.262138):0.265862,(Tsut:2.139364,Tst:2.139364):0.388636):14.0);
"""

sp_tree = dendropy.Tree.get(data=sp_tree_str, schema="newick")
gene_to_species_map = dendropy.TaxonNamespaceMapping.create_contained_taxon_mapping(
        containing_taxon_namespace=sp_tree.taxon_namespace,
    num_contained=1)
with open("simulated.trees", "w") as f:
    for i in range(20000):
        gene_tree = treesim.contained_coalescent_tree(containing_tree=sp_tree, gene_to_containing_taxon_map=gene_to_species_map)
        outtre = str(gene_tree.as_string(schema='newick'))
        outtre = outtre.replace("[&R] ", "")
        outtre = outtre.replace("_1:", ":")
        f.write(outtre)


#print(gene_tree.as_ascii_plot())
