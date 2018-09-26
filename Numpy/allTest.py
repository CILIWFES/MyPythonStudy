from numpy import *
import matplotlib.pyplot as plt
import random
import os

dataSet = list()  # 生成dataSet向量集
# 赋予随机数[  [a,b],[],[]]
for i in range(10):
    list = [random.random(), random.random()]
    dataSet.append(list)

# dataSet.appe?nd([1,2,3])#测试行数不满足的转变结果
print(dataSet)

# 转化为矩阵
dataMat = mat(dataSet)
print(dataMat)

print(dataMat.T)
dataMat = dataMat.T  # 矩阵转置

plt.scatter(dataMat[0].tolist(), dataMat[1].tolist(), c='red', marker='o')

x = np.linspace(-2, 2, 100)  # 生成-2到2,100个样本
print(x)

y = 2.8 * x + 9  # 得到对应的y样本

plt.plot(x, y)  # 生成线图,平滑连接

plt.show()  # 展示
