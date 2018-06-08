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