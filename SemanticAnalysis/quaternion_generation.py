# !/usr/bin/python
# -*- coding: UTF-8 -*-

# ------------------------------------------
#           2020-7-8
# ------------------------------------------
#           终极版本2.0
# ------------------------------------------

import re as re
from WordAnalysis import words_analysis

# 根据词法分析进行四元式分析
# infile = open("output.txt", "r+", encoding="UTF-8")
TOKEN = []
load_line = ""
line_idx = -1

ans = []
filt = ""
# 用于写if的ie  while的we等
we_or_re = []
do_while_ans = []
function_return = {}

# 建立空字典，方便处理临时变量
dic = {}
# 建立全局返回值
total_ans = []
# 建立临时变量的使用个数
t_num = 0

# 标识符
iT = words_analysis.iT
# 字符
cT = words_analysis.cT
# 字符串
sT = words_analysis.sT
# 常数
CT = words_analysis.CT
# 关键字
KT = words_analysis.KT
# 界符
PT = words_analysis.PT
# 函数表
FT = words_analysis.FT
'''
单目：
( = a _ t)	( ++ a _ t)  (-- a _ t)	 ( ! a _ t)
双目：
( == a b t)  ( < a b t)  ( > a b t)   (<= a b t)   ( >= a b t)   ( != a b t)  
( % a b t)   ( | a b t)  ( ^ a b t)	( + a b t)   ( - a b t)   ( * a b t)   ( / a b t)   ( % a b t) 
( && a b t)  (|| a b t) 
'''


def readNextLine():
    global line_idx
    line_idx += 1

    return TOKEN[line_idx]


def compare(op1, op2):
    """
    比较两个运算符的优先级,乘除运算优先级比加减高
    op1优先级比op2高返回True，否则返回False
    """
    return (op1 in ["*", "/", "%"]) and (op2 in ["+", "-", "&&", "||", "&", "|", ""])


def select_table(temp_table, temp_num):
    global cT
    global sT
    global CT
    global KT
    global PT
    global FT
    global iT
    temp_num = int(temp_num)
    if temp_table == "cT":
        return str(cT[int(temp_num - 1)])
    if temp_table == "sT":
        return str(sT[int(temp_num - 1)])
    if temp_table == "CT":
        return str(CT[int(temp_num - 1)])
    if temp_table == "KT":
        return str(KT[int(temp_num - 1)])
    if temp_table == "PT":
        return str(PT[int(temp_num - 1)])
    if temp_table == "FT":
        return str(FT[int(temp_num - 1)])
    if temp_table == "iT":
        return str(iT[int(temp_num - 1)])


# 根据token进行整句翻译
def whole_sentence():
    global t_num
    global filt
    ans = []
    # 表的名称暂存
    temp_table = ""
    # 表中的位置暂存
    temp_num = ""
    # 记录逗号个数 每当两个逗号生成一个完整token
    log_comma = 0
    for i in range(len(filt)):
        if filt[i] == ",":
            log_comma += 1
            if log_comma == 2:
                ans.append(select_table(temp_table, temp_num))
                # 表的名称暂存
                temp_table = ""
                # 表中的位置暂存
                temp_num = ""
                log_comma = 0
                continue
            continue
        if log_comma == 0:
            temp_table += filt[i]
            continue
        if log_comma == 1:
            temp_num += filt[i]
            continue
    return ans


# 复合计算 现在还没有实现
def fuhe_cal(strr):
    global iT
    global cT
    global sT
    global CT
    global KT
    global PT
    global FT
    global t_num
    global filt
    fuhao_stack = []
    zimu_stack = []
    for i in strr:
        # print(i)
        # 这里可以做报错处理 可能没声明就用了
        # 自定义的标识符无条件入栈
        if (i in iT) or (i in CT):
            zimu_stack.append(i)
            continue
        # 遇到分号就退出
        if i == ";":
            break
        # 当是+-*/的时候考虑多种情况
        elif (i in KT) or (i in PT):
            # 当空的时候无条件进入
            if len(fuhao_stack) == 0:
                fuhao_stack.append(i)
                continue
            if i == "(":
                fuhao_stack.append(i)
                continue
            elif i == ")":
                while fuhao_stack[-1] != "(":
                    # 符号弹出一个 字母弹出两个回去一个
                    cell1 = fuhao_stack.pop()
                    cell2 = zimu_stack.pop()
                    cell3 = zimu_stack.pop()
                    total_ans.append(cell1 + ',' + cell3 + ',' + cell2 + "," + "t" + str(t_num))
                    zimu_stack.append(str("t" + str(t_num)))
                    t_num += 1
                # 弹出左括号
                fuhao_stack.pop()
                continue
            else:
                # 如果栈的最后一个符号优先级大于要进栈的就进行操作  且这个符号先不要急着入栈
                if compare(fuhao_stack[-1], i):
                    while compare(fuhao_stack[-1], i):
                        cell1 = fuhao_stack.pop()
                        cell2 = zimu_stack.pop()
                        cell3 = zimu_stack.pop()
                        total_ans.append(cell1 + ',' + cell3 + ',' + cell2 + "," + "t" + str(t_num))
                        zimu_stack.append(str("t" + str(t_num)))
                        t_num += 1
                    fuhao_stack.append(i)
                else:
                    fuhao_stack.append(i)
    if (len(fuhao_stack) != 0) and (len(zimu_stack) != 0):
        while len(fuhao_stack) != 0:
            cell1 = fuhao_stack.pop()
            cell2 = zimu_stack.pop()
            cell3 = zimu_stack.pop()
            total_ans.append(cell1 + ',' + cell3 + ',' + cell2 + "," + "t" + str(t_num))
            zimu_stack.append(str("t" + str(t_num)))
            t_num += 1
    # 检查是否还有剩余
    # print(fuhao_stack,zimu_stack)


# 计算一个句子中逗号的个数
def cal_cooma(strr):
    ans = 0
    for i in range(len(strr)):
        if strr[i] == ",":
            ans += 1
    return ans


