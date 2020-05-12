#面向对象程序设计(OOP)，是一种以对象为主体的编程方式
#面向对象程序设计至少具备封装、继承、多态三大特性

class Human(object): #一个基类。任何基类都要派生于object类
	def __init__(self,sex): #构造函数。任何成员函数都需要有第一个默认参数self，相当于C++的this指针
		self.__sex = sex #初始化基类的数据成员。将数据成员命名为__开头，表示其为私有成员。如果命名是单下划线开头，则是建议为私有成员(非强制性)
	def set_sex(self,sex): #私有成员需要通过函数接口进行访问，实现了封装性
		self.__sex = sex
	def get_sex(self):
		return self.__sex
	def show_sex(self):
		if self.get_sex()=="男":
			print("男性")
		else: print("女性")

class Student(Human): #一个派生类，派生于Human类，实现了继承性
	num_of_Student = 0 #该对象属于类成员，为全体类对象共有，类似于C++的静态成员。注意，类属性会被同名的实例属性隐藏
	def __init__(self,name,score,sex):
		Human.__init__(self,sex) #显式调用基类的构造函数，对派生类对象的基类成员进行初始化
		self.__name = name #初始化派生类的数据成员
		self.__score = score
		Student.num_of_Student += 1 #使用类属性统计学生的数量
	def __str__(self): #重载的__str__函数，可以重定义Student类实例转换为字符串的行为
		retn_str = "Student Object ("
		retn_str += "name:" + self.__name + " "
		retn_str += "score:" + str(self.__score) + " "
		retn_str += "school:" + getattr(self,"SchoolName","[None]") + " " #getattr()函数可以从某实例中读取某属性，第三个参数为读取不到该属性时默认的返回值，若不提供这个参数，读取不到该属性时则抛出AttributeError异常
		if hasattr(self,"studentID"): #setattr()函数可以检查某实例是否包含某属性
			retn_str += "ID:" + str(self.studentID) + " "
		retn_str += ")"
		return retn_str
	def set_grade(self,score): #派生类私有成员的访问接口
		if 0 <= score <= 100: #python中可以使用形如 0 <= score <= 100 的连等式
			self.__score = score
		else:
			raise ValueError("Bad Score!") #对于赋值数据成员操作的合法性进行检查
	def get_grade(self):
		if self.__score >= 90:
			return "A"
		elif self.__score >= 60:
			return "B"
		else: return "C"
	def show_sex(self): #派生类的show_sex函数覆盖了基类的show_sex函数，实现了多态性
		if self.get_sex()=="男": #派生类要通过基类的公共接口才能访问基类的私有成员
			print("男学生")
		else: print("女学生")

#基础操作
mike = Student("Mike",97,"男") #定义一个Student类对象mike
mike.set_sex("女") #通过从基类继承来的方法操作对象
mike.show_sex() #通过派生类重载的方法操作对象。输出结果为 女学生
print(mike._Human__sex) #可以通过类似 _Human__sex 的形式强制访问对象的私有成员（不推荐操作），这是因为实际上__开头的成员会被python解释器解释为 _Human__sex 的形式

#可以后期为对象添加成员（注意：无论添加的是数据成员还是函数成员，都只对添加的那个对象有效，对所属类的其它对象无效）
mike.studentID = "123456" #为对象添加数据成员（后期添加的成员，即使以__开头也不会被看做是私有成员，且会造成成员函数内访问困难）
def show_studentID(self):
	print(self.studentID)
import types
mike.studentID = "456789" #后期添加的成员，即使以__开头也不会被看做是私有成员，本次修改有效
mike.show_studentID = types.MethodType(show_studentID,mike) #使用types.MethodType()为对象添加函数成员
mike.show_studentID() #输出结果为 456789

#可以后期为类添加成员（对全体类成员有效。注意：为所有成员后期添加的属性，即使以__开头也仍然不会被看做是私有成员）
Student.SchoolName = "Default School" #为Student类所有成员添加SchoolName数据成员，其默认值为"Default School"
def set_SchoolName(self,SchoolName):
	self.SchoolName = SchoolName
Student.set_SchoolName = set_SchoolName #为Student类所有成员添加set_SchoolName函数
mike.set_SchoolName("Tsinghua")
print(mike.SchoolName) #输出结果为 Tsinghua

#可以通过重载的__str__函数直接输出mike对象
print(mike) #输出结果为 Student Object (name:Mike score:97 school:Tsinghua ID:456789 )

#不能通过 对象名.私有成员名 访问这个私有成员
#尤其是赋值语句，可以成功执行是因为这行语句实际意味着为该对象后期添加了一个公有的成员，而不是修改对应的私有成员，真正的私有成员会被python解释器实际解释为 _Human__sex 的形式
mike.__score = 60 #看似“更改”了私有成员的值
print(mike.get_grade()) #输出结果仍然为 A

#可以使用type()函数获取某对象的类型
print(type(mike)) #输出结果为 <class '__main__.Student'>

#可以使用isinstance()函数判断某对象的类型
isinstance(mike,Student) # True
isinstance(mike,Human) # True
isinstance(mike,type(mike)) #True
isinstance(mike,(Student,int)) #True 该表达式表示mike是否是(Student,int)中的类型之一
issubclass(Human,Student) #False issubclass()函数可以判断两个参数中前者是否是后者的派生类
issubclass(Student,Human) #True

#使用dir()函数可以获取某对象的所有成员
#形如__dir__的成员是系统使用的特殊成员，例如__str__可以用于重定义Student类实例转换为字符串
print(dir(mike))
#输出结果如下 ['_Human__sex', '_Student__name', '_Student__score', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__score', '__setattr__', '__sizeof__', '__str__', '__studentID', '__subclasshook__', '__weakref__', 'get_grade', 'get_sex', 'set_grade', 'set_sex', 'show_sex', 'show_studentID']
print(dir(int))
#输出结果如下 ['__abs__', '__add__', '__and__', '__bool__', '__ceil__', '__class__', '__delattr__', '__dir__', '__divmod__', '__doc__', '__eq__', '__float__', '__floor__', '__floordiv__', '__format__', '__ge__', '__getattribute__', '__getnewargs__', '__gt__', '__hash__', '__index__', '__init__', '__init_subclass__', '__int__', '__invert__', '__le__', '__lshift__', '__lt__', '__mod__', '__mul__', '__ne__', '__neg__', '__new__', '__or__', '__pos__', '__pow__', '__radd__', '__rand__', '__rdivmod__', '__reduce__', '__reduce_ex__', '__repr__', '__rfloordiv__', '__rlshift__', '__rmod__', '__rmul__', '__ror__', '__round__', '__rpow__', '__rrshift__', '__rshift__', '__rsub__', '__rtruediv__', '__rxor__', '__setattr__', '__sizeof__', '__str__', '__sub__', '__subclasshook__', '__truediv__', '__trunc__', '__xor__', 'as_integer_ratio', 'bit_length', 'conjugate', 'denominator', 'from_bytes', 'imag', 'numerator', 'real', 'to_bytes']

#使用类属性可以实时统计学生的数量
print(mike.num_of_Student,Student.num_of_Student) #输出结果为 1 1