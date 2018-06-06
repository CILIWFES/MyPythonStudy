dict={"test":1,"aa":5}
print(type(dict))
print(dict)
del dict["test"]
print(dict)

dict["66"]="45";
dict[0.5]=6;

print('aa' in dict)
for x in dict:
    print(x,"add",dict[x])

print(id(dict)==id(dict.copy()))
print(dict.fromkeys([0,2,5,""],5))#获得一个新字典,由序列作为其字典的key,5为默认value

print(dict.get("aa",9))
del dict['aa']
print(dict.get("aa",9))#获取不到返回默认值9


print(dict.keys())
print(dict.values())
print(dict.pop('66',5))#删除key66,并且返回值
print(dict.pop('66',5))#不存在值时返回5
dict['sda']='dadad'
dict["485d"]="adsdaa"

print(dict)
print(dict.popitem())#随机返回并删除一对键值,一般为末尾对
print(dict)


dict1={6:5,7:8,9:10}
dict2={5:5,7:8,6:10}
print(dict1.update(dict2))#更新dict1的值到dict2
print(dict1)
