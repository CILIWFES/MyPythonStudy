from collections import Counter
from math import pow
import numpy as np

class CART(object):
    def __init__(self):
        self.tree = {}
        self.classList = []
        self.isDiscrete = True
        self.function = None

    # 主函数入口
    def train(self, trainSet, classList, isDiscrete):
        trainSet=np.mat(trainSet)
        classList=np.mat(classList)
        # 选择要处理的数据类型,并对离散型数据进行转化
        self.selectFunction(isDiscrete)
        self.classList = classList[:]
        self.buildTree(trainSet, classList)

    def selectFunction(self, isDiscrete):
        if isDiscrete:
            self.function = self.Discrete
        else:
            self.function = self.Continuous

    # 离散型 计算Gini基尼指数
    def Discrete(self, vec1, vec2):
        vec1=vec1.T
        vec2=vec2.T
        # calculate freqency
        fre1 = list(Counter(vec1.tolist()[0]).values())
        fre2 = list(Counter(vec2.tolist()[0]).values())

        size1 = float(np.alen(vec1))
        size2 = float(np.alen(vec2))
        result1 = 1
        result2 = 1

        for item in fre1:
            result1 -= pow(item / float(size1), 2)

        for item in fre2:
            result2 -= pow(item / float(size2), 2)

        result1 = result1 * size1 / float(size1 + size2)
        result2 = result2 * size2 / float(size1 + size2)
        return result2 + result1

    # 连续型,计算方差
    def Continuous(self, vec1, vec2):
        vec1=vec1.astype(float).T
        vec2=vec2.astype(float).T
        avg1 = np.sum(vec1) / np.alen(vec1)
        avg2 = np.sum(vec2) / np.alen(vec2)
        result1 = 0
        result2 = 0
        for item in vec1.tolist()[0]:
            result1 += pow(item - avg1, 2)
        result1 = pow(result1 / float(np.alen(vec1)), 0.5)

        for item in vec2.tolist()[0]:
            result2 += pow(item - avg2, 2)
        result2 = pow(result2 / float(np.alen(vec2)), 0.5)
        return result1 + result2

    def buildTree(self, trainSet, classList):

        for indx in range(np.shape(trainSet)[1]):
            lst=trainSet[:,indx].T.tolist()[0]
            for item in set(lst):


