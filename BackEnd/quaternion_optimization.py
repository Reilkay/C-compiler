# 四元式优化
# --------------------------- 2020.7.8 ----------------------------
# 完成debug，测试多基本块——通过，测试复杂代码的化简——通过
# -----------------------------------------------------------------


class Vertext():
    # 包含了顶点信息,以及顶点连接边

    def __init__(self, id_, key):
        # 构造函数
        self.id = id_  # 序号（0、1、2...）
        self.key = key  # 主标记

        # 下列直接进行初始化
        self.variables = {}  # 标记变量名字典
        self.if_know = False  # 是否已知
        self.if_num = False  # 是否为纯数字
        self.if_char = False  # 是否为字符
        self.if_bool = False  # 是否为布尔型，纯数字为false，数字表示正误为true（r_num为对应true)
        self.r_num = 0  # 数字的值
        self.v_char = ''
        self.op = ''  # 运算的符号
        self.connectedTo = []  # 初始化临接列表

    def addnum(self, r_num):
        # 添加实数
        self.if_know = True
        self.if_num = True
        self.r_num = r_num

    def addbool(self, r_num):
        # 添加布尔型
        self.if_know = True
        self.if_num = True
        self.if_bool = True
        self.r_num = r_num

    def addchar(self, v_char):
        # 添加字符
        self.if_know = True
        self.if_char = True
        self.v_char = v_char

    def addop(self, op, op_list):
        # 添加符号，以及计算路径
        self.if_know = True
        self.op = op
        self.connectedTo = op_list

    def addvariable(self, variable):
        # 添加涉及的变量名
        lenthv = len(variable)
        lenthk = len(self.key)
        if self.key == '':
            self.key == variable
            return

        if lenthk == 1 or not (self.key[0] == 't' and '0' <= self.key[1] <= '9'):
            # key为用户定义

            if lenthv > 1 and variable[0] == 't' and '0' <= variable[1] <= '9':
                # variable非用户定义
                self.variables[variable] = "False"
            else:
                # variable用户定义
                self.variables[variable] = "True"
        else:
            # key为非用户定义

            if lenthv > 1 and variable[0] == 't' and '0' <= variable[1] <= '9':
                # variable非用户定义
                self.variables[variable] = "False"
            else:
                # variable用户定义
                # 将用户定义的变量名设为表示字符
                self.variables[self.key] = "False"
                self.key = variable

    def delvariable(self, variable):
        if self.variables:
            # 如果当前只有一个变量（主标记免删）
            if variable == self.key:
                # 若需要删除的是表示字符

                # 找到里面的用户自定义变量，提取出来作为表示字符
                for vn in self.variables:
                    if self.variables[vn] == "True":
                        self.key = vn
                        del self.variables[vn]
                        return

                # 若无用户自定义变量，则使用字典用存入的第一个变量来表示
                for vn0 in self.variables:
                    self.key = vn0
                    del self.variables[vn0]
                    return
            else:
                # 若需要删除的非表示字符
                del self.variables[variable]
        else:
            if self.if_num or self.if_char:
                # 可删除重复定义的变量，又可避免删除运算中的变量
                self.key = ''


'''
Graph包含了所有的顶点
包含了一个主表(临接列表)
'''


