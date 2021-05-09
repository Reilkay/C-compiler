#!/usr/bin/python
# -*- coding: UTF-8 -*-

# ------------------------------------------
#           2020-7-2
# ------------------------------------------
#           优化 Token    优化函数定义判断
# ------------------------------------------

# 该词法分析进行了扩展 具有双重功能，可以输出token序列，也可以输出其大概的语意，其中大概语意存放在total中，并没有输出

import re as re
dic = {
    'const': 'CONSTTK',
    'register':'REGISTK',
    'int': 'INTTK',
    'char': 'CHARTK',
    'float':'FLOATTK',
    'double':'DOUBLETK',
    'long':'LONGTK',
    'void': 'VOIDTK',
    'main': 'MAINTK',
    'if': 'IFTK',
    'else': 'ELSETK',
    'do': 'DOTK',
    'while': 'WHILETK',
    'for': 'FORTK',
    'scanf': 'SCANFTK',
    'printf': 'PRINTFTK',
    'return': 'RETURNTK',
    '+': 'PLUS',
    '++':'自加',
    '--':'自减',
    '%':'取模',
    '&':'算数与',
    '|':'算数或',
    '^':"异或",
    '!':'非',
    '&&':'逻辑与',
    '||':'逻辑或',
    '-': 'MINU',
    '*': 'MULT',
    '/': 'DIV',
    '<': 'LSS',
    '<=': 'LEQ',
    '>': 'GRE',
    '>=': 'GEQ',
    '==': 'EQL',
    '!=': 'NEQ',
    '=': 'ASSIGN',
    ';': 'SEMICN',
    ',': 'COMMA',
    '(': 'LPARENT',
    ')': 'RPARENT',
    '[': 'LBRACK',
    ']': 'RBRACK',
    '{': 'LBRACE',
    '}': 'RBRACE'
}

dic2 = {
    r'\a': "响铃",
    r'\b': "退格",
    r'\f': "换页",
    r'\n': "换行",
    r'\r': "回车",
    r'\t': "水平制表",
    r'\v': "垂直制表",
    r'\\': "反斜杠",
    r'\?': "问号字符",
    r'\'': "单引号字符",
    r'\"': "双引号字符",
    r'\0': "空字符"
    #r'\ddd': "任意字符，三位八进制",
    #r'\xhh': "任意字符，二位十六进制"
}
#转义字符表
zhuanyi = list(dic2.keys())
keys = list(dic.keys())
keyword = list(keys[0:17])
yunsuan = list(keys[17:37])
jiefu = list(keys[37:])
filt = ["\n", " ", "\r", "\t"]
total = ''
iT = []         #标识符
cT = []         #字符
sT = []         #字符串
CT = []         #常数
KT = keyword    #关键字
PT = yunsuan + jiefu     #界符
FT = []         #函数表
# 注意注释不要在符号表中体现
fout = ''


def isfunction(strr):
    rgl_exp1 = r'''
                (\s*)  
                ((VOID)|(void)|(char)|(short)|(int)|(float)|(long)|(double)) # 识别函数返回值类型
                (\s*(\*)?\s*)                                                # 识别返回值是否为指针类型以及中间是否包含空格
                (\w+)                                                        # 识别函数名
                ((\s*)(\()(\n)?)                                             # 函数开始小括号
                ((\s*)?(const)?(\s*)?                                        # 参数前是否有const
                ((void)|(char)|(short)|(int)|(float)|(long)|(double))        # 参数类型
                (\s*)(\*)?(\s*)?(restrict)?(\s*)?(\w+)(\s*)?(\,)?(\n)?(.*)?)*# 最后的*表示有多个参数
                ((\s*)(\))(\n)?)                                             # 函数结束小括号
                '''
    pat1 = re.compile(rgl_exp1, re.X)
    ret = pat1.match(strr)
    if None == ret:
        return False
        # print('不包含C函数定义!')
    else:
        return True
        # print("包含C函数定义!")


# 存进去的整个函数的一行 信息较多
def searchFT(strr):
    global fout
    temp = 0
    for i in FT:
        temp = temp + 1
        if strr == i:
            fout = fout + " <FT," + str(temp) + ">" + ","  # 如果搜索到了 就输出
            return
    temp = temp + 1
    FT.append(strr)  # 没搜到 添加进去
    fout = fout + " <FT," + str(temp) + ">" + ","
    return


