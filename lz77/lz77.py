import sys

try:
    window_size = int(sys.argv[1])
except:
    window_size = 10

try:
    filename = sys.argv[2]
except:
    filename = 'secret'

binFile = open(filename+'.bin', 'rb')
binMsg = binFile.read()
binFile.close()
compressed = b''
l = len(binMsg)
i = 0
while i < l :
    found = False
    for j in range(i-window_size, i):
        if (j < 0): 
            continue
        if (binMsg[j] == binMsg[i]):
            n = 1
            found = True
            while ((i+n) < l-1 and n < 255 and binMsg[j + n] == binMsg[i + n]):
                n += 1
            compressed += (i - j).to_bytes(length=1, byteorder='big', signed=False)
            compressed += n.to_bytes(length=1, byteorder='big', signed=False)
            compressed += binMsg[i+n].to_bytes(length=1, byteorder='big', signed=False)
            i+=n
            break
    if (not found):
        compressed += b'\x00\x00' + binMsg[i].to_bytes(length=1, byteorder='big', signed=False)
    i += 1    
binFile = open('compressed_secret.bin', 'wb')
binFile.write(compressed)
binFile.close()    
