# -*- coding: UTF-8 -*-

import sys
import math

from blowfish_utils import *
from values import *

(P,S) = init(KEY)

try:
    message = sys.argv[1]
except:
    message = MESSAGE
    
try:
    filename = sys.argv[2]
except:
    filename = 'secret'

(msgBlocks, msglen) = divideByBlocks(message, 8)

#print(msgBlocks)

for i in range(0, msglen):
    (xL, xR) = encrypt(msgBlocks[i]>>32 & 0xffffffff, msgBlocks[i] & 0xffffffff) 
    msgBlocks[i] = (xL << 32) + xR
    msgBlocks[i] = (msgBlocks[i]).to_bytes(length=8, byteorder='big', signed=False)

encryptedMessage = b''.join(msgBlocks)
#print(hex(int.from_bytes(encryptedMessage, byteorder='big', signed=False)))

binFile = open(filename+'.bin', 'wb')
binFile.write(encryptedMessage)
binFile.close()

#print(msgBlocks)