# 处理 int a = a + b或a = a + b类似的句式 在四元式word中定义成了do{S}中的S
'''
大概这种句子
考虑过滤掉 int
int a;
int a = 1;
a = 1;
int a = a + b * c;
int a = fun(1);
a = fun(1);
a ++ ;
'''
def s_trans(flag=0):
    global function_return
    global filt
    global t_num
    global do_while_ans
    # 为了和do-while能够搭配上 因为do-while需要延时输出 flag = 0 为正常情况
    if flag == 0:
        temp = re.match('(.*?),(.*?),(.*?),(.*?),', filt, re.I | re.M)
        log_comma = 0
        # 过滤掉int等
        if select_table(str(temp.group(1)), str(temp.group(2))) in KT:
            for i in range(len(filt)):
                if filt[i] == ",":
                    log_comma += 1
                if log_comma == 2:
                    filt = filt[i + 1:]
                    # print(filt)
                    break
        log_comma = 0
        # 重新匹配一下 太乱了
        temp = re.search('(.*?),(.*?),(.*?),(.*?),', filt, re.I | re.M)

        # 这种a++; 还剩下a ++ ;
        # 后置 ++或--
        if select_table(str(temp.group(3)), str(temp.group(4))) in ["++", "--"] \
                and select_table(str(temp.group(1)), str(temp.group(2))) in iT:
            # 后置++ / --
            if select_table(str(temp.group(3)), str(temp.group(4))) == "++":
                # 操作数
                total_ans.append(
                    "+" + ',' + select_table(str(temp.group(1)), str(temp.group(2))) + ',' + "1" + ',' + 't' + str(
                        t_num))
                total_ans.append("=" + ',' + 't' + str(t_num) + ',' + "_" + "," + select_table(str(temp.group(1)),
                                                                                               str(temp.group(2))))
                t_num += 1
            if select_table(str(temp.group(3)), str(temp.group(4))) == "--":
                # 符号
                # cell2 = select_table(temp_table1, temp_num1)
                # 操作数
                total_ans.append(
                    "-" + ',' + select_table(str(temp.group(1)), str(temp.group(2))) + ',' + "1" + ',' + 't' + str(
                        t_num))
                total_ans.append("=" + ',' + 't' + str(t_num) + ',' + "_" + "," + select_table(str(temp.group(1)),
                                                                                               str(temp.group(2))))
                t_num += 1
            # print(total_ans)
            return
        # 这种++a; 还剩下++ a ;
        # 前置++或--
        if select_table(str(temp.group(1)), str(temp.group(2))) in ["++", "--"] \
                and select_table(str(temp.group(3)), str(temp.group(4))) in iT:
            # 后置++ / --
            if select_table(str(temp.group(1)), str(temp.group(2))) == "++":
                # 操作数
                total_ans.append(
                    "+" + ',' + select_table(str(temp.group(3)), str(temp.group(4))) + ',' + "1" + ',' + 't' + str(
                        t_num))
                total_ans.append(
                    "=" + ',' + 't' + str(t_num) + ',' + "_" + "," + select_table(str(temp.group(3)),
                                                                                  str(temp.group(4))))
                t_num += 1
            if select_table(str(temp.group(1)), str(temp.group(2))) == "--":
                # 符号
                # cell2 = select_table(temp_table1, temp_num1)
                # 操作数
                total_ans.append(
                    "-" + ',' + select_table(str(temp.group(3)), str(temp.group(4))) + ',' + "1" + ',' + 't' + str(
                        t_num))
                total_ans.append(
                    "=" + ',' + 't' + str(t_num) + ',' + "_" + "," + select_table(str(temp.group(3)),
                                                                                  str(temp.group(4))))
                t_num += 1
            # print(total_ans)
            return

        # int a ; 现在只剩下 a ;
        # print(temp.group(4))
        if select_table(str(temp.group(3)), str(temp.group(4))) == ";" \
                and select_table(str(temp.group(1)), str(temp.group(2))) in iT:
            total_ans.append("=" + ',' + '0' + ',' + "_" + "," + select_table(str(temp.group(1)), str(temp.group(2))))
            # print(total_ans)
            return

        # 如果是int fun(int a,int b) {S;	return m;}: int 已经被过滤掉
        #   (function fun _ _)
        #    quat(S)
        #   (end fun _ m)
        #   main函数特殊不做四元式生成
        elif select_table(str(temp.group(3)), str(temp.group(4))) == "(" \
                and select_table(str(temp.group(1)), str(temp.group(2))) in FT \
                and select_table(str(temp.group(1)), str(temp.group(2))) != " main":
            total_ans.append(
                "function" + "," + select_table(str(temp.group(1)), str(temp.group(2))) + "," + "_" + "," + "_")
            # 记录函数名字填表用
            function_name = select_table(str(temp.group(1)), str(temp.group(2)))
            # 处理中括号 { 就再读一行就行
            load_line = readNextLine()
            load_line = load_line.replace(" ", "")
            # print(re.match(r'<(.*),(.*)>,',load_line,re.I | re.M))
            filt = load_line
            filt = filt.replace("<", "")
            filt = filt.replace(">", "")
            # 处理完毕 开始处理S4
            # 过滤掉左括号后需要再读一行才是处理语句
            load_line = readNextLine()
            load_line = load_line.replace(" ", "")
            filt = load_line
            filt = filt.replace("<", "")
            filt = filt.replace(">", "")
            judge_return = re.search('(.*?),(.*?),(.*?),(.*?),', filt, re.I | re.M)
            is_return = select_table(str(judge_return.group(1)), str(judge_return.group(2)))
            # 不匹配到右括号为止
            while is_return != "return":
                s_trans()
                load_line = readNextLine()
                load_line = load_line.replace(" ", "")
                filt = load_line
                filt = filt.replace("<", "")
                filt = filt.replace(">", "")
                judge_return = re.search('(.*?),(.*?),(.*?),(.*?),', filt, re.I | re.M)
                is_return = select_table(str(judge_return.group(1)), str(judge_return.group(2)))
            # 加入end
            # 如果不是void
            if select_table(str(judge_return.group(3)), str(judge_return.group(4))) != ";":
                total_ans.append("end" + "," + select_table(str(temp.group(1)), str(temp.group(2))) + "," + "_" + "," + \
                                 select_table(str(judge_return.group(3)), str(judge_return.group(4))))
                function_return[function_name] = select_table(str(judge_return.group(3)), str(judge_return.group(4)))
            # 如果是void
            elif select_table(str(judge_return.group(3)), str(judge_return.group(4))) == ";":
                total_ans.append(
                    "end" + "," + select_table(str(temp.group(1)), str(temp.group(2))) + "," + "_" + "," + "_")
            # 扫到右括号
            load_line = readNextLine()
            return

        # a = fun(1)
        temp = re.search('(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),', filt, re.I | re.M)
        if select_table(str(temp.group(1)), str(temp.group(2))) in iT \
                and select_table(str(temp.group(3)), str(temp.group(4))) == "=" \
                and select_table(str(temp.group(5)), str(temp.group(6))) in FT \
                and select_table(str(temp.group(5)), str(temp.group(6))) != "main":
            total_ans.append(
                "jump" + "," + "_" + "," + "_" + "," + select_table(str(temp.group(5)), str(temp.group(6))))
            total_ans.append(str("=" + ',' + function_return[
                select_table(str(temp.group(5)), str(temp.group(6)))] + ',' + "_" + "," + select_table(
                str(temp.group(1)), str(temp.group(2)))))
            return
        # a = 1 ; a = a + b 等 考虑 a = 1 的特殊情况 只有1一种情况
        elif select_table(str(temp.group(1)), str(temp.group(2))) in iT \
                and select_table(str(temp.group(3)), str(temp.group(4))) == "=" \
                and select_table(str(temp.group(5)), str(temp.group(6))) not in FT:
            # 先保留a 然后再复合运算
            append_ = select_table(str(temp.group(1)), str(temp.group(2)))
            # 过滤 a和=
            for i in range(len(filt)):
                if filt[i] == ",":
                    log_comma += 1
                if log_comma == 4:
                    filt = filt[i + 1:]
                    break
            if cal_cooma(filt) == 4:
                # 数字或标识符
                temp_table1 = ""
                temp_num1 = ""
                comma_num = 0
                for i in range(len(filt)):
                    if filt[i] == ",":
                        comma_num += 1
                        continue
                    if filt[i] == 2:
                        break
                    if comma_num == 0:
                        temp_table1 += filt[i]
                        continue
                    if comma_num == 1:
                        temp_num1 += filt[i]
                        continue
                    break
                if select_table(temp_table1,temp_num1) in iT:
                    total_ans.append("=" + ',' + select_table(temp_table1,temp_num1) + ',' + "_" + "," + append_)
                if select_table(temp_table1, temp_num1) in CT:
                    total_ans.append("=" + ',' + select_table(temp_table1, temp_num1) + ',' + "_" + "," + append_)
                return
            log_comma = 0
            # 翻译整个句子
            translated = whole_sentence()
            fuhe_cal(translated)
            total_ans.append("=" + ',' + "t" + str(t_num - 1) + ',' + "_" + "," + append_)
            return

    # flag = 1 为do - while情况 ---------------------------------------------------------------------------------------------
    elif flag == 1:
        temp = re.match('(.*?),(.*?),(.*?),(.*?),', filt, re.I | re.M)
        log_comma = 0
        # 过滤掉int等
        if select_table(str(temp.group(1)), str(temp.group(2))) in KT:
            for i in range(len(filt)):
                if filt[i] == ",":
                    log_comma += 1
                if log_comma == 2:
                    filt = filt[i + 1:]
                    # print(filt)
                    break
        log_comma = 0
        # 重新匹配一下 太乱了
        temp = re.search('(.*?),(.*?),(.*?),(.*?),', filt, re.I | re.M)

        # 这种a++; 还剩下a ++ ;
        # 后置 ++或--
        if select_table(str(temp.group(3)), str(temp.group(4))) in ["++", "--"] \
                and select_table(str(temp.group(1)), str(temp.group(2))) in iT:
            # 后置++ / --
            if select_table(str(temp.group(3)), str(temp.group(4))) == "++":
                # 操作数
                do_while_ans.append(
                    "+" + ',' + select_table(str(temp.group(1)), str(temp.group(2))) + ',' + "1" + ',' + 't' + str(
                        t_num))
                do_while_ans.append("=" + ',' + 't' + str(t_num) + ',' + "_" + "," + select_table(str(temp.group(1)),
                                                                                                  str(temp.group(2))))
                t_num += 1
            if select_table(str(temp.group(3)), str(temp.group(4))) == "--":
                # 符号
                # cell2 = select_table(temp_table1, temp_num1)
                # 操作数
                do_while_ans.append(
                    "-" + ',' + select_table(str(temp.group(1)), str(temp.group(2))) + ',' + "1" + ',' + 't' + str(
                        t_num))
                do_while_ans.append("=" + ',' + 't' + str(t_num) + ',' + "_" + "," + select_table(str(temp.group(1)),
                                                                                                  str(temp.group(2))))
                t_num += 1
            # print(total_ans)
            return do_while_ans
        # 这种++a; 还剩下++ a ;
        # 前置++或--
        if select_table(str(temp.group(1)), str(temp.group(2))) in ["++", "--"] \
                and select_table(str(temp.group(3)), str(temp.group(4))) in iT:
            # 后置++ / --
            if select_table(str(temp.group(1)), str(temp.group(2))) == "++":
                # 操作数
                do_while_ans.append(
                    "+" + ',' + select_table(str(temp.group(3)), str(temp.group(4))) + ',' + "1" + ',' + 't' + str(
                        t_num))
                do_while_ans.append(
                    "=" + ',' + 't' + str(t_num) + ',' + "_" + "," + select_table(str(temp.group(3)),
                                                                                  str(temp.group(4))))
                t_num += 1
            if select_table(str(temp.group(1)), str(temp.group(2))) == "--":
                # 符号
                # cell2 = select_table(temp_table1, temp_num1)
                # 操作数
                do_while_ans.append(
                    "-" + ',' + select_table(str(temp.group(3)), str(temp.group(4))) + ',' + "1" + ',' + 't' + str(
                        t_num))
                do_while_ans.append(
                    "=" + ',' + 't' + str(t_num) + ',' + "_" + "," + select_table(str(temp.group(3)),
                                                                                  str(temp.group(4))))
                t_num += 1
            # print(total_ans)
            return do_while_ans

        # int a ; 现在只剩下 a ;
        # print(temp.group(4))
        if select_table(str(temp.group(3)), str(temp.group(4))) == ";" \
                and select_table(str(temp.group(1)), str(temp.group(2))) in iT:
            do_while_ans.append(
                "=" + ',' + '0' + ',' + "_" + "," + select_table(str(temp.group(1)), str(temp.group(2))))
            # print(total_ans)
            return do_while_ans
        # 如果是int fun(...)不用动
        elif select_table(str(temp.group(3)), str(temp.group(4))) == ";" \
                and select_table(str(temp.group(1)), str(temp.group(2))) in FT:
            return do_while_ans
        # a = fun(1)
        temp = re.search('(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),', filt, re.I | re.M)
        if select_table(str(temp.group(1)), str(temp.group(2))) in iT \
                and select_table(str(temp.group(3)), str(temp.group(4))) == "=" \
                and select_table(str(temp.group(5)), str(temp.group(6))) in FT:
            do_while_ans.append(str(
                "=" + ',' + select_table(str(temp.group(5)), str(temp.group(6))) + ',' + "_" + "," + select_table(
                    str(temp.group(1)), str(temp.group(2)))))
            return do_while_ans
        # a = 1 ; a = a + b 等
        elif select_table(str(temp.group(1)), str(temp.group(2))) in iT \
                and select_table(str(temp.group(3)), str(temp.group(4))) == "=" \
                and select_table(str(temp.group(5)), str(temp.group(6))) not in FT:
            # 先保留a 然后再复合运算
            append_ = select_table(str(temp.group(1)), str(temp.group(2)))
            # 过滤 a和=
            for i in range(len(filt)):
                if filt[i] == ",":
                    log_comma += 1
                if log_comma == 4:
                    filt = filt[i + 1:]
                    break
            log_comma = 0
            # 翻译整个句子
            translated = whole_sentence()
            fuhe_cal(translated)
            do_while_ans.append("=" + ',' + "t" + str(t_num - 1) + ',' + "_" + "," + append_)
            return do_while_ans


