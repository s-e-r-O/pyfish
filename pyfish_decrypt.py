# -*- coding: UTF-8 -*-

import sys
import math

from pyfish_utils import *
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

for i in range(0, math.ceil(
    len(byteBlocks)/16)):
    msgBlocks.append(int.from_bytes(byteBlocks[i*16:(i+1)*16], byteorder='big', signed=False))

for i in range(0, len(msgBlocks)):
    (xL, xR) = decrypt(msgBlocks[i]>>64 & 0xffffffffffffffff, msgBlocks[i] & 0xffffffffffffffff) 
    msgBlocks[i] = (xL << 64) + xR
    msgBlocks[i] = (msgBlocks[i]).to_bytes(length=16, byteorder='big', signed=False)

decryptedMessage = b''.join(msgBlocks)
try:
    print(decryptedMessage.decode('utf-8'))
except:
    try:
        print(decryptedMessage.decode('latin-1'))
    except:
        print('Weird characters found. :(')