class Graph():
    # 图 => 由顶点所构成的图

    def __init__(self):
        self.vertList = {}  # 临接字典
        self.numVertices = 0  # 顶点个数初始化

    def addVertex(self, id_, key):
        # 添加顶点
        self.numVertices = self.numVertices + 1  # 顶点个数累加
        newVertex = Vertext(id_, key)  # 创建该顶点的顶点信息
        self.vertList[id_] = newVertex  # 加入临接列表
        return newVertex

    def getVertex_key(self, n):
        # 通过key查找定点
        for i in range(self.numVertices):
            if self.vertList[i].key == n:
                return self.vertList[i]
            if n in self.vertList[i].variables:
                return self.vertList[i]
        return None

    def getVertex_id(self, n):
        # 通过id查找定点
        if n < self.numVertices:
            return self.vertList[n]
        else:
            return None

    def getVertex_num(self, n):
        # 通过num查找实数定点
        for i in range(self.numVertices):
            if self.vertList[i].if_num and not (self.vertList[i].if_bool):
                if n == self.vertList[i].r_num:
                    return self.vertList[i]
        return None

    def getVertex_bool(self, n):
        # 通过num查找布尔型定点
        for i in range(self.numVertices):
            if self.vertList[i].if_bool:
                if n == self.vertList[i].r_num:
                    return self.vertList[i]
        return None

    def getVertex_char(self, n):
        # 通过char查找字符定点
        for i in range(self.numVertices):
            if self.vertList[i].if_char:
                if n == self.vertList[i].v_char:
                    return self.vertList[i]
        return None

    def getVertex_op_list(self, op, lista):
        # 通过表达式查找定点
        for i in range(self.numVertices):
            if self.vertList[i].if_know and (not self.vertList[i].if_num) and (not self.vertList[i].if_char):
                if op == self.vertList[i].op and lista == self.vertList[i].connectedTo:
                    return self.vertList[i]
        return None

    def clr(self):
        # 重新初始化图
        self.vertList = {}
        self.numVertices = 0

    def if_retain(self, n):
        # 查找该点是否需要保留（优化时需要将无意义结点删去）
        if self.vertList[n].key == '':
            return False
        elif self.vertList[n].if_bool:
            return True
        elif not (len(self.vertList[n].key) > 1 and self.vertList[n].key[0] == 't' and '0' <= self.vertList[n].key[
            1] <= '9'):
            return True
        elif len(self.vertList[n].connectedTo) > 0:
            return True
        else:
            for i in range(self.numVertices):
                if i == n:
                    continue
                if self.vertList[n] in self.vertList[i].connectedTo:
                    return True
            return False


area_list = ['function', 'end',
             'if', 'el', 'ie',
             'for', 'wh', 'do', 'we', 'dwh',
             'jump']
g = Graph()


def if_number(s):
    # 判断字符中存放的是否是一个数字
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


def if_char(s):
    # 判断字符中存放的是否是一个字符
    if s[0] == '\'' and s[-1] == '\'':
        return True
    else:
        return False


def get_op_num(b_char, c_char, op):
    # 计算两数运算结果
    b = float(b_char)
    c = float(c_char)
    if op == '+':
        return b + c, False
    elif op == '-':
        return b - c, False
    elif op == '*':
        return b * c, False
    elif op == '/':
        return b / c, False
    elif op == '%':
        return b % c, False
    elif op == '^':
        return b ^ c, False
    elif op == '&':
        return b & c, False
    elif op == '|':
        return b | c, False
    elif op == '&&':
        if b >= 1 and c >= 1:
            return 1, True
        else:
            return 0, True
    elif op == '||':
        if b >= 1 or c >= 1:
            return 1, True
        else:
            return 0, True
    elif op == '==':
        if b == c:
            return 1, True
        else:
            return 0, True
    elif op == '>':
        if b > c:
            return 1, True
        else:
            return 0, True
    elif op == '<':
        if b < c:
            return 1, True
        else:
            return 0, True
    elif op == '>=':
        if b >= c:
            return 1, True
        else:
            return 0, True
    elif op == '<=':
        if b <= c:
            return 1, True
        else:
            return 0, True
    elif op == '!=':
        if b != c:
            return 1, True
        else:
            return 0, True