# 识别是哪种四元式
def category_select(table, num):
    # 利用filt传值
    if str(table[num - 1]) == "if":
        if_trans()
    if str(table[num - 1]) == "while":
        if_trans()
    if str(table[num - 1]) == "for":
        if_trans()
    if str(table[num - 1]) == "do":
        if_trans()
    if str(table[num - 1]) == "if":
        if_trans()
    if str(table[num - 1]) == "if":
        if_trans()
    if str(table[num - 1]) == "if":
        if_trans()


def danmu_cal():
    global t_num
    # temp = 0
    # 符号
    temp_table1 = ""
    temp_num1 = ""
    # 数字或标识符
    temp_table2 = ""
    temp_num2 = ""
    comma_num = 0
    for i in range(len(filt)):
        if filt[i] == ",":
            comma_num += 1
            continue
        if filt[i] == 4:
            break
        if comma_num == 0:
            temp_table1 += filt[i]
            continue
        if comma_num == 1:
            temp_num1 += filt[i]
            continue
        if comma_num == 2:
            temp_table2 += filt[i]
            continue
        if comma_num == 3:
            temp_num2 += filt[i]
            continue
        break
    # 前是符号 后是运算符 或者前是运算符后是符号
    return temp_table1, temp_num1, temp_table2, temp_num2


