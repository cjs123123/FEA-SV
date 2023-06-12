import FE
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

f=open("location.txt","r")
data=f.readlines()#密文数据都在data里
l=len(data)
f.close()

#不同明文空间下（10,20,30,40,50）的FE计算开销(位置记录：哈希和加密生成的计算开销)，密钥长度为1024bit
runtimes=50#工作者数量
runtime=runtimes
a=[]
b=[]
c=[]
n=1024#密钥长度
aes=256#AES密钥长度,有128，192，256
z=10#保留原始坐标小数点后几位
result=[]#存工作者id

#一起运算,放在开始一起加密
key ='460469bd2159423ea2cbcf6c6163f65d'#AES密钥,256bits
pk1=136500454720492102571233040988617590974094992457410096163795084835044941903605233401626081371133968610258003218072057348567896875880690649576483225906315220046161240154921938018788631130725497914474984901347292182551346052336222312365382986463563275413517735018207417491553983870836282829239463297156217925263
pk2=55944714551696131386845049057468115634219636720297437351703737731124924813704228294489828694052702393393241477236335706685836691565523967660039816688188223986110017971592163314969553908578725517053034416140951644848770749007717585544327535518560997660670379378924472436610886143591965126655101293026194147386
msk1=56361495217894646931827979009195251714831542232640493324514746633529278699980266710007965047369819563696788149859306522633985366488659757491212083836900127610696744055626930566842547099727343570054559535615391209968664523145743017508177660286263680466133408290973491641898303945267201631612966931894860207696
msk2=135870595221623989612683907186687510406642293849067300239677311803550857854416315890234582425959122773157971688895277224434842356883220558553034099236099215520834118009440956774944683138915297370202146690415774223547539565380155879914933285769914036655728110368903176608257390681478506650339312663289734192298
msk3=106378390677093700620951806560294408897225898801355579060520990178890746127013136701222744872773808188595401018570183450172234761560176574012906560378423505263434191164670681011509825746477488418401589660211254481489351949176431932841440528375121831530324875442276990822887489357680133578939825066016608004120
msk4=141389898085890621473007822654183045847416045647577955203987294517600268807789644524320003656338086787239566070181077578831942094234483863429631190069443196715801084837072101322185640109298660938257495820258404919959866866716256243308707821577523888411152205930269450758160556216118113565765486193258103421900

pk3=pk1*msk1+pk2*msk2
pk4=pk1*msk3+pk2*msk4#FE核心代码
pk=[[pk1,pk2],[pk3,pk4]]#公钥
msk=[[msk1,msk2],[msk3,msk4]]#主私钥
B=[]



for line in data:
    first=line.strip("\n")
    afirst=first.split()#不能用split(' ')，而是默认什么不填，是因为若用split(' ')，只会分割出第一个空格，后面的空格不会分割，而用默认的话是全部分割
    x,y=float(afirst[2]),float(afirst[3])
    wx=int(x*(10**z))#工作者坐标(wx,wy)，请求者坐标（rx,ry）
    wy=int(y*(10**z))
    e=FE.random_num(1024)#每个工人自己生成
    ct1=pk1*e
    ct2=pk2*e
    ct3=wx+(pk1*msk1+pk2*msk2)*e
    ct4=wy+(pk1*msk3+pk2*msk4)*e
    ct5=wx*wx+wy*wy
    ct6=1
    first=first+"	"+str(ct1)+"	"+str(ct2)+"	"+str(ct3)+"	"+str(ct4)+"	"+str(ct5)+"	"+str(ct6)+"\n"#末尾再存个对象
    B.append(first)
    
f=open("cipher.txt","a+")
f.writelines(B)
f.close()
print("全密文结束！")#全部工作者的位置记录都处理结束

'''f=open("cipher.txt","r")
data=f.readlines()#密文数据都在data里
l=len(data)
f.close()

r=random.randint(0,l)
rm=data[r]#数据集随机选取一行
requester=rm.strip("\n")#获取请求者数据
requester=requester.split()
requester_id,requester_t,xx,yy=requester[0],requester[1],float(requester[2]),float(requester[3])
D=str(10000000000000000000000000)#位置策略
rx=str(int(xx*(10**z)))#工作者坐标(wx,wy)，请求者坐标（rx,ry）
ry=str(int(yy*(10**z)))

enctext_rx = FE.AES_Encrypt(key,rx)#请求者位置加密
enctext_ry = FE.AES_Encrypt(key,ry)
enctext_D = FE.AES_Encrypt(key,D)

rx_decrypted = FE.AES_Decrypt(key,enctext_rx)#解密一次就行
ry_decrypted = FE.AES_Decrypt(key,enctext_ry)
D_decrypted = FE.AES_Decrypt(key,enctext_D)

drx=int(rx_decrypted)
dry=int(ry_decrypted)
dD=int(D_decrypted)

s_time=time.time()

while runtimes>0:#多少个工作者数量
    i=random.randint(0,l)
    m=data[i]#数据集随机选取一行
    worker=m.strip("\n")#获取工人数据
    worker=worker.split()
    worker_id,worker_t,x,y=worker[0],worker[1],float(worker[2]),float(worker[3])

    #true_d=(wx-rx)**2+(wy-ry)**2#真实位置距离
    
    k=FE.Requester_crypt(msk,drx,dry)#函数加密
    
    ct=[[int(worker[5]),int(worker[6])],[int(worker[7]),int(worker[8])],int(worker[9]),int(worker[10])]#函数距离计算
    
    d=FE.FE(k,ct)#函数加密计算

    if dD>=d:
        result.append(worker_id)

e_time=time.time()

cc=e_time-s_time

f=open("data.txt","a+")#"a+"会持续写入，"w"只写一次
lines=["明文空间",str(z),"位小数","工作者数",str(runtime),"AES密钥长度：",str(aes),"验证计算生成时间",str(cc),"\n"]
f.writelines(lines)
f.close()'''
print("运行结束！")
