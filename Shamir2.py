import pysnooper
import random
import math


"""
This program generates a Shamir (t,n)-Threshold Scheme, with the desired
settings - as set by the user. The scheme can be initiated by running this
python script through the command line, or run directly via the python shell.

For specifications, the program requires the following 4 parameters:
-Prime field, over which all calculations will be conducted
-Desired secret, in the form of some number less than the prime field
-Number of total participants
-Size of threshold
"""

# 输入q, n, t, k
@pysnooper.snoop()
def initiateScheme(predefinedVars):
    kField = []
    n = 0
    t = 0
    #*Allows scheme to be run multiple times with different secret
    if not predefinedVars:#制定基础参数
        Elements = input("输入一个质数(q)\n")

        q = int(Elements)
        q = testPrimality(q)
        
        Field = createField(q)
        print("\n正在创造有限域:")
        print("q:", Field)

        kField = Field
        #输入n，t
        n = input("请设定参与者人数 n (n要小于质数q)\n")
        t = input("请设定门限值t (t要小于参与者人数n)\n")
        
        predefinedVars = [n, t, q, Field]
        
        if(n >= t):
            print("创建新的(" + t + ", " + n + ")-门限值秘密共享方案")
        
        else:
            print("恢复人数必须小于参与人数！")
            initiateScheme()
    else:#已经有基础参数
        kField = predefinedVars[3]
        q = predefinedVars[2]
        t = predefinedVars[1]
        n = predefinedVars[0]
    #在字段中输入所需的秘密字段索引
    secretInd = input("\n在(0~q-1)的域中挑一个作为秘密值(k)\n")
    secret_k = kField[int(secretInd)]
    print("k:", secret_k)
    #恢复函数？
    recovered_k = runScheme(t, n, secret_k, q, Field)
    
    return predefinedVars, recovered_k

# 检查是不是素数，是就返回原数不是让一直输入
def testPrimality(q):
    i = q
    q = math.sqrt(q)
    q = int(q)
    for p in range(2, (q+1)):
        f = i / p
        if(f.is_integer()):
            #print(f)
            #print(i)
            #print(p)
            newQ = input("请输入个质数")
            newQ = int(newQ)
            newQ = testPrimality(newQ)
            i = newQ
            break
    return i

# 创建有限域 GF(q)，q的有限域
def createField(q):
    ModuloK = []
    for i in range(0, q):
        ModuloK.append(i) 
    
    return ModuloK
    
# 运行runScheme算法,在最开始的算法里有提及
def runScheme(t_str, n_str, k, q, Field):
    x_subi = [0]
    a_subj = [0]
    pShares = [0]
    pShares_regex = [0]
    
    t = int(t_str)
    n = int(n_str)
    
    for i in range(1, n+1):
        #print("ran")
        x = getDistinctX(x_subi, Field)
        x_subi.append(x)

    print("x的所有取值:", x_subi)#n个参与者所有取值
    
    for j in range(1, t):
        ind = random.randint(0, q)
        a_subj.append(Field[ind])
    # 根据需要加减a_i的值
    print("a_1的值:", a_subj[1], "a_2的值:", a_subj[2])
    if (t>3):
        print("a_3的值:", a_subj[3], "a_4的值:", a_subj[4])    

    
    for i in range(1, n+1):
        x = x_subi[i]
        # print("x_i的值:",x)
        polynomialSum = k
        #print(k)
        for j in range(1, t):
            a = a_subj[j]
            # print("a:", a)
            exponent = math.pow(x, j)
            # print("exponent:", exponent)
            polynomialSum += a * exponent
            # print("polynomialSum:", polynomialSum)
        
        regEx = polynomialSum % q
        print("(%d, %d)" %(x, regEx))
        pShares_regex.append(regEx)
        # print("all f(x) :", pShares_regex)
        
        pShares.append(polynomialSum)

    # 根据你需要的多项式，手动修改
    # print("f(x) = %d + %d x +%d x^2  mod %d" %(k, a_subj[1], a_subj[2], q))
    #print("f(x) = %d + %d x +%d x^2 +%d x^3 + %d x^4 mod %d" %(k, a_subj[1], a_subj[2], a_subj[3], a_subj[4] ,q))
    print("f(x) = %d + %d x +%d x^2  mod %d" %(k, a_subj[1], a_subj[2],q))
    print("份额已生成！")
    displayShares_i(pShares_regex)


    generatedK = tryAccessStructure(k, pShares, x_subi, t_str, q)#这步是干什么的
    
    return generatedK