# 双目运算四元式生成 利用filt 处理单行
def shuangmu_cal():
    global filt
    global total_ans
    global t_num
    # 第一个操作数 第二个操作数 符号信息
    temp_table1 = ""
    temp_table2 = ""
    temp_num1 = ""
    temp_num2 = ""
    temp_fuhao = ""
    temp_fuhao_num = ""
    # 记录逗号个数
    log_comma = 0
    for i in range(len(filt)):
        # 根据逗号个数匹配
        if filt[i] == ",":
            log_comma += 1
            continue
        if log_comma == 6:
            # 每当逗号数目为6 说明一个元组生成
            # -------------------------------------
            # 初始化逗号数目
            break
        if log_comma == 0:
            temp_table1 += filt[i]
            continue
        if log_comma == 1:
            temp_num1 += filt[i]
            continue
        if log_comma == 2:
            temp_fuhao += filt[i]
            continue
        if log_comma == 3:
            temp_fuhao_num += filt[i]
            continue
        if log_comma == 4:
            temp_table2 += filt[i]
            continue
        if log_comma == 5:
            temp_num2 += filt[i]
    # 符号
    cell1 = select_table(temp_fuhao, temp_fuhao_num)
    # 操作数1
    cell2 = select_table(temp_table1, temp_num1)
    # 操作数2
    cell3 = select_table(temp_table2, temp_num2)
    return cell1, cell2, cell3


