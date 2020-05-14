#作为一种动态语言、弱类型语言，python的面向对象实现具有很强的灵活性

class BaseClass(object):
	__slots__ = ("read","__x") #__slots__变量控制当前类的实例可以后期附加哪些属性（该变量作用范围仅限于当前类，无法被继承）
	def __init__(self,x):
		self.__x = x
	@property #使用内置的property装饰器可以进一步封装数据成员的读写函数，让其调用时做到无感调用
	def x(self): #定义某数据成员的读取函数。此处的函数名即为调用者看到的属性名称
		return self.__x
	@x.setter
	def x(self,x): #定义某数据成员的写入函数，函数名需要与对应@property的函数名一致。如果需要定义只读属性，则只需要不定义此处的setter函数即可
		if not isinstance(x,int): #对数据成员的写入进行合法性检测
			raise ValueError("X must be an int")
		if not 0 <= x <= 100:
			raise ValueError("x must between 0 and 100")
		self.__x = x
	def show(self,text):
		print("I want to show you a text: ",text)

class AnotherClass(object): #另一个含有show()成员的类。但除了含有show()外，该类与BaseClass类完全不同
	def show(self,number):
		print("I want to show you a number: ",number)

def ShowSomething(obj): #期望传入BaseClass类实例，但实际上只要传入的对象具有show()成员，就是合法的
	if hasattr(obj,"show"): #判断传入的对象是否含有show属性
		obj.show("something")


#不能添加__slots__变量中不包含的属性
# base.add = 0 #AttributeError：__slots__变量限制了当前实例可以附加的属性

#通过使用@property对数据成员进行高度封装，可以最大程度简化调用的代码
base = BaseClass(10)
base.x = 5 #实际调用了base.x(self,x)函数，如果出入非法的值，将会抛出ValueError异常
print("x = %d" % base.x) #实际调用了base.x(self)函数，输出结果 x = 5

#“鸭子类型”，只要没有语法错误和手动的类型检查，传入任何类型都是合法的
ShowSomething(base) #正确，输出为 I want to show you a text:  something
ShowSomething(AnotherClass()) #正确，输出为 I want to show you a number:  something

#可以使用多重继承简化复杂的派生关系
#多重继承容易产生歧义、意外的行为等复杂问题，使用时需要谨慎
#下面构建了一个菱形的继承关系
class A(object):
	def __init__(self,a):
		print("init A with ",a)
	def show(self,str):
		print("A show :",str)
class B1(A):
	def __init__(self,a,b1,b2):
		#A.__init__(self,a)
		super(B1,self).__init__(a,b2)
		print("init B1 with ",b1)
	def show(self,str):
		print("B1 show :",str)
class B2(A):
	def __init__(self,a,b2):
		#A.__init__(self,a)
		super(B2,self).__init__(a)
		print("init B2 with ",b2)
	def get(self,str):
		print("B2 get :",str)
class C(B1,B2): #C类继承了具有同一个基类的两个类
	def __init__(self,a,b1,b2,c): #多重继承的类如果没有__init__函数，将按照__mro__的顺序查找有效的构造函数并继承
		#B1.__init__(self,a,b1) #此处不能显示调用两个基类的构造函数初始化基类部分，因为这会导致B1,B2共同的基类被初始化两次
		#B2.__init__(self,a,b2)
		super(C,self).__init__(a,b1,b2) #使用super函数进行初始化，此函数可以保证共同基类只被初始化一次。注意：此函数并非直接调用基类，而是根据本类的__mro__属性依次进行初始化，注意需要根据具体初始化的函数提供完整的参数
		print("init C with ",c)
	def put(self,str):
		print("C put :",str)

#多重继承的派生类中，python按照类的成员__mro__中列出的顺序依次查找该派生类继承来的成员（__mro__，即方法解析顺序）
#该__mro__的顺序是根据python的C3算法计算得出的
#若遇到任何隐式调用，python查找对应的成员的路径仍然为__mro__给出的顺序
#关于C3线性化算法的详情，可以参考 http://kaiyuan.me/2016/04/27/C3_linearization/
print(C.__mro__) #输出结果为 (<class '__main__.C'>, <class '__main__.B1'>, <class '__main__.B2'>, <class '__main__.A'>, <class 'object'>)
#创建一个多重继承类的实例
s = C(1,2,3,4)
#上面的创建过程中，所有类的构造函数输出结果为 
#init A with  1
#init B2 with  3
#init B1 with  2
#init C with  4
#这符合__mro__中给出的初始化顺序（注意是先初始化基类，再初始化派生类，此处作用类似于C++的虚构造函数）

