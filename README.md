# C语言编译器设计

> 该项目为编译原理团队课程设计作业

## 介绍

队名：在线通宵debug

成员：[Samsara_丶](https://github.com/Samsara-1999)、[RayK](https://github.com/Reilkay)、[657695385](https://github.com/657695385)




## 环境

+ 语言：Python

+ 运行环境：Python 3.7.0

+ 使用`PyCharm`开发环境

+ 文件结构

  ```
  24-hour-debug
  ├─过程报告
  └─课设代码
    │  main.py
    ├─BackEnd
    │  │  quaternion_optimization.py
    │  └─ assembly.py
    ├─GUI
    │  │  MenuMain.py
    │  └─ MenuRoot.py
    ├─ParserModule
    │  │  cal_select.py
    │  └─ parser.py
    ├─SemanticAnalysis
    │  │  quaternion_generation.py
    │  └─ symbol_table.py
    └─WordAnalysis
    	 └─ words_analysis.py
  ```

+ 文法：LL(1)-->[具体文法](Doc/文法.md)

  

## TODO

- [x] 前端部分

    - [x] 词法分析

    - [x] 语法分析

    - [x] 语义分析

        - [x] 符号表

		- [x] 翻译文法

		- [x] 活动记录

        - [x] 四元式中间代码

- [x] 后端部分

    - [x] 代码优化

    - [x] 生成目标代码
    
      

### 进度更新时间

**2020-07-10**