#由于python将类也看做是一种对象，因此可以对将类用于赋值、传参、增删属性等，甚至可以在程序执行期间动态创建、修改类（相比于C++的类模板更灵活一些）

#使用type函数，可以动态创建出类对象，事实上，这也是python解释器在创建类对象时的具体做法
#type函数的用法为 type(类名, 所有基类的tuple, 所有属性的dict)
#注意：只有一个参数的type函数，用途是获取该参数的类型
Foo = type("Foo",(object,),{"bar":"Foo Bar"})  #创建了一个名为Foo、继承于object、含有一个bar属性的类
print(Foo().bar) #与常规方式建立的类用法无异，输出结果为 Foo Bar
def ShowBar(self):
	print("Show:",self.bar)
FooChild = type("FooChild",(Foo,),{"ShowBar":ShowBar}) #也可以为某个类添加方法成员
FooChild().ShowBar() #与常规方式建立的类用法无异，输出结果为 Show: Foo Bar

# 使用元类(metaclass)可以动态干涉类的创建过程
# 该元类可以将目标类的所有非系统属性的名称转换为大写
class UpperAttrMetaClass(type): # 元类派生于type类，惯例上来说，所有元类命名时都应该以MetaClass结尾
	# __new__函数是在创建类时调用的特殊函数
	# __new__函数用于创建类对象并将其返回
	# __new__函数的四个参数分别为cls,name,bases,dct
	# cls参数等价于普通类的self参数
	# name,bases,dct这三个参数就是type()函数的三个参数
	def __new__(cls,name,bases,dct):
		# 下面一行代码做了这几件事：
		# 1.枚举出即将要创建的类的所有属性 2.过滤掉所有的系统属性(以__开头的属性) 3.将剩余的属性名称转为大写字符
		# 4.将前面三步生成的生成器转化为普通的dict
		upper_attr = dict( (name.upper(),value) for name,value in dct.items() if not name.startswith("__") )
		# __new__函数的返回值应该为创建好的类对象
		# 所以返回时可以直接调用type函数生成类对象： return type(name,bases,upper_attr)
		# 但是由于元类直接派生于type，因此可以直接调用基类的__new__函数： return type.__new__(cls,name,bases,upper_attr)
		# 然而这里实际上使用super函数调用上一级的__new__函数，用于缓解多重继承问题
		# 关于super()函数，可以参考上一份笔记中多重继承的部分
		return super(UpperAttrMetaClass,cls).__new__(cls,name,bases,upper_attr)

#如果某个类需要使用自定义的元类，则需要使用命名关键字参数metaclass直接给出
class Foo2(metaclass=UpperAttrMetaClass):
	def bar(self):
		print("Foo2 BAR")

# Foo2().bar() #错误，属性bar已经被转换为大写的BAR
Foo2().BAR() #输出结果为 Foo2 BAR

#元类的主要用途是创建API
#关于元类的内容，还有待补充...