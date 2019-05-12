from bitstring import Bits

def RC(read):
    complement={'0b01':'0b10','0b10':'0b01','0b00':'0b11','0b11':'0b00',True:False,False:True,'0b0':'0b11','0b1':'0b10'}
    rc=''
    if type(read)!=bool:
        for i in range(0,len(read),2):
            rc=complement[str(read[i:i+2])]+rc
        return Bits(rc)
    else:
        return Bits(complement[read])