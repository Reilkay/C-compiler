import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox

from GUI.MenuMain import MenuMain


class MenuRoot(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('编译原理课程设计')
        self.geometry('800x200')
        self.path = tk.StringVar()
        self.path.set("未选择")
        # 程序界面
        self.setupUI()

    def setupUI(self):
        lab_message = tk.Label(self, text="当前选择文件：", font=('Arial', 15))
        lab_message.grid(row=0, column=0, sticky=tk.W)
        lab_message = tk.Label(self, textvariable=self.path, font=('Arial', 15), width=40, anchor=tk.NW)
        lab_message.grid(row=0, column=1, sticky=tk.W)

        frame_button = tk.Frame(self)
        button_entry = tk.Button(frame_button, text='选择文件', font=('Arial', 15), width=15, height=1,
                                 command=self.ask_file)
        button_entry.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        button_run = tk.Button(frame_button, text='运行', font=('Arial', 15), width=15, height=1, command=self.run)
        button_run.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        button_exit = tk.Button(frame_button, text='退出', font=('Arial', 15), width=15, height=1,
                                command=self.exit_window)
        button_exit.grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        frame_button.grid(row=0, column=2, rowspan=2)

    def ask_file(self):
        input_path = askopenfilename(filetypes=[('C源文件', '*.c'), ('Text文件', '*.txt')])
        if input_path:
            self.path.set(input_path)

    def run(self):
        if self.path.get() == "未选择":
            tk.messagebox.showerror('错误', '未选择输入文件')
            return
        mainDialog = MenuMain(self.path)
        self.wait_window(mainDialog)
        self.destroy()

    def exit_window(self):
        self.destroy()