# int fun1不翻译四元式 或者是 int a = 1 翻译四元式
def hanshu_or_bianliang():
    global t_num
    # 过滤掉 int 等
    global filt
    cishu = 0
    for i in range(len(filt)):
        if filt[i] == ",":
            cishu += 1
            if cishu == 2:
                filt = filt[i + 1:]
                break
    # 再次初始化
    cishu = 0
    # temp判断是函数还是变量 函数就不要生成四元式
    temp_table1 = ""
    temp_num1 = ""
    temp_table2 = ""
    temp_num2 = ""
    for i in range(len(filt)):
        if filt[i] == ",":
            cishu += 1
            continue
        # 识别出前一个标识符 int float......
        if cishu == 0:
            temp_table1 += filt[i]
        elif cishu == 1:
            temp_num1 += filt[i]
        elif cishu == 2:
            temp_table2 += filt[i]
        elif cishu == 3:
            temp_num2 += filt[i]
    # 如果是函数 说明是声明 直接返回
    if temp_table1 == "FT":
        return
    # 变量声明就翻译四元式
    else:
        # 符号 操作数1 操作数2
        cell1, cell2, cell3 = shuangmu_cal()
        total_ans.append(cell1 + ',' + cell2 + ',' + '_' + ',' + cell3)


'''
if(E) {S1} else {S2}:
quat(E)
(if res(E) _ _)
quat(s1)
(el _ _ _)
quat(s2)
(ie _ _ _)
'''


# debug正确！！！！！
def if_trans():
    global t_num
    # 栈中保存if信息
    we_or_re.append("if")
    # 过滤掉if debug正确
    global filt
    cishu = 0
    for i in range(len(filt)):
        if filt[i] == ",":
            cishu += 1
            if cishu == 2:
                filt = filt[i + 1:]
                break
    cishu = 0
    # 过滤掉左括号
    for i in range(len(filt)):
        if filt[i] == ",":
            cishu += 1
            if cishu == 2:
                filt = filt[i + 1:]
                break
    # if(change)
    if cal_cooma(filt) == 4:
        temp_table = ""
        temp_num = ""
        comma_num = 0
        # print(filt)
        for j in range(0, len(filt)):
            if filt[j] == ",":
                comma_num += 1
                if comma_num == 2:
                    break
                continue
            if comma_num == 0:
                temp_table += filt[j]
                continue
            if comma_num == 1:
                temp_num += filt[j]
        total_ans.append("==" + ',' + select_table(temp_table, temp_num) + ',' + "1" + ',' + 't' + str(t_num))
        total_ans.append("if" + ',' + 't' + str(t_num) + ',' + '_' + ',' + '_')
        t_num += 1
        return
    # 判断是双目还是单目 例如!a 或者 a>b
    # 记录左括号后的逗号个数 如果4个逗号后是右括号 就说明是单目运算符号
    temp = 0
    temp_table = ""
    temp_num = ""
    comma_num = 0
    # print(filt)
    for i in range(len(filt)):
        if filt[i] == ',':
            temp += 1
            if temp == 4:
                for j in range(i + 1, len(filt)):
                    if filt[j] == ",":
                        comma_num += 1
                        if comma_num == 2:
                            break
                        continue
                    if comma_num == 0:
                        temp_table += filt[j]
                        continue
                    if comma_num == 1:
                        temp_num += filt[j]
        continue
    if str(select_table(temp_table, temp_num)) == ")":
        temp_table1, temp_num1, temp_table2, temp_num2 = danmu_cal()
        # 取非
        if select_table(temp_table1, temp_num1) == "!":
            total_ans.append("==" + ',' + select_table(temp_table2, temp_num2) + ',' + "0" + ',' + 't' + str(t_num))
            total_ans.append("if" + ',' + 't' + str(t_num) + ',' + '_' + ',' + '_')
            t_num += 1
        # 前置++ / --
        if select_table(temp_table1, temp_num1) == "++":
            # 符号
            # cell2 = select_table(temp_table1, temp_num1)
            # 操作数
            cell3 = select_table(temp_table2, temp_num2)
            total_ans.append("+" + ',' + str(cell3) + ',' + "1" + ',' + 't' + str(t_num))
            total_ans.append("=" + ',' + 't' + str(t_num) + ',' + "_" + "," + str(cell3))
            t_num += 1
            total_ans.append("!=" + ',' + cell3 + ',' + "0" + ',' + 't' + str(t_num))
            total_ans.append("if" + ',' + 't' + str(t_num) + ',' + '_' + ',' + '_')
            t_num += 1
        if select_table(temp_table1, temp_num1) == "--":
            # 符号
            # cell2 = select_table(temp_table1, temp_num1)
            # 操作数
            cell3 = select_table(temp_table2, temp_num2)
            total_ans.append("-" + ',' + str(cell3) + ',' + "1" + ',' + 't' + str(t_num))
            total_ans.append("=" + ',' + 't' + str(t_num) + ',' + "_" + "," + str(cell3))
            t_num += 1
            total_ans.append("!=" + ',' + cell3 + ',' + "0" + ',' + 't' + str(t_num))
            total_ans.append("if" + ',' + 't' + str(t_num) + ',' + '_' + ',' + '_')
            t_num += 1
        # 后置++ / --
        if select_table(temp_table1, temp_num1) == "++":
            # 符号
            # cell2 = select_table(temp_table1, temp_num1)
            # 操作数
            cell3 = select_table(temp_table2, temp_num2)
            total_ans.append("!=" + ',' + cell3 + ',' + "0" + ',' + 't' + str(t_num))
            total_ans.append("if" + ',' + 't' + str(t_num) + ',' + '_' + ',' + '_')
            t_num += 1
            total_ans.append("+" + ',' + cell3 + ',' + "1" + ',' + 't' + str(t_num))
            total_ans.append("=" + ',' + 't' + str(t_num) + ',' + "_" + "," + cell3)
            t_num += 1
        if select_table(temp_table1, temp_num1) == "--":
            # 符号
            # cell2 = select_table(temp_table1, temp_num1)
            # 操作数
            cell3 = select_table(temp_table2, temp_num2)
            total_ans.append("!=" + ',' + cell3 + ',' + "0" + ',' + 't' + str(t_num))
            total_ans.append("if" + ',' + 't' + str(t_num) + ',' + '_' + ',' + '_')
            t_num += 1
            total_ans.append("-" + ',' + cell3 + ',' + "1" + ',' + 't' + str(t_num))
            total_ans.append("=" + ',' + 't' + str(t_num) + ',' + "_" + "," + cell3)
            t_num += 1
    else:
        # 计算双目运算符
        cell1, cell2, cell3 = shuangmu_cal()
        total_ans.append(str(cell1) + ',' + str(cell2) + ',' + str(cell3) + ',' + 't' + str(t_num))
        total_ans.append("if" + ',' + 't' + str(t_num) + ',' + '_' + ',' + '_')
        t_num += 1


