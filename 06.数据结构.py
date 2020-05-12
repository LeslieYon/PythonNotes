a = ["a","b","c","d","e","f","g"]
b = "abcdefghijklmnopqrstuvwxyz"
c = ("a","b","c","d","e","f","g")
d = {"a":1,"b":2,"c":3}

#可以使用方括号+下标的方式对字符串、list、tuple等(注意dict不支持)进行切片(截取)操作
print(	a[:5]	)	#截取a的前五个元素
print(	a[-1:]	)	#截取a的最后一个元素
print(	a[-4:-1]	)	#截取a的倒数第四个到倒数第二个元素
print(	a[2:8]	)	#截取a中下标为2~7的元素
print(	b[::3]	)	#截取b中下标为3的倍数的元素
print(	b[4:10:2]	)	#截取b中下标为4~9且是2的倍数的元素
print(	c[-6:-1:2]	)	#截取a的倒数第六个到倒数第二个，且下标为2的倍数的元素

#可以通过for...in...实现迭代操作
#通过Iterable可以判断某个对象是否可以被迭代
from collections.abc import Iterable

if isinstance(a,Iterable): #list可迭代
	for s in a:
		print(s,end="\t")
	print("\n",end="")

if isinstance(b,Iterable): #str可迭代
	for s in b:
		print(s,end="\t")
	print("\n",end="")

if isinstance(c,Iterable): #tuple可迭代
	for s in c:
		print(s,end="\t")
	print("\n",end="")

if isinstance(d,Iterable): #dict可迭代
	for s in d:
		print(s,end="\t")
	print("\n",end="")

for s,t,u in [(1,1,1),(2,2,2),(3,3,3)]: #可以同时迭代多个元素，前提是表达式返回的tuple的元素个数要和迭代的元素个数相同
	print(s,t,u,end="\t")
print("\n",end="")

for s,t in d.items(): #对于dict，使用items函数获取每个项目，获取到每个项目的tuple，才能进行多元素迭代
	print(s,t,end="\t")
print("\n",end="")

#注意，下面的(s,t)是另一种显式写法，表明这是一个tuple
for (s,t) in enumerate(d):  #可以用enumerate(枚举)函数为可迭代对象的每个元素分配下标
	print(s,t,end="\t")
print("\n",end="")

if isinstance(123,Iterable): #数字属于不可迭代对象
	for s in 123:
		print(s,end="\t")
	print("\n",end="")

import os; os.system('cls') #清屏

#可以快速生成多种类型的列表(列表生成式)
#range(m,n)函数，可以生成[m,n)区间的数字序列
d = list(range(1,21)); print(d) #生成一个由1~20组成的list，此处也可以生成set、tuple
#使用 [(每个元素生成规则) 生成列表的过滤条件]
#“每个元素生成规则”可以是表达式，也可以是语句
#“生成列表的过滤条件”可以是嵌套的for、if等语句
print ( [ x*x for x in range(10,21)] )
#上面的结果为 [100, 121, 144, 169, 196, 225, 256, 289, 324, 361, 400]
print ( { x*x if x%2==0 else -x*x for x in range(10,21)} )
#上面的结果为 {100, -121, 144, -169, 196, -225, 256, -289, 324, -361, 400}
print ( { a+b for a in "abcd" for b in "ABCD"} )
#上面的结果为 {'aA', 'aB', 'aC', 'aD', 'bA', 'bB', 'bC', 'bD', 'cA', 'cB', 'cC', 'cD', 'dA', 'dB', 'dC', 'dD'}
e = {"aBcDe",123456,"FgHiJk",678910,"LnMoPqR"}
print( { x*2 if isinstance(x,int) else x.upper() for x in e} )
#上面的结果为 {246912, 'ABCDE', 'FGHIJK', 'LNMOPQR', 1357820}

#生成器(generator)可以将生成列表的规则存储起来，而不是列表本身
#可以用于生成超长列表，而无需担心性能问题
#隐式定义生成器
f = ( x*x if x%2==0 else -x*x for x in range(10,21) ) #外层使用小括号，即为定义一个生成器对象
#显式定义生成器
def g(): #定义一个生成器函数
	for x in range(10,21):
		if x%2==0:
			yield(x*x) #该函数每次执行到yield语句时返回，下一次调用时接着执行
		else:
			yield(-x*x)
	return "done" #执行到return语句时，表明该生成器已生成完所有元素
l = g() #首次“调用”生成器函数，会获得一个生成器对象，该l对象等价于上文的f对象
#使用next()函数使生成器生成一个新的对象，当调用超过最后一个元素时，抛出StopIteration异常
print(next(f),next(l)) #结果为 100 100
#生成器也属于可迭代对象
for x,y in zip(f,l):	#使用zip函数，该函数返回一个tuple，用于同时遍历多个序列（遍历总次数为最先结束的序列）
						#对于zip_longest函数，遍历总次数则为最后结束的序列。在这之前结束的序列返回值用None代替
	print(x,y) #结果为f、l的所有剩余元素

#可以使用itertools.chain()依次遍历不同类型、长度序列
from itertools import chain
for x in chain(c,g()):
	print(x,end="\t") #输出结果为c、g()序列的所有元素
print("\n",end="")

#迭代器(Iterator)是一种可以不断使用next()函数获取下一个元素的对象
#所有的生成器(generator)对象都属于一种迭代器(iterator)
#从抽象意义上来说,迭代器是一种有序的、不可预知长度的数据流，因此list、dict、str等都不能算是迭代器对象（尽管它们是可迭代的(Iterable)）
#可以使用iter()函数为list、dict、str获取一个迭代器对象