from pwn import *

exe = context.binary = ELF('./fuck')


# gdbscript = '''
# break *0x{exe.symbols.main:x}
# continue
# '''.format(**locals())


p = process('./fuck')
gdb.attach(p)

p.recvline()
p.sendline('asd')


p.interactive()