'''
while(E) {S}:
(wh _ _ _)
quat(E)
(do res(E) _ _)
quat(S)
(we _ _ _)
'''


# debug正确！！！！！
def while_trans():
    global t_num
    # 过滤掉while
    global filt
    cishu = 0
    for i in range(len(filt)):
        if filt[i] == ",":
            cishu += 1
            if cishu == 2:
                filt = filt[i + 1:]
                break
    cishu = 0
    # 过滤掉左括号
    for i in range(len(filt)):
        if filt[i] == ",":
            cishu += 1
            if cishu == 2:
                filt = filt[i + 1:]
                break
    # 入栈 不要在这里入 在主函数入栈
    # we_or_re.append("while")
    total_ans.append("wh" + ',' + '_' + ',' + '_' + ',' + '_')
    if cal_cooma(filt) == 4:
        temp = 0
        temp_table = ""
        temp_num = ""
        comma_num = 0
        # print(filt)
        for j in range(0, len(filt)):
            if filt[j] == ",":
                comma_num += 1
                if comma_num == 2:
                    break
                continue
            if comma_num == 0:
                temp_table += filt[j]
                continue
            if comma_num == 1:
                temp_num += filt[j]
        total_ans.append("==" + ',' + select_table(temp_table, temp_num) + ',' + "1" + ',' + 't' + str(t_num))
        total_ans.append("if" + ',' + 't' + str(t_num) + ',' + '_' + ',' + '_')
        t_num += 1
        return
    # 计算四元式
    # 判断是双目还是单目 例如!a 或者 a>b
    # 记录左括号后的逗号个数 如果4个逗号后是右括号 就说明是单目运算符号
    temp = 0
    temp_table = ""
    temp_num = ""
    comma_num = 0
    for i in range(len(filt)):
        if filt[i] == ',':
            temp += 1
            if temp == 4:
                for j in range(i + 1, len(filt)):
                    if filt[j] == ",":
                        comma_num += 1
                        continue
                    if comma_num == 2:
                        break
                    if comma_num == 0:
                        temp_table += filt[j]
                        continue
                    if comma_num == 1:
                        temp_num += filt[j]
        continue
    if str(select_table(temp_table, temp_num)) == ")":
        temp_table1, temp_num1, temp_table2, temp_num2 = danmu_cal()
        # 取非
        if select_table(temp_table1, temp_num1) == "!":
            total_ans.append("==" + ',' + select_table(temp_table2, temp_num2) + ',' + "0" + ',' + 't' + str(t_num))
            # total_ans.append("if" + ',' + 't' + str(t_num) + ',' + '_' + ',' + '_')
            t_num += 1
        # 前置++ / --
        if select_table(temp_table1, temp_num1) == "++":
            # 符号
            # cell2 = select_table(temp_table1, temp_num1)
            # 操作数
            cell3 = select_table(temp_table2, temp_num2)
            total_ans.append("+" + ',' + str(cell3) + ',' + "1" + ',' + 't' + str(t_num))
            total_ans.append("=" + ',' + 't' + str(t_num) + ',' + "_" + "," + str(cell3))
            t_num += 1
            total_ans.append("!=" + ',' + cell3 + ',' + "0" + ',' + 't' + str(t_num))
            # total_ans.append("if" + ',' + 't' + str(t_num) + ',' + '_' + ',' + '_')
            t_num += 1
        if select_table(temp_table1, temp_num1) == "--":
            # 符号
            # cell2 = select_table(temp_table1, temp_num1)
            # 操作数
            cell3 = select_table(temp_table2, temp_num2)
            total_ans.append("-" + ',' + str(cell3) + ',' + "1" + ',' + 't' + str(t_num))
            total_ans.append("=" + ',' + 't' + str(t_num) + ',' + "_" + "," + str(cell3))
            t_num += 1
            total_ans.append("!=" + ',' + cell3 + ',' + "0" + ',' + 't' + str(t_num))
            # total_ans.append("if" + ',' + 't' + str(t_num) + ',' + '_' + ',' + '_')
            t_num += 1
        # 后置++ / --
        if select_table(temp_table1, temp_num1) == "++":
            # 符号
            # cell2 = select_table(temp_table1, temp_num1)
            # 操作数
            cell3 = select_table(temp_table2, temp_num2)
            total_ans.append("!=" + ',' + cell3 + ',' + "0" + ',' + 't' + str(t_num))
            # total_ans.append("if" + ',' + 't' + str(t_num) + ',' + '_' + ',' + '_')
            t_num += 1
            total_ans.append("+" + ',' + cell3 + ',' + "1" + ',' + 't' + str(t_num))
            total_ans.append("=" + ',' + 't' + str(t_num) + ',' + "_" + "," + cell3)
            t_num += 1
        if select_table(temp_table1, temp_num1) == "--":
            # 符号
            # cell2 = select_table(temp_table1, temp_num1)
            # 操作数
            cell3 = select_table(temp_table2, temp_num2)
            total_ans.append("!=" + ',' + cell3 + ',' + "0" + ',' + 't' + str(t_num))
            # total_ans.append("if" + ',' + 't' + str(t_num) + ',' + '_' + ',' + '_')
            t_num += 1
            total_ans.append("-" + ',' + cell3 + ',' + "1" + ',' + 't' + str(t_num))
            total_ans.append("=" + ',' + 't' + str(t_num) + ',' + "_" + "," + cell3)
            t_num += 1
    else:
        # 计算双目运算符
        cell1, cell2, cell3 = shuangmu_cal()
        total_ans.append(str(cell1) + ',' + str(cell2) + ',' + str(cell3) + ',' + 't' + str(t_num))
        # total_ans.append("if" + ',' + 't' + str(t_num) + ',' + '_' + ',' + '_')
        t_num += 1
    total_ans.append("do" + ',' + "t" + str(t_num - 1) + ',' + '_' + ',' + '_')


