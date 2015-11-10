#/usr/bin python

import struct

def uint1(stream):
    return ord(stream.read(1))

def uint2(stream):
    return struct.unpack('H', stream.read(2))[0]

def uint4(stream):
    return struct.unpack('I', stream.read(4))[0]

def uint8(stream):
    return struct.unpack('Q', stream.read(8))[0]

def hash32(stream):
    return stream.read(32)[::-1]

def time(stream):
    time = uint4(stream)
    return time

def varint(stream):
    size = uint1(stream)

    if size < 0xfd:
        return size
    if size == 0xfd:
        return uint2(stream)
    if size == 0xfe:
        return uint4(stream)
    if size == 0xff:
        return uint8(stream)
    return -1

def hashStr(bytebuffer):
    return ''.join(('%x'%ord(a)) for a in bytebuffer)
    
def main():
    #block2file('1M.dat')
    try:
        blockfile = open('1M.dat', 'rb')
    except IOError as detail:
        raise Exception("Could not open"+ blockfile, detail)
    
    print "Magic Number:\t %8x" % uint4(blockfile)
    print "Blocksize:\t %u" % uint4(blockfile)

    """Block Header"""
    print "Version:\t %d" % uint4(blockfile)
    print "Previous Hash\t %s" % hashStr(hash32(blockfile))
    print "Merkle Root\t %s" % hashStr(hash32(blockfile))
    print "Time\t\t %s" % str(time(blockfile))
    print "Difficulty\t %8x" % uint4(blockfile)
    print "Nonce\t\t %s" % uint4(blockfile)
    
    print "Tx Count\t %d" % varint(blockfile)
    
    print "Version Number\t %s" % uint4(blockfile)
    print "Inputs\t\t %s" % varint(blockfile)
    print "Previous Tx\t %s" % hashStr(hash32(blockfile))
    print "Prev Index \t %d" % uint4(blockfile)
    script_len = varint(blockfile)
    print "Script Length\t %d" % script_len
    script_sig = blockfile.read(script_len)
    print "ScriptSig\t %s" % hashStr(script_sig)
    print "ScriptSig\t %s" % hashStr(script_sig).decode('hex')
    print "Seq Num\t\t %8x" % uint4(blockfile)

    print "Outputs\t\t %s" % varint(blockfile)
    print "Value\t\t %s" % str((uint8(blockfile)*1.0)/100000000.00)
    script_len = varint(blockfile)
    print "Script Length\t %d" % script_len
    script_pubkey = blockfile.read(script_len)
    print "Script Pub Key\t %s" % hashStr(script_pubkey)
    print "Lock Time %8x" % uint4(blockfile)
    print

if __name__ == "__main__":
    main()
