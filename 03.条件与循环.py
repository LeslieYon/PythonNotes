#if语句
a = 20
if a >= 20 :
	print("a大于等于20")

#if...else语句
b = 20
if  b <= 5 :
	print("b小于5")
else :
	print("b大于5")

#if...elif...else语句
c = 20
if c <=	5 :
	print("c小于等于5")
elif c <= 10 : # 可以有多个elif分支
	print("c小于等于10")
elif c == 20 : # 也可以用表达式 c is 20 ，但这属于非标准用法
	print("c等于20")
else :
	print("c大于20")

#判断表达式简写
#只要x是非零数值、非空字符串、非空list等，就判断为True，否则为False
x = ""
if x:
	print("x为真")
else :
	print("x为假") #跳转到这里执行

#注意：条件表达式不能对不同类型的表达式进行比较
d = input("Please inupt a number:") #input函数的返回值类型为str
d = int(d) #若果没有这行，下面比较表达式会报错 TypeError
if d > 100 :
	print("d大于100")

#for...in...循环
e = range(101) #range函数：产生0~n-1的list
sum = 0 #注意变量作用域
for x in e : #也可以直接写for x in range(101)
	sum = sum + x
	#也可以写sum+=x
print(sum) #结果为5050

#while循环
x = 0
sum = 0
while x <= 100 :
	sum+=x; x+=1 #使用分号可以把多个语句写在同一行
print(sum) #结果为5050

#也可以使用break和continue关键字，与C语言相同