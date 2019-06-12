from pwn import *
import struct


ad = struct.pack('<L', 0xcafebabe).decode(errors='replace')


print(ad)
print(len(ad))


# print(ad.encode().decode())
