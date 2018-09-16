import sys
import os
import numpy as np

print(sys.getdefaultencoding())

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0] + "/Support/chapter01"


# 读取字符串并转化为数值类型
def fileToMatrix(path, delimiter):
    recordlist = []
    fp = open(path, "r")
    content = fp.read()
    fp.close()
    rowlist = content.splitlines()
    recordlist = [list(map(eval, row.split(delimiter))) for row in rowlist if row.strip()]
    return np.mat(recordlist)


# pathList = os.listdir(rootPath)
# for path in pathList:
#   recordmat = fileToMatrix(rootPath + "/" + path, "\t")
recordmat = fileToMatrix(rootPath + "/test.txt", "\t")
print(recordmat)

import pickle

file_obj = open(rootPath + "/rocordmat.dat", "wb")  # 必须要wb
# 序列化
pickle.dump(recordmat, file_obj)
file_obj.close()
# 读取序列化文件
read_obj = open(rootPath + "/rocordmat.dat", "rb")  # 必须rb
readmat = pickle.load(read_obj)
print(readmat)


# 读取一定行数的文件
def readFileLines(path, nmax=0):
    fp = open(path, "r")
    ncount = 0
    while True:
        content = fp.readline()
        if content == "" or (ncount >= nmax and nmax != 0):
            break
        yield content
        if nmax != 0: ncount += 1
    fp.close()


for line in readFileLines(rootPath + "/test.txt", 20):
    print(line.strip())  # 消除回车

import matplotlib.pyplot as plt

# 生成曲线数据
x = np.linspace(-5, 5, 200)
y = np.sin(x)
# 生成0~len(y)的噪声
yn = y + np.random.rand(1, len(y)) * 1.5 - 1.5 / 2
# 绘图
fig = plt.figure()
# 把画布分成1行1列 1x1块,当前画布处于第1块
ax = fig.add_subplot(1, 1, 1)
# 绘制散点图
ax.scatter(x, yn, s=10, color='blue', marker='o')
# 绘制图线
ax.plot(x, y, color='r')
plt.show()

# 树与分类结构的可视化
from ML import TreePlotter as tp

myTree = {'root': {0: 'lef node', 1: {'level 2': {0: 'leaf node', 1: 'leaf node'}},
                   2: {'lead 2': {0: 'leaf node', 1: 'leaf node'}}}}
tp.createPlot(myTree)

# 图与网格结构的可视化
data = np.mat([[0.1, 0.1], [0.9, 0.5], [0.3, 0.6], [0.7, 0.2], [0.1, 0.7], [0.5, 0.1]])
m, n = np.shape(data)
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.scatter(data.T[0].tolist(), data.T[1].tolist(), color='blue', marker='o')

for point in data.tolist():
    plt.annotate("(" + str(point[0]) + "," + str(point[1]) + ")", xy=(point[0], point[1]))
xList = []
yList = []
for px, py in zip(data.T.tolist()[0], data.T.tolist()[1]):
    xList.append([px])
    yList.append([py])
ax.plot(xList, yList, 'r')
plt.show()
