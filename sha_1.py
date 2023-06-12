import pysnooper
import random
import math
import time
import numpy as np
import random
import pysnooper
import numpy.matlib
import hashlib
import json
import uuid

def getDistinctX(x_subi): 
    #x_subi = []
    #更改，原来len(F)=5,搞错选数阈值了，ind在面作为角标
    x = random.randint(1, q-1)
    if not x in x_subi:
        return x
    else:
        x = getDistinctX(x_subi)
        return x#去重随机
def random_num(n):#128位随机数
    if n==128:
        y=uuid.uuid4().hex #
        return int(y,16)#128输出10进制
    elif n==256:
        y1=uuid.uuid4().hex
        y2=uuid.uuid4().hex
        y3=y1+y2
        return int(y3,16)#512输出10进制
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
runtimes=2#运行时间
runtime=runtimes
t=25#最大25
n=40#这个没啥影响
lk=40#上限40
q=random_num(lk)
secret_k=q-1
#Field=[i for i in range(0,q)]#这步很久
aa=[]
bb=[]

while runtimes>0:
    s_time=time.time()
    x_subi = [0]
    a_subj = [0]
    pShares = [0]
    pShares_regex = [0]
    for i in range(1, n+1):#造x定义域
        x = getDistinctX(x_subi)#域中随机选择成为x,[1,q-1]
        x_subi.append(x)

    #print("x的所有取值:", x_subi)#n个参与者所有取值
    
    for j in range(1, t):#制定公式中的参数
        ind = random.randint(1, q-1)#也是1~q-1之间取
        a_subj.append(ind)
    # 根据需要加减a_i的值    
    #print("多项式的参数:", a_subj)
    k=secret_k
    for i in range(1, n+1):#挨个取x值
        x = x_subi[i]
        polynomialSum = k
        for j in range(1, t):#每个x都在完整公式下算出，因此a都得取到
            a = a_subj[j]
            exponent = x**j
            polynomialSum += a * exponent
        
        regEx = polynomialSum % q#计算出当前x值的秘密份额
        pShares_regex.append(regEx)#算出一个秘密份额存一个
        
        pShares.append(polynomialSum)#存没mod前的值，这个才能算出最后的公式
    l=len(a_subj)
    #显示多项式
    #print("多项式：f(x) = ",k,end="")
    #for ii in range(1,l):
        #print("+",str(a_subj[ii])+"x^"+str(ii),end="")
    #print("mod ",q)
    #print("份额已生成！")
    #print(x_subi)
    #print(pShares_regex)
    #print(pShares)
    
    c_time=time.time()
    
    #秘密恢复并核对
    Subset = [0]#下标
    y_subset = []
    x_subset = []
    for i in range(1,t+1):#t个下标
        Subset.append(i)
        
    for ID in Subset:#从0开始[0,t]
        y_i = pShares[ID]#pShares从[0,t],y_i从[0,t]t+1个值
        x_i = x_subi[ID]#x_i从[0,t]t+1个值
        y_subset.append(y_i)#y_subset从[0,t]t+1个值
        x_subset.append(x_i)#x_subset从[0,t]t+1个值
    #print("y_subset:",y_subset)
    #print("x_subset:",x_subset)
    recoveredK = 0
    for j in range(1, len(x_subset)):#恢复秘密值k的核心代码,计算过程好像是对的,数字大了就不对了
        x_j = x_subset[j]
        b_j = 1
        b_c=1
        c_j=1
        for L in range(1, len(x_subset)):
            if(L != j):
                b_c*=x_subset[L]
        for L in range(1, len(x_subset)):
            if(L != j):
                c_j*=(x_j-x_subset[L])
        b_j=float(b_c/c_j)
        recoveredK += y_subset[j] * (b_j)

    recoveredK_int = int(round(recoveredK))#round四舍五入函数
    
    e_time=time.time()
    s=c_time-s_time
    r=e_time-c_time
    print("恢复出的秘密值k：", recoveredK_int)
    if(recoveredK_int != k):
        print("恢复出错; 数量未超过门限值" +str(t)+"？")
    else:
        print("秘密值k已恢复成功！")
    aa.append(s)
    bb.append(r)
    runtimes-=1

tt=sum(aa)/runtime
rr=sum(bb)/runtime
f=open("data.txt","a+")
lines=["运行次数",str(runtime),"次","份额生成时间:",str(tt),"恢复时间:",str(rr),"shamir密钥长度：",str(lk),"nt：",str(n),str(t),"\n"]
f.writelines(lines)
f.close()
print("运行结束！")
