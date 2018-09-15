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
# ddof=1表示n-1

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
    dv1 = np.std(dataSet1, ddof=1)
    dv2 = np.std(dataSet2, ddof=1)

    print("协方差=", np.cov(dataSet1 - avg1, dataSet2 - avg2))

    # 协方差/两个标准差的乘积
    p = np.mean(np.multiply(dataSet1 - avg1, dataSet2 - avg2)) / (dv1 * dv2)
    # 相关系数
    return p


print(CorrelationCoefficient(matrix1, matrix2))


def myCov(dataSet1, dataSet2):
    # print(np.cov(np.append(dataSet1, dataSet2, 0)))
    dataSet1 = np.mat(
        [88.5, 96.8, 104.1, 111.3, 117.7, 124.0, 130.0, 135.4, 140.2, 145.3, 151.9, 159.5, 165.9, 169.8, 171.6, 172.3,
         172.7])
    dataSet2 = np.mat(
        [12.54, 14.65, 16.64, 18.98, 21.26, 24.06, 27.33, 30.46, 33.74, 37.69, 42.49, 48.08, 53.37, 57.08, 59.35, 60.68,
         61.40])
    avgX1 = dataSet1.mean()

    avgX2 = dataSet2.mean()
    matrix = np.append(dataSet1 - avgX1, dataSet2 - avgX2, 0)

    return (matrix * matrix.T) / (np.shape(matrix)[1] - 1)


print(myCov(None, None))


# 马氏距离
def MahalanobisDistance(dataSet1, dataSet2):
    matrix = np.append(dataSet1, dataSet2, 0)
    # 求协方差的逆矩阵
    covinv = np.linalg.inv(np.cov(matrix, ddof=1))

    def MahalanobisClosure(plot1, plot2):  # 返回闭包增加灵活性
        x1_x2 = plot1 - plot2
        distma = np.sqrt(x1_x2 * covinv * x1_x2.T)
        return distma

    return MahalanobisClosure


matrix3 = np.mat(
    [88.5, 96.8, 104.1, 111.3, 117.7, 124.0, 130.0, 135.4, 140.2, 145.3, 151.9, 159.5, 165.9, 169.8, 171.6, 172.3,
     172.7])
matrix4 = np.mat(
    [12.54, 14.65, 16.64, 18.98, 21.26, 24.06, 27.33, 30.46, 33.74, 37.69, 42.49, 48.08, 53.37, 57.08, 59.35, 60.68,
     61.40]
)
MahalanobisClosure = MahalanobisDistance(matrix3, matrix4)
matrix = np.append(matrix3, matrix4, 0).T
print(MahalanobisClosure(matrix[0], matrix[1]))


# 求特征值与特征向量
def getEigenvalues(matrix):
    evals, evecs = np.linalg.eig(matrix)
    return evals, evecs


matrix = np.mat([[8, 1, 6], [3, 5, 7], [4, 9, 2]])
evals, evecs = getEigenvalues(matrix)
print("特征值:", evals)
print("特征向量:", evecs)


# 由特征值与特征向量还原矩阵
def goBack(evals, evecs):
    sigma = evals * np.eye(np.alen(evals))  # 特征值构成的对焦矩阵
    return evecs * sigma * np.linalg.inv(evecs)


print(goBack(evals, evecs))


# 加权欧式距离
def WeightedEuclideanDistance(plot1, plot2):
    matrix = np.append(plot1, plot2, 0)
    # stdMatrix = np.std(matrix, axis=0, ddof=1)
    # print(stdMatrix)
    # matrix=np.multiply(matrix,1/stdMatrix)
    # matrix=matrix[0]-matrix[1]
    # matrix=np.sqrt(matrix*matrix.T)
    varmat = np.std(matrix.T, axis=0)
    normvmat = (matrix - np.mean(matrix)) / varmat.T
    normvl2 = normvmat[0] - normvmat[1]
    matrix = np.sqrt(normvl2 * normvl2.T)
    return matrix

matrix2 = np.mat([[4, 5, 6]])
matrix1 = np.mat([[1, 2, 3]])
print(WeightedEuclideanDistance(matrix1, matrix2))
