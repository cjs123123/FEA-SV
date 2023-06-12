import numpy as np
import random
import pysnooper
import numpy.matlib
import hashlib
import json
import time
import uuid
import base64
from Crypto.Cipher import AES

'''def Worker_crypt(pk,e,s,x,y):#含s密文
    pk[1][0]=pk[1][0]*e
    pk[1][1]=pk[1][1]*e
    ct=[pk[0][0]*e+s,[x+pk[1][0],y+pk[1][1]],x*x+y*y+s,1]#ct[一个]两个][1][一个]
    return ct

def no_crypt(ct,s):#无s密文
    ct[0]=ct[0]-s
    ct[2]=ct[2]-s
    return ct

def Requester_crypt(msk,x,y):#Requester加密的密文
    k=[[2*msk[0]*x,2*msk[1]*y],[-2*x,-2*y],1,x*x+y*y]#k[两个][两个][1][一个]
    return k

def FE(k,ct):#求距离函数
    d=k[0][0]*ct[0]+k[0][1]*ct[0]+ct[1][0]*k[1][0]+ct[1][1]*k[1][1]+ct[2]*k[2]+ct[3]*k[3]
    return d




    
pk=[[3],[9,24]]
msk=[3,8]
e=3
s=9
ct=Worker_crypt(pk,e,s,12,12)
ct=no_crypt(ct,9)
k=Requester_crypt(msk,11,11)
d=FE(k,ct)

print(d)
#这个是一维a'''




def Worker_crypt(pk,e,x,y):#pk加密坐标 
    ak=[[0,0],[0,0]]
    ak[0][0]=pk[0][0]*e
    ak[0][1]=pk[0][1]*e
    ak[1][0]=pk[1][0]*e
    ak[1][1]=pk[1][1]*e
    ct=[ak[0],[x+ak[1][0],y+ak[1][1]],x*x+y*y,1]#ct[两个]两个][1][一个]
    return ct

def Requester_crypt(msk,x,y):#Requester加密的密文
    k=[[2*msk[0][0]*x+2*msk[1][0]*y,2*msk[0][1]*x+2*msk[1][1]*y],[-2*x,-2*y],1,x*x+y*y]#k[两个][两个][1][一个]
    return k

def FE(k,ct):#求距离函数,去s后ct
    d=k[0][0]*ct[0][0]+k[0][1]*ct[0][1]+ct[1][0]*k[1][0]+ct[1][1]*k[1][1]+ct[2]*k[2]+ct[3]*k[3]
    return d

def hash(ciphertext):
    ciphertext_string = json.dumps(ciphertext,skipkeys=True).encode()
    return hashlib.sha256(ciphertext_string).hexdigest()#16进制输出
def random_hex(n):#128位16进制随机数
    if n==256:
        y=uuid.uuid4().hex
        return y
    elif n==128:
        y=uuid.uuid4().hex
        y=y[:16]
        return str(y)
    elif n==512:
        y1=uuid.uuid4().hex
        y2=uuid.uuid4().hex
        return y1+y2
    elif n==1024:
        y1=uuid.uuid4().hex
        y2=uuid.uuid4().hex
        y3=uuid.uuid4().hex
        y4=uuid.uuid4().hex
        return y1+y2+y3+y4
    else:
        y=uuid.uuid4().hex
        y2=bin(int(y,16))[2:]#化为二进制
        y2=y2[:int(n/2)]
        y2=int(y2,2)
        y2=hex(y2)
        return y2[2:].upper()
        


def random_num(n):#128位随机数
    if n==128:
        y=uuid.uuid4().hex #
        return int(y,16)#128输出10进制
    elif n==256:
        y1=uuid.uuid4().hex
        y2=uuid.uuid4().hex
        y3=y1+y2
        return int(y3,16)#256输出10进制
    elif n==512:
        y1=uuid.uuid4().hex
        y2=uuid.uuid4().hex
        y3=uuid.uuid4().hex
        y4=uuid.uuid4().hex
        return int(y1+y2+y3+y4,16)
    elif n==1024:
        y1=uuid.uuid4().hex
        y2=uuid.uuid4().hex
        y3=uuid.uuid4().hex
        y4=uuid.uuid4().hex
        y5=uuid.uuid4().hex
        y6=uuid.uuid4().hex
        y7=uuid.uuid4().hex
        y8=uuid.uuid4().hex
        return int(y1+y2+y3+y4+y5+y6+y7+y8,16)
    elif n==2048:
        y1=uuid.uuid4().hex
        y2=uuid.uuid4().hex
        y3=uuid.uuid4().hex
        y4=uuid.uuid4().hex
        y5=uuid.uuid4().hex
        y6=uuid.uuid4().hex
        y7=uuid.uuid4().hex
        y8=uuid.uuid4().hex
        y9=uuid.uuid4().hex
        y10=uuid.uuid4().hex
        y11=uuid.uuid4().hex
        y12=uuid.uuid4().hex
        y13=uuid.uuid4().hex
        y14=uuid.uuid4().hex
        y15=uuid.uuid4().hex
        y16=uuid.uuid4().hex
        return int(y1+y2+y3+y4+y5+y6+y7+y8+y9+y10+y11+y12+y13+y14+y15+y16,16)
    else:
        y=uuid.uuid4().hex
        y2=bin(int(y,16))[2:]#化为二进制
        y2=y2[:n]
        return int(y2,2)
def AES_Encrypt(key, data):#加密
  vi = '0102030405060708'
  pad = lambda s: s + (16 - len(s) % 16) * chr(16 - len(s) % 16)
  data = pad(data)
  # 字符串补位
  cipher = AES.new(key.encode('utf8'), AES.MODE_CBC, vi.encode('utf8'))
  encryptedbytes = cipher.encrypt(data.encode('utf8'))
  # 加密后得到的是bytes类型的数据
  encodestrs = base64.b64encode(encryptedbytes)
  # 使用Base64进行编码,返回byte字符串
  enctext = encodestrs.decode('utf8')
  # 对byte字符串按utf-8进行解码
  return enctext


def AES_Decrypt(key, data):#解密
  vi = '0102030405060708'
  data = data.encode('utf8')
  encodebytes = base64.decodebytes(data)
  # 将加密数据转换位bytes类型数据
  cipher = AES.new(key.encode('utf8'), AES.MODE_CBC, vi.encode('utf8'))
  text_decrypted = cipher.decrypt(encodebytes)
  unpad = lambda s: s[0:-s[-1]]
  text_decrypted = unpad(text_decrypted)
  # 去补位
  text_decrypted = text_decrypted.decode('utf8')
  return text_decrypted

