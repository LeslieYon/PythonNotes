#函数式编程(Functional Programming)允许将函数修改、分配给一个变量、作为参数、作为返回值等操作
#函数式编程是一种高度抽象化的编程方式，这种编程方式更注重程序执行的结果而非过程，思维方式更贴近数学思维

#函数名被看做是某种类型的变量
x = abs #这行意味着x指向了abs函数本身
print( x(-5) ) #对于x的调用和对于abs的调用完全相同
abs = 10 #函数名也可以被重新赋值
print ( abs ) #输出结果为 10
abs = x #重新将abs指向默认的位置

#函数可以作为参数传入到另一个函数
def my_function_1(x,y,f): #参数f被用作传递函数本身，带有这种参数的函数被称为高阶函数
	return f(x) + f(y)
print(my_function_1(5,-5,abs)) #结果为 10

#map(函数,序列)允许将“函数”依次作用到“序列”中的每一个元素上，并返回一个Iterator（注意：map函数属于惰性计算函数）
#下面的代码生成了纯负数组成的list，并使用map函数将其全部转换为正数，再使用list将结果转换为标准序列并输出
print( list( map(abs, [x for x in range(-100,0)]) ) )

#reduce(函数,序列)允许将“函数”依次累计作用到“序列”中的每一个元素上，并返回最后一次调用“函数”的返回值
#注意：“函数”参数必须有两个参数，才能使“函数”依次累计作用到“序列”中的每一个元素上
from functools import reduce
def add(x,y):return x*10+y #该函数将x、y两个十进制数连接起来，变成xy。
print( reduce(add,[x for x in range(1,10)]) ) #输出结果为整数 123456789

