# 符号表定义与生成
# ------- 2020.7.9 -------------
# 完成debug，测试多基本块通过
# ------------------------------

# !/usr/bin/python
# -*- coding: UTF-8 -*-

from WordAnalysis import words_analysis

# 2020-6-27
# 符号表组织 整体框架
# bool:1    int:2   float:4     double:8    char:1

# 类型代码字典
tval_dic = {"i": "整型", "r": "实型", "c": "字符型", "b": "布尔型", "a": "数组型", "d": "结构型"}

# 种类代码字典
cat_dic = {"f": "函数", "c": "常量", "t": "类型", "d": "域名",
           "v": "变量", "vn": "换名形参", "vf": "赋值形参"}

# 标识符表
iT = words_analysis.iT
# 字符表
cT = words_analysis.cT
# 字符串表
sT = words_analysis.sT
# 常数表
CT = words_analysis.CT
# 关键字表
KT = words_analysis.KT
# 界符表
PT = words_analysis.PT
# 函数名表
FT = words_analysis.FT


class SymbolError(Exception):
    def __init__(self, ErrorInfo):
        super().__init__(self)  # 初始化父类
        self.error_info = ErrorInfo

    def __str__(self):
        return self.error_info


# 符号表synbl
class SynblTable:
    # 名字 类型 种类 地址
    def __init__(self, name_, type_, cat_, addr_):
        self.name_ = name_
        self.type_ = type_
        self.cat_ = cat_
        self.addr_ = addr_


# 类型表 typel
class Typel:
    # 类码 指针
    def __init__(self, tval_, tpoint_):
        self.tval_ = tval_
        self.tpoint_ = tpoint_


# 数组表 ainfl
class Ainfl:
    # 下界 上界 成分类型指针 成分长度
    def __init__(self, low_, up_, ctp_, clen_):
        self.low_ = low_
        self.up_ = up_
        self.ctp_ = ctp_
        self.clen_ = clen_


# 结构表
class Rinfl:
    # 结构域名 区距 域成分类型指针
    def __init__(self, id_, off_, tp_):
        self.id_ = id_
        self.off_ = off_
        self.tp_ = tp_


# 函数表
class Pfinfl:
    # 函数名（自己增加） 层次号 区距 参数个数 入口地址 参数表
    def __init__(self, level_, off_, fn_, entry_, param_):
        self.level_ = level_
        self.off_ = off_
        self.fn_ = fn_
        self.entry_ = entry_
        self.param_ = param_


# 参数表
class Parameter:
    # 名字 类型 种类 地址
    def __init__(self, name_, type_, cat_, addr_):
        self.name_ = name_
        self.type_ = type_
        self.cat_ = cat_
        self.addr_ = addr_


# 常量表
class Consl:
    def __init__(self, value_):
        self.value_ = value_


# 长度表
class Lenl:
    def __init__(self, length_):
        self.length_ = length_


# 活动记录
class Vall:
    def __init__(self, oldsp_, backadd_, total_display_, param_num_,
                 formal_unit_, display_table_, local_variable_):
        self.oldsp_ = oldsp_
        self.backadd_ = backadd_
        self.total_display_ = total_display_
        self.param_num_ = param_num_
        self.formal_unit_ = formal_unit_
        self.display_table_ = display_table_
        self.local_variable_ = local_variable_


# Display表
class Display:
    def __init__(self, details_):
        self.details_ = details_


# 形式单元
class Formal_unit:
    def __init__(self, details_):
        self.details_ = details_


# 局部变量
class Local_variable:
    def __init__(self, details_):
        self.details_ = details_


# Display表、形式单元、局部变量为活动记录的相关类
# 编译过程中，不对活动记录进行填写
# 此处仅定义出其结构


def addiT(list_line, place_kt, num_kt, function_symbol_table, CAT):
    # 变量处理

    # 储存该行token串的列表
    # 记录变量类型的字符在列表中位置
    # 变量类型在KT中存储的位置
    # 本函数下的符号表
    # 变量种类，从标识符传进则为'v'，从函数参数传入

    # 标识符前带变量类型必为定义  此文法中不存在对变量的声明

    # 变量名称
    va_num = int(list_line[place_kt + 3]) - 1
    va = iT[va_num]

    for oldiT in function_symbol_table:
        if oldiT.name_ == va:
            raise SymbolError('变量重定义')

    # 变量类型
    if num_kt == 2:
        type_a = 'itp'
        a_len = 2
    elif num_kt == 3:
        type_a = 'ctp'
        a_len = 1
    elif num_kt == 4:
        type_a = 'rtp'
        a_len = 4
    elif num_kt == 5:
        type_a = 'rtp'
        a_len = 8
    else:
        raise SymbolError('无void型变量')

    if list_line[place_kt + 4] == 'PT' and list_line[place_kt + 5] == '20':
        # 此处存放的是'='，变量被进行赋值

        if list_line[place_kt + 6] == 'CT':
            # 为数字常量
            if type_a == 'ctp':
                raise SymbolError('变量类型与变量值不匹配')

        elif list_line[place_kt + 6] == 'cT':
            # 为字符常量
            if type_a != 'ctp':
                raise SymbolError('变量类型与变量值不匹配')

    a_lentable = Lenl(a_len)
    newiT = SynblTable(va, type_a, CAT, a_lentable)

    return newiT


