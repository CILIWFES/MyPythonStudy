import numpy as np
import math as math
import scipy.spatial.distance as dist
from typing import *

matrix1 = np.mat([1, 0])
matrix2 = np.mat([0, 1])
"""
皆是(矩阵表示的)向量操作
"""


# 闵科夫斯基距离
def MinkowskiDistance(plot1, plot2, powerNumber: int):
    sum = np.abs(np.power(plot1 - plot2, powerNumber)).sum()
    distance = math.pow(sum, 1.0 / powerNumber)
    return distance


# 欧式距离
def EuclideanDistance(plot1, plot2):
    return MinkowskiDistance(plot1, plot2, 2)


# 曼哈顿距离
def ManhattonDistance(plot1, plot2):
    return MinkowskiDistance(plot1, plot2, 1)


print(ManhattonDistance(matrix1, matrix2))


# 切比雪夫距离
def ChebyshevDistance(plot1, plot2):
    distance = np.abs(plot2 - plot1).max()
    return distance


print(ChebyshevDistance(matrix2, matrix1))


# 夹角余弦
def Cosine(plot1, plot2):
    return (plot1 * plot2.T) / (math.sqrt(plot1 * plot1.T) * math.sqrt(plot2 * plot2.T))


print(Cosine(matrix2, matrix1).sum())  # sqrt(2)


# 汉明距离,输入的是数值编码向量
def HammingDistance(dataSet1, dataSet2):
    nonZeroIndex = np.nonzero(dataSet2 - dataSet1)
    return np.alen(nonZeroIndex)


print(HammingDistance(matrix1, matrix2))


# 杰卡德距离,准确得来说是看两者相差的%
def JaccardDistance(dataSet1, dataSet2):
    matrix = np.append(dataSet1, dataSet2, 0)
    return dist.pdist(matrix, "jaccard").sum()  # 已经集成各个距离公式


print(JaccardDistance(matrix1, matrix2))


# 相关计算
# =1-相关系数
# 相关系数 p=协方差/样本一标准差
def CorrelationCoefficient(dataSet1, dataSet2):
    # 使用Numpy求标准差系数
    # return np.corrcoef(np.append(dataSet1,dataSet2,0))
    # 自己计算
    # 计算均值
    avg1 = np.mean(dataSet1)
    avg2 = np.mean(dataSet2)

    # 自己写的标准差
    # print(np.power(np.power(dataSet1-avg1,2).sum()/np.alen(dataSet1),0.5))

    # 计算标准差方差
    dv1 = np.std(dataSet1)
    dv2 = np.std(dataSet2)

    print("协方差=",np.cov(dataSet1-avg1,dataSet2-avg2))

    # 协方差/两个标准差的乘积
    p = np.mean(np.multiply(dataSet1 - avg1, dataSet2 - avg2)) / (dv1 * dv2)
    # 相关系数
    return p


print(CorrelationCoefficient(matrix1, matrix2))


# 马氏距离
def MahalanobisDistance(dataSet1, dataSet2):
    # 求协方差的逆矩阵
    covinv = np.linalg.inv(np.cov(np.append(dataSet1, dataSet2, 0)))
    x1_x2 = dataSet1 - dataSet2
    distma = np.sqrt(x1_x2.T * covinv * x1_x2)
    return distma

print(ManhattonDistance(matrix1, matrix2))

