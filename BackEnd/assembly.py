# !/usr/bin/python
# -*- coding: UTF-8 -*-
# ------------------------------------------
#           2020-7-9
# ------------------------------------------
#           初极版本1.0
# ------------------------------------------
# 原定c输入r输出


# 用户定义变量和临时变量的活跃信息表 以及每行的数据的活跃信息
user_var = {}
temp_var = {}
row_active = []
# 记录ax中的信息
ax_ = {}
# 记录bx中的信息
bx_ = {}
# 跳转语句序号
else_num = 0
wh_num = 0
for_num = 0
part1 = []
part2 = []
# 记录语句前面的标号
jishu = 0


# 生成汇编和优化四元式接口转化
def jiekou_aim(strr):
    # 格式如下：
    # a = [['function', 'main', '_', '_'], ['=', '10.0', '_', 'b'], ['=', '15.0', '_', 'c'], ['=', '30.0', '_', 'd']]
    temp = {}
    for i in range(len(strr)):
        temp[i + 1] = strr[i]
    return temp


# 返回true说明不用考虑 直接写入ax就行
def search_act(hang, strr):
    global ax_
    global row_active
    if len(ax_) == 0:
        return True
    for i in range(len(strr) - 1):
        # 当前寄存器中和当前语句有重复的元素 更新活跃信息
        if strr[i] == list(ax_)[-1]:
            ax_[list(ax_)[-1]] = row_active[hang][i]
            break
    if len(ax_) == 0 or ax_[list(ax_)[-1]] == "n":
        return True
    if ax_[list(ax_)[-1]] == "y":
        return False


def search_act2(hang, strr):
    global bx_
    global row_active
    if len(bx_) == 0:
        return True
    for i in range(len(strr) - 1):
        # 当前寄存器中和当前语句有重复的元素 更新活跃信息
        if strr[i] == list(bx_)[-1]:
            bx_[list(bx_)[-1]] = row_active[hang][i]
            break
    if len(bx_) == 0 or bx_[list(bx_)[-1]] == "n":
        return True
    if bx_[list(bx_)[-1]] == "y":
        return False


# 记录每行的活跃信息，放在row_active里面 先运行这个函数
def huoyue(strr, variate_name_list):
    global user_var
    global temp_var
    global row_active
    # 第一个是用户定义变量，第二个是临时变量
    for i in variate_name_list[0]:
        # 不用担心重复
        user_var[str(i)] = "y"
    for i in variate_name_list[1]:
        temp_var[str(i)] = "n"
    # print(user_var)
    # print(temp_var)
    # 逆序访问
    temp_list = []
    for i in range(0, strr.__len__())[::-1]:
        # print(strr[i][3])
        temp_list = []
        for j in range(0, 4)[::-1]:
            # print(j)
            # 在最后一位列表就变成n
            if j == 3:
                if strr[i][j] in user_var:
                    temp_list.append(user_var[str(strr[i][j])])
                    user_var[str(strr[i][j])] = "n"
                elif strr[i][j] in temp_var:
                    temp_list.append(temp_var[str(strr[i][j])])
                    temp_var[str(strr[i][j])] = "n"
                else:
                    temp_list.append("_")
                # print(temp_list)
            else:
                if strr[i][j] in user_var:
                    temp_list.append(user_var[str(strr[i][j])])
                    user_var[str(strr[i][j])] = "y"
                elif strr[i][j] in temp_var:
                    temp_list.append(temp_var[str(strr[i][j])])
                    temp_var[str(strr[i][j])] = "y"
                else:
                    temp_list.append("_")
            # 记得反转
            # print(temp_list)
        temp_list.reverse()
        row_active.append(temp_list)
    row_active.reverse()
    # print(temp_var)
    # print(user_var)


