#标准函数定义如下
def my_function_1(x,y,z) : # 可以包含多个参数（位置参数）
	#如果需要，需要单独针对参数类型进行检查
	if not isinstance(x,(int,float)):
		raise TypeError("Bad operand type")
	#函数功能部分
	print("This is a function.")
	#可以返回多个值（实则为返回一个tuple）
	return x,y,z
	#没有写return时，函数默认返回None值

#带默认值参数的函数
def my_function_2(x,y=1,z=2) :# y,z参数包含有默认值，注意：默认参数必须指向不可变对象
	print("x:",x,"\ty:",y,"\tz:",z)
	return x,y,z

#某函数参数的默认值指向可变对象
def my_function_3(x=["abc"]) :# 参数指向可变对象，这会导致该参数保留上一次执行的结果
	x.append("test")
	print(x)
	return x

#正确处理可变对象作为参数
def my_function_4(x=None): #使用None作为默认参数值
	if x == None: #手动判断参数类型，单独做处理
		x = ["abc"]
	x.append("test")
	print(x)
	return x

#带有（个数）可变参数的函数
def my_function_5(*package): #此处的package参数相当于一个tuple
	print("These are all of them:")
	for one in package: #遍历tuple
		print(one, end='\t')
	print("\n",end='')
	return

#带有关键字参数的函数，该参数允许函数接受额外的名称和值的参数
#注意：关键字参数本身不对内部参数名称进行检查
def my_function_6(main, **extra): #extra将接受额外的参数（值传递），并将其组装为一个dict
	if 'age' in extra: #手动对extra内包含的参数名进行检查
		print("age is there")
	print("main:", main)
	print("extra data:",extra)
	return

#带有命名关键字参数的函数，该类型参数调用时必须显式调用且必须提供（有默认值时除外）
#命名关键字参数前也可以有可变参数，例如 (main,*package,age) 也是合法的
def my_function_7(main,*,age,nation="China"):
	print(main,age,nation)
	return

#函数参数列表包含参数的顺序应为：位置参数、默认参数、可变参数、命名关键字参数、关键字参数
def my_function_8(a,b=1,*c,d,**e):
	print(a,b,c,d,e)
	return

print(my_function_1(1,2,3)[0]) #输出为 1
# my_function_1(1,2) #错误：参数个数不匹配
# my_function_1("1",2,3) #错误：参数类型不匹配

my_function_2(1)		#输出为 x: 1    y: 1    z: 2
my_function_2(1,5)		#输出为 x: 1    y: 5    z: 2
my_function_2(1,z=5)	#输出为 x: 1    y: 1    z: 5

#注意，指向可变对象的默认参数会存储上一次调用的结果
my_function_3() #输出为 ['abc', 'test']
my_function_3() #输出为 ['abc', 'test', 'test'] ，这是因为这里可变的对象本身作为默认参数值，而不是指定的值
#my_function_4使用Nano替代可变对象作为参数默认值，解决了这个问题
my_function_4() #输出为 ['abc', 'test']
my_function_4() #输出为 ['abc', 'test']

#调用包含可变参数的函数
my_function_5() #可以什么不包含
my_function_5(1,2,3,"a","B","C",0.25) #可以包含多种类型，输出为 1       2       3       a       B       C       0.25
#可以直接将tuple或list拆分作为可变参数传递
my_function_5(*(1,2,3,"a","B","C",0.25)) #输出同上
my_function_5(*[1,2,3,"a","B","C",0.25]) #输出同上

#调用包含关键字参数的函数
# sex="male",age=25 将被组装成一个dict（值传递），并传递给关键字参数extra
my_function_6("Tom", sex="male", age=25) #输出为 main: Tom extra data: {'sex': 'male', 'age': 25}
# 可以直接将dict拆分作为关键字参数传递
my_function_6("Tom", **{'sex': 'male', 'age': 25}) #输出结果同上

#调用包含命名关键字参数的函数
# my_function_7("Jack") #错误：age参数必须显式提供
my_function_7("Jack",age=7) #输出 Jack 7 China
my_function_7("Mike",age=7,nation="USA")#输出 Mike 7 USA

#调用包含多种参数类型的函数
my_function_8(0,d=5)						#输出为 0 1 () 5 {}
my_function_8(0,1,d=5)						#输出为 0 1 () 5 {}
my_function_8(0,1,2,3,4,d=5)				#输出为 0 1 (2, 3, 4) 5 {}
my_function_8(0,1,2,3,4,d=5,e=6,f=7,g=8)	#输出为 0 1 (2, 3, 4) 5 {'e': 6, 'f': 7, 'g': 8}
my_function_8(*(0,1,2,3,4),**{"d": 5, 'e': 6, 'f': 7, 'g': 8}) #正确的调用，可以通过(*args,**kw)的方式调用任意函数，输出同上