def getDAG(list_part):
    # 建立DAG图
    list_part_num = len(list_part)
    j = 0
    while j < list_part_num:

        if list_part[j][0] == '=':  # 0型四元式(=,B,_,A)

            # 记录B是否是数字
            if_num_B = if_number(list_part[j][1])

            # 记录B是否是字符
            if_char_B = if_char(list_part[j][1])

            if if_num_B:
                # 当B为数字时

                num_B = float(list_part[j][1])
                vb = g.getVertex_num(num_B)

                va = g.getVertex_key(list_part[j][3])
                if va != None:
                    # 因为A需要重新赋值，要删去原有的值。若A已经被赋值（存在）则需要删去
                    va.delvariable(list_part[j][3])

                if vb == None:
                    # 若不存在该数字的记录,则新建A保存数字
                    new_va = g.addVertex(g.numVertices, list_part[j][3])
                    new_va.addnum(num_B)
                else:
                    vb.addvariable(list_part[j][3])

            elif if_char_B:
                # 当B为字符时

                vb = g.getVertex_char(list_part[j][1])
                va = g.getVertex_key(list_part[j][3])
                if va != None:
                    # 因为A需要重新赋值，要删去原有的值。若A已经被赋值（存在）则需要删去
                    va.delvariable(list_part[j][3])

                if vb == None:
                    # 若不存在该字符的记录,则新建A保存字符
                    new_va = g.addVertex(g.numVertices, list_part[j][3])
                    new_va.addchar(list_part[j][1])
                else:
                    vb.addvariable(list_part[j][3])

            else:
                # 当B为变量时

                vb = g.getVertex_key(list_part[j][1])
                va = g.getVertex_key(list_part[j][3])
                if va != None:
                    # 因为A需要重新赋值，要删去原有的值。若A已经被赋值（存在）则需要删去
                    va.delvariable(list_part[j][3])

                if vb == None:
                    vb = g.addVertex(g.numVertices, list_part[j][1])

                vb.addvariable(list_part[j][3])

        elif list_part[j][2] == '_':  # 1型四元式(op,B,_,A)

            vb = g.getVertex_key(list_part[j][1])
            if vb == None:
                vb = g.addVertex(g.numVertices, list_part[j][1])
            va = g.getVertex_key(list_part[j][3])
            if va != None:
                # 因为A需要重新赋值，要删去原有的值。若A已经被赋值（存在）则需要删去
                va.delvariable(list_part[j][3])

            listva = []
            listva.append(vb)

            new_va = g.getVertex_op_list(list_part[j][0], listva)
            if new_va == None:
                new_va = g.addVertex(g.numVertices, list_part[j][3])
                new_va.addop(list_part[j][0], listva)
            else:
                new_va.addvariable(list_part[j][3])

        else:  # 2型四元式(op,B,C,A)

            # 记录B是否是数字
            if_num_B = if_number(list_part[j][1])
            # 记录C是否是数字
            if_num_C = if_number(list_part[j][2])

            if if_num_B and if_num_C:
                # 如果B和C都是常数
                # 当能直接计算出A的值时，不会对常数新建结点，也无需建立从A出发的结点之间的链接。便于后续优化
                va = g.getVertex_key(list_part[j][3])
                if va != None:
                    # 因为A需要重新赋值，要删去原有的值。若A已经被赋值（存在）则需要删去
                    va.delvariable(list_part[j][3])

                num_A, bool_A = get_op_num(list_part[j][1], list_part[j][2], list_part[j][0])

                if bool_A:
                    new_va = g.getVertex_bool(num_A)
                    if new_va == None:
                        # 若不存在该数字的记录,则新建A保存数字
                        new_va = g.addVertex(g.numVertices, list_part[j][3])
                        new_va.addbool(num_A)
                    else:
                        new_va.addvariable(list_part[j][3])
                else:
                    new_va = g.getVertex_num(num_A)
                    if new_va == None:
                        # 若不存在该数字的记录,则新建A保存数字
                        new_va = g.addVertex(g.numVertices, list_part[j][3])
                        new_va.addnum(num_A)
                    else:
                        new_va.addvariable(list_part[j][3])

            elif if_num_B and not if_num_C:
                # 如果B是常数，C是结点

                vc = g.getVertex_key(list_part[j][2])

                va = g.getVertex_key(list_part[j][3])
                if va != None:
                    # 因为A需要重新赋值，要删去原有的值。若A已经被赋值（存在）则需要删去
                    va.delvariable(list_part[j][3])

                if vc != None and vc.if_num:

                    num_A, bool_A = get_op_num(list_part[j][1], vc.r_num, list_part[j][0])
                    if bool_A:
                        new_va = g.getVertex_bool(num_A)
                        if new_va == None:
                            # 若不存在该数字的记录,则新建A保存数字
                            new_va = g.addVertex(g.numVertices, list_part[j][3])
                            new_va.addbool(num_A)
                        else:
                            new_va.addvariable(list_part[j][3])
                    else:
                        new_va = g.getVertex_num(num_A)
                        if new_va == None:
                            # 若不存在该数字的记录,则新建A保存数字
                            new_va = g.addVertex(g.numVertices, list_part[j][3])
                            new_va.addnum(num_A)
                        else:
                            new_va.addvariable(list_part[j][3])
                else:
                    # 若vc为空，则一定是一个未知的变量

                    num_B = float(list_part[j][1])
                    vb = g.getVertex_num(num_B)
                    if vb == None:
                        vb = g.addVertex(g.numVertices, '')
                        vb.addnum(num_B)

                    if vc == None:
                        vc = g.addVertex(g.numVertices, list_part[j][2])

                    listva = []
                    listva.append(vb)
                    listva.append(vc)
                    new_va = g.getVertex_op_list(list_part[j][0], listva)

                    if new_va == None:
                        new_va = g.addVertex(g.numVertices, list_part[j][3])
                        new_va.addop(list_part[j][0], listva)
                    else:
                        new_va.addvariable(list_part[j][3])

            elif if_num_C and not if_num_B:
                # 如果C是常数，B是结点

                vb = g.getVertex_key(list_part[j][1])
                va = g.getVertex_key(list_part[j][3])
                if va != None:
                    # 因为A需要重新赋值，要删去原有的值。若A已经被赋值（存在）则需要删去
                    va.delvariable(list_part[j][3])

                if vb != None and vb.if_num:

                    num_A, bool_A = get_op_num(vb.r_num, list_part[j][2], list_part[j][0])
                    if bool_A:
                        new_va = g.getVertex_bool(num_A)
                        if new_va == None:
                            # 若不存在该数字的记录,则新建A保存数字
                            new_va = g.addVertex(g.numVertices, list_part[j][3])
                            new_va.addbool(num_A)
                        else:
                            new_va.addvariable(list_part[j][3])
                    else:
                        new_va = g.getVertex_num(num_A)
                        if new_va == None:
                            # 若不存在该数字的记录,则新建A保存数字
                            new_va = g.addVertex(g.numVertices, list_part[j][3])
                            new_va.addnum(num_A)
                        else:
                            new_va.addvariable(list_part[j][3])

                else:
                    # 若vb为空，则一定是一个未知的变量

                    num_C = float(list_part[j][2])
                    vc = g.getVertex_num(num_C)
                    if vc == None:
                        vc = g.addVertex(g.numVertices, '')
                        vc.addnum(num_C)

                    if vb == None:
                        vb = g.addVertex(g.numVertices, list_part[j][1])

                    listva = []
                    listva.append(vb)
                    listva.append(vc)
                    new_va = g.getVertex_op_list(list_part[j][0], listva)

                    if new_va == None:
                        new_va = g.addVertex(g.numVertices, list_part[j][3])
                        new_va.addop(list_part[j][0], listva)
                    else:
                        new_va.addvariable(list_part[j][3])
            else:
                # B和C都是结点

                vb = g.getVertex_key(list_part[j][1])
                vc = g.getVertex_key(list_part[j][2])

                va = g.getVertex_key(list_part[j][3])
                if va != None:
                    # 因为A需要重新赋值，要删去原有的值。若A已经被赋值（存在）则需要删去
                    va.delvariable(list_part[j][3])

                if vb != None and vb.if_num and vc != None and vc.if_num:
                    # 当B和C都存储常数时，A通过计算也会得到常数

                    num_A, bool_A = get_op_num(vb.r_num, vc.r_num, list_part[j][0])
                    if bool_A:
                        new_va = g.getVertex_bool(num_A)
                        if new_va == None:
                            # 若不存在该数字的记录,则新建A保存数字
                            new_va = g.addVertex(g.numVertices, list_part[j][3])
                            new_va.addbool(num_A)
                        else:
                            new_va.addvariable(list_part[j][3])
                    else:
                        new_va = g.getVertex_num(num_A)
                        if new_va == None:
                            # 若不存在该数字的记录,则新建A保存数字
                            new_va = g.addVertex(g.numVertices, list_part[j][3])
                            new_va.addnum(num_A)
                        else:
                            new_va.addvariable(list_part[j][3])

                else:
                    # 否则需要建立A的生成表达式

                    vb = g.getVertex_key(list_part[j][1])
                    vc = g.getVertex_key(list_part[j][2])
                    if vb == None:
                        vb = g.addVertex(g.numVertices, list_part[j][1])
                    if vc == None:
                        vc = g.addVertex(g.numVertices, list_part[j][2])

                    listva = []
                    listva.append(vb)
                    listva.append(vc)
                    new_va = g.getVertex_op_list(list_part[j][0], listva)

                    if new_va == None:
                        new_va = g.addVertex(g.numVertices, list_part[j][3])
                        new_va.addop(list_part[j][0], listva)
                    else:
                        new_va.addvariable(list_part[j][3])
        j = j + 1


