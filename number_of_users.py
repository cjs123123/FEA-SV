f=open("data.txt","r")#"a+"会持续写入，"w"只写一次
data=f.readlines()
f.close()
C=[]
for line in data:
    first=line.strip("\n")
    first=first.split()
    a=first[0]
    C.append(a)
C=set(C)
C=list(C)
print(len(C))
#330个用户
