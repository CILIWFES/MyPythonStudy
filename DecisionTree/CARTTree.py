from collections import Counter
from math import pow


class CARTTree(object):
    def __init__(self):
        self.tree = {}
        self.classList = []
        self.isDiscrete = True
        self.function = None

    # 主函数入口
    def train(self, trainSet, classList, isDiscrete):
        # 选择要处理的数据类型,并对离散型数据进行转化
        self.classList = {k: indx for indx, k in enumerate(classList)}
        self.selectFunction(isDiscrete)
        self.tree = self.buildTree(trainSet, classList)

    def selectFunction(self, isDiscrete):
        if isDiscrete:
            self.function = self.Discrete
        else:
            self.function = self.Continuous

    # 离散型 计算Gini基尼指数
    # lst1与ls2皆为预测项
    def Discrete(self, lst1, lst2):
        # calculate freqency
        fre1 = list(Counter(lst1).values())
        fre2 = list(Counter(lst2).values())

        size1 = float(len(lst1))
        size2 = float(len(lst2))
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
    # lst1与ls2皆为预测项
    def Continuous(self, lst1, lst2):
        avg1 = sum(lst1) / len(lst1)
        avg2 = sum(lst2) / len(lst2)
        result1 = 0
        result2 = 0
        for item in lst1:
            result1 += pow(item - avg1, 2)
        result1 = pow(result1 / float(len(lst1)), 0.5)

        for item in lst2:
            result2 += pow(item - avg2, 2)
        result2 = pow(result2 / float(len(lst2)), 0.5)
        return result1 + result2

    def buildTree(self, trainSet, classSet):

        # 递归结束判断
        # 1.
        classList = [data[-1] for data in trainSet]
        counter = Counter(classList)
        if len(counter.values()) == 1:  # 正常结局
            return counter.most_common().pop(0)[0]
        if len(trainSet[0]) == 2 and len(set([data[0] for data in trainSet])) == 1:  # 错误数据的结局
            return counter.most_common().pop(0)[0]
        # 2.

        minSelect = (0, "")
        # 初始越大越好
        minValue = 100
        # 遍历条件,选择最优切分条件与最优切分点
        for indx in range(len(trainSet[0]) - 1):
            lst = [data[indx] for data in trainSet]
            featureSet = set(lst)

            del lst
            featureDict = {}
            # 获取分割的分类
            for feature in featureSet:
                tempLst = [data[-1] for data in trainSet if data[indx] == feature]
                featureDict[feature] = tempLst

            del featureSet
            # 选择最小的分类
            minFeatureValue = 1.1
            minFeature = ''
            for feature, lst in featureDict.items():
                otherList = [data[-1] for data in trainSet if data[indx] != feature]
                returnValue = self.function(lst, otherList)
                if returnValue < minFeatureValue:
                    minFeatureValue = returnValue
                    minFeature = feature
            if minFeatureValue < minValue:
                minValue = minFeatureValue
                minSelect = (indx, minFeature, list(set([data[indx] for data in trainSet if data[indx] != minFeature])))

        leftLst = []
        rightLst = []
        # 下面要针对切分点进行切分
        for indx in range(len(trainSet)):
            # 切分时最好能把最优切分特征列给删除
            temp = trainSet[indx][:]
            featureTemp = temp[minSelect[0]]
            del temp[minSelect[0]]
            if featureTemp == minSelect[1]:
                leftLst.append(temp)
            else:
                rightLst.append(temp)

        featureName = classSet[minSelect[0]]
        classSet = classSet[:]
        del classSet[minSelect[0]]

        # 建立tree,放入最优节点
        # 递归左节点
        # 递归右节点
        tree = {featureName: {minSelect[1]: self.buildTree(leftLst, classSet),
                              str(minSelect[2]): self.buildTree(rightLst, classSet)}}
        return tree

    def predict(self, tree, testLst):
        tempLst = list(tree.items())[0]
        rootName = tempLst[0]
        childDict = tempLst[1]
        indx = self.classList[rootName]
        del rootName
        value = str(testLst[indx])
        if value in childDict:
            tree = childDict[value]
            if type(tree) is str:
                return tree
            else:
                del tempLst
                return self.predict(tree, testLst)
        else:
            tempDict = list(childDict.items())
            selectIndx = 0
            for i in range(len(tempDict)):
                if type(eval(tempDict[i][0])) is list:
                    selectIndx = i
                    break
            tree = tempDict[selectIndx][1]
            if type(tree) is str:
                return tree
            else:
                del tempLst
                del tempDict
                return self.predict(tree, testLst)

    def getDumpData(self):
        data = dict()
        data['tree'] = self.tree
        data['classList'] = self.classList
        return data

    def loadDumpData(self, data):
        self.tree = data['tree']
        self.classList = data['classList']
        return self
