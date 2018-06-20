f=open(r'D:\Config.ini','r+')
"""
声明open(路径,模式,编码(utf8))
模式:
1.文本
r w rw a  对于字符流
只读 写 读写 追加
2.*b 二进制 对应字节流如 rb wb

r 只能读 
w 只能写 覆盖整个文件 不存在则创建 
a 只能写 从文件底部添加内容 不存在则创建 

1、使用'W'，文件若存在，首先要清空，然后（重新）创建，

2、使用'a'模式 ，把所有要写入文件的数据都追加到文件的末尾，即使你使用了seek（）指向文件的其他地方，如果文件不存在，将自动被创建。
"""
print(f.read())
f.seek(0)
print(f.read(2))
print(f.read(2))
print(f.read(2))
print(f.read(2))
print(f.read(2))
f.seek(0)
print(f.readline())#读取第一行
f.seek(0)
print(f.readlines())#读取出来放在列表里

f.close()
print()
f=open('D:\Config.ini','rb')
print(f.read())

import os
os.getcwd()#当前系统目录,当没写路径,默认在此地寻找(相对路径)
print(os.getcwd())

os.chdir("D:\\")#改变默认目录到D盘
print(os.getcwd())
f.close()

test=open('test.txt','w',encoding='utf8')#居然过编译了
a=['dadasda','weayaiuic\n','64545685']
test.write("asdasdasdasd\n")
test.write("sadada\n")
test.writelines(a)#a必须是全字符
test.flush()
test.close()
test=open('test1.txt','a',encoding='utf8')#居然过编译了
test.write("\n追加测试")
test.flush()
test.close()
a=0
with open('test.txt','r',encoding='utf8') as f:#自动close
    for line in f:
        print(line)