#下面的代码实现将字符串转换为浮点数
CHAR_TO_FLOAT = {'0':0,'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'.':-1} #小数点用 -1 表示
def c_to_float(c): return CHAR_TO_FLOAT[c]
def str2float(str):
	nums = map(c_to_float,str) #字符串转换为纯数字list
	point = 0 #整数与小数部分标记，默认从整数部分(0)开始
	def to_float(x,y):
		nonlocal point #如果要修改外函数的变量，则需要将此变量声明为nonlocal
		if y == -1: #若下一位是小数点，则当前位为个位
			point = 1 #标记整数部分结束
			return x #直接返回之前累计的结果
		if point == 0: #若当前为整数位，累加运算结果
			return x*10+y
		else: #若当前为小数位，累加运算结果
			point = point*10 #当前位权重的倒数
			return x+y/point #累加运算结果
	return reduce(to_float,nums,0.0) #reduce的第三个参数：初始值。如果提供该参数，则首次调用“函数”时第一个参数为该初始值参数。这里是避免小数点出现在“函数”的第一个参数。
print(str2float(".00123")) #结果为 0.0012300000000000002
print(str2float("123.123")) #结果为 123.12299999999999

#filter(函数,序列)依次对“序列”元素作用“函数”，根据“函数”的返回值决定是否保留这个元素，并返回一个Iterator
#filter函数与map函数一样，属于惰性计算函数，即需要下一个元素时，才会动态计算出这个元素
#下面的代码生成了一个整数1~100的list，并使用filter函数过滤掉所有的非偶数（使用lambda表达式），再由list函数将结果转换为list类型并输出
print( list( filter(lambda x:x%2==0, [x for x in range(1,101) ] ) ) ) #输出1~100之间所有的偶数

#sorted(序列,key,reverse)函数返回经过排序的序列
#参数key接受一个函数，允许在排序时将这个函数作用于每个元素。注意：实际返回的元素仍然是原始的元素
#参数reverse是布尔型变量，允许翻转排序结果（默认为从小到大排序）
#下面的代码对给出的list按照绝对值从大到小的顺序进行排序
print( sorted([-5,8,1,-10,9,-2,-7,-9,20],key=abs,reverse=True) ) #输出结果为 [20, -10, 9, -9, 8, -7, -5, -2, 1]

#python对匿名函数提供有限的支持
#使用lambda表达式创建一个匿名函数
lambda x,y:x*x+y*y #这行相当于def func(x,y):return x*x+y*y
#可以使用lambda表达式创建一些代码简单，且函数名称无关紧要的函数
#上面filter函数的示例语句中lambda x:x%2==0就是一个匿名函数
#lambda表达式返回一个函数对象，可以赋值给其它对象
func_1=lambda x,y:x*x+y*y;print(func_1(3,4)) #结果为 25

#函数可以作为另一个函数的返回值
#当内函数引用了外函数的临时变量，外函数又返回了内函数的引用时，构成一个闭包
def outer(a):
	b = 0
	def inner(c):
		nonlocal b #如果要修改外函数的变量，则需要将此变量声明为nonlocal
		if c%2==0:b = 10
		else:b = 20
		print("a=%d,b=%d,c=%d"%(a,b,c))
		return a+b+c
	return inner #外函数返回了内函数的引用
outer(1)(1) #输出结果为 a=1,b=20,c=1
#每一次调用外函数都会生成一份独立的内函数并将这个内函数引用的外函数变量与之绑定并返回
def cratecounter(): #一个创建计数器函数的函数
	count = 0
	def counter():
		nonlocal count
		count += 1
		return count
	return counter
counterA=cratecounter()
counterB=cratecounter()
print(counterA(),counterA()) #输出结果 1 2
print(counterB(),counterB(),counterB()) #输出结果 1 2 3
#内函数绑定的外函数变量是在调用时才绑定的
def count():
	fs = []
	for i in range(1, 4):
		def f():
			return i*i
		fs.append(f) #注意：此处仅仅“保存”了f函数自身，而不是f函数的运算结果
	return fs
(f1, f2, f3) = count() #也可以直接写成 f1, f2, f3 = count()
print(f1(),f2(),f3()) #输出结果为 9 9 9

#使用装饰器(Decorator)可以对函数调用过程进行“修饰”，而无需修改原函数的代码
def log(func): #该函数实现在调用某个函数之前打印日志
	def wrapper(*args, **kw): #注意：任何函数的参数列表都能表示成(*args, **kw)的形式
		print('call %s():' % func.__name__) #打印日志
		return func(*args, **kw) #执行真正要调用的函数
	return wrapper #返回要执行的函数对象

#用于下方wraps实例
from functools import wraps

#可以自适应给予参数为文本或函数的装饰器(多层嵌套的装饰器、提供额外参数的装饰器)
def log2(text):
	if isinstance(text,str): #如果调用者传递了文本，则返回一个装饰器函数
		def decorator(func):
			@wraps(func) #在定义函数之前用wraps()函数，可以让即将定义的函数的__name__属性修改为指定的函数(wrap函数属于functools.wraps)
			def wrapper(*args, **kw): #内嵌的装饰器函数，返回真正要调用的函数
				print('%s %s():' % (text, func.__name__)) #输出调用者提供的文本，以及调用者真正要调用的函数
				return func(*args, **kw)
			return wrapper
		return decorator
	else: #如果调用者传递了非文本(即要调用的函数)，则返回这个函数
		def wrapper(*args, **kw):
			wrapper.__name__ = func.__name__ #上面@wraps(func)的用法，相当于此处直接在函数中手动修改__name__属性
			print('call %s():' % text.__name__)
			return text(*args, **kw)
		return wrapper

# @log #相当于f1 = log(f1)
@log2("Log2 . run ->") #这一行相当于在调用函数之前加上 log2("Log2 . run ->")(真正调用的函数)(参数列表)
#该log2装饰器可以自适应上面提供额外参数的形式与直接调用的形式@log2
def f1(x,y):
	print("x=%d,y=%d"%(x,y))
	return x+y

# log(print)("hello, %s"%"world") #输出结果为 call print(): \n hello, world
#使用@log，可以避免上一行log(print)的不便之处
# print("sum=%d"%f1(5,6)) #输出结果为 call f1(): \n x=5,y=6 \n sum=11
f1(7,8) #输出结果为 Log2 . run -> f1(): \n x=7,y=8
print(f1.__name__) #由于已经修改了装饰器的__name__属性，所以输出结果为 f1

#可以使用偏函数(partial function)实现对函数参数列表的“修饰”
#即：如果可以确定调用某函数的某参数的值，可以使用偏函数将其固定下来
from functools import partial #partial(函数名,该函数的参数列表)
def int_1(x):return int(x,base=16) #“固定”某函数的参数
int_2 = partial(int,base=16) #上一行的另一种写法，使用了偏函数(partial函数属于functools.partial)
#注意：int()的第二个参数，表示传入的第一个参数的进制数，默认为10
print(int_1("FF"),int_2("FF")) #输出结果为 255 255