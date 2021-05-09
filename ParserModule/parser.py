import re

from WordAnalysis import words_analysis
from ParserModule.cal_select import CalSelect


class AnaError(Exception):
    def __init__(self, ErrorInfo):
        super().__init__(self)  # 初始化父类
        self.error_info = ErrorInfo

    def __str__(self):
        return self.error_info


class Parser(object):
    def __init__(self):
        # words_analysis.start()
        # Token表
        self.iT = words_analysis.iT
        self.cT = words_analysis.cT
        self.sT = words_analysis.sT
        self.CT = words_analysis.CT
        self.KT = words_analysis.KT
        self.PT = words_analysis.PT
        self.FT = words_analysis.FT
        # Token内容
        self.content = words_analysis.fout + "\n <##,1>"
        pattern = re.compile(r'<(.*?)>')
        self.element = pattern.findall(self.content)
        self.element_code = []
        self.element_value = []
        for item in self.element:
            self.element_code.append(item.split(",")[0])
            self.element_value.append(int(item.split(",")[1]))
        # print(vars(self)[self.element_code[3]][23])
        # Select表
        self.select = CalSelect()
        self.select.run_cal()
        self.SELECT = self.select.SELECT
        # 局部变量
        self.success = False
        self.index = -1
        self.line = 1
        self.line_index = 0
        self.line_content = self.content.splitlines()
        self.line_length = [item.count('<') for item in self.line_content]
        self.error_message = ""

    def nextT(self):
        self.index += 1
        self.line_index += 1
        if self.line_index > self.line_length[self.line-1]:
            self.line += 1
            self.line_index = 1
        return self.index

    def runAnalysis(self):
        self.nextT()
        self.程序()
        return self.success

    def 程序(self):
        self.函数()

    def 形参(self):
        if self.element_code[self.index] == "KT":
            self.nextT()
            if self.element_code[self.index] == "iT":
                self.nextT()
                self.形参_()
            else:
                self.error_message = "error({}, {}): expected variable name!".format(self.line, self.line_index)
                print(self.error_message)
                raise AnaError(self.error_message)
        else:
            pass

    def 形参_(self):
        if self.element[self.index] == "PT,22":
            self.nextT()
            self.形参()
        else:
            pass

    def 函数(self):
        if self.element_code[self.index] == "KT":
            self.nextT()
            if self.element_code[self.index] == "FT":
                self.nextT()
                if self.element[self.index] == "PT,23":
                    self.nextT()
                    self.形参()
                    if self.element[self.index] == "PT,24":
                        self.nextT()
                        if self.element[self.index] == "PT,27":
                            self.nextT()
                            self.函数主体()
                            if self.element[self.index] == "PT,28":
                                self.nextT()
                                if self.element[self.index] != "##,1":
                                    self.函数()
                                else:
                                    self.over()
                            else:
                                self.error_message = \
                                    "error({}, {}): expected right curly brackets!".format(self.line, self.line_index)
                                print(self.error_message)
                                raise AnaError(self.error_message)
                        else:
                            self.error_message = \
                                "error({}, {}): expected left curly brackets!".format(self.line, self.line_index)
                            print(self.error_message)
                            raise AnaError(self.error_message)
                    else:
                        self.error_message = \
                            "error({}, {}): expected right parenthesis!".format(self.line, self.line_index)
                        print(self.error_message)
                        raise AnaError(self.error_message)
                else:
                    self.error_message = "error({}, {}): expected left parenthesis!".format(self.line, self.line_index)
                    print(self.error_message)
                    raise AnaError(self.error_message)
            else:
                self.error_message = "error({}, {}): expected function!".format(self.line, self.line_index)
                print(self.error_message)
                raise AnaError(self.error_message)
        else:
            pass

    def 函数主体(self):
        self.变量申请()
        self.处理语句()
        self.返回语句()

    def 变量申请(self):
        if (vars(self)[self.element_code[self.index]][self.element_value[self.index]-1]
                in self.SELECT["<变量申请>-><数据类型> iT <赋初值> ; <变量申请>"]):
            self.nextT()
            if self.element_code[self.index] == "iT":
                self.nextT()
                self.赋初值()
                if self.element[self.index] == "PT,21":
                    self.nextT()
                    self.变量申请()
                else:
                    self.error_message = "error({}, {}): expected semicolon!".format(self.line, self.line_index)
                    print(self.error_message)
                    raise AnaError(self.error_message)
            else:
                self.error_message = "error({}, {}): expected variable name!".format(self.line, self.line_index)
                print(self.error_message)
                raise AnaError(self.error_message)
        else:
            pass

    def 赋初值(self):
        if self.element[self.index] == "PT,20":
            self.nextT()
            self.G()
        else:
            pass

    def 处理语句(self):
        if ((self.element_code[self.index] in self.SELECT["<处理语句>-><赋值语句与函数调用> ; <处理语句>"])
                or (vars(self)[self.element_code[self.index]][self.element_value[self.index]-1]
                    in self.SELECT["<处理语句>-><赋值语句与函数调用> ; <处理语句>"])):
            self.赋值语句与函数调用()
            if self.element[self.index] == "PT,21":
                self.nextT()
                self.处理语句()
            else:
                self.error_message = "error({}, {}): expected semicolon!".format(self.line, self.line_index)
                print(self.error_message)
                raise AnaError(self.error_message)
        elif (vars(self)[self.element_code[self.index]][self.element_value[self.index]-1]
                in self.SELECT["<处理语句>-><判断语句> <处理语句>"]):
            self.判断语句()
            self.处理语句()
        elif (vars(self)[self.element_code[self.index]][self.element_value[self.index]-1]
                in self.SELECT["<处理语句>-><循环语句> <处理语句>"]):
            self.循环语句()
            self.处理语句()
        else:
            pass

    def 赋值语句与函数调用(self):
        if ((self.element_code[self.index] in self.SELECT["<赋值语句与函数调用>-><赋值语句>"])
                or (vars(self)[self.element_code[self.index]][self.element_value[self.index]-1]
                    in self.SELECT["<赋值语句与函数调用>-><赋值语句>"])):
            self.赋值语句()
        elif (self.element_code[self.index] in self.SELECT["<赋值语句与函数调用>->FT ( <变量> )"]
                or self.element[self.index] in ["KT,15", "KT,16"]):
            self.nextT()
            if self.element[self.index] == "PT,23":
                self.nextT()
                self.变量()
                if self.element[self.index] == "PT,24":
                    self.nextT()
                else:
                    self.error_message = "error({}, {}): expected right parenthesis!".format(self.line, self.line_index)
                    print(self.error_message)
                    raise AnaError(self.error_message)
            else:
                self.error_message = "error({}, {}): expected left parenthesis!".format(self.line, self.line_index)
                print(self.error_message)
                raise AnaError(self.error_message)
        else:
            self.error_message = "error({}, {}): expected expression!".format(self.line, self.line_index)
            print(self.error_message)
            raise AnaError(self.error_message)

    def 变量(self):
        if self.element_code[self.index] in self.SELECT["<变量>-><A> <变量'>"]:
            self.A()
            self.变量_()
        else:
            pass

    def 变量_(self):
        if self.element[self.index] == "PT,22":
            self.nextT()
            self.A()
            self.变量_()
        else:
            pass

    def 赋值语句(self):
        if self.element_code[self.index] in self.SELECT["<赋值语句>->iT <子赋值>"]:
            self.nextT()
            self.子赋值()
        elif (vars(self)[self.element_code[self.index]][self.element_value[self.index]-1]
                in self.SELECT["<子赋值>-><单目运算符>"]):
            self.nextT()
            if self.element_code[self.index] == 'iT':
                self.nextT()
            else:
                self.error_message = "error({}, {}): expected variable name!".format(self.line, self.line_index)
                print(self.error_message)
                raise AnaError(self.error_message)
        else:
            self.error_message = "error({}, {}): expected expression!".format(self.line, self.line_index)
            print(self.error_message)
            raise AnaError(self.error_message)

    def 子赋值(self):
        if self.element[self.index] == "PT,20":
            self.nextT()
            self.G()
        elif (vars(self)[self.element_code[self.index]][self.element_value[self.index]-1]
                in self.SELECT["<子赋值>-><单目运算符>"]):
            self.nextT()
        else:
            self.error_message = "error({}, {}): expected expression!".format(self.line, self.line_index)
            print(self.error_message)
            raise AnaError(self.error_message)

    def G(self):
        if self.element_code[self.index] in self.SELECT["<G>->cT"]:
            self.nextT()
        elif ((self.element_code[self.index] in self.SELECT["<G>-><运算>"])
                or (vars(self)[self.element_code[self.index]][self.element_value[self.index]-1]
                    in self.SELECT["<G>-><运算>"])):
            self.运算()
        else:
            self.error_message = "error({}, {}): expected expression!".format(self.line, self.line_index)
            print(self.error_message)
            raise AnaError(self.error_message)

    def 运算(self):
        if self.element_code[self.index] in self.SELECT["<运算>->CT <实数子运算>"]:
            self.nextT()
            self.实数子运算()
        elif self.element_code[self.index] in self.SELECT["<运算>->FT ( <变量> ) <实数子运算>"]:
            self.nextT()
            if self.element[self.index] == "PT,23":
                self.nextT()
                self.变量()
                if self.element[self.index] == "PT,24":
                    self.nextT()
                    self.实数子运算()
                else:
                    self.error_message = "error({}, {}): expected right parenthesis!".format(self.line, self.line_index)
                    print(self.error_message)
                    raise AnaError(self.error_message)
            else:
                self.error_message = "error({}, {}): expected left parenthesis!".format(self.line, self.line_index)
                print(self.error_message)
                raise AnaError(self.error_message)
        elif self.element_code[self.index] in self.SELECT["<运算>->iT <子运算>"]:
            self.nextT()
            self.子运算()
        elif (vars(self)[self.element_code[self.index]][self.element_value[self.index]-1]
                in self.SELECT["<运算>-><单目运算符> iT"]):
            self.nextT()
            if self.element_code[self.index] == 'iT':
                self.nextT()
            else:
                self.error_message = "error({}, {}): expected variable name!".format(self.line, self.line_index)
                print(self.error_message)
                raise AnaError(self.error_message)
        elif (vars(self)[self.element_code[self.index]][self.element_value[self.index]-1]
                in self.SELECT["<运算>->! iT"]):
            self.nextT()
            if self.element_code[self.index] == 'iT':
                self.nextT()
            else:
                self.error_message = "error({}, {}): expected variable name!".format(self.line, self.line_index)
                print(self.error_message)
                raise AnaError(self.error_message)
        elif (vars(self)[self.element_code[self.index]][self.element_value[self.index]-1]
                in self.SELECT["<运算>->( <运算> ) <实数子运算>"]):
            self.nextT()
            self.运算()
            if self.element[self.index] == "PT,24":
                self.nextT()
                self.实数子运算()
            else:
                self.error_message = "error({}, {}): expected right parenthesis!".format(self.line, self.line_index)
                print(self.error_message)
                raise AnaError(self.error_message)
        else:
            self.error_message = "error({}, {}): expected expression!".format(self.line, self.line_index)
            print(self.error_message)
            raise AnaError(self.error_message)

    def A(self):
        if self.element_code[self.index] in self.SELECT["<A>->iT"]:
            self.nextT()
        elif self.element_code[self.index] in self.SELECT["<A>->CT"]:
            self.nextT()
        elif self.element_code[self.index] in self.SELECT["<A>->FT ( <变量> )"]:
            self.nextT()
            if self.element[self.index] == "PT,23":
                self.nextT()
                self.变量()
                if self.element[self.index] == "PT,24":
                    self.nextT()
                else:
                    self.error_message = "error({}, {}): expected right parenthesis!".format(self.line, self.line_index)
                    print(self.error_message)
                    raise AnaError(self.error_message)
            else:
                self.error_message = "error({}, {}): expected left parenthesis!".format(self.line, self.line_index)
                print(self.error_message)
                raise AnaError(self.error_message)
        elif self.element_code[self.index] in self.SELECT["<A>->cT"]:
            self.nextT()
        elif self.element_code[self.index] in self.SELECT["<A>->sT"]:
            self.nextT()
        else:
            self.error_message = "error({}, {}): expected expression!".format(self.line, self.line_index)
            print(self.error_message)
            raise AnaError(self.error_message)

    def 实数子运算(self):
        if (vars(self)[self.element_code[self.index]][self.element_value[self.index]-1]
                in self.SELECT["<实数子运算>-><运算符> <运算>"]):
            self.nextT()
            self.运算()
        else:
            pass

    def 子运算(self):
        if (vars(self)[self.element_code[self.index]][self.element_value[self.index]-1]
                in self.SELECT["<子运算>-><运算符> <运算>"]):
            self.nextT()
            self.运算()
        elif (vars(self)[self.element_code[self.index]][self.element_value[self.index]-1]
                in self.SELECT["<子运算>-><单目运算符>"]):
            self.nextT()
        else:
            pass

    def 判断语句(self):
        if self.element[self.index] == "KT,10":
            self.nextT()
            if self.element[self.index] == "PT,23":
                self.nextT()
                self.条件()
                if self.element[self.index] == "PT,24":
                    self.nextT()
                    if self.element[self.index] == "PT,27":
                        self.nextT()
                        self.处理语句()
                        if self.element[self.index] == "PT,28":
                            self.nextT()
                            self.H()
                        else:
                            self.error_message = \
                                "error({}, {}): expected right curly brackets!".format(self.line, self.line_index)
                            print(self.error_message)
                            raise AnaError(self.error_message)
                    else:
                        self.error_message = \
                            "error({}, {}): expected left curly brackets!".format(self.line, self.line_index)
                        print(self.error_message)
                        raise AnaError(self.error_message)
                else:
                    self.error_message = "error({}, {}): expected right parenthesis!".format(self.line, self.line_index)
                    print(self.error_message)
                    raise AnaError(self.error_message)
            else:
                self.error_message = "error({}, {}): expected left parenthesis!".format(self.line, self.line_index)
                print(self.error_message)
                raise AnaError(self.error_message)
        else:
            self.error_message = "error({}, {}): expected expression!".format(self.line, self.line_index)
            print(self.error_message)
            raise AnaError(self.error_message)

    def H(self):
        if self.element[self.index] == "KT,11":
            self.nextT()
            self.子判断语句()
        else:
            pass

    def 子判断语句(self):
        if self.element[self.index] == "KT,10":
            self.nextT()
            if self.element[self.index] == "PT,23":
                self.nextT()
                self.条件()
                if self.element[self.index] == "PT,24":
                    self.nextT()
                    if self.element[self.index] == "PT,27":
                        self.nextT()
                        self.处理语句()
                        if self.element[self.index] == "PT,28":
                            self.nextT()
                            self.H()
                        else:
                            self.error_message = \
                                "error({}, {}): expected right curly brackets!".format(self.line, self.line_index)
                            print(self.error_message)
                            raise AnaError(self.error_message)
                    else:
                        self.error_message = \
                            "error({}, {}): expected left curly brackets!".format(self.line, self.line_index)
                        print(self.error_message)
                        raise AnaError(self.error_message)
                else:
                    self.error_message = "error({}, {}): expected right parenthesis!".format(self.line, self.line_index)
                    print(self.error_message)
                    raise AnaError(self.error_message)
            else:
                self.error_message = "error({}, {}): expected left parenthesis!".format(self.line, self.line_index)
                print(self.error_message)
                raise AnaError(self.error_message)
        else:
            pass

    def 条件(self):
        if self.element[self.index] == "PT,8":
            self.nextT()
            self.A()
        else:
            self.A()
            self.子判断()

    def 子判断(self):
        if (vars(self)[self.element_code[self.index]][self.element_value[self.index] - 1]
                in self.SELECT["<子判断>-><判断运算符> <A>"]):
            self.nextT()
            self.A()
        else:
            pass

    def 循环语句(self):
        if (vars(self)[self.element_code[self.index]][self.element_value[self.index] - 1]
                in self.SELECT["<循环语句>->while ( <条件> ) { <处理语句> }"]):
            self.nextT()
            if self.element[self.index] == "PT,23":
                self.nextT()
                self.条件()
                if self.element[self.index] == "PT,24":
                    self.nextT()
                    if self.element[self.index] == "PT,27":
                        self.nextT()
                        self.处理语句()
                        if self.element[self.index] == "PT,28":
                            self.nextT()
                        else:
                            self.error_message = \
                                "error({}, {}): expected right curly brackets!".format(self.line, self.line_index)
                            print(self.error_message)
                            raise AnaError(self.error_message)
                    else:
                        self.error_message = \
                            "error({}, {}): expected left curly brackets!".format(self.line, self.line_index)
                        print(self.error_message)
                        raise AnaError(self.error_message)
                else:
                    self.error_message = "error({}, {}): expected right parenthesis!".format(self.line, self.line_index)
                    print(self.error_message)
                    raise AnaError(self.error_message)
            else:
                self.error_message = "error({}, {}): expected left parenthesis!".format(self.line, self.line_index)
                print(self.error_message)
                raise AnaError(self.error_message)
        elif (vars(self)[self.element_code[self.index]][self.element_value[self.index] - 1]
                in self.SELECT["<循环语句>->do { <处理语句> } while ( <条件> ) ;"]):
            self.nextT()
            if self.element[self.index] == "PT,27":
                self.nextT()
                self.处理语句()
                if self.element[self.index] == "PT,28":
                    self.nextT()
                    if self.element[self.index] == "KT,13":
                        self.nextT()
                        if self.element[self.index] == "PT,23":
                            self.nextT()
                            self.条件()
                            if self.element[self.index] == "PT,24":
                                self.nextT()
                                if self.element[self.index] == "PT,21":
                                    self.nextT()
                                else:
                                    self.error_message = \
                                        "error({}, {}): expected semicolon!".format(self.line, self.line_index)
                                    print(self.error_message)
                                    raise AnaError(self.error_message)
                            else:
                                self.error_message = \
                                    "error({}, {}): expected right parenthesis!".format(self.line, self.line_index)
                                print(self.error_message)
                                raise AnaError(self.error_message)
                        else:
                            self.error_message = \
                                "error({}, {}): expected right parenthesis!".format(self.line, self.line_index)
                            print(self.error_message)
                            raise AnaError(self.error_message)
                    else:
                        self.error_message = "error({}, {}): expected 'while' !".format(self.line, self.line_index)
                        print(self.error_message)
                        raise AnaError(self.error_message)
                else:
                    self.error_message = \
                        "error({}, {}): expected right curly brackets!".format(self.line, self.line_index)
                    print(self.error_message)
                    raise AnaError(self.error_message)
            else:
                self.error_message = \
                    "error({}, {}): expected left curly brackets!".format(self.line, self.line_index)
                print(self.error_message)
                raise AnaError(self.error_message)
        elif (vars(self)[self.element_code[self.index]][self.element_value[self.index] - 1]
                in self.SELECT["<循环语句>->for ( <赋值语句> ; <条件> ; <运算> ) { <处理语句> }"]):
            self.nextT()
            if self.element[self.index] == "PT,23":
                self.nextT()
                self.赋值语句()
                if self.element[self.index] == "PT,21":
                    self.nextT()
                    self.条件()
                    if self.element[self.index] == "PT,21":
                        self.nextT()
                        self.运算()
                        if self.element[self.index] == "PT,24":
                            self.nextT()
                            if self.element[self.index] == "PT,27":
                                self.nextT()
                                self.处理语句()
                                if self.element[self.index] == "PT,28":
                                    self.nextT()
                                else:
                                    self.error_message = "error({}, {}): expected right curly brackets!"\
                                        .format(self.line, self.line_index)
                                    print(self.error_message)
                                    raise AnaError(self.error_message)
                            else:
                                self.error_message = \
                                    "error({}, {}): expected left curly brackets!".format(self.line, self.line_index)
                                print(self.error_message)
                                raise AnaError(self.error_message)
                        else:
                            self.error_message = \
                                "error({}, {}): expected right parenthesis!".format(self.line, self.line_index)
                            print(self.error_message)
                            raise AnaError(self.error_message)
                    else:
                        self.error_message = "error({}, {}): expected semicolon!".format(self.line, self.line_index)
                        print(self.error_message)
                        raise AnaError(self.error_message)
                else:
                    self.error_message = "error({}, {}): expected semicolon!".format(self.line, self.line_index)
                    print(self.error_message)
                    raise AnaError(self.error_message)
            else:
                self.error_message = "error({}, {}): expected left parenthesis!".format(self.line, self.line_index)
                print(self.error_message)
                raise AnaError(self.error_message)
        else:
            self.error_message = "error({}, {}): expected expression!".format(self.line, self.line_index)
            print(self.error_message)
            raise AnaError(self.error_message)

    def 返回语句(self):
        if self.element[self.index] == "KT,17":
            self.nextT()
            self.A()
            if self.element[self.index] == "PT,21":
                self.nextT()
            else:
                self.error_message = "error({}, {}): expected semicolon!".format(self.line, self.line_index)
                print(self.error_message)
                raise AnaError(self.error_message)
        else:
            pass

    # def 函数(self):
    #     pass
    def over(self):
        self.success = True
