class testClass:
    def __init__(self):
        self.name=6
        self.age=8
        print("className1")
    @staticmethod
    def testStatic():#静态方法
        return 5
    def testMethod(self):
        f="da"
        print("adsad")
    def __add__(self, other):
        return self.age*other.age
# a=testClass()
# b=a.testMethod
# print(b)
# print(type(b))
# print(b())

class testClass2():
    def __init__(self):
        self.age=5
        self.name=5
        print("className2")
    def testMethon2(self):
        print("wqewe")
    def __add__(self, other):
        return self.age+other.age


class testClass3(testClass2,testClass):#优先从左到右为标准
    def __init__(self,age):
        testClass.__init__(self)
        testClass2.__init__(self)
        print("className3")
        self.age=age;
    def testMethon3(self):
        print("wqewe")
# print(testClass2().testMethod())
test31=testClass3(10)
test32=testClass3(3)
print(test31+test32)



class staticTestClass:
    count=0
    def __init__(self):
        staticTestClass.count+=1;
        self.yy=0;
staticTest1=staticTestClass()
staticTest2=staticTestClass()

print("staticTest",staticTest1.count)
print("staticTes2",staticTest2.count)
print("staticTesClass",staticTestClass.count)

staticTestClass.count+=1
print("staticTest",staticTest1.count)
print("staticTes2",staticTest2.count)
print("staticTesClass",staticTestClass.count)

staticTest1.count+=1
print("staticTest",staticTest1.count)
print("staticTes2",staticTest2.count)
print("staticTesClass",staticTestClass.count)

staticTestClass.count+=1#一变全变
print("staticTest",staticTest1.count)
print("staticTes2",staticTest2.count)
print("staticTesClass",staticTestClass.count)


class attrTestClass:
    param0=10086
    def __init__(self):
        self.param1=19;
        self.param1=20;
        self.param2=22;
attrTest1=attrTestClass()
attrTest2=attrTestClass()


print('getattr',getattr(attrTest1,'param1',18))
print('getattrDefalt',getattr(attrTest1,'param12',18))#若属性不存在返回默认值18
print('getattrStatic',getattr(attrTestClass,'param0'))#获取全局变量

print('hasattr is',hasattr(attrTestClass,'param0'))#判断是否有变量
print('hasattr is',hasattr(attrTestClass,'param2'))#判断是否有变量
print('hasattr is',hasattr(attrTest1,'param2'))#判断是否有变量

print('getattr',getattr(attrTest1,'param2'))
setattr(attrTest1,'param2',2)#设置变量
print('getattr',getattr(attrTest1,'param2'))

print('getattr',getattr(attrTest1,'param2'))#删除前
delattr(attrTest1,'param2',2)#设置变量
print('getattr',getattr(attrTest1,'param2'))#删除后



