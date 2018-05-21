import sys
import math

from blowfish_utils import *
from values import *

(P,S) = init(KEY)

try:
    filename = sys.argv[1]
except:
    filename = 'secret'

binFile = open(filename+'.bin', 'rb')
byteBlocks = binFile.read()
binFile.close()
msgBlocks = []

for i in range(0, math.ceil(len(byteBlocks)/8)):
    msgBlocks.append(int.from_bytes(byteBlocks[i*8:(i+1)*8], byteorder='big', signed=False))

for i in range(0, len(msgBlocks)):
    (xL, xR) = decrypt(msgBlocks[i]>>32 & 0xffffffff, msgBlocks[i] & 0xffffffff) 
    msgBlocks[i] = (xL << 32) + xR
    msgBlocks[i] = (msgBlocks[i]).to_bytes(length=8, byteorder='big', signed=False)

decryptedMessage = b''.join(msgBlocks)
print(decryptedMessage.decode('utf-8'))