import math

def dataProcessor():
    binFile = open('compressed_secret.bin', 'rb')
    byteBlocks = binFile.read()
    binFile.close()
    compressedData = []
    print(byteBlocks)
    for i in range(0, math.ceil(len(byteBlocks)/3)):
        a = int.from_bytes(byteBlocks[(i*3):(i*3+1)], byteorder='big', signed=False)
        b = int.from_bytes(byteBlocks[(i*3+1):(i*3+2)], byteorder='big', signed=False)
        c = byteBlocks[(i*3+2):(i*3+3)]
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
decompressedMessage = decoder(encodedArr)

binFile = open('decompressed_secret.bin', 'wb')
binFile.write(decompressedMessage)
binFile.close()