from collections import Counter
from math import pow


class CART(object):
    def __init__(self):
        self.tree = {}
        self.classList = []
        self.isDiscrete = True
        self.function = None

    # 主函数入口
    def train(self, trainSet, classList, isDiscrete):
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
    def Discrete(self, lst1, vec2):
        lst1 = lst1.T
        vec2 = vec2.T
        # calculate freqency
        fre1 = list(Counter(lst1.tolist()[0]).values())
        fre2 = list(Counter(vec2.tolist()[0]).values())

        size1 = float(len(lst1))
        size2 = float(len(vec2))
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
    def Continuous(self, lst1, lst2):
        avg1 = sum(lst1) / len(lst1)
        avg2 = sum(lst2) / len(lst2)
        result1 = 0
        result2 = 0
        for item in lst1.tolist()[0]:
            result1 += pow(item - avg1, 2)
        result1 = pow(result1 / float(len(lst1)), 0.5)

        for item in lst2.tolist()[0]:
            result2 += pow(item - avg2, 2)
        result2 = pow(result2 / float(len(lst2)), 0.5)
        return result1 + result2

    def buildTree(self, trainSet, classList):
        classSet = [data[-1] for data in trainSet]
        for indx in range(len(classSet)):
            # 先按列切割
            allLst = [data[indx] for data in trainSet]
            allSet = set(allLst)
            lst = []
            for item in allSet:
                lst.append([data for data in allLst if data == item])

            # 开始选择
            for item in lst:
                otherLst