def addFT(list_line, place_kt, num_kt, function_name_table, function_symbol_table):
    # 函数处理

    # 储存该行token串的列表
    # 记录变量类型的字符在列表中位置
    # 变量类型在KT中存储的位置
    # 函数名称表
    # 本函数下的符号表

    if list_line[-1] == '21' and list_line[-2] == 'PT':
        # 结尾时分号，为函数声明不同填写符号表
        return function_symbol_table, function_name_table

    else:
        # 函数定义，填写符号表
        vf_num = int(list_line[place_kt + 3]) - 1
        vf = FT[vf_num]  # 获取函数名

        if vf in function_name_table:
            raise SymbolError('函数重定义')

        function_name_table.append(vf)

        if num_kt == 2:
            type_f = 'itp'
        elif num_kt == 3:
            type_f = 'ctp'
        elif num_kt == 4:
            type_f = 'rtp'
        elif num_kt == 5:
            type_f = 'rtp'
        else:
            type_f = 'void'

        # 为方便后续参数填入符号表中，此处进行预创建与预填入
        list_para = []
        num_para = 0
        new_ADDR = Pfinfl(0, 0, num_para, None, list_para)  # 填函数表
        # 层次号、区距以0做暂存,入口地址以None暂存
        new_FT = SynblTable(vf, type_f, 'f', new_ADDR)

        function_symbol_table.append(new_FT)

        i = place_kt + 6
        n = len(list_line)

        if list_line[i] == 'PT' and list_line[i + 1] == '24':
            # ')'
            # 此函数无参数
            # 参数个数为0，参数列表为空
            # 与预处理内容一致，无需更改
            return function_symbol_table, function_name_table

        while i < n:
            va_num_kt = int(list_line[i + 1]) - 1
            va_newiT = addiT(list_line, i, va_num_kt, function_symbol_table, 'vf')  # 调用变量处理函数
            list_para.append(va_newiT)
            num_para = num_para + 1
            i = i + 4
            if list_line[i] == 'PT' and list_line[i + 1] == '24':
                # ')'
                break
            else:
                # 此处为逗号，分隔变量
                i = i + 2

        # 参数个数与参数列表更改
        function_symbol_table[0].fn_ = num_para
        function_symbol_table[0].param_ = list_para

        return function_symbol_table, function_name_table


def create_symbol_table(list_token):
    # 储存该行token串的列表

    symbol_table = []  # 用于存放总符号表的列表
    function_symbol_table = []  # 每一个函数用符号表（防止不同函数中相同的内部变量冲突）
    function_name_table = []  # 存放函数名，防止函数重定义
    for list_line in list_token:
        # line_len=len(list_line)/2
        if 'KT' in list_line:
            # KT[2]=='int'
            # KT[3]=='char'
            # KT[4]=='float'
            # KT[5]=='double'
            # KT[7]=='void'
            # PT[19]=='='
            # PT[20]==';'分号
            # PT[21]==','逗号
            # PT[22]=='('
            # PT[23]==')'

            place_kt = list_line.index('KT')  # 变量(或函数)类型的存储位置
            num_kt = int(list_line[place_kt + 1]) - 1  # 该标识符的编号（token序列中加一输出）

            if num_kt == 2 or num_kt == 3 or num_kt == 4 or num_kt == 5 or num_kt == 7:
                if list_line[place_kt + 2] == 'FT':
                    # 对应函数
                    if function_symbol_table:
                        symbol_table.append(function_symbol_table)
                        function_symbol_table = []

                    function_symbol_table, function_name_table = addFT(list_line, place_kt, num_kt, function_name_table,
                                                                       function_symbol_table)

                elif list_line[place_kt + 2] == 'iT':
                    # 对应标识符
                    newiT = addiT(list_line, place_kt, num_kt, function_symbol_table, 'v')

                    if newiT != None:
                        function_symbol_table.append(newiT)

    if function_symbol_table:
        symbol_table.append(function_symbol_table)
        function_symbol_table = []
    return symbol_table


def symbol_table_start(readin):
    readin = readin.replace(' ', '')  # 过滤空格
    readin = readin.replace('<', '')  # 消去<
    readin = readin.replace('>', '')  # 消去>
    listall = readin.split('\n')  # 每一行切割成一个列表
    list_token = []  # 储存每行token串的列表
    for i in listall:
        i = i.split(',')  # 按逗号切割，每两个为一个token值

        i = i[0:len(i) - 1]  # 去掉最后一个因尾逗号产生的空字符
        list_token.append(i)

    create_symbol_table(list_token)


'''
    #测试输出
    for i in symbol_table:
        for j in i:
            print(j.name_)
        print("---")
'''

if __name__ == "__main__":
    words_analysis.start()
    symbol_table_start()
