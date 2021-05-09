import tkinter as tk

from BackEnd import quaternion_optimization, assembly
from ParserModule.parser import Parser, AnaError
from SemanticAnalysis import symbol_table, quaternion_generation
from SemanticAnalysis.symbol_table import SymbolError
from WordAnalysis import words_analysis
from ParserModule.cal_select import CalSelect


class MenuMain(tk.Toplevel):
    def __init__(self, path):
        super().__init__()
        self.title('控制中心')
        self.geometry('1180x600')

        # 数据
        self.content = tk.Text(self, font=('Arial', 12), height=30, width=130)
        # 弹窗界面
        self.setup_UI()
        self.grab_set()
        # 词法分析：TOKEN
        words_analysis.start(path.get())
        self.content_in = words_analysis.fout
        # SELECT集
        select1 = CalSelect()
        select1.run_cal()
        self.SELECT = select1.SELECT
        # 语法分析
        self.parseTrue = False
        self.parse_message = ""
        parser1 = Parser()
        try:
            parser1.runAnalysis()
            self.parseTrue = True
        except AnaError as e:
            self.parse_message = e.error_info
        if not self.parseTrue:
            return
        # 符号表
        self.symbolTrue = False
        self.symbol_message = ""
        try:
            symbol_table.symbol_table_start(self.content_in)
            self.symbolTrue = True
        except SymbolError as e:
            self.symbol_message = e.error_info
        if not self.symbolTrue:
            return
        # 四元式
        self.total_qua, self.qua = quaternion_generation.start(self.content_in)
        # 四元式优化
        self.opt, self.opt_div = quaternion_optimization.optimization(self.qua)
        # 汇编生成
        self.assembly_resu = assembly.start(self.opt, self.opt_div)

    def setup_UI(self):
        # self.content.config(state=tk.DISABLED)
        self.content.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
        frame_button = tk.Frame(self)
        button_dist = tk.Button(frame_button, text='输出Token', font=('Arial', 15), width=15, height=1,
                                command=self.disToken)
        button_dist.grid(row=0, column=0, padx=10, pady=5, sticky=tk.E + tk.W)
        button_diss = tk.Button(frame_button, text='输出Select', font=('Arial', 15), width=15, height=1,
                                command=self.disSelect)
        button_diss.grid(row=0, column=1, padx=10, pady=5, sticky=tk.E + tk.W)
        button_disf = tk.Button(frame_button, text='输出四元式', font=('Arial', 15), width=15, height=1,
                                command=self.disFour)
        button_disf.grid(row=0, column=2, padx=10, pady=5, sticky=tk.E + tk.W)
        button_disf = tk.Button(frame_button, text='输出优化四元式', font=('Arial', 15), width=15, height=1,
                                command=self.disFourAf)
        button_disf.grid(row=0, column=3, padx=10, pady=5, sticky=tk.E + tk.W)
        button_disc = tk.Button(frame_button, text='输出汇编', font=('Arial', 15), width=15, height=1,
                                command=self.disCompilation)
        button_disc.grid(row=0, column=4, padx=10, pady=5, sticky=tk.E + tk.W)
        button_exit = tk.Button(frame_button, text='退出', font=('Arial', 15), width=15, height=1,
                                command=self.exit_window)
        button_exit.grid(row=0, column=5, padx=10, pady=5, sticky=tk.E + tk.W)
        frame_button.grid(row=1, column=0, columnspan=3)

    def disToken(self):
        self.content.config(state=tk.NORMAL)
        self.content.delete('1.0', 'end')
        self.content.insert(tk.END, 'Token:\n')
        lines = self.content_in.splitlines(True)
        for line in lines:
            self.content.insert(tk.END, line)
            self.content.update()
        self.content.config(state=tk.DISABLED)

    def disSelect(self):
        self.content.config(state=tk.NORMAL)
        self.content.delete('1.0', 'end')
        self.content.insert(tk.END, 'SELECT:\n')
        for keys, values in self.SELECT.items():
            self.content.insert(tk.END, "SELECT("+str(keys)+") = "+str(values))
            self.content.insert(tk.INSERT, '\n')
            self.content.update()
        self.content.config(state=tk.DISABLED)

    def disFour(self):
        if not self.parseTrue:
            tk.messagebox.showerror('语法错误', '错误信息：\n'+self.parse_message)
            return
        if not self.symbolTrue:
            tk.messagebox.showerror('定义错误', '错误信息：\n'+self.symbol_message)
            return
        self.content.config(state=tk.NORMAL)
        self.content.delete('1.0', 'end')
        self.content.insert(tk.END, '四元式:\n')
        for line in self.total_qua:
            self.content.insert(tk.END, "("+line+")")
            self.content.insert(tk.INSERT, '\n')
            self.content.update()
        self.content.config(state=tk.DISABLED)

    def disFourAf(self):
        if not self.parseTrue:
            tk.messagebox.showerror('语法错误', '错误信息：\n' + self.parse_message)
            return
        if not self.symbolTrue:
            tk.messagebox.showerror('定义错误', '错误信息：\n'+self.symbol_message)
            return
        self.content.config(state=tk.NORMAL)
        self.content.delete('1.0', 'end')
        self.content.insert(tk.END, '四元式（优化后）:\n')
        for line in self.opt:
            line_content = "("+line[0]+","+line[1]+","+line[2]+","+line[3]+")"
            self.content.insert(tk.END, line_content)
            self.content.insert(tk.INSERT, '\n')
            self.content.update()
        self.content.config(state=tk.DISABLED)

    def disCompilation(self):
        if not self.parseTrue:
            tk.messagebox.showerror('语法错误', '错误信息：\n' + self.parse_message)
            return
        if not self.symbolTrue:
            tk.messagebox.showerror('定义错误', '错误信息：\n'+self.symbol_message)
            return
        self.content.config(state=tk.NORMAL)
        self.content.delete('1.0', 'end')
        self.content.insert(tk.END, '汇编代码:\n')
        for line in self.assembly_resu:
            self.content.insert(tk.END, line)
            self.content.update()
        self.content.config(state=tk.DISABLED)

    def exit_window(self):
        self.destroy()
