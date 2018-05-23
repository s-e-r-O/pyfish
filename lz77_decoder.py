import math

def dataProcessor():
    binFile = open('compressed_secret.bin', 'rb')
    byteBlocks = binFile.read()
    binFile.close()
    compressedData = []
    for i in range(0, math.floor(len(byteBlocks)/3)):
        a = int.from_bytes(byteBlocks[i*3], byteorder='big', signed=False)
        b = int.from_bytes(byteBlocks[(i*3)+1], byteorder='big', signed=False)
        c = byteBlocks[(i*3)+2]
        compressedData.append((a,b,c))
    return compressedData

def decoder(encodedArray):
    message = b''
    for i in range(0, len(encodedArray)):
        mesLen = len(message)
        for j in range(mesLen - encodedArray[i][0], mesLen - encodedArray[i][0] + encodedArray[i][1]):
            message += message[j]
        message += encodedArray[i][2]
    return message

encodedArr = dataProcessor()
#encodedArr = [(0,0,'a'),(0,0,'b'),(2,2,'c'),(0,3,'a'),(0,2,'a'),(2,3,'a')]
#encodedArr = [(0,0,'t'),(0,0,'o'),(0,0,'b'),(0,0,'e'),(3,1,'r'),(0,0,'n'),(3,1,'t'),(9,4,'$')]
decompressedMessage = decoder(encodedArr)
print(decoder(encodedArr))
binFile = open('decompressed_secret.bin', 'wb')
binFile.write(decompressedMessage)
binFile.close()