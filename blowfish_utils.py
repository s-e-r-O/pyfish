import math

from constants import *

lim = pow(2,32)
P = list(PI_P_ARRAY)
S = list(map(list,PI_S_BOXES))

def f(x):
    return ((((S[0][x >> 24] + S[1][x >> 16 & 0xff]) % lim) ^ S[2][x >> 8 & 0xff]) + S[3][x & 0xff]) % lim 

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

def init(key):
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

def encrypt(xL, xR):
    for i in range(0,16):
        xL = xL ^ P[i]
        xR = f(xL) ^ xR
        (xL, xR) = (xR, xL)
    (xL, xR) = (xR, xL)
    xR = xR ^ P[16]
    xL = xL ^ P[17]
    return (xL,xR)

def decrypt(xL, xR):
    for i in range(16, 0, -2):
        xL ^= P[i+1]
        xR ^= f(xL)
        xR ^= P[i]
        xL ^= f(xR)
    xL ^= P[1]
    xR ^= P[0]
    (xL, xR) = (xR, xL)
    return (xL, xR)
