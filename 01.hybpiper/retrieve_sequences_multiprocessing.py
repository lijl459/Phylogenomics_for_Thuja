#!/usr/bin/env python
import sys,os
from Bio import SeqIO
import multiprocessing

helptext = '''Usage: 
    python retrieve_sequences.py baitfile.fasta sequence_dir aa/dna/intron/supercontig num_cores

This script will get the sequences generated from multiple runs of the HybSeqPipeline (reads_first.py).
Have all of the runs in the same directory (sequence_dir). 
It retreives all the gene names from the bait file used in the run of the pipeline.

You must specify whether you want the protein (aa) or nucleotide (dna) sequences.
You can also specify 'intron' to retreive the intron sequences, 
or 'supercontig' to get intron and exon sequences.

Will output unaligned fasta files, one per gene, to current directory.
'''


#for gene in target_genes:

def retrieve_sequences(gene):
    gene_seqs = []
    for rec in gene_seqs:
        rec.id = rec.id.split("-")[0]
        rec.description = ''
    for sample in sample_names:
        if seq_dir == 'intron':
            sample_path = os.path.join(sampledir,sample,gene,sample,'sequences',seq_dir,"{}_{}.fasta".format(gene,filename))
        else:
            sample_path = os.path.join(sampledir,sample,gene,sample,'sequences',seq_dir,gene+'.'+seq_dir)
        if os.path.isfile(sample_path):
            gene_seqs.append(SeqIO.read(sample_path,'fasta'))
    print("Found {} sequences for {}.".format(len(gene_seqs),gene))
    
    if seq_dir == 'intron':
        outfilename = "{}_{}.fasta".format(gene,filename)
    else:
        outfilename = gene + '.' + seq_dir
    
    SeqIO.write(gene_seqs,open(outfilename,'w'),'fasta')

if __name__ == "__main__":

    if len(sys.argv) < 4:
        print(helptext)
        sys.exit(1)

    if sys.argv[3] == 'dna':
        seq_dir = "FNA"
    elif sys.argv[3] == 'aa':
        seq_dir = "FAA"
    elif sys.argv[3] == 'intron':
        seq_dir = 'intron'
        filename = 'introns'
    elif sys.argv[3] == 'supercontig':
        seq_dir = 'intron'
        filename = 'supercontig'

    else:
        print(helptext)
        sys.exit(1)    

    #Use gene names parsed from a bait file.
    baitfile = sys.argv[1]
    target_genes_dict = SeqIO.to_dict(SeqIO.parse(baitfile,'fasta'))
    target_genes = list(set([x.id.split('-')[-1] for x in SeqIO.parse(baitfile,'fasta')]))

    sampledir = sys.argv[2]
    sample_names = [x for x in os.listdir(sampledir) if os.path.isdir(os.path.join(sampledir,x)) and not x.startswith('.')]
    
    
    print("Retreiving {} genes from {} samples".format(len(target_genes),len(sample_names)))
    
    # Retrieve sequences to parallel
    if len(sys.argv) == 5:
        num_cores = int(sys.argv[4])
    else:
        num_cores = 6

    items = target_genes
    p = multiprocessing.Pool(num_cores)
    b = p.map(retrieve_sequences, items)
    p.close()
    p.join()
    