def reduce(integer, F):#将前几个总和约等于integer的数存于regex,置位binary为1
    F.sort(reverse=True)#降序
    print(F)
    binary = []
    regEx = []
    for i, f in enumerate(F):
        if(integer >= f):
            integer -= f

            binary.append(1)
            regEx.append(f)
        else:
            binary.append(0)

    return binary, regEx

#反复尝试的一个函数
def tryAccessStructure(k, pShares, x_subi, t_str, q):
    P_Subset = getSubset()

    generatedK = generateK(pShares, x_subi, P_Subset, q)
    if(generatedK != k):
        print("恢复出错; 数量未超过门限值: " + t_str)
    else:
        print("秘密值k已恢复成功！")
    r = input("要试试别的恢复组合么？ (Y or N)\n")
    if(r.upper() == "Y"):
        generatedK = tryAccessStructure(k, pShares, x_subi, t_str, q)

    return generatedK

#生成x的值x是F中的数，x = 1~5
def getDistinctX(x_subi, F): 
    #x_subi = []
    ind = random.randint(1, len(F)-1)#更改，原来len(F)=5,搞错选数阈值了，ind在面作为角标
    # ind = range(0, (len(F)-1))
    x = F[ind]
    if not x in x_subi:
        return x
    else:
        x = getDistinctX(x_subi, F)
        return x#去重随机


#查看某个人的秘密份额
def displayShares_i(pShares):
    P_ID_str = input("想查看哪个参与者的秘密份额？输入他的编号 (1到n)\n")
    P_ID = int(P_ID_str)
    try:
        Share = pShares[P_ID]
        Share = int(Share)
        print("这个第"+ P_ID_str +"参与者的秘密份额是: " + str(Share))
        Repeat = input("还想查看哪个参与者的秘密份额？(Y, or N)\n")
        if(Repeat.upper() == "Y"):
            displayShares_i(pShares)
    except:
        print("编号超出了: \n 编号须在1到n里")
        displayShares_i(pShares)
    
    return 

# 获取子密钥,想要恢复秘密就输入秘密份额存入subset
def getSubset():
    Subset_RAWstr = input("\n请输入想恢复秘密值的这些参与者编号\n编号从 'ID#1 ID#2 到 ID#T' \n其中ID#i是第i个参与者的编号\n")
    Subset_str = Subset_RAWstr.split()#按空格划分，返回字符串列表
    Subset = [0]
    Subset_mm = input("依次输入这些参与者的秘密份额：\n")
    for ID in Subset_str:
        try:
            ID = int(ID)
            Subset.append(ID)#转换成整数列表
        except:
            print("输入错误, 请重新输入！")
            Subset = getSubset()
            #ADD RECURSIVE FUNCTION
        
    return Subset

# 恢复秘密k 
def generateK(pShares, x_subi, Subset, q):
    y_subset = []
    x_subset = []
    
    Subset.sort()#
    for ID in Subset:
        y_i = pShares[ID]
        x_i = x_subi[ID]#因为原来是5以内，现在变大了，无法对号入座。
        y_subset.append(y_i)
        x_subset.append(x_i)
    
    recoveredK = 0
    for j in range(1, (len(x_subset))):
        x_j = x_subset[j]
        b_j = 1
        for L in range(1, len(x_subset)):
            if(L != j):
                x_L = x_subset[L]
                newCoeff = float(x_L)/(x_L - x_j)
                b_j = b_j * newCoeff
        recoveredK += y_subset[j] * (b_j)

    recoveredK_int = int(round(recoveredK))
    print("恢复出的秘密值k：", recoveredK_int)
    
    return recoveredK_int

#主程序
def runPackage(predefinedVars, recoveredKs):
    predefinedVars, returnK = initiateScheme(predefinedVars)
    # print("predefinedVars:", predefinedVars, "returnK:", returnK)
    if returnK in predefinedVars:
        print("New secret found:" + str(returnK))
        recoveredKs.append(returnK)
        print(recoveredKs)
    else:
        print("无效子密钥组合，无法恢复！")

    response = input("试试别的秘密值k的设定？程序将再次运行(Y or N).\n")
    if(response.upper() == "Y"):
        runPackage(predefinedVars, recoveredKs)
    
# initiateScheme()

runPackage([], [])
