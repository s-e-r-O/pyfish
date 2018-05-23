import math

def dataProcessor():
    binFile = open('compressed.bin', 'rb')
    byteBlocks = binFile.read()
    binFile.close()
    compressedData = []
    for i in range(0, math.floor(len(byteBlocks)/17)):
        a = int.from_bytes(byteBlocks[i*8:(i+1)*8], byteorder='big', signed=False)
        b = int.from_bytes(byteBlocks[(i+1)*8:(i+2)*8], byteorder='big', signed=False)
        c = byteBlocks[(i+2)*8]
        compressedData.append((a,b,c))
    return compressedData

def decoder(encodedArray, size):
    message = ""
    for i in range(0, len(encodedArray)):
        position = size - encodedArray[i][0]
        mesLen = len(message)
        for j in range(mesLen - position, mesLen - position + encodedArray[i][1]):
            print(j)
            print(message)
            message += message[j]
        message += encodedArray[i][2]
    return message

#encodedArr = dataProcessor()
#encodedArr = [(0,0,'a'),(0,0,'b'),(2,2,'c'),(0,3,'a'),(0,2,'a'),(2,3,'a')]
encodedArr = [(0,0,'t'),(0,0,'o'),(0,0,'b'),(0,0,'e'),(3,1,'r'),(0,0,'n'),(3,1,'t'),(9,4,'$')]
print(decoder(encodedArr, 4))