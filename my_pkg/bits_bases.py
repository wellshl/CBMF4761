from bitstring import Bits

def base_to_bits(seq):
    binary={'T':'0b01','C':'0b00','A':'0b10','G':'0b11'}
    bases=list(seq)
    bases=''.join([binary[base] for base in bases])
    return Bits(bases)

def bits_to_base(bits):
    binary={'0b01':'T','0b00':'C','0b10':'A','0b11':'G','0b1':'T',True:'T',False:'C'}
    bases=''.join([binary[str(bits[i:i+2])] for i in range(0,len(bits),2)])
    return bases