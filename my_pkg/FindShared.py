from bitstring import Bits
from RC import RC
import classContigs
import classReads
import config
import time

k=config.k

class FindShared():
    def __init__(self):
        None
    
    def contig_contig(self,class1):
        used={}
        for contig in class1.contigs:
            splits=class1.split_contig(contig,"LEFT")
            for other in [other for other in class1.contigs if other is not contig]:
                othersplits=class1.split_contig(other,"RIGHT")
                for each in splits:
                    if each in othersplits:
                        start=splits.index(each)*2
                        end=splits.index(each)*2-2+k-2
                        otherend=othersplits.index(each)*2+end-start
                        used[other]=(contig,end,otherend)
                        break #will break at ambiguities, fix later
                                                    
        class1.update_new_contigs(used)
        
    def contig_read(self,class1,class2,contig):
        class1.split_contig(contig,"LEFT")
        some_reads=None
        some_other_reads=None
        for each in class1.kmers: 
            if each in class2.kmers:
                start=class1.kmers.index(each)*2
                current=each
                some_reads=class2.kmers[each]
            if RC(each) in class2.kmers:
                start=class1.kmers.index(each)*2
                current=each
                some_other_reads=class2.kmers[RC(each)]
            if some_reads!=None or some_other_reads!=None:
                break
            
        NT={}
        if some_reads!=None:
            for name,pos,sign in some_reads: #rc=0 always
                pos=pos.uint
                if sign==Bits('0b1'):
                    nt=class2.reads[name][pos-2:pos]
                    if nt not in NT:
                        NT[nt]=1
                    else:
                        NT[nt]+=1
                else:
                    nt=RC(class2.reads[name][pos+k-2-2:pos+k-2])
                    if nt not in NT:
                        NT[nt]=1
                    else:
                        NT[nt]+=1
                                 
        
        if some_other_reads!=None:
            for name,pos,sign in some_other_reads: #rc=1 always
                pos=pos.uint
                if sign==Bits('0b1'):
                    nt=RC(class2.reads[name][pos+k-2-2:pos-k+2])
                    if nt not in NT:
                        NT[nt]=1
                    else:
                        NT[nt]+=1
                else:
                    nt=class2.reads[name][pos-2:pos]
                    if nt not in NT:
                        NT[nt]=1
                    else:
                        NT[nt]+=1
        
        new_nt=NT.keys()[NT.values().index(max(NT.values()))]
        current=new_nt+current[:-2]
        extend=new_nt   
        return start,extend,current
               
    def check_read(self,current,class2):
        some_reads=None
        some_other_reads=None
        if current in class2.kmers:
            some_reads=class2.kmers[current]
        if RC(current) in class2.kmers:
            some_other_reads=class2.kmers[RC(current)]
            
        return some_reads,some_other_reads
        
    def extend_reads(self,some_reads,some_other_reads,extend,current,class2):
        NT={}
        if some_reads!=None:
            for name,pos,sign in some_reads: #rc=0 always
                pos=pos.uint
                if sign==Bits('0b1'):
                    nt=class2.reads[name][pos-2:pos]
                    if nt not in NT:
                        NT[nt]=1
                    else:
                        NT[nt]+=1
                else:
                    nt=RC(class2.reads[name][pos+k-2-2:pos+k-2])
                    if nt not in NT:
                        NT[nt]=1
                    else:
                        NT[nt]+=1
                                 
        
        if some_other_reads!=None:
            for name,pos,sign in some_other_reads: #rc=1 always
                pos=pos.uint
                if sign==Bits('0b1'):
                    nt=RC(class2.reads[name][pos+k-2-2:pos+k-2])
                    if nt not in NT:
                        NT[nt]=1
                    else:
                        NT[nt]+=1
                else:
                    nt=class2.reads[name][pos-2:pos]
                    if nt not in NT:
                        NT[nt]=1
                    else:
                        NT[nt]+=1

                    
        new_nt=NT.keys()[NT.values().index(max(NT.values()))]
        current=new_nt+current[:-2]
        extend=new_nt+extend
        return current,extend


                    