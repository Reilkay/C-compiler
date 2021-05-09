def isnonterminal(symbol):
    if symbol[0] == '<' and symbol[-1] == '>':
        return True
    return False


class CalSelect(object):
    def __init__(self):
        # 初始化集合字典
        self.FIRST = {}
        self.FOLLOW = {}
        self.SELECT = {}
        # 初始化文法
        self.grammar = [
            "<程序>-><函数>",
            "<形参>-><数据类型> 变量名 <形参'>",
            "<形参>->ε",
            "<形参'>->, <形参>",
            "<形参'>->ε",
            "<返回值类型>->int",
            "<返回值类型>->float",
            "<返回值类型>->double",
            "<返回值类型>->char",
            "<返回值类型>->void",
            "<函数>-><返回值类型> 函数名 ( <形参> ) { <函数主体> } <函数>",
            "<函数>->ε",
            "<函数主体>-><变量申请> <处理语句> <返回语句>",
            "<变量申请>-><数据类型> 变量名 <赋初值> ; <变量申请>",
            "<变量申请>->ε",
            "<赋初值>->= <G>",
            "<赋初值>->ε",
            "<数据类型>->int",
            "<数据类型>->float",
            "<数据类型>->double",
            "<数据类型>->char",
            "<处理语句>-><赋值语句与函数调用> ; <处理语句>",
            "<处理语句>-><判断语句> <处理语句>",
            "<处理语句>-><循环语句> <处理语句>",
            "<处理语句>->ε",
            "<赋值语句与函数调用>-><赋值语句>",
            "<赋值语句与函数调用>->函数名 ( <变量> )",
            "<赋值语句与函数调用>->printf ( <变量> )",
            "<赋值语句与函数调用>->scanf ( <变量> )",
            "<变量>-><A> <变量'>",
            "<变量>->ε",
            "<变量'>->, <A> <变量'>",
            "<变量'>->ε",
            "<赋值语句>->变量名 <子赋值>",
            "<赋值语句>-><单目运算符> 变量名",
            "<子赋值>->= <G>",
            "<子赋值>-><单目运算符>",
            "<G>->字符",
            "<G>-><运算>",
            "<运算>->常数 <实数子运算>",
            "<运算>->函数名 ( <变量> ) <实数子运算>",
            "<运算>->变量名 <子运算>",
            "<运算>-><单目运算符> 变量名",
            "<运算>->! 变量名",
            "<运算>->( <运算> ) <实数子运算>",
            "<A>->变量名",
            "<A>->常数",
            "<A>->函数名 ( <变量> )",
            "<A>->字符",
            "<A>->字符串",
            "<实数子运算>-><运算符> <运算>",
            "<实数子运算>->ε",
            "<子运算>-><运算符> <运算>",
            "<子运算>-><单目运算符>",
            "<子运算>->ε",
            "<运算符>->+",
            "<运算符>->-",
            "<运算符>->*",
            "<运算符>->/",
            "<运算符>->%",
            "<运算符>->&",
            "<运算符>->^",
            "<运算符>->&&",
            "<运算符>->||",
            "<运算符>->|",
            "<单目运算符>->++",
            "<单目运算符>->--",
            "<判断语句>->if ( <条件> ) { <处理语句> } <H>",
            "<H>->else <子判断语句>",
            "<H>->ε",
            "<子判断语句>->if ( <条件> ) { <处理语句> } <H>",
            "<子判断语句>->{ <处理语句> }",
            "<条件>-><A> <子判断>",
            "<条件>->! <A>",
            "<子判断>-><判断运算符> <A>",
            "<子判断>->ε",
            "<判断运算符>->==",
            "<判断运算符>->>",
            "<判断运算符>-><",
            "<判断运算符>->>=",
            "<判断运算符>-><=",
            "<判断运算符>->!=",
            "<循环语句>->while ( <条件> ) { <处理语句> }",
            "<循环语句>->do { <处理语句> } while ( <条件> ) ;",
            "<循环语句>->for ( <赋值语句> ; <条件> ; <运算> ) { <处理语句> }",
            "<返回语句>->return <A> ;"
        ]
        # 初始化终结符
        for i in range(0, len(self.grammar)):
            self.grammar[i] = self.grammar[i].replace('函数名', 'FT')
            self.grammar[i] = self.grammar[i].replace('变量名', 'iT')
            self.grammar[i] = self.grammar[i].replace('常数', 'CT')
            self.grammar[i] = self.grammar[i].replace('字符串', 'sT')
            self.grammar[i] = self.grammar[i].replace('字符', 'cT')
        # 初始化first集、follow集和select集字典的键值对中的值为空
        for line in self.grammar:
            part_begin = line.split("->")[0]
            part_end_temp = line.split("->")[1]
            part_end = part_end_temp.split(" ")
            self.FIRST[part_begin] = []
            self.FOLLOW[part_begin] = []
            self.SELECT[line] = []
        self.FOLLOW[self.grammar[0].split("->")[0]].append('#')

    # 求first集中第一部分：针对->直接推出第一个字符为终结符部分
    def getFirst(self):
        for line in self.grammar:
            part_begin = line.split("->")[0]
            part_end_temp = line.split("->")[1]
            part_end = part_end_temp.split(" ")
            if not isnonterminal(part_end[0]):
                self.FIRST[part_begin].append(part_end[0])

    # 求first第二部分：针对A -> B型，把B的first集加到A的first集合中
    def getFirst_2(self):
        for line in self.grammar:
            part_begin = line.split("->")[0]
            part_end_temp = line.split("->")[1]
            part_end = part_end_temp.split(" ")
            # 如果型如A -> B：则把B的first集加到A的first集中去
            if isnonterminal(part_end[0]):
                for i in range(0, len(part_end)):
                    if not isnonterminal(part_end[i]):
                        self.FIRST[part_begin].append(part_end[i])
                        break
                    list_remove = self.FIRST.get(part_end[i]).copy()
                    if 'ε' in list_remove and i is not len(part_end) - 1:
                        list_remove.remove('ε')
                    self.FIRST[part_begin].extend(list_remove)
                    if 'ε' not in self.FIRST[part_end[i]]:
                        break

    def getFirst_3(self):
        while 1:
            test = self.FIRST
            self.getFirst_2()
            # 去除重复项
            for i, j in self.FIRST.items():
                temp = []
                for word in list(set(j)):
                    temp.append(word)
                self.FIRST[i] = temp
            if test == self.FIRST:
                break

    def getFOLLOW_3(self):
        while 1:
            test = self.FOLLOW
            self.getFollow()
            # 去除重复项
            for i, j in self.FOLLOW.items():
                temp = []
                for word in list(set(j)):
                    temp.append(word)
                self.FOLLOW[i] = temp
            if test == self.FOLLOW:
                break

    # 计算follow集的第一部分，先计算 S -> A b 类型的
    def getFollow(self):
        for line in self.grammar:
            part_begin = line.split("->")[0]
            part_end_temp = line.split("->")[1]
            part_end = part_end_temp.split(" ")
            if part_begin == "<G>":
                pass
            # 如果是 S->a 直接推出终结符 则 continue
            if len(part_end) == 1 and not isnonterminal(part_end[0]):
                continue
            # 否则执行下面的操作
            else:
                # 将->后面的倒序
                part_end.reverse()
                # 最后一个为非终结符
                if isnonterminal(part_end[0]):

                    for i in range(0, len(part_end)):
                        if not isnonterminal(part_end[i]):
                            break
                        self.FOLLOW[part_end[i]].extend(self.FOLLOW.get(part_begin))
                        if 'ε' not in self.FIRST[part_end[i]]:
                            break

                    terminal_temp = part_end[0]
                    for item in part_end[1:]:
                        if not isnonterminal(item):
                            terminal_temp = item
                        else:
                            if isnonterminal(terminal_temp):
                                list_remove = self.FIRST.get(terminal_temp).copy()
                                if "ε" in list_remove:
                                    list_remove.remove("ε")
                                self.FOLLOW[item].extend(list_remove)
                            elif terminal_temp != 'ε':
                                self.FOLLOW[item].append(terminal_temp)
                            terminal_temp = item
                # 如果终结符在句型的末端
                else:
                    terminal_temp = part_end[0]
                    for item in part_end[1:]:
                        if not isnonterminal(item):
                            terminal_temp = item
                        else:
                            if isnonterminal(terminal_temp):
                                list_remove = self.FIRST.get(terminal_temp).copy()
                                if "ε" in list_remove:
                                    list_remove.remove("ε")
                                self.FOLLOW[item].extend(list_remove)
                            elif terminal_temp != 'ε':
                                self.FOLLOW[item].append(terminal_temp)
                            terminal_temp = item

    def getSelect(self):
        for line in self.grammar:
            part_begin = line.split("->")[0]
            part_end_temp = line.split("->")[1]
            part_end = part_end_temp.split(" ")
            line_first = []
            for item in part_end:
                if not isnonterminal(item):
                    line_first.append(item)
                    break
                else:
                    line_first.extend(self.FIRST[item])
                    if 'ε' not in self.FIRST[item]:
                        break
            line_first = list(set(line_first))
            can_derive_empty = True
            part_end.reverse()
            for item in part_end:
                if not isnonterminal(item):
                    if item != 'ε':
                        can_derive_empty = False
                        break
                else:
                    if 'ε' not in self.FIRST[item]:
                        can_derive_empty = False
                        break
            list_remove = line_first.copy()
            if "ε" in list_remove:
                list_remove.remove("ε")
            if can_derive_empty:
                self.SELECT[line].extend(list_remove)
                self.SELECT[line].extend(self.FOLLOW[part_begin])
            else:
                self.SELECT[line].extend(list_remove)
            self.SELECT[line] = list(set(self.SELECT[line]))

    def debug_out(self):
        for i, j in self.FIRST.items():
            str = j[0]
            for temp in j[1:]:
                str = str + ',' + temp
            print("FIRST(" + i + ")" + " = {" + str + "}")

        for i, j in self.FOLLOW.items():
            str = j[0]
            for temp in j[1:]:
                str = str + ',' + temp
            print("FOLLOW(" + i + ")" + " = {" + str + "}")
        for i, j in self.SELECT.items():
            str = j[0]
            for temp in j[1:]:
                str = str + ',' + temp
            print("SELECT(" + i + ")" + " = {" + str + "}")

    def run_cal(self):
        self.getFirst()
        self.getFirst_3()
        self.getFirst_3()
        self.getFOLLOW_3()
        self.getFOLLOW_3()
        self.getSelect()
        # self.debug_out()


if __name__ == "__main__":
    CalSelect().run_cal()
