'''
在python中，每一个.py文件都被认为是一个模块(module)，文件名称就是模块的名称
注意：在python中，对象命名可以是中文，但不能以数字开头
为了防止模块名冲突，可以将多个模块封装成一个包(package)
这些模块和包应该有类似于下面的目录结构
mycompany
 ├─ web
 │  ├─ __init__.py # “包”的标志文件。必须有，但可以是空的，该文件用于初始化
 │  ├─ utils.py
 │  └─ www.py
 ├─ __init__.py
 ├─ abc.py
 └─ utils.py

在上方的目录结构中，mycompany和web都构成一个包
而www.py对应的模块名为 mycompany.web.www
两个utils.py对应的模块名分别为 mycompany.web.utils 和 mycompany.utils
如果模块名只写mycompany.web，则对应的文件默认为该目录下的__init__.py文件
'''

#系统查找模块的目录列表存储在sys.path中
from sys import path
print(path)
#输出结果为 ['E:\\Desktop\\python学习', 'D:\\Program Files\\Python\\python38.zip', 'D:\\Program Files\\Python\\DLLs', 'D:\\Program Files\\Python\\lib', 'D:\\Program Files\\Python', 'D:\\Program Files\\Python\\lib\\site-packages']
#其中，第一个搜寻位置永远指向当前.py文件所在的目录
#也可以手动给path变量增加需要搜寻的位置，有效期为本次程序执行期间

#python中的变量命名约定
#形似__name__为系统使用的有特殊含义的变量
#形似_name或__name的表示当前变量为本模块私有变量，不应该被其它模块使用
#全大写字母的变量表示为常量
#注意：python并没有强制保证该约定的正确性，该约定仅为一种约定

#一个标准的python模块应该有如下的格式

#!/usr/bin/env python3  #linux/mac系统python文件戳
# -*- coding: utf-8 -*- #声明当前python脚本的编码

' a test module '  #任何模块的第一个字符串都被视为该模块的文档注释

__author__ = 'Mike'  #__auther__存储了当前模块的作者信息

import sys

def test():
	args = sys.argv #sys.argv是一个保存的当前程序所有命令行参数的list
	if len(args)==1:
		print('Hello, world!')
	elif len(args)==2:
		print('Hello, %s!' % args[1])
	else:
		print('Too many arguments!')

print("__name__",__name__)

if __name__=='__main__': #若当前模块是被直接执行的，则__name__参数的值为'__main__'，若是被其它模块导入的，为当前模块名
	test()
	import os; os.system('pause')