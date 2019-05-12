import bits_bases

def write_file(contigs,filename):
	with open(filename,'w') as out_handle:
		for name,seq in contigs.items():
			out_handle.write(">"+name+"\n"+bits_bases.bits_to_base(seq))
