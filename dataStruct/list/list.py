"""序列是Python中最基本的数据结构。序列中的每个元素都分配一个数字 - 它的位置，或索引，第一个索引是0，第二个索引是1，依此类推。

Python有6个序列的内置类型，但最常见的是列表和元组。

序列都可以进行的操作包括索引，切片，加，乘，检查成员。

此外，Python已经内置确定序列的长度以及确定最大和最小的元素的方法。

列表是最常用的Python数据类型，它可以作为一个方括号内的逗号分隔值出现。

列表的数据项不需要具有相同的类型"""
"""----------------------------------------初始化----------------------------------------------------"""
print("##############初始化##############################")
a="test"
list1=['Google', 'Runoob', 1997.555, 2000]#可存放类型不同的值
list2=["a", "b", "c", "d",[4,8,"a's'das"],"pp",458785.358]#可存放列表
list3=[1, 2, True,3, "asd\nkdsa",4, 5.0 ,a,'dasdsada',"""
sdasdsadsad
sada
adsa""",87,False]#可存放变量
testList = ['下标0','下标1', '下标2', '下标3', '下标4','下标5','下标6','下标7','下标8','下标9']
lists=[list1,list2,list3]#列表可以放列表
print("list1:",list1,"""
list2""",list2,"""
list3""",list3,"""
总列表 list""",lists,"""
测试列表 testList""",testList)




"""-----------------------------------------读操作--------------------------------------------------"""
print("""################查操作####################""")

def find(i):
    print("查询下标为",i,"的元素list[",i,"]: ", testList[i])


def find2(i,j):
    print("查询起始下标为",i,"终止下标为",j,"之间的的元素list[",i,":",j,"]: ", testList[i:j])


# find2(2,5)





"""-----------------------------------------改操作--------------------------------------------------"""
print("""#################改操作####################""")
def update1():#简单修改
    print("第三个元素为 : ", testList[2])
    testList[2] = 2001
    print("更新后的第三个元素为 : ", testList[2])
def update2(i,j,list):#范围修改
    import copy;
    temp=copy.deepcopy(testList)
    print("第",i,"到第",j,"个之间的元素为 : ", temp[i:j])
    temp[i:j] = list
    print("更新后的list为 : ", temp)



# update2(1,2,[1,5,8,44]);



"""-----------------------------------------删操作--------------------------------------------------"""
print("""#################删操作####################""")
def delete():
    import copy
    temp=copy.deepcopy(testList);#深拷贝
    print("删除前:",testList)
    del temp[2]
    print("删除下标为2的元素 del testList[2]: ", temp)

def delete2(start,end):
    import copy
    temp = copy.deepcopy(testList);  # 深拷贝
    print("删除前:", testList)
    del temp[start:end]
    print("删除下标为",start,"到",end,"之间的的元素 del testList[",start,":",end,"]: ", temp)



#delete2(2,8)



"""-----------------------------------------Python列表脚本操作符--------------------------------------------------------
列表对 + 和 * 的操作符与字符串相似。+ 号用于组合列表，* 号用于重复列表。"""
print("""#################列表脚本操作符####################""")

print("testList列表的长度为:",len(testList))  # 获取testList列表的长度
tempList=[1,2,3,4,5];
print("testListt+tempList=",testList+tempList)
print(tempList*5)#重复五遍

print(tempList.append(6))#尾部添加6

print(tempList.append(6))#尾部添加6
print(tempList)

print(testList[-1])#倒数第一个

print(3 in tempList)#3在里面吗?在返回true

for x in tempList:#迭代遍历
    print(x)

print(id(testList.copy())==id(testList))

"""##############################################################################################################
心得体会:
列表的拆分:list[1:5],将会获得list[1]至list[4],一个4个值(包头不包尾)













"""
