import os
import argparse

def main(message, blowfish, decrypt):
    if (message != None):
        msg = message
    else:
        msg = 'CHEWBACCA GUSTA DE CHUÑO Y CHICLES EN LLUVIA FRESCA'
    if (blowfish):
        if (not decrypt):
            os.system('py blowfish_encrypt.py -m "' + msg + '"')
            os.system('py lz77/lz77.py')
        else:
            os.system('py lz77/lz77_decoder.py')
            os.system('py blowfish_decrypt.py decompressed_secret')
    else:
        if (not decrypt):
            os.system('py pyfish_encrypt.py -m "' + msg + '"')
            os.system('py lz77/lz77.py')
        else:
            os.system('py lz77/lz77_decoder.py')
            os.system('py pyfish_decrypt.py decompressed_secret')
    print('Done!!')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--message')
    parser.add_argument('-b', dest='blowfish', action='store_true')
    parser.add_argument('-d', dest='decrypt', action='store_true')
    args = parser.parse_args()
    main(args.message, args.blowfish, args.decrypt)