# 这个很难处理
'''
for(S1;S2;S3) {S4}:
(for _ _ _)
quat(S1)
(wh _ _ _)
quat(S2)
(do res(S2) _ _)
quat(S4)
quat(S3)
(we _ _ _)
'''


def for_trans():
    # for(S1;S2;S3) {S4}
    global t_num
    # 过滤掉for
    global filt
    cishu = 0
    for i in range(len(filt)):
        if filt[i] == ",":
            cishu += 1
            if cishu == 2:
                filt = filt[i + 1:]
                break
    cishu = 0
    # 过滤掉左括号
    for i in range(len(filt)):
        if filt[i] == ",":
            cishu += 1
            if cishu == 2:
                filt = filt[i + 1:]
                break
    total_ans.append("for" + ',' + "_" + ',' + '_' + ',' + '_')
    # 处理S1
    cell1, cell2, cell3 = shuangmu_cal()
    # debug
    total_ans.append(cell1 + ',' + cell3 + ',' + '_' + ',' + cell2)
    total_ans.append("wh" + ',' + "_" + ',' + '_' + ',' + '_')
    # 过滤掉S1语句
    cishu = 0
    for i in range(len(filt)):
        if filt[i] == ",":
            cishu += 1
            if cishu == 8:
                filt = filt[i + 1:]
                break
    # print(filt)
    # 处理S2
    cell1, cell2, cell3 = shuangmu_cal()
    total_ans.append(str(cell1) + ',' + str(cell2) + ',' + str(cell3) + ',' + 't' + str(t_num))
    t_num += 1
    total_ans.append("do" + ',' + "t" + str(t_num - 1) + ',' + '_' + ',' + '_')
    # 过滤掉S2语句
    cishu = 0
    for i in range(len(filt)):
        if filt[i] == ",":
            cishu += 1
            if cishu == 8:
                filt = filt[i + 1:]
                break
    # 处理S3
    # 暂存S3
    temp_ = ""
    temp_a = ""
    temp_b = ""
    temp_table1, temp_num1, temp_table2, temp_num2 = danmu_cal()
    # 前置++
    if select_table(temp_table1, temp_num1) == "++":
        temp_a = str(("+" + ',' + select_table(temp_table2, temp_num2) + ',' + "1" + ',' + 't' + str(t_num)))
        # temp_ += "\n"
        temp_b = str(("=" + ',' + 't' + str(t_num) + ',' + "_" + "," + select_table(temp_table2, temp_num2)))
        t_num += 1
    # 后置++
    elif select_table(temp_table2, temp_num2) == "++":
        temp_a = str(("+" + ',' + select_table(temp_table1, temp_num1) + ',' + "1" + ',' + 't' + str(t_num)))
        # temp_ += "\n"
        temp_b = str(("=" + ',' + 't' + str(t_num) + ',' + "_" + "," + select_table(temp_table1, temp_num1)))
        t_num += 1
    # 前置--
    elif select_table(temp_table1, temp_num1) == "--":
        temp_a = str(("-" + ',' + select_table(temp_table2, temp_num2) + ',' + "1" + ',' + 't' + str(t_num)))
        # temp_ += "\n"
        temp_b = str(("=" + ',' + 't' + str(t_num) + ',' + "_" + "," + select_table(temp_table2, temp_num2)))
        t_num += 1
    # 后置--
    elif select_table(temp_table2, temp_num2) == "--":
        temp_a = ("-" + ',' + select_table(temp_table1, temp_num1) + ',' + "1" + ',' + 't' + str(t_num))
        # temp_ += "\n"
        temp_b = str(("=" + ',' + 't' + str(t_num) + ',' + "_" + "," + select_table(temp_table1, temp_num1)))
        t_num += 1
    # 处理S4
    # 处理中括号 { 就再读一行就行
    load_line = readNextLine()
    load_line = load_line.replace(" ", "")
    # print(re.match(r'<(.*),(.*)>,',load_line,re.I | re.M))
    filt = load_line
    filt = filt.replace("<", "")
    filt = filt.replace(">", "")
    # 处理完毕 开始处理S4
    # 过滤掉左括号后需要再读一行才是处理语句
    load_line = readNextLine()
    load_line = load_line.replace(" ", "")
    filt = load_line
    filt = filt.replace("<", "")
    filt = filt.replace(">", "")
    # 不匹配到右括号为止
    while cal_cooma(str(filt)) != 2:
        s_trans()
        load_line = readNextLine()
        load_line = load_line.replace(" ", "")
        filt = load_line
        filt = filt.replace("<", "")
        filt = filt.replace(">", "")
    # 处理最后
    # 别忘了添加S3
    total_ans.append(temp_a)
    total_ans.append(temp_b)
    total_ans.append("we" + ',' + '_' + ',' + '_' + ',' + '_')


