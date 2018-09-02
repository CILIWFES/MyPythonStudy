# -*- coding: utf-8 -*-
import math
import copy
from collections import Counter


class C45DTree(object):
    def __init__(self):
        self.tree = {}
        self.dataSet = []
        self.labels = []

    def getDumpData(self):
        data = {}
        data["tree"] = self.tree
        data["labels"] = self.labels
        return data

    def loadDumpData(self, data):
        self.tree = data["tree"]
        self.labels = data["labels"]
        return self

    def train(self):
        labels = copy.deepcopy(self.labels)
        self.tree = self.buildTree(self.dataSet, labels)

    def buildTree(self, dataList, labels):
        cateList = [data[-1] for data in dataList]
        if cateList.count(cateList[0]) == len(cateList):
            return cateList[0]
        if len(dataList[0]) == 1:
            return self.maxCate(cateList)
        bestFeatIndex = self.getBestFeat(dataList)
        bestFeatLabel = labels[bestFeatIndex]
        tree = {bestFeatLabel: {}}
        del (labels[bestFeatIndex])

        uniqueVals = set([data[bestFeatIndex] for data in dataList])
        for value in uniqueVals:
            subLabels = labels[:]

            splitDataset = self.splitDataSet(dataList, bestFeatIndex, value)

            subTree = self.buildTree(splitDataset, subLabels)
            tree[bestFeatLabel][value] = subTree
        return tree

    def maxCate(self, catelist):
        return Counter(catelist).most_common().pop(0)[0]

    def getBestFeat(self, dataSet):
        numFeatureLength = len(dataSet[0]) - 1
        baseEntropy = self.computeEntropy(dataSet)
        bestInfoGain = 0.0
        bestFeature = -1
        for indx in range(numFeatureLength):
            featureList = [data[indx] for data in dataSet]
            uniqueSet = set(featureList)  # 去重：该列的唯一值集
            newEntropy = 0.0
            splitInfo = self.calculateSplitInfo(featureList)  # C45特别之处
            for value in uniqueSet:
                subDataSet = self.getCateList(dataSet, indx, value)
                prob = len(subDataSet) / float(len(dataSet))  # (sx/S)
                newEntropy += prob * self.computeEntropy(subDataSet)  # 条件熵(sx/S*I(s1x,s2x))
            if splitInfo == 0:
                ASD = 45
            infoGain = (baseEntropy - newEntropy) / splitInfo  # C45特别之处
            if (infoGain > bestInfoGain):
                bestInfoGain = infoGain
                bestFeature = indx
        return bestFeature

    # C45算法特别之处,计算SpiltInfo
    def calculateSplitInfo(self, featureList):
        freList = list(Counter(featureList).values())
        P_S = len(featureList)
        splitInfo = 0.0
        for freData in freList:
            P_Si = freData / (float(P_S) + 1)  # 避免出现1
            splitInfo -= P_Si * math.log(P_Si, 2)
        return splitInfo

    def computeEntropy(self, dataSet):
        datalen = float(len(dataSet))
        cateList = [data[-1] for data in dataSet]
        items = dict(Counter(cateList))
        infoEntropy = 0.0
        for key in items:
            prob = float(items[key]) / datalen
            infoEntropy += prob * math.log(1 / prob, 2)
        return infoEntropy

    def splitDataSet(self, dataSet, indx, value):
        rtnList = []
        for featVec in dataSet:
            if featVec[indx] == value:
                rFeatVec = featVec[:indx]
                rFeatVec.extend(featVec[indx + 1:])
                rtnList.append(rFeatVec)
        return rtnList

    # 获取决策标签列
    def getCateList(self, dataSet, indx, value):
        cateList = []
        for featVec in dataSet:
            if featVec[indx] == value:
                cateList.append(featVec[-1])
        return cateList

    def predict(self, inputTree, testVec):
        root = list(inputTree.keys())[0]
        secondDict = inputTree[root]
        featIndex = self.labels.index(root)
        key = testVec[featIndex]
        valueOfFeat = secondDict[str(key)]
        if isinstance(valueOfFeat, dict):
            classLabel = self.predict(valueOfFeat, testVec)
        else:
            classLabel = valueOfFeat
        return classLabel
