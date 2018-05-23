# -*- coding: UTF-8 -*-

import getopt, sys
import math
import argparse

from pyfish_utils import *
from values import *

# usage: pyfish_encrypt.py [--message=message] [--output=output] [--test=testfile]
# usage: pyfish_encrypt.py [-m message] [-o output] [-t testfile]

def main(arg_message, arg_output, arg_test):
    if (arg_message != None):
        message = arg_message
    else:
        message = MESSAGE
    
    if (arg_test != None):
        test = True
        testFile = open(arg_test, 'r')
        message = testFile.read()
        testFile.close()
    else:
        test = False
    
    if (arg_output != None):
        filename = arg_output
    else:
        filename = 'secret'

    (P,S) = init(KEY)

    (msgBlocks, msglen) = divideByBlocks(message, 16)

    for i in range(0, msglen):
        (xL, xR) = encrypt(msgBlocks[i]>>64 & 0xffffffffffffffff, msgBlocks[i] & 0xffffffffffffffff) 
        msgBlocks[i] = (xL << 64) + xR
        msgBlocks[i] = (msgBlocks[i]).to_bytes(length=16, byteorder='big', signed=False)

    encryptedMessage = b''.join(msgBlocks)

    if (not test):
        binFile = open(filename+'.bin', 'wb')
        binFile.write(encryptedMessage)
        binFile.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--message')
    parser.add_argument('-o', '--output')
    parser.add_argument('-t', '--test')
    args = parser.parse_args()
    main(args.message, args.output, args.test)