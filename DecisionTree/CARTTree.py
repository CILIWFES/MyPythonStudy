from math import pow
from DecisionTree.DataBean import DataBean


class CARTTree(object):
    def __init__(self):
        self.tree = {}
        self.classNameIndex = {}
        self.classIndex = {}
        self.isDiscrete = True
        self.function = None
        self.trainSet = None
        self.rootDataBean = None

    def makeDataBean(self, featureIndexReal, featuresValue, featuresOtherValue, beforDataBean):
        if beforDataBean is None:
            rows = [i for i in range(len(self.trainSet))]
            featurs = [i for i in range(len(self.trainSet[0]) - 1)]
            return DataBean(self.trainSet, rows, featurs, -1, -1)

        left = DataBean(self.trainSet, None, None, featureIndexReal, featuresValue, True, beforDataBean)
        right = DataBean(self.trainSet, None, None, featureIndexReal, featuresOtherValue, False, beforDataBean)
        return left, right

    # 主函数入口
    def train(self, trainSet, classList, isDiscrete):
        self.trainSet = trainSet
        # 选择要处理的数据类型,并对离散型数据进行转化
        self.classNameIndex = {k: indx for indx, k in enumerate(classList)}
        self.classIndex = {indx: k for indx, k in enumerate(classList)}
        self.selectFunction(isDiscrete)
        self.rootDataBean = self.makeDataBean(None, None, None, None)
        self.tree = self.buildTree(self.rootDataBean)

    def selectFunction(self, isDiscrete):
        if isDiscrete:
            self.function = self.Discrete
        else:
            self.function = self.Continuous

    # 离散型 计算Gini基尼指数
    # lst1与ls2皆为预测项
    def Discrete(self, choiceCnt, unionCnt):
        size1 = sum(choiceCnt)
        size2 = sum(unionCnt)
        result1 = 1
        result2 = 1

        for item in choiceCnt:
            result1 -= pow(item / float(size1), 2)

        for item in unionCnt:
            result2 -= pow(item / float(size2), 2)

        result1 = result1 * size1 / float(size1 + size2)
        result2 = result2 * size2 / float(size1 + size2)
        return result2 + result1

    # 连续型,计算方差
    # lst1与ls2皆为预测项
    # 也可以按区间,算区间内外的信息增益或者基尼系数
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

    # 策略树核心,递归调用
    def buildTree(self, dataBean: DataBean):

        # 递归结束判断
        labelInfo = dataBean.getLabelInfo()
        lenLabelInfo = len(labelInfo.most_common())
        if lenLabelInfo == 1:  # 正常结局
            return labelInfo.most_common()[0][0]
        elif len(dataBean.featurs) <= 0 or (
                len(dataBean.featurs) == 1 and len(dataBean.featureInfo(-1)) == 1):  # 错误数据的结局
            return labelInfo.most_common()[0][0]
        # 2.
        minSelect = None
        # 初始越大越好
        minValue = 999
        # 遍历条件,选择最优切分条件与最优切分点
        for indx in range(dataBean.lenFeaturs()):
            featureInfo = dataBean.featureInfo(indx)
            # 选择最小的分类
            minFeatureValue = 999
            otherFeatures = []
            minFeatureTemp = ""
            minFeature = ""
            # 遍历子集
            for key, item in featureInfo.items():
                lst = [v for k, v in item.items() if k is not 'all']
                # 拼接其他字符串
                otherLst = self.MergeOtherDict(featureInfo, key)
                returnValue = self.function(lst, otherLst)
                if returnValue < minFeatureValue:
                    minFeatureValue = returnValue
                    if minFeatureTemp:
                        otherFeatures.append(minFeatureTemp)
                    minFeatureTemp = key
                else:
                    otherFeatures.append(key)

            if minFeatureValue < minValue:
                minValue = minFeatureValue
                minFeature = minFeatureTemp
                realFeatureIndex = dataBean.getFeature(indx)
                minSelect = (realFeatureIndex, self.classIndex[realFeatureIndex], minFeature, otherFeatures)

        # 建立tree,放入最优节点
        # 递归左节点
        # 递归右节点
        left, right = self.makeDataBean(minSelect[0], minSelect[2], minSelect[3], dataBean)
        dataBean.choiceFeatureIndx = minSelect[0]
        dataBean.choiceFeatureValue = left
        dataBean.choiceFeatureOtherValue = right

        tree = {minSelect[1]: {minSelect[2]: self.buildTree(left),
                               str(minSelect[3]): self.buildTree(right)}}
        return tree

    # 合并其他字典key,基尼系数
    def MergeOtherDict(self, featureInfo, key):
        otherDic = {}
        for otherKey, otherItem in featureInfo.items():
            if otherKey is not key:
                for itemKey, item in otherItem.items():

                    if itemKey is not 'all':
                        if itemKey in otherDic:
                            otherDic[itemKey] += item
                        else:
                            otherDic[itemKey] = item
        return [v for k, v in otherDic.items()]

    def predict(self, tree, testLst):
        tempLst = list(tree.items())[0]
        rootName = tempLst[0]
        childDict = tempLst[1]
        indx = self.classNameIndex[rootName]
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
        data['classList'] = self.classNameIndex
        return data

    def loadDumpData(self, data):
        self.tree = data['tree']
        self.classNameIndex = data['classList']
        return self
