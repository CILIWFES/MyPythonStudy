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
    param=777
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

print('delattr',getattr(attrTest1,'param2'))#删除前
delattr(attrTest1,'param2')#删除变量
print('delattr',getattr(attrTest1,'param2',20))#删除后


print('delattr',getattr(attrTestClass,'param0'))#删除前
delattr(attrTestClass,'param0')#删除变量
print('delattrattrTestClass',getattr(attrTestClass,'param0',16))#删除后的静态类
print('delattrattrTest1',getattr(attrTest1,'param0',16))#删除后的对象



print('delattr',getattr(attrTest1,'param'))#删除前
#delattr(attrTest1,'param')#不能再对象内删除静态变量
print('attrTestClass',getattr(attrTestClass,'param',16))#删除后的静态类
print('attrTest1',getattr(attrTest1,'param',16))#删除后的对象


setattr(attrTest1,"sdasa",555)#可以设置变量
print("LALALALLALALALLALALALALLALALLAL",getattr(attrTest1,"sdasa",5))




class pythonClass:
    "doc显示这里的信息"
    count=1;
    def __init__(self):
        self.name="HelloClass"
    def showWord(self):
        print('Word')
    def __del__(self):
        className=self.__class__.__name__
        print(className,'被销毁')
print(pythonClass.__dict__)
print(type(pythonClass.__dict__))

print(pythonClass().__dict__)
print(type(pythonClass().__dict__))

print(pythonClass.__doc__)
print(pythonClass().__doc__)
print(type(pythonClass.__doc__))

print(pythonClass.__module__)#__module__: 类定义所在的模块（类的全名是'__main__.className'，如果类位于一个导入模块mymod中，那么className.__module__ 等于 mymod）
print(pythonClass().__module__)
print(type(pythonClass.__module__))

print(pythonClass.__bases__)
print(type(pythonClass.__bases__)) #__bases__ : 类的所有父类构成元素（包含了一个由所有父类组成的元组）

test=pythonClass()
# del test
del pythonClass#可以删除类声明
print(test)#删除后仍然可以使用类

class operatorClassTest1:
    key = "default"
    value = 0
    def __add__(self, other):
        ret = self.value
        if other.key == self.key:
            ret += other.value
        return ret


class operatorClassTest2:
    key = "default"
    value = 0
    def __add__(self, other):
        ret = other.value
        if other.key == self.key:
            ret += self.value
        return ret


class operatorClassTest3:
    key = "default"
    valueTest=0

test1=operatorClassTest1()
test1.value=1
test2=operatorClassTest2()
test2.value=2
test3=operatorClassTest3()
test3.valueTest=3
print('first',test1+test2)#最直接大的应用
test2.key='getSmoeThing'
print('scend',test1+test2)#内部逻辑影响输出结果

print('otner',test2+test1)#反向主体(自创的词)

#print("test",test1+test3)#会报错

class memberClass:
    __testSelfParam=0
    _testChileParam=1
    testPublicParam=2
    def __private(self):
        print("private is start")
    def _protected(self):
        print("protected is start")
class chileMemberClass(memberClass):
    def __init__(self):
        a=1
    def __test(self):
        print(555)
    def _chileMemberClass(self):
        print('保护方法被调用')
    def go(self):
        self._protected()

test1=chileMemberClass()
print(test1.testPublicParam)#不能直接调用保护方法
test1.go()





