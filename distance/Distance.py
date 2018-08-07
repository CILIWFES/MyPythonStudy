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
    matrix=np.append(dataSet1, dataSet2, 0)
    # 求协方差的逆矩阵
    covinv = np.linalg.inv(np.cov(matrix))
    x1_x2 = matrix.T[0] - matrix.T[1]
    distma = np.sqrt(np.dot(np.dot(x1_x2,covinv), x1_x2.T))
    return distma

matrix3=np.mat([88.5, 96.8, 104.1, 111.3, 117.7, 124.0, 130.0, 135.4, 140.2, 145.3, 151.9, 159.5, 165.9, 169.8, 171.6, 172.3, 172.7])
matrix4=np.mat([12.54, 14.65,16.64,18.98,21.26,24.06,27.33,30.46,33.74,37.69,42.49,48.08,53.37,57.08,59.35,60.68,61.40])
print(MahalanobisDistance(matrix3, matrix4))
print(np.cov(np.append(matrix3, matrix4, 0)))


matrix3=np.mat([88.5, 96.8, 104.1, 111.3, 117.7, 124.0, 130.0, 135.4, 140.2, 145.3, 151.9, 159.5, 165.9, 169.8, 171.6, 172.3, 172.7])
matrix4=np.mat([12.54, 14.65,16.64,18.98,21.26,24.06,27.33,30.46,33.74,37.69,42.49,48.08,53.37,57.08,59.35,60.68,61.40])
avgX1=np.sum(matrix3)/np.shape(matrix3)[1]

avgX2=np.sum(matrix4)/np.shape(matrix4)[1]
matrix=np.append(matrix3-avgX1, matrix4-avgX2, 0)

print((matrix*matrix.T)/(np.shape(matrix)[1]-1))