def searchiT(strr):
    #global iT
    global fout
    temp = 0
    for i in iT:
        temp = temp+1
        if strr == i:
            fout = fout + " <iT," +str(temp) + ">" +","      #如果搜索到了 就输出
            return
    temp = temp+1
    iT.append(strr)                                                 #没搜到 添加进去
    fout = fout + " <iT," + str(temp) + ">" + ","
    return


def searchcT (strr):
    #global iT
    global fout
    temp = 0
    for i in cT:
        temp = temp+1
        if strr == i:
            fout = fout + " <cT," +str(temp) + ">" +","      #如果搜索到了 就输出
            return
    temp = temp+1
    cT.append(strr)                                                 #没搜到 添加进去
    fout = fout + " <cT," + str(temp) + ">" + ","
    return


def searchsT (strr):
    #global iT
    global fout
    temp = 0
    for i in sT:
        temp = temp+1
        if strr == i:
            fout = fout  + " <sT," +str(temp) + ">" +","      #如果搜索到了 就输出
            return
    temp = temp+1
    sT.append(strr)                                                 #没搜到 添加进去
    fout = fout + " <sT," + str(temp) + ">" + ","
    return


def searchCT (strr):
    #global iT
    global fout
    temp = 0
    for i in CT:
        temp = temp+1
        if strr == i:
            fout = fout + " <CT," +str(temp) + ">" +","      #如果搜索到了 就输出
            return
    temp = temp+1
    CT.append(strr)                                                 #没搜到 添加进去
    fout = fout + " <CT," + str(temp) + ">" + ","
    return


def searchKT (strr):
    #global iT
    global fout
    temp = 0
    for i in KT:
        temp = temp+1
        if strr == i:
            fout = fout + " <KT," +str(temp) + ">" +","      #如果搜索到了 就输出
            return
    temp = temp+1
    # KT.append(strr)                                                 #没搜到 不要添加进去
    fout = fout + " <KT," + str(temp) + ">" + ","
    return


def searchPT (strr):
    #global iT
    global fout
    temp = 0
    for i in PT:
        temp = temp+1
        if strr == i:
            fout = fout + " <PT," +str(temp) + ">" +","      #如果搜索到了 就输出
            return
    temp = temp+1
    #PT.append(strr)                                                 #没搜到 不要添加进去
    fout = fout + " <PT," + str(temp) + ">" + ","
    return


def iskeyword(judge):
    global keyword
    for i in  keyword:
        if judge == i:
            return True
    return False


def isyunsuan(judge):
    global yunsuan
    for i in yunsuan:
        if judge == i:
            return True
    return False


def isjiefu(judge):
    global jiefu
    for i in  jiefu:
        if judge == i:
            return True
    return False


def isfilt (judge):
    global filt
    global fout
    for i in filt:
        if judge == i and judge != "\n":
            return True
        if judge == i and judge == "\n":
            fout += "\n"
            return True
    return False