def do_trans():
    global filt
    global t_num
    global do_while_ans
    global total_ans
    total_ans.append("dwh" + ',' + '_' + ',' + '_' + ',' + '_')
    cishu = 0
    # 过滤掉左中括号 { 单独是一行 要连续加载两行
    load_line = readNextLine()
    load_line = load_line.replace(" ", "")
    filt = load_line
    filt = filt.replace("<", "")
    filt = filt.replace(">", "")
    load_line = readNextLine()
    load_line = load_line.replace(" ", "")
    filt = load_line
    filt = filt.replace("<", "")
    filt = filt.replace(">", "")
    cishu = 0
    # 不匹配到右括号为止
    while cal_cooma(str(filt)) != 2:
        do_while_ans = s_trans(1)
        load_line = readNextLine()
        load_line = load_line.replace(" ", "")
        filt = load_line
        filt = filt.replace("<", "")
        filt = filt.replace(">", "")
    # ↑当前的行是右括号所在的行 要再读一行
    load_line = readNextLine()
    load_line = load_line.replace(" ", "")
    filt = load_line
    filt = filt.replace("<", "")
    filt = filt.replace(">", "")
    log_comma = 0
    temp_table = ""
    temp_num = ""
    for i in range(len(filt)):
        # 根据逗号个数匹配
        if filt[i] == ",":
            log_comma += 1
            continue
        if log_comma == 2:
            # 每当逗号数目为2 说明一个元组生成
            # -------------------------------------
            # 初始化逗号数目
            log_comma = 0
            break
        if log_comma == 0:
            temp_table += filt[i]
            continue
        if log_comma == 1:
            temp_num += filt[i]
            continue
    if select_table(temp_table, temp_num) == "while":
        temp = re.match('(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*)', filt, re.I | re.M)
        if select_table(str(temp.group(5)), str(temp.group(6))) == "!":
            total_ans.append("=" + ',' + 't' + str(t_num - 1) + "," + '_' + ',' + select_table(str(temp.group(7)),
                                                                                               str(temp.group(8))))
        else:
            total_ans.append("=" + ',' + 't' + str(t_num - 1) + "," + '_' + ',' + select_table(str(temp.group(5)),
                                                                                               str(temp.group(6))))
        while_trans()
        total_ans += do_while_ans
        total_ans.append("we" + ',' + '_' + ',' + '_' + ',' + '_')


def else_trans():
    total_ans.append("el" + ',' + '_' + ',' + '_' + ',' + '_')


# 当匹配 } 的时候启动
def you_kuohao():
    if len(we_or_re) == 0:
        return
    if str(we_or_re[-1]) == "if":
        total_ans.append("ie" + ',' + '_' + ',' + '_' + ',' + '_')
        we_or_re.pop()
    # 记得弹出去
    elif str(we_or_re[-1]) == "while":
        total_ans.append("we" + ',' + '_' + ',' + '_' + ',' + '_')
        we_or_re.pop()


# 正则表达式匹配 每次读程序的一行
def re_pipei():
    # 过滤后的文字
    global filt
    load_line = readNextLine()
    # 当还有行没读完
    while len(load_line) != 0:
        load_line = load_line.replace(" ", "")
        # print(re.match(r'<(.*),(.*)>,',load_line,re.I | re.M))
        # filt = re.match(r'<(.*),(.*)>,', load_line, re.I | re.M)
        # filt = str(filt.group())
        filt = load_line
        filt = filt.replace("<", "")
        filt = filt.replace(">", "")
        # print(filt)
        # 过滤结束
        temp_table = ""
        temp_num = ""
        log_comma = 0
        for i in range(len(filt)):
            # 根据逗号个数匹配
            if filt[i] == ",":
                log_comma += 1
                continue
            if log_comma == 2:
                # 每当逗号数目为2 说明一个元组生成
                # -------------------------------------
                # 初始化逗号数目
                log_comma = 0
                break
            if log_comma == 0:
                temp_table += filt[i]
                continue
            if log_comma == 1:
                temp_num += filt[i]
                continue
        # print("翻译后：", whole_sentence(), "\n")
        # print(temp_table)
        # print(temp_num,"111")
        if select_table(temp_table, temp_num) == "if":
            if_trans()
        elif select_table(temp_table, temp_num) == "do":
            do_trans()
        elif select_table(temp_table, temp_num) == "}":
            you_kuohao()
        elif select_table(temp_table, temp_num) == "while":
            # 入栈在主函数入栈
            we_or_re.append("while")
            while_trans()
        elif select_table(temp_table, temp_num) == "else":
            else_trans()
        elif select_table(temp_table, temp_num) == "for":
            for_trans()
        elif cal_cooma(filt) <= 2:
            # 没用的语句
            haha = cal_cooma(filt)
        else:
            s_trans()
        # 读入下一行
        load_line = readNextLine()
        # 当只剩下换行符号 就退出
        if len(load_line) == 1:
            break

    # print(load_line)
    # print(filt)


def siyuanshi_jiekou(strr):
    # strr是下面这个形式
    # strr = ['*,4,3,t0', '+,t0,2,t1', '=,t1,_,change1', '=,0,_,change3']
    lis = []
    total = []
    for i in strr:
        temp = re.match('(.*?),(.*?),(.*?),(.*)', i, re.I | re.M)
        cell1 = str(temp.group(1))
        cell2 = str(temp.group(2))
        cell3 = str(temp.group(3))
        cell4 = str(temp.group(4))
        lis.append(cell1)
        lis.append(cell2)
        lis.append(cell3)
        lis.append(cell4)
        total.append(lis)
        lis = []
        # print(total)
    return total


def init_gene():
    global iT, cT, sT, CT, KT, PT, FT
    iT = words_analysis.iT
    cT = words_analysis.cT
    sT = words_analysis.sT
    CT = words_analysis.CT
    KT = words_analysis.KT
    PT = words_analysis.PT
    FT = words_analysis.FT


# 按照格式规范 这是启动按钮
def start(token):
    global ans
    global total_ans
    global TOKEN
    init_gene()
    TOKEN = token.splitlines()
    TOKEN.append("\n")
    re_pipei()
    ans = siyuanshi_jiekou(total_ans)
    return total_ans, ans


if __name__ == "__main__":
    start()
    # print(total_ans)
    # print("最终结果如下：\n")
    # for i in total_ans:
    # print(i,"\n")
