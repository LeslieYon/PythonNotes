#和其它很多高级语言一样，Python也支持异常处理的语法

#使用断言（assert）可以对某个表达式的值做出假设判定
#如果断言失败了，则会抛出AssertionError异常
#注意：运行Python脚本时手动加上-O参数，可以强制忽略所有的断言
def test1(x):
	#当参数x不是整数时，以下的断言式抛出异常 AssertionError: X should be INT!
	assert isinstance(x,int),"X should be INT!"
	print("x的平方是：",x**2)
	return

#使用logging模块，可以更精准地控制调试信息
import logging
#日志等级有DEBUG、INFO、WARNING、ERROR等级别，等级越高，输出的信息越详细
#例如DEBUG级别可以输出在其之下所有级别的信息
logging.basicConfig(level=logging.DEBUG)
def test2(x):
	logging.info("x=%d"%x) #此行产生了输出，是因为上面的日志记录等级为DEBUG
	print("x的平方是：",x**2)
	return

#使用try...except...finally语句可以实现对可能抛出的异常的处理
try: #try关键词用于标识可能抛出异常的代码
	r = 10/0 #这一行会抛出ZeroDivisionError异常
except ValueError as e: #每一个except都可以用于捕获某一类异常，具体的异常信息为该异常类的实例e
	print("ValueError:",e)
except ZeroDivisionError as e: #可以有多个except，由于面向对象的多态性，子类异常应该放在前面捕获，否则会被基类的except覆盖掉
	print("ZeroDivisionError:",e)
	logging.exception(e) #也可以使用logging模块记录异常信息，并输出到屏幕或文件中
else: #（可选）当没有任何异常发生时，执行else分支
	print("no error!")
finally: #（可选）无论如何，finally部分都会被最终执行
	print("finally...")
#注意：一旦有错误被成功捕获，代码将不会终止，而是继续执行下去
#Python中所有的异常类继承关系可以参考官方文档：https://docs.python.org/3/library/exceptions.html#exception-hierarchy

#使用raise关键字可以抛出一个异常对象
class FooError(ValueError):pass #可以定义自己的错误类型
def Foo(x):
	try:
		r = x / (x-2) # x=2时，本行抛出除零错误ZeroDivisionError
		return r
	except ZeroDivisionError as e: #捕获ZeroDivisionError异常
		print("ZeroDivisionError:", e) #记录异常信息
		raise FooError("FooError!") #再次抛出自定义的异常FooError
def Bar(x):
	try:
		print("result:",Foo(x)) # x=2时，本行抛出自定义错误FooError
	except FooError as e: #捕获FooError异常
		raise #直接将异常抛出，相当于 raise e
try:
	Bar(4) #本行没有错误
	Bar(2) #本行会抛出FooError错误
except ValueError as e: #由于自定义的FooError属于ValueError的派生类，因此FooError也可以被ValueError及其基类捕获
	print("ValueError:",e) #最终显示错误信息 ValueError: FooError!

#使用doctest可以对某个功能实现文档测试
#下面的函数实现了一个自定义的dict类，允许使用 实例.属性 的方式访问dict的元素
class MyDict(dict):
	'''
	这是MyDict的说明部分
	通常，说明部分位于函数或类开始的部位
	可以在说明部分写入示例代码，这些代码还可以用于文档测试
	示例代码的写法遵循Python控制台出现写法的仿真
	以下是示例代码的写法的演示
	>>> d = MyDict(a=1, b="test")
	>>> d['b']
	'test'
	>>> d.x = 100
	>>> d['x']
	100
	>>> d['y'] = 200
	>>> d.y
	200
	>>> d.z #出现异常时示例代码的写法可以使用...省略中间的内容
	Traceback (most recent call last):
		...
	AttributeError: 'MyDict' object has no attribute 'z'
	>>> d['z']
	Traceback (most recent call last):
		...
	KeyError: 'z'
	'''
	def __init__(self,*args,**kw): #调用内置dict的构造函数，初始化dict实例
		super().__init__(*args,**kw)
	def __getattr__(self,attr): #重写__getattr__函数，使本类支持通过 实例.属性 的方式读取dict元素
		try:
			return self[attr]
		except KeyError:
			raise AttributeError(r"'MyDict' object has no attribute '%s'" % attr)
	def __setattr__(self,key,value): #重写__setattr__函数，使本类支持通过 实例.属性 的方式写入dict元素
		self[key] = value

#使用untitest可以对某个功能实现单元测试
#使用单元测试时，需要额外导入unittest模块
#通常，单元测试的代码位于另一个独立的模块中，新模块命名时以_test结尾
import unittest
#from MyDict import MyDict #单元测试代码在独立的模块中时，需要手动导入被测试的模块
class TestDict(unittest.TestCase): #单元测试类继承于unittest.TestCase
	def test_init(self): #当执行单元测试时，系统会自动执行所有以test_开头的函数
		d1 = MyDict(a=1,b="test") #新类型应当可以使用关键字参数初始化
		d2 = MyDict({"a":1,"b":"test2"}) #应当可以使用一个dict初始化
		#使用assertEqual，断言某个表达式的值
		self.assertEqual(d1.a,1)  #应当可以直接使用属性访问某个元素
		self.assertEqual(d2.b,"test2")
	def test_key(self):
		d = MyDict()
		d['testkey'] = 'value' #应当可以通过传统的下标方式写入
		#使用self.assertTrue，断言某个表达式的值为真
		self.assertTrue('testkey' in d) #应当可以使用in关键字判断是否包含某个元素
		self.assertEqual(d['testkey'],'value') #应当可以通过传统的下标方式访问
	def test_attr(self):
		d = MyDict()
		d.testkey = 'value' #应当可以通过直接使用属性的方式写入
		self.assertTrue('testkey' in d)
		self.assertEqual(d.testkey,'value') #应当可以通过直接使用属性的方式访问
	def test_error(self):
		d = MyDict()
		#通过with语句，可以断言某个表达式是否会抛出某种异常
		with self.assertRaises(KeyError): #通过传统的下标方式访问不存在的元素时，应当抛出KeyError异常
			value = d['value']
		with self.assertRaises(AttributeError): #通过直接访问属性的方式访问不存在的元素时，应当抛出AttributeError异常
			value = d.value
	def setUp(self): #存在于setUp函数中的代码，会在所有test_函数执行之前自动执行
		print("setUp...")
	def tearDown(self): #存在于tearDown函数中的代码，会在所有test_函数执行之后自动执行
		print("tearDown...")

if __name__ == "__main__": #通常只有在直接运行当前模块时，才会执行测试功能
	#通过doctest.testmod函数启动文档测试
	import doctest
	doctest.testmod()

	unittest.main() #执行单元测试，这一行执行结束后，当前模块会直接退出，后面所有的代码都会被忽视
	#因此用于单元测试的模块，最好不要再放置其它的功能
	#除了直接运行单元测试模块之外，也可以通过 Python -m 被测试模块 单元测试模块 对某个模块进行单元测试