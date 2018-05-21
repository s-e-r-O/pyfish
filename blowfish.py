import sys
import math

from constants import *
from values import *

lim = pow(2,32)
P = list(PI_P_ARRAY)
S = list(map(list,PI_S_BOXES))

def f(x):
    return ((((S[0][x >> 24] + S[1][x >> 16 & 0xff]) % lim) ^ S[2][x >> 8 & 0xff]) + S[3][x & 0xff]) % lim 

def encrypt(xL, xR):
    for i in range(0,16):
        xL = xL ^ P[i]
        xR = f(xL) ^ xR
        (xL, xR) = (xR, xL)
    (xL, xR) = (xR, xL)
    xR = xR ^ P[16]
    xL = xL ^ P[17]
    return (xL,xR)

def str2int(word):
    i = bytearray()
    i.extend(map(ord, word))
    return int.from_bytes(i, byteorder='big', signed=False)

def divideByBlocks(word, length):
    l = len(word)
    numBlocks = math.ceil(l/length)
    blocks = []
    for i in range(0, numBlocks):
        blocks.append(str2int(word[i*length: (i+1)*length]))

    if (l % length) != 0 :
        blocks[numBlocks-1] = blocks[numBlocks-1] << ((length - (l % length))*8)
    return (blocks, numBlocks)

def init(P, S, key):
    (keyBlocks, keylen) = divideByBlocks(key, 4)

    for i in range (0, 18):
        P[i] ^= keyBlocks[i % keylen]

    xL = xR = 0

    for i in range(0,18,2):
        (P[i],P[i+1]) = encrypt(xL, xR)
        (xL, xR) = (P[i],P[i+1])

    for i in range(0,4):
        for j in range(0, 256, 2):
            (S[i][j],S[i][j+1]) = encrypt(xL, xR)
            (xL, xR) = (S[i][j],S[i][j+1])
    return (P,S)

(P,S) = init(P, S, KEY)

# Not so sure about this

try:
    message = sys.argv[1]
except:
    message = MESSAGE

(msgBlocks, msglen) = divideByBlocks(message, 8)

for i in range(0, msglen):
    (xL, xR) = encrypt(msgBlocks[i]>>32 & 0xffffffff, msgBlocks[i] & 0xffffffff) 
    msgBlocks[i] = (xL << 32) + xR
    msgBlocks[i] = (msgBlocks[i]).to_bytes(length=8, byteorder='big', signed=False)

encryptedMessage = b''.join(msgBlocks)
print(hex(int.from_bytes(encryptedMessage, byteorder='big', signed=False)))

binFile = open('secret.bin', 'wb')
binFile.write(encryptedMessage)
binFile.close()