def DAG_get_list(list2, list_v):
    # 由DAG图生成优化后的四元式代码

    for i in range(g.numVertices):

        # g.vertList[i]
        if g.if_retain(i) and g.vertList[i].if_know:
            # 纯数字、非用户定义且对表达式生成没有贡献 and 外部定义变量 ：无需生成四元式

            if g.vertList[i].if_num:
                # 当用数字对变量赋值时，若变量不为用户自定义变量，则可不生成四元式

                if len(g.vertList[i].key) > 1 and g.vertList[i].key[0] == 't' and '0' <= g.vertList[i].key[1] <= '9':
                    if not (g.vertList[i].if_bool):
                        continue
                listn = []
                listn.append('=')
                num_char = str(g.vertList[i].r_num)
                listn.append(num_char)
                listn.append('_')
                listn.append(g.vertList[i].key)

                list2.append(listn)
                if g.vertList[i].key not in list_v:
                    list_v.append(g.vertList[i].key)

                if g.vertList[i].variables:
                    for k in g.vertList[i].variables:
                        if not (len(k) > 1 and k[0] == 't' and '0' <= k[1] <= '9'):
                            # 非用户自定义变量同样需要生成四元式
                            listg = []
                            listg.append('=')
                            listg.append(num_char)
                            listg.append('_')
                            listg.append(k)

                            list2.append(listg)
                            if k not in list_v:
                                list_v.append(k)
            elif g.vertList[i].if_char:
                # 用字符给变量赋值

                listn = []
                listn.append('=')
                listn.append(g.vertList[i].v_char)
                listn.append('_')
                listn.append(g.vertList[i].key)

                list2.append(listn)
                if g.vertList[i].key not in list_v:
                    list_v.append(g.vertList[i].key)

                if g.vertList[i].variables:
                    for k in g.vertList[i].variables:
                        if not (len(k) > 1 and k[0] == 't' and '0' <= k[1] <= '9'):
                            # 非用户自定义变量同样需要生成四元式
                            listg = []
                            listg.append('=')
                            listg.append(g.vertList[i].v_char)
                            listg.append('_')
                            listg.append(k)

                            list2.append(listg)
                            if k not in list_v:
                                list_v.append(k)
            else:
                # 变量通过表达式生成
                # 若A可直接计算出常数，则在生成DAG图时已经计算得出，其形式也是数字赋值型。因此此处的A一定通过其他变量计算得来

                listn = []
                listn.append(g.vertList[i].op)

                # 若两个变量（B、C）中存在纯数字，则直接提取出数字存入四元式
                if g.vertList[i].connectedTo[0].if_num:
                    bkey = str(g.vertList[i].connectedTo[0].r_num)
                else:
                    bkey = g.vertList[i].connectedTo[0].key
                    if bkey not in list_v:
                        list_v.append(bkey)
                listn.append(bkey)

                if len(g.vertList[i].connectedTo) > 1:
                    # 当临近列表长度为1时，说明A是通过单目运算符生成，不涉及第二个变量
                    if g.vertList[i].connectedTo[1].if_num:
                        ckey = str(g.vertList[i].connectedTo[1].r_num)
                    else:
                        ckey = g.vertList[i].connectedTo[1].key
                        if ckey not in list_v:
                            list_v.append(ckey)
                    listn.append(ckey)
                else:
                    listn.append('_')

                listn.append(g.vertList[i].key)

                list2.append(listn)
                if g.vertList[i].key not in list_v:
                    list_v.append(g.vertList[i].key)

                if g.vertList[i].variables:
                    for k in g.vertList[i].variables:
                        if not (len(k) > 1 and k[0] == 't' and '0' <= k[1] <= '9'):
                            # 非用户自定义变量同样需要生成四元式
                            listg = []
                            listg.append(g.vertList[i].op)
                            listg.append(bkey)
                            if len(g.vertList[i].connectedTo) > 1:
                                listg.append(ckey)
                            else:
                                listg.append('_')
                            listg.append(k)

                            list2.append(listg)
                            if k not in list_v:
                                list_v.append(k)


def optimization(list1):
    # 基本块内的局部优化
    list_num = len(list1)  # 四元组个数
    i = 0
    list_part = []  # 存放同一基本块内的四元式
    list2 = []  # 存放优化后的四元式
    list_v = []  # 存放涉及的变量

    while i < list_num:
        if list1[i][0] in area_list:
            # 基本块划分的标识符
            if list_part:
                # 判断列表是否为空，非空则进入if

                getDAG(list_part)
                DAG_get_list(list2, list_v)

                g.clr()  # 将图初始化
                list_part = []  # 基本块内四元式列表初始化

            list2.append(list1[i])

        else:
            list_part.append(list1[i])

        i = i + 1

    if list_part:
        # 判断判断是否有剩余四元式未处理
        getDAG(list_part)
        DAG_get_list(list2, list_v)

    list_v_division = [[], []]
    for i in list_v:
        if len(i) > 1 and i[0] == 't' and '0' <= i[1] <= '9':
            list_v_division[1].append(i)
        else:
            list_v_division[0].append(i)

    return list2, list_v_division
