import random
import time
import hashlib
import uuid
import json
import pysnooper

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



def gcd(a, b):#ab最大公约数
    if b == 0:
        return a
    else:
        return gcd(b, a % b)


def findModReverse(a, m):#求模逆，和恢复组合使用
    if gcd(a, m) != 1:
        return None
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % m


def divresult(m):#构建Mj恢复秘密用的，长度为t*t
    tt=len(m)*len(m)
    Mj = [1]*tt
    for i in range(0, len(m)):
        for j in range(0, len(m)):
            if i == j:
                Mj[i] = Mj[i] * 1
            else:
                Mj[i] = Mj[i] * m[j]
    return Mj


def fun(d, t):#计算N和M
    N = 1
    M = 1
    for i in range(0, t):
        N = N * d[i]
    for i in range(len(d) - t + 1, len(d)):
        M = M * d[i]
    return N, M


def findk(d, k,n):#生成秘密份额ki,长度n
    k1 = [1]*(n+2)#为什么加2，怕不够长？
    for i in range(0, len(d)):
        k1[i] = k % d[i]
    k1 = k1[0:len(d)]
    return k1


def ChineseSurplus(k, d, t,n):#恢复秘密k
    m = d[0:t]
    a = k[0:t]
    flag = 1

    m1 = 1
    for i in range(0, len(m)):
        m1 = m1 * m[i]

    Mj = divresult(m)
    Mj1 = [0]*(n+2)

    for i in range(0, len(m)):
        Mj1[i] = findModReverse(Mj[i], m[i])
    x = 0

    for i in range(0, len(m)):
        x = x + Mj[i] * Mj1[i] * a[i]

    result = x % m1
    return result


def judge_d(m, num):#定义数组d，用于判断每个d，结合find_d一起用
    flag = 1
    for i in range(0, num):
        for j in range(0, num):
            if (gcd(m[i], m[j]) != 1) & (i != j):
                flag = 0
                break
    return flag


def find_d(n):#生成d模数组
    d = [1]*n
    temp = random.randint(pow(10, 167), pow(10, 168))
    d[0] = temp
    i = 1
    while i < 5:
        temp = random.randint(pow(10, 167), pow(10, 168))
        d[i] = temp
        if judge_d(d, i + 1) == 1:
            i = i + 1
    return d



#k是秘密，d是模数组，d1_dn相乘=m，N:上限，M:下限，k1是子密钥，
runtimes=200#运行次数
runtime=runtimes
a=[]
b=[]
n=45#用户数量n
t=int((3/5)*n)#门限值
m=2048#密钥长度
while runtimes>0:
    k =random_num(m)
    k1_time=time.time()
    d = find_d(n)
    N, M = fun(d, t)
    k1 = findk(d, k,n)
    k2_time=time.time()
    #份额生成阶段结束
    result = ChineseSurplus(k1, d, t,n)
    #明文恢复结束
    k3_time=time.time()
    gen_time=k2_time-k1_time#份额生成时间
    re_time=k3_time-k2_time#秘密恢复时间

    a.append(gen_time)
    b.append(re_time)
    runtimes-=1

    
aa=sum(a)/runtime
bb=sum(b)/runtime
f=open("data.txt","a+")#"a+"会持续写入，"w"只写一次
lines=["密钥长度",str(m),"bit ","用户数量",str(n)," 门限值",str(t)," 运行次数",str(runtime)," 生成份额时间",str(aa)," 恢复秘密时间",str(bb),"\n"]
f.writelines(lines)
f.close()
print("运行结束！")