#可以重载类中的各种特殊属性，实现和内置类型同样方便的很多特性，此处列举其中的一部分
class One(object):
	def __init__(self,x):
		self.__x = x
	def __str__(self): #重载__str__属性可以定义类的实例在被转化为字符串时的行为（之前已经提到过）
		return "One object with " + str(self.__x)
	__repr__ = __str__ #在shell中直接输入对象名时，系统的输出为__repr__属性
	def __iter__(self): #用于获得一个该类实例的可迭代对象
		return self
	def __next__(self): #拥有__next__属性的类被看做时可迭代的
		if self.__x <= 1:
			raise StopIteration()
		self.__x /= 2
		return self.__x
	def __getitem__(self,n): #__getitem__函数可以让该类实例支持下标操作
		if isinstance(n,int): #支持普通的下标访问操作
			return self.__x / (2**n)
		elif isinstance(n,slice): #支持简单的切片操作。注意，若将该类实例视为类似dict的对象，则n的类型还有可能是str
			start = n.start #注意：一般还要对start、stop、step做范围检查，例如是否越界，是否是负数等情况
			end = n.stop #注意，slice类型还有第三个参数步长：n.step
			l = []
			if start is None: start = 0
			for x in range(start,end):
				l.append(self.__x / (2**x))
			return l
		else: raise TypeError("Unsupport type")
	def __getattr__(self,name): #__getattr__函数可以自定义该类实例获取属性时的默认行为。只要调用了没有定义的属性时，才会调用__getattr__函数
		if isinstance(name,str) and name.startswith("extra_") : #此处定义额外的未知属性必须以 extra_ 开头
			print("extra attr: ", name)
			#return name 使用下一行的lambda返回一个函数，而不是直接返回name，可以让该属性类似函数，可被调用
			return lambda :name #返回一个函数，而不是直接返回具体的值
		else: raise AttributeError("No attribute \'%s\'"%name) #也可以在__getattr__中返回类似系统默认返回的AttributeError错误
	def __call__(self,name): #__call__函数可以让该类实例拥有直接被调用的能力
		return self.__getattr__(name) #此处直接调用__getattr__函数

o = One(998)
#通过重载的__str__可以输出自定义的内容
print(o) #输出结果为 One object with 998
#使用for对可迭代对象进行迭代时，会先使用__iter__获得一个可迭代对象，
#然后循环调用__next__函数获得下一项，直到__next__抛出StopIteration异常时为止
for x in One(998): print(x)
#通过重载的__getitem__可以让某类的实例支持下标操作
print(One(998)[3]) #通过下标访问某元素，输出结果为 124.75
print(One(998)[2:5]) #通过切片访问某个范围的元素，输出结果为 [249.5, 124.75, 62.375]
# print(One(998)["111"]) #TypeError: Unsupport type，这里实现的__getitem__函数不支持str类型的下标
#使用__getattr__处理调用未知属性时的行为
o.extra_a() #调用了未知属性，使用__getattr__处理，结果为 extra attr:  extra_a
# o.extra() #调用了未知属性，使用__getattr__处理，由于该属性名称不符合自定义的规则，因此抛出AttributeError异常
#使用__call__可以让实例拥有直接被调用的能力
o("extra_b")() #隐式调用__call__函数，结果为 extra attr:  extra_b

#可以使用枚举类把一组相关的常量定义在一个class中，并且可以直接作为表达式
from enum import Enum
#下面定义了一组关于月份的常量，其中Month相当于类名，而Jan等常量则相当于类属性，
#这会自动为每一个常量分配一个常数值，默认为从0开始，依次递增
Month = Enum('Month', ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'))
#可以使用如下方式遍历一个enum
#Month.__members__返回一个包含所有常量的dict
#该dict的第二个元素member是每个常量的实例，member.value是这个实例具体对应的常数值
for name, member in Month.__members__.items():
	print(name, '=>', member, ',', member.value) #输出结果为 Jan => Month.Jan , 1 ...
#可以通过多种方式直接使用enum
print(Month.Jan) #输出结果为 Month.Jan
if (Month(2)==Month.Feb): print(Month.Feb.value) #if的条件表达式为真，输出结果为 2
#可以自定义每个常量对应的值
class weekday(Enum):
	mon = 1
	tue = 2
	wed = 3
	thu = 4
	fri = 5
	sat = 6
	sun = 7
print(weekday.sun.value) #输出结果为 7