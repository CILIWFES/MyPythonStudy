import numpy as np
import math as math
import scipy.spatial.distance as dist
from typing import *

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


# 切比雪夫距离
def ChebyshevDistance(plot1, plot2):
    distance = np.abs(plot2 - plot1).max()
    return distance


# 夹角余弦
def Cosine(plot1, plot2):
    return (plot1 * plot2.T) / (math.sqrt(plot1 * plot1.T) * math.sqrt(plot2 * plot2.T))

#汉明距离,输入的是数值编码向量
def HammingDistance(plot1,plot2):
    nonZeroIndex=np.nonzero(plot2-plot1)
    return np.alen(nonZeroIndex)


#杰卡德距离,准确得来说是看两者相差的%
def JaccardDistance(plot1,plot2):
    matrix=np.append(plot1,plot2,0)
    return dist.pdist(matrix,"jaccard")#已经集成各个距离公式


matrix1 = np.mat([1, 0])
matrix2 = np.mat([0, 1])


print(ManhattonDistance(matrix1, matrix2))

print(ChebyshevDistance(matrix2, matrix1))

print(Cosine(matrix2, matrix1))#sqrt(2)

print(HammingDistance(matrix1,matrix2))

print(JaccardDistance(matrix1,matrix2))