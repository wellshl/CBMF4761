from bitstring import Bits
from RC import RC
from bits_bases import base_to_bits
import config
import gzip

k=config.k

class Reads:
    def __init__(self,file):
        self.reads={}
        self.kmers={}
        with gzip.open(file,'r') as file: 
            split=file.read().split('\n')
            index=1
            for i in range(1,len(split)-3,4):
                seq=split[i]
                if not set(list(seq)).intersection(['N','M','K','R','Y','W','S','V','B','H','D']):
                    seq=base_to_bits(seq)
                    name=Bits(uint=index,length=25) #will store up to 20 million reads
                    self.reads[name]=seq 
                    index+=1
                    
                    for i in range(0,len(seq)-k+2,2):
                        kmer=seq[i:(i+k)]
                        if str(kmer[(k+2)/2:(k+2)/2+2]) in ['0b00','0b01']:
                            if kmer in self.kmers: 
                                self.kmers[kmer].append((name,Bits(uint=i,length=8),Bits('0b1'))) #will store up to 100 positions
                            else:
                                self.kmers[kmer]=[(name,Bits(uint=i,length=8),Bits('0b1'))]
                        else:
                            if RC(kmer) not in self.kmers:
                                self.kmers[RC(kmer)]=[(name,Bits(uint=i,length=8),Bits('0b0'))]
                            else:
                                self.kmers[RC(kmer)].append((name,Bits(uint=i,length=8),Bits('0b0')))

                        