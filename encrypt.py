from scipy.io.wavfile import read
import numpy as np
import wave
import struct

key = []

def generateKey(initialKey, data, size):
    # size is size of plaintext

    height, width = data.shape;
    bytes = []
    for i in range(height):
        for j in range(width):
            bytes.append(data[i][j])

    # initialization
    s = []
    t = []
    for i in range(0, 256):
        s.append(i)

    for i in range(len(initialKey)):
        t.append(initialKey[i])

    p=0
    for i in range(len(initialKey),256):
        t.append(bytes[p])
        p+=1

    # initial Permutation
    j = 0
    for i in range(0, 256):
        j = (j + s[i] + t[i]) % 256
        temp = s[i]
        s[i] = s[j]
        s[j] = temp

    # Stream generation
    i, j = 0, 0
    for i in range(size):
        i = (i + 1) % 256
        j = (j + s[i]) % 256
        temp = s[i]
        s[i] = s[j]
        s[j] = temp
        t = (s[i] + s[j]) % 256
        key.append(s[t])

#Reading data from Wave file
a = read("C:\\Users\\Kaushal28\\Desktop\\NSE\\c.wav")
data = np.array(a[1], dtype=int)
print(data)
print(len(data))
original = wave.open("C:\\Users\\Kaushal28\\Desktop\\NSE\\c.wav", "r")

# Splitting into two arrays
first, second = np.hsplit(data, 2)

f = []
s = []
for x in first:
    f.append(int(x[0]/100))

for x in second:
    s.append(int(x[0]/100))

#Generating key based on initial key.
initialKey = [100, 200, 300, 400, 500, 600, 700, 800, 900]
generateKey(initialKey, data, max(len(f), len(s)))
print(key)

#Encrypting these two arrays.
cf = []
cs = []
i = 0
for x in f:
    cf.append(x ^ key[i])
    i += 1
i = len(key)-1
for x in s:
    cs.append(x ^ key[i])
    i -= 1

# Creating new wave file to write the encrypted data frames
encrypted = wave.open("C:\\Users\\Kaushal28\\Desktop\\NSE\\encrypted.wav", "wb")
encrypted.setparams(original.getparams())

print(cf)

# writing frames
for i in range(0, max(len(cf), len(cs))):
    encrypted.writeframes(struct.pack("hh",cf[i],cs[i]))


#-------------------------------------------------END OF ENCRYPTION---------------------------------------------#




a = read("C:\\Users\\Kaushal28\\Desktop\\NSE\\encrypted.wav")
data = np.array(a[1], dtype=int)

print( len(data))
first, second = np.hsplit(data, 2)

f = []
s = []
for x in first:
    f.append(x[0])

for x in second:
    s.append(x[0])


ef = []
es = []
i = 0
for x in f:
    ef.append(x ^ key[i])
    i += 1
i = len(key)-1
for x in s:
    es.append(x ^ key[i])
    i -= 1

org = wave.open("C:\\Users\\Kaushal28\\Desktop\\NSE\\encrypted.wav", "r")
encrypted = wave.open("C:\\Users\\Kaushal28\\Desktop\\NSE\\decrypted.wav", "wb")
encrypted.setparams(org.getparams())
for i in range(0, max(len(ef), len(es))):
    encrypted.writeframes(struct.pack("hh",ef[i]*100,es[i]*100))

#----------------------------------------END OF DECRYPTION--------------------------------------------#