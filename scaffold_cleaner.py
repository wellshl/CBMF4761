#!/usr/bin/python
import argparse
import time

parser=argparse.ArgumentParser(description='scaffold_cleaner')
parser.add_argument('-r','--reads',required=True)
parser.add_argument('-c','--contigs',required=True)
parser.add_argument('-k','--kmer',type=int)
parser.add_argument('-t','--trim',type=int)
parser.add_argument('-f','--outfile',type=str)
args=parser.parse_args()

with open('my_pkg/config.py','w') as in_handle:
	if args.kmer:
		in_handle.write('k='+str(args.kmer*2)+'\n')
	else:
		in_handle.write('k=31*2'+'\n')

	if args.trim:
		in_handle.write('trimsize='+str(args.trim*2))
	else:
		in_handle.write('trimsize=200*2')
	in_handle.close()

import my_pkg

start=time.time()
contigs=my_pkg.classContigs.Contigs(args.contigs)
end=time.time()
print "Time to load contigs: "+str(end-start)

start=time.time()
reads=my_pkg.classReads.Reads(args.reads)
end=time.time()
print "Time to load reads: "+str(end-start)

def scaffold_cleaner(args):


	my_pkg.FindShared.FindShared().contig_contig(contigs)

	for contig in contigs.contigs:
	    start,extend,current=my_pkg.FindShared.FindShared().contig_read(contigs,reads,contig)
	    check=my_pkg.FindShared.FindShared().check_read(current,reads)
	    while check[0]!=None or check[1]!=None:
	        current,extend=my_pkg.FindShared.FindShared().extend_reads(check[0],check[1],extend,current,reads)
	        check=my_pkg.FindShared.FindShared().check_read(current,reads)
	    contigs.extend_contig(contig,start,extend)
	    
	my_pkg.FindShared.FindShared().contig_contig(contigs)

start=time.time()
scaffold_cleaner(args)
end=time.time()
print 'Time to assemble: '+str(end-start)

if args.outfile:
	my_pkg.write_fasta.write_file(contigs.contigs,args.outfile)
else:
	for name,seq in contigs.contigs.items():
		print ">"+name+"\n"+my_pkg.bits_bases.bits_to_base(seq)


