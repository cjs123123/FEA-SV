
f=open("Gowalla_totalCheckins.txt","r")
data=f.readlines()
l=len(data)
f.close()
B=[]
for line in data:
    first=line.strip("\n")
    first=first.split()#不能用split(' ')，而是默认什么不填，是因为若用split(' ')，只会分割出第一个空格，后面的空格不会分割，而用默认的话是全部分割
    x,y=float(first[2]),float(first[3])
    if 39.433333<x<41.5 and 115.41666<y<117.50:
        B.append(line)

f=open("data.txt","a+")#"a+"会持续写入，"w"只写一次
f.writelines(B)#将筛选出来数据存进data.txt
f.close()
print("运行结束！")


    
