DESCRIPTION:

A program that "cleans" contig scaffolds into a single contig or as few contigs as possible using short-read data. Designed for input directly from a de novo assembly pipeline. Requires forward-oriented contigs and reads that were unused in the assembly.

=======================================================================================================================
SYSTEM REQUIREMENTS:

*****CODE MUST BE RUN USING PYTHON 2.7*****
The Bitstring package (https://pythonhosted.org/bitstring/index.html) and the Python standard library

Before running, execute the following inside the CBMF4761 directory so the package modules will load:
export PYTHONPATH=$PWD

The program is able to handle fastq files with millions of reads but will perform very slowly. Usage for large and small files is the same.

=======================================================================================================================
INPUT:

A FASTA file containing the contigs to be assembled
A FASTQ.GZ file containing gzipped unused reads after de novo assembly

=======================================================================================================================
OUTPUT:

Optimized contigs in FASTA format

=======================================================================================================================
USAGE:

Required:
-c contigs 	[a FASTA file containing contigs of the scaffold in any order]
-r reads 	[a FASTQ.GZ file containing reads AFTER SUBTRACTION from mapping to the contigs]

Optional:
-k kmer		[an integer value to be used for the kmer size, must be odd. default, 31]
-f outfile	[a filename to which the output should be written. default, print to STDOUT]
-t trim size	[an integer value to be used for the contig trimming size. default, 200]

=======================================================================================================================
EXAMPLES:

Run with default value of k and print to stdout:
python scaffold_cleaner.py -c test_contigs.fasta -r test_reads.fastq

Run with specified value of k and t and write to out_file:
python scaffold_cleaner.py -c test_contigs.fasta -r test_reads.fastq -k 51 -t 250 -f out_file.fasta