# variate_name_list是两个的加和
def make_assembly(four_dict, variate_name_list):
    # CX用于循环 AX存储变量 BX和DX用于函数 DX是输出 BX是形参
    # print(variate_name_list)
    # print(len(four_dict))
    global else_num
    global wh_num
    global for_num
    global part1
    global part2
    global jishu
    four_len = len(four_dict)
    part1 = ["assume cs:code,ds:dseg", "dseg segment"]
    # 声明变量部分
    for si in variate_name_list:
        st = "\t" + si + " dw 0"
        part1.append(st)
    part1.append("dseg ends")

    # 代码块
    # 将数据段段地址装入AX寄存器
    part2 = ["code segment", "start:", "\tmov ax,dseg", "\tmov ds,ax"]

    # 正式进入
    # 忽略标识
    flag = 0
    for si in four_dict:
        # flag == 1 说明是可忽略部分
        if flag == 1:
            flag = 0
            continue

        # 下面这个太磨叽了
        # 函数语句
        if four_dict[si][0] == "function":
            part2.append(four_dict[si][1] + "\tproc")
            while four_dict[si][0] != "end":
                # 赋值语句 怎么感觉我写错了啊
                if four_dict[si][0] == "=":
                    # 需要考虑活跃信息
                    # 可以直接填写
                    if search_act2(si, four_dict[si]) == True:
                        part2.append("L" + str(jishu) + ":\tmov " + "bx " + "," + four_dict[si][1])
                        jishu += 1
                        # 记得更新bx中的值
                        bx_[str(four_dict[si][3])] = str(row_active[si][3])
                    # 不可以直接写 就先替换出去
                    elif search_act2(si, four_dict[si]) == False:
                        part2.append("\tmov " + str(bx_[list(bx_)[-1]]) + "," + "bx")
                        part2.append("L" + str(jishu) + ":\tmov " + "bx " + "," + four_dict[si][1])
                        jishu += 1
                        bx_[str(four_dict[si][3])] = str(row_active[si][3])
                    # part2.append("L" + str(jishu) + ":" + "\tmov bx," + four_dict[si][1])
                    # part2.append("\tmov " + four_dict[si][3] + ",bx")

                # 加法语句
                if four_dict[si][0] == "+":
                    # 需要考虑活跃信息
                    # 可以直接填写
                    if search_act2(si, four_dict[si]) == True:
                        part2.append("L" + str(jishu) + ":\tmov " + "bx " + "," + four_dict[si][1])
                        jishu += 1
                        part2.append("\tadd " + "bx " + "," + four_dict[si][2])
                        # 记得更新bx中的值
                        bx_[str(four_dict[si][3])] = str(row_active[si][3])
                    # 不可以直接写 就先替换出去
                    elif search_act2(si, four_dict[si]) == False:
                        part2.append("\tmov " + str(bx_[list(bx_)[-1]]) + "," + "bx")
                        part2.append("L" + str(jishu) + ":\tmov " + "bx " + "," + four_dict[si][1])
                        jishu += 1
                        part2.append("\tadd " + "bx " + "," + four_dict[si][2])
                        bx_[str(four_dict[si][3])] = str(row_active[si][3])

                # 减法语句
                elif four_dict[si][0] == "-":
                    # 需要考虑活跃信息
                    # 可以直接填写
                    if search_act2(si, four_dict[si]) == True:
                        part2.append("L" + str(jishu) + ":\tmov " + "bx " + "," + four_dict[si][1])
                        jishu += 1
                        part2.append("\tsub " + "bx " + "," + four_dict[si][2])
                        # 记得更新bx中的值
                        bx_[str(four_dict[si][3])] = str(row_active[si][3])
                    # 不可以直接写 就先替换出去
                    elif search_act2(si, four_dict[si]) == False:
                        part2.append("\tmov " + str(bx_[list(bx_)[-1]]) + "," + "bx")
                        part2.append("L" + str(jishu) + ":\tmov " + "bx " + "," + four_dict[si][1])
                        jishu += 1
                        part2.append("\tsub " + "bx " + "," + four_dict[si][2])
                        bx_[str(four_dict[si][3])] = str(row_active[si][3])

                # 乘法语句
                elif four_dict[si][0] == "*":
                    # 需要考虑活跃信息
                    # 可以直接填写
                    if search_act2(si, four_dict[si]) == True:
                        part2.append("L" + str(jishu) + ":\tmov " + "bx " + "," + four_dict[si][1])
                        jishu += 1
                        part2.append("\tmul " + "bx " + "," + four_dict[si][2])
                        # 记得更新bx中的值
                        bx_[str(four_dict[si][3])] = str(row_active[si][3])
                    # 不可以直接写 就先替换出去
                    elif search_act2(si, four_dict[si]) == False:
                        part2.append("\tmov " + str(bx_[list(bx_)[-1]]) + "," + "bx")
                        part2.append("L" + str(jishu) + ":\tmov " + "bx " + "," + four_dict[si][1])
                        jishu += 1
                        part2.append("\tmul " + "bx " + "," + four_dict[si][2])
                        bx_[str(four_dict[si][3])] = str(row_active[si][3])

                # 除法语句
                elif four_dict[si][0] == "/":
                    # 需要考虑活跃信息
                    # 可以直接填写
                    if search_act2(si, four_dict[si]) == True:
                        part2.append("L" + str(jishu) + ":\tmov " + "bx " + "," + four_dict[si][1])
                        jishu += 1
                        part2.append("\tdiv " + "bx " + "," + four_dict[si][2])
                        # 记得更新bx中的值
                        bx_[str(four_dict[si][3])] = str(row_active[si][3])
                    # 不可以直接写 就先替换出去
                    elif search_act2(si, four_dict[si]) == False:
                        part2.append("\tmov " + str(bx_[list(bx_)[-1]]) + "," + "bx")
                        part2.append("L" + str(jishu) + ":\tmov " + "bx " + "," + four_dict[si][1])
                        jishu += 1
                        part2.append("\tdiv " + "bx " + "," + four_dict[si][2])
                        bx_[str(four_dict[si][3])] = str(row_active[si][3])

                # 或语句
                elif four_dict[si][0] == "|":
                    # 需要考虑活跃信息
                    # 可以直接填写
                    if search_act2(si, four_dict[si]) == True:
                        part2.append("L" + str(jishu) + ":\tmov " + "bx " + "," + four_dict[si][1])
                        jishu += 1
                        part2.append("\tor " + "bx " + "," + four_dict[si][2])
                        # 记得更新bx中的值
                        bx_[str(four_dict[si][3])] = str(row_active[si][3])
                    # 不可以直接写 就先替换出去
                    elif search_act2(si, four_dict[si]) == False:
                        part2.append("\tmov " + str(bx_[list(bx_)[-1]]) + "," + "bx")
                        part2.append("L" + str(jishu) + ":\tmov " + "bx " + "," + four_dict[si][1])
                        jishu += 1
                        part2.append("\tor " + "bx " + "," + four_dict[si][2])
                        bx_[str(four_dict[si][3])] = str(row_active[si][3])

                # 与语句
                elif four_dict[si][0] == "&":
                    # 需要考虑活跃信息
                    # 可以直接填写
                    if search_act2(si, four_dict[si]) == True:
                        part2.append("L" + str(jishu) + ":\tmov " + "bx " + "," + four_dict[si][1])
                        jishu += 1
                        part2.append("\tand " + "bx " + "," + four_dict[si][2])
                        # 记得更新bx中的值
                        bx_[str(four_dict[si][3])] = str(row_active[si][3])
                    # 不可以直接写 就先替换出去
                    elif search_act2(si, four_dict[si]) == False:
                        part2.append("\tmov " + str(bx_[list(bx_)[-1]]) + "," + "bx")
                        part2.append("L" + str(jishu) + ":\tmov " + "bx " + "," + four_dict[si][1])
                        jishu += 1
                        part2.append("\tand " + "bx " + "," + four_dict[si][2])
                        bx_[str(four_dict[si][3])] = str(row_active[si][3])
                si += 1
            part2.append("\tmov " + "dx " + ",bx")
            part2.append("endp")

        # 函数赋值语句 end
        if four_dict[si][0] == "jump":
            part2.append("call\t" + four_dict[si][3])
            # 忽略下个赋值语句
            flag = 1
            # dx用于输出
            # 需要考虑活跃信息
            # 可以直接填写
            if search_act(si, four_dict[si]) == True:
                part2.append("L" + str(jishu) + ":\tmov " + "bx " + "," + four_dict[si][1])
                jishu += 1
                part2.append("\tand " + "bx " + "," + four_dict[si][2])
                # 记得更新bx中的值
                bx_[str(four_dict[si][3])] = str(row_active[si][3])
            # 不可以直接写 就先替换出去
            elif search_act(si, four_dict[si]) == False:
                part2.append("\tmov " + str(bx_[list(bx_)[-1]]) + "," + "bx")
                part2.append("L" + str(jishu) + ":\tmov " + "bx " + "," + four_dict[si][1])
                jishu += 1
                part2.append("\tand " + "bx " + "," + four_dict[si][2])
                bx_[str(four_dict[si][3])] = str(row_active[si][3])

        # 这个是不是我写错了啊啊啊！！！！！！！！！！！！！！！！！！！！-----------------------------------------------------
        # 赋值语句入口
        # ['=', '3', '/', 'a']
        if four_dict[si][0] == "=":
            # 需要考虑活跃信息
            # 可以直接填写
            if search_act(si, four_dict[si]) == True:
                part2.append("L" + str(jishu) + ":\tmov " + "ax " + "," + four_dict[si][1])
                jishu += 1
                # 记得更新ax中的值
                ax_[str(four_dict[si][3])] = str(row_active[si][3])
            # 不可以直接写 就先替换出去
            elif search_act(si, four_dict[si]) == False:
                part2.append("\tmov " + str(list(ax_)[-1]) + "," + "ax")
                part2.append("L" + str(jishu) + ":\tmov " + "ax " + "," + four_dict[si][1])
                jishu += 1
                ax_[str(four_dict[si][3])] = str(row_active[si][3])
            # part2.append("L" + str(jishu) + ":" + "\tmov ax," + four_dict[si][1])
            # part2.append("\tmov " + four_dict[si][3] + ",ax")

        # if-else end
        elif four_dict[si][0] == "if":
            # 之前的ax存放的是判断信息
            part2.append("\tand " + "ax," + "ax")
            # 如果判断结果为0: 写跳转语句
            part2.append("\tjz " + "else" + str(else_num))

        # else end
        elif four_dict[si][0] == "el":
            # 在这之前让判断正确的语句跳转过去
            part2.append("\tjmp " + "L" + str(si + 1))
            part2.append("else" + str(else_num) + ":")
            else_num += 1

        # ie end  不用执行汇编语言
        elif four_dict[si][0] == "ie":
            part2.append("\tjmp " + "L" + str(jishu))
            part2.append("else" + str(else_num) + ":")
            else_num += 1
            continue

        # wh  不用执行汇编语言 但要接一个标号
        elif four_dict[si][0] == "wh":
            part2.append("while" + str(wh_num) + ":")
            continue

            # 这个巨难写！！！ do-while----------------------------------------------------------------------------------
        elif four_dict[si][0] == "dwh":
            temp_si = si  # 记录si位置 方便回溯
            # 搜索到do
            while four_dict[si][0] != "do":
                si += 1
            # 跳过do
            si += 1
            while four_dict[si][0] != "end":
                # 赋值语句 怎么感觉我写错了啊
                if four_dict[si][0] == "=":
                    # 需要考虑活跃信息
                    # 可以直接填写
                    if search_act(si, four_dict[si]) == True:
                        part2.append("L" + str(jishu) + ":\tmov " + "ax " + "," + four_dict[si][1])
                        jishu += 1
                        # 记得更新ax中的值
                        ax_[str(four_dict[si][3])] = str(row_active[si][3])
                    # 不可以直接写 就先替换出去
                    elif search_act(si, four_dict[si]) == False:
                        part2.append("\tmov " + str(list(ax_)[-1]) + "," + "ax")
                        part2.append("L" + str(jishu) + ":\tmov " + "ax " + "," + four_dict[si][1])
                        jishu += 1
                        ax_[str(four_dict[si][3])] = str(row_active[si][3])
                    # part2.append("L" + str(jishu) + ":" + "\tmov ax," + four_dict[si][1])
                    # part2.append("\tmov " + four_dict[si][3] + ",ax")

                # 加法语句
                if four_dict[si][0] == "+":
                    # 需要考虑活跃信息
                    # 可以直接填写
                    if search_act(si, four_dict[si]) == True:
                        part2.append("L" + str(jishu) + ":\tmov " + "ax " + "," + four_dict[si][1])
                        jishu += 1
                        part2.append("\tadd " + "ax " + "," + four_dict[si][2])
                        # 记得更新ax中的值
                        ax_[str(four_dict[si][3])] = str(row_active[si][3])
                    # 不可以直接写 就先替换出去
                    elif search_act(si, four_dict[si]) == False:
                        part2.append("\tmov " + str(list(ax_)[-1]) + "," + "ax")
                        part2.append("L" + str(jishu) + ":\tmov " + "ax " + "," + four_dict[si][1])
                        jishu += 1
                        part2.append("\tadd " + "ax " + "," + four_dict[si][2])
                        ax_[str(four_dict[si][3])] = str(row_active[si][3])

                # 减法语句
                elif four_dict[si][0] == "-":
                    # 需要考虑活跃信息
                    # 可以直接填写
                    if search_act(si, four_dict[si]) == True:
                        part2.append("L" + str(jishu) + ":\tmov " + "ax " + "," + four_dict[si][1])
                        jishu += 1
                        part2.append("\tsub " + "ax " + "," + four_dict[si][2])
                        # 记得更新ax中的值
                        ax_[str(four_dict[si][3])] = str(row_active[si][3])
                    # 不可以直接写 就先替换出去
                    elif search_act(si, four_dict[si]) == False:
                        part2.append("\tmov " + str(list(ax_)[-1]) + "," + "ax")
                        part2.append("L" + str(jishu) + ":\tmov " + "ax " + "," + four_dict[si][1])
                        jishu += 1
                        part2.append("\tsub " + "ax " + "," + four_dict[si][2])
                        ax_[str(four_dict[si][3])] = str(row_active[si][3])

                # 乘法语句
                elif four_dict[si][0] == "*":
                    # 需要考虑活跃信息
                    # 可以直接填写
                    if search_act(si, four_dict[si]) == True:
                        part2.append("L" + str(jishu) + ":\tmov " + "ax " + "," + four_dict[si][1])
                        jishu += 1
                        part2.append("\tmul " + "ax " + "," + four_dict[si][2])
                        # 记得更新ax中的值
                        ax_[str(four_dict[si][3])] = str(row_active[si][3])
                    # 不可以直接写 就先替换出去
                    elif search_act(si, four_dict[si]) == False:
                        part2.append("\tmov " + str(list(ax_)[-1]) + "," + "ax")
                        part2.append("L" + str(jishu) + ":\tmov " + "ax " + "," + four_dict[si][1])
                        jishu += 1
                        part2.append("\tmul " + "ax " + "," + four_dict[si][2])
                        ax_[str(four_dict[si][3])] = str(row_active[si][3])

                # 除法语句
                elif four_dict[si][0] == "/":
                    # 需要考虑活跃信息
                    # 可以直接填写
                    if search_act(si, four_dict[si]) == True:
                        part2.append("L" + str(jishu) + ":\tmov " + "ax " + "," + four_dict[si][1])
                        jishu += 1
                        part2.append("\tdiv " + "ax " + "," + four_dict[si][2])
                        # 记得更新ax中的值
                        ax_[str(four_dict[si][3])] = str(row_active[si][3])
                    # 不可以直接写 就先替换出去
                    elif search_act(si, four_dict[si]) == False:
                        part2.append("\tmov " + str(list(ax_)[-1]) + "," + "ax")
                        part2.append("L" + str(jishu) + ":\tmov " + "ax " + "," + four_dict[si][1])
                        jishu += 1
                        part2.append("\tdiv " + "ax " + "," + four_dict[si][2])
                        ax_[str(four_dict[si][3])] = str(row_active[si][3])

                # 或语句
                elif four_dict[si][0] == "|":
                    # 需要考虑活跃信息
                    # 可以直接填写
                    if search_act(si, four_dict[si]) == True:
                        part2.append("L" + str(jishu) + ":\tmov " + "ax " + "," + four_dict[si][1])
                        jishu += 1
                        part2.append("\tor " + "ax " + "," + four_dict[si][2])
                        # 记得更新ax中的值
                        ax_[str(four_dict[si][3])] = str(row_active[si][3])
                    # 不可以直接写 就先替换出去
                    elif search_act(si, four_dict[si]) == False:
                        part2.append("\tmov " + str(list(ax_)[-1]) + "," + "ax")
                        part2.append("L" + str(jishu) + ":\tmov " + "ax " + "," + four_dict[si][1])
                        jishu += 1
                        part2.append("\tor " + "ax " + "," + four_dict[si][2])
                        ax_[str(four_dict[si][3])] = str(row_active[si][3])

                # 与语句
                elif four_dict[si][0] == "&":
                    # 需要考虑活跃信息
                    # 可以直接填写
                    if search_act(si, four_dict[si]) == True:
                        part2.append("L" + str(jishu) + ":\tmov " + "ax " + "," + four_dict[si][1])
                        jishu += 1
                        part2.append("\tand " + "ax " + "," + four_dict[si][2])
                        # 记得更新ax中的值
                        ax_[str(four_dict[si][3])] = str(row_active[si][3])
                    # 不可以直接写 就先替换出去
                    elif search_act(si, four_dict[si]) == False:
                        part2.append("\tmov " + str(list(ax_)[-1]) + "," + "ax")
                        part2.append("L" + str(jishu) + ":\tmov " + "ax " + "," + four_dict[si][1])
                        jishu += 1
                        part2.append("\tand " + "ax " + "," + four_dict[si][2])
                        ax_[str(four_dict[si][3])] = str(row_active[si][3])
                si += 1
            # 回去
            si = temp_si
            # continue

        # while
        elif four_dict[si][0] == "do":
            # 之前的ax存放的是判断信息
            part2.append("\tand " + "ax," + "ax")
            # 如果判断结果为0: 写跳转语句
            # part2.append("\tjz " + "else" + str(else_num))

        elif four_dict[si][0] == "we":
            # 回到判断语句
            part2.append("\tjmp " + "while" + str(wh_num))
            part2.append("else" + str(else_num) + ":")
            else_num += 1
            wh_num += 1

        elif four_dict[si][0] == "for":
            # 不需要输出
            continue

        # 小于号语句
        elif four_dict[si][0] == "<":
            if list(ax_)[-1] != four_dict[si][1]:
                part2.append("L" + str(jishu) + ":\tcmp " + four_dict[si][1] + "," + four_dict[si][2])
                jishu += 1
            else:
                part2.append("L" + str(jishu) + ":\tcmp " + "ax" + "," + four_dict[si][2])
                jishu += 1
            part2.append("\tjnb " + "else" + str(else_num))
            # 忽略下一句
            flag = 1

        # 大于号语句
        elif four_dict[si][0] == ">":
            if list(ax_)[-1] != four_dict[si][1]:
                part2.append("L" + str(jishu) + ":\tcmp " + four_dict[si][1] + "," + four_dict[si][2])
                jishu += 1
            else:
                part2.append("L" + str(jishu) + ":\tcmp " + "ax" + "," + four_dict[si][2])
                jishu += 1
            part2.append("\tjna " + "else" + str(else_num))
            # flag = 1  # 忽略下一句

        # 小于等于号语句
        elif four_dict[si][0] == "<=":
            if list(ax_)[-1] != four_dict[si][1]:
                part2.append("L" + str(jishu) + ":\tcmp " + four_dict[si][1] + "," + four_dict[si][2])
                jishu += 1
            else:
                part2.append("L" + str(jishu) + ":\tcmp " + "ax" + "," + four_dict[si][2])
                jishu += 1
            part2.append("\tja " + "else" + str(else_num))
            # 忽略下一句
            flag = 1

        # 大于等于号语句
        elif four_dict[si][0] == ">=":
            if list(ax_)[-1] != four_dict[si][1]:
                part2.append("L" + str(jishu) + ":\tcmp " + four_dict[si][1] + "," + four_dict[si][2])
                jishu += 1
            else:
                part2.append("L" + str(jishu) + ":\tcmp " + "ax" + "," + four_dict[si][2])
                jishu += 1
            part2.append("\tjb " + "else" + str(else_num))
            # flag = 1  # 忽略下一句

        # 加法语句
        elif four_dict[si][0] == "+":
            # 需要考虑活跃信息
            # 可以直接填写
            if search_act(si, four_dict[si]) == True:
                part2.append("L" + str(jishu) + ":\tmov " + "ax " + "," + four_dict[si][1])
                jishu += 1
                part2.append("\tadd " + "ax " + "," + four_dict[si][2])
                # 记得更新ax中的值
                ax_[str(four_dict[si][3])] = str(row_active[si][3])
            # 不可以直接写 就先替换出去
            else:
                part2.append("\tmov " + str(list(ax_)[-1]) + "," + "ax")
                part2.append("L" + str(jishu) + ":\tmov " + "ax " + "," + four_dict[si][1])
                jishu += 1
                part2.append("\tadd " + "ax " + "," + four_dict[si][2])
                ax_[str(four_dict[si][3])] = str(row_active[si][3])

        # 减法语句
        elif four_dict[si][0] == "-":
            # 需要考虑活跃信息
            # 可以直接填写
            if search_act(si, four_dict[si]) == True:
                part2.append("L" + str(jishu) + ":\tmov " + "ax " + "," + four_dict[si][1])
                jishu += 1
                part2.append("\tsub " + "ax " + "," + four_dict[si][2])
                # 记得更新ax中的值
                ax_[str(four_dict[si][3])] = str(row_active[si][3])
            # 不可以直接写 就先替换出去
            else:
                part2.append("\tmov " + str(list(ax_)[-1]) + "," + "ax")
                part2.append("L" + str(jishu) + ":\tmov " + "ax " + "," + four_dict[si][1])
                jishu += 1
                part2.append("\tsub " + "ax " + "," + four_dict[si][2])
                ax_[str(four_dict[si][3])] = str(row_active[si][3])

        # 乘法语句
        elif four_dict[si][0] == "*":
            # 需要考虑活跃信息
            # 可以直接填写
            if search_act(si, four_dict[si]) == True:
                part2.append("L" + str(jishu) + ":\tmov " + "ax " + "," + four_dict[si][1])
                jishu += 1
                part2.append("\tmul " + "ax " + "," + four_dict[si][2])
                # 记得更新ax中的值
                ax_[str(four_dict[si][3])] = str(row_active[si][3])
            # 不可以直接写 就先替换出去
            else:
                part2.append("\tmov " + str(list(ax_)[-1]) + "," + "ax")
                part2.append("L" + str(jishu) + ":\tmov " + "ax " + "," + four_dict[si][1])
                jishu += 1
                part2.append("\tmul " + "ax " + "," + four_dict[si][2])
                ax_[str(four_dict[si][3])] = str(row_active[si][3])

        # 除法语句
        elif four_dict[si][0] == "/":
            # 需要考虑活跃信息
            # 可以直接填写
            if search_act(si, four_dict[si]) == True:
                part2.append("L" + str(jishu) + ":\tmov " + "ax " + "," + four_dict[si][1])
                jishu += 1
                part2.append("\tdiv " + "ax " + "," + four_dict[si][2])
                # 记得更新ax中的值
                ax_[str(four_dict[si][3])] = str(row_active[si][3])
            # 不可以直接写 就先替换出去
            else:
                part2.append("\tmov " + str(list(ax_)[-1]) + "," + "ax")
                part2.append("L" + str(jishu) + ":\tmov " + "ax " + "," + four_dict[si][1])
                jishu += 1
                part2.append("\tdiv " + "ax " + "," + four_dict[si][2])
                ax_[str(four_dict[si][3])] = str(row_active[si][3])
        # 或语句
        elif four_dict[si][0] == "|":
            # 需要考虑活跃信息
            # 可以直接填写
            if search_act(si, four_dict[si]) == True:
                part2.append("L" + str(jishu) + ":\tmov " + "ax " + "," + four_dict[si][1])
                jishu += 1
                part2.append("\tor " + "ax " + "," + four_dict[si][2])
                # 记得更新ax中的值
                ax_[str(four_dict[si][3])] = str(row_active[si][3])
            # 不可以直接写 就先替换出去
            else:
                part2.append("\tmov " + str(list(ax_)[-1]) + "," + "ax")
                part2.append("L" + str(jishu) + ":\tmov " + "ax " + "," + four_dict[si][1])
                jishu += 1
                part2.append("\tor " + "ax " + "," + four_dict[si][2])
                ax_[str(four_dict[si][3])] = str(row_active[si][3])
        # 与语句
        elif four_dict[si][0] == "&":
            # 需要考虑活跃信息
            # 可以直接填写
            if search_act(si, four_dict[si]) == True:
                part2.append("L" + str(jishu) + ":\tmov " + "ax " + "," + four_dict[si][1])
                jishu += 1
                part2.append("\tand " + "ax " + "," + four_dict[si][2])
                # 记得更新ax中的值
                ax_[str(four_dict[si][3])] = str(row_active[si][3])
            # 不可以直接写 就先替换出去
            else:
                part2.append("\tmov " + str(list(ax_)[-1]) + "," + "ax")
                part2.append("L" + str(jishu) + ":\tmov " + "ax " + "," + four_dict[si][1])
                jishu += 1
                part2.append("\tand " + "ax " + "," + four_dict[si][2])
                ax_[str(four_dict[si][3])] = str(row_active[si][3])

        # RJ 不用实现
        elif four_dict[si][0] == "RJ":
            part2.append("L" + str(jishu) + ":" + "\tjmp short " + "L" + str(four_dict[si][1]))
            jishu += 1

        # 输入语句
        elif four_dict[si][0] == "scanf":
            part2.append("L" + str(jishu) + ":" + "\tmov ah,01h")
            jishu += 1
            part2.append("\tint 21h")
            part2.append("\tmov " + four_dict[si][1] + ",al")

        # 输出语句
        elif four_dict[si][0] == "print":
            part2.append("L" + str(jishu) + ":" + "\tmov dl," + four_dict[si][1])
            jishu += 1
            part2.append("\tmov ah,2")
            part2.append("\tint 21h")

        elif four_dict[si][0] == "end" and four_dict[si][1] == "main":
            part2.append("L" + str(jishu) + ":\tmov ax,4c00h")
            jishu += 1
            part2.append("\tint 21h")

    # 收尾
    part2.append("mov ax,4c00h")
    part2.append("int 21h")
    part2.append("code ends")
    part2.append("end start")
    total = part1 + part2
    out_assembly = []
    for si in total:
        # print(si)
        out_assembly.append(si + "\n")
    # 去掉小数点吗
    # out_assembly = list(out_assembly)
    ##存储汇编
    return out_assembly
    '''
    four_file = open("assembly.txt", "w+")
    four_file.writelines(out_assembly)
    four_file.close()
    '''


def start(ulist0, ulist_v0):
    siyuanshi = jiekou_aim(ulist0)
    var_table = ulist_v0[0] + ulist_v0[1]
    huoyue(ulist0, ulist_v0)
    resu = make_assembly(siyuanshi, var_table)
    return resu


if __name__ == "__main__":
    start()
