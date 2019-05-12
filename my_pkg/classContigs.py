from bitstring import Bits
from bits_bases import base_to_bits
import config

k=config.k
trimsize=config.trimsize

print '\nkmer size='+str(k/2)
print 'trim size='+str(trimsize/2)

class Contigs:
    def __init__(self,file):
        self.contigs={}
        self.new_contigs={}
        with open(file) as file:
            for each in file.read().split(">")[1:]:
                if each.split('\n')[1]>trimsize/2:
                    self.contigs[each.split('\n')[0].split()[0]]=base_to_bits(each.split('\n')[1])

            
    def split_contig(self,name,side): #number of contigs
        if side=="LEFT":
            trim=self.contigs[name][:trimsize]
        if side=="RIGHT":
            trim=self.contigs[name][-trimsize:]
         
        self.kmers=[]
        for i in range(0,trimsize-k+2,2):
            self.kmers.append(trim[i:(i+k)])
        return self.kmers
        
    def update_new_contigs(self,used):
        for other in [other for other in used.keys() if other not in [item[0] for item in used.values()]]:
            name=other+"_"+used[other][0]
            seq=self.contigs[other][:-trimsize+used[other][2]]+self.contigs[used[other][0]][used[other][1]:]
            current=used[other][0]
            while current in used.keys():
                name=name+"_"+used[current][0]
                seq=seq[:-trimsize+used[current][2]]+self.contigs[used[current][0]][used[current][1]:]
                current=used[current][0]
            
            self.new_contigs[name]=seq
        
        
        for each in self.contigs:
            if each not in used.keys():
                if each not in [item[0] for item in used.values()]:
                    self.new_contigs[each]=self.contigs[each]

        self.contigs=self.new_contigs
        self.new_contigs={}
    
    def extend_contig(self,contig,start,extend):
        self.contigs[contig]=extend+self.contigs[contig][start:]


            