def analyze(strr):
    global dic
    global keys
    global keyword
    global jiefu
    global yunsuan
    global filt
    global total
    temp = ''
    i = 0
    # 开始分析
    while i < len(strr):
        temp = ''
        #print(i)
        if isfilt(strr[i]):
            i = i+1
            continue

        if strr[i] == "/" and strr[i + 1] == "/":        #注释
            while isfilt(strr[i] == False):
                temp = temp + strr[i]
                i = i+1
            total = total+"NOTESCON"+" "+temp+"\n"
            continue

        if strr[i] == "/" and strr[i + 1] == "*":  # 注释
            while strr[i] != "*" and strr[i + 1] != "/":
                temp = temp + strr[i]
                i = i + 1
            total = total + "NOTES2CON" + " " + temp + "\n"
            i = i+1  #过滤掉注释符号
            continue

        if strr[i] == '\"':                #字符集
            temp = temp + strr[i]
            i = i+1
            while strr[i]!= '\"':
                flag = strr[i] + strr[i+1]
                if flag in zhuanyi:
                    total = total+"Escape character"+" "+ flag + "\n"
                    i = i + 1
                temp = temp + strr[i]
                i = i + 1
            #temp = temp + strr[i]
            #print("STRCON", temp)
            total = total+"STRCON"+" "+ temp + "\n"
            searchsT(temp)
            i = i + 1
            continue

        if strr[i] == '\'':               #单个字符
            #temp = temp + strr[i]
            i = i + 1
            while strr[i] != '\'':
                temp = temp + strr[i]
                i = i + 1
            #temp = temp + strr[i]
            #print("CHARCON", temp)
            total = total + "CHARCON"+" " + temp+ "\n"
            searchcT(temp)
            i = i + 1
            continue

        if strr[i].islower():          # 关键字 或者 是标识符 或者 是函数名称
            # 记录i的位置 回溯
            save_i = i
            while strr[i] != '\n' and strr[i] != '{' and strr[i] != ';':
                temp = temp + strr[i]
                i = i + 1
            # 如果是函数定义格式
            if isfunction(temp):
                # 回溯到之前的位置
                i = save_i
                temp = ""
                # 过滤掉返回值类型
                while strr[i].islower() or strr[i].isdigit() or strr[i].isupper():
                    temp = temp + strr[i]
                    i = i + 1
                if iskeyword(temp):
                    # print(temp)
                    # print(dic[str(temp)],temp)
                    total = total + dic[str(temp)] + " " + temp + "\n"
                    searchKT(str(temp))
                    # 清空temp
                    temp = ""
                # 记录函数名称
                while strr[i] != '\n' and strr[i] != '{' and strr[i] != ';' and strr[i] != '(':
                    temp = temp + strr[i]
                    i = i + 1
                # print("FUNCTION", temp)
                total = total + "FUNCTION_NAME" + " " + temp + "\n"
                searchFT(temp)
                continue
            else:
                #回溯到之前的位置
                i = save_i
                temp = ""
                while strr[i].islower() or strr[i].isdigit() or strr[i].isupper():
                    temp = temp+strr[i]
                    i = i + 1
                if iskeyword(temp):
                    #print(temp)
                    #print(dic[str(temp)],temp)
                    total = total + dic[str(temp)] + " " + temp+ "\n"
                    searchKT(str(temp))
                else:
                    #print("IDENFR", temp)
                    total = total + "IDENFR" + " " + temp+ "\n"
                    searchiT(temp)
                    continue
            continue


        if str(strr[i]).isdigit():             #常数
            while str(strr[i]).isdigit() or (strr[i] == '.' and str(strr[i + 1]).isdigit()):
                temp = temp+strr[i]
                i = i+1
            #print("INTCON", temp)
            total = total + "INTCON" + " " + temp+ "\n"
            searchCT(temp)
            i = i-1
            i = i + 1
            continue

        if strr[i].isupper() or strr[i].islower() or (strr[i] == '_'):   #标识符
            while strr[i].isupper() or strr[i].islower() or (strr[i] == '_'):
                temp = temp+strr[i]
                i = i+1
            #print("IDENFR", temp)
            total = total + "IDENFR" + " " + temp+ "\n"
            searchiT(temp)
            i = i-1
            i = i + 1
            continue

        if isyunsuan(strr[i]):     #运算符，特别注意>=与>的区别 要向后看一个
            if isyunsuan(strr[i]) and isyunsuan(strr[i] + strr[i + 1]):
                total = total + dic[strr[i]+strr[i+1]] + " " + strr[i]+strr[i+1] + "\n"
                searchPT(strr[i]+strr[i+1])
                #print(dic[strr[i]+strr[i+1]],strr[i]+strr[i+1])
                i = i+1
                i = i + 1
                continue
            else:
                total = total + dic[strr[i]] + " " + strr[i]+ "\n"
                searchPT(strr[i])
                #print(dic[strr[i]],strr[i])
                i = i + 1
                continue

        if isjiefu(strr[i]):   #界符
            total = total + dic[strr[i]] + " " + strr[i] + "\n"
            searchPT(strr[i])
            #print(dic[strr[i]],strr[i])
            i = i + 1
            continue


def start(path="C:/Users/zrztt/PycharmProjects/yufafenxi/testfile.txt"):
    infile = open(path, "r+", encoding="UTF-8")
    # outfile = open("output.txt", "w", encoding="UTF-8")
    readin = str(infile.read())
    analyze(readin)
    # outfile.write(fout)
    infile.close()
    # outfile.close()
