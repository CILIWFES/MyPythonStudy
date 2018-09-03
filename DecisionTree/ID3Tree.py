# -*- coding: utf-8 -*-

from numpy import *
import math
import copy
from collections import Counter


class ID3Tree(object):
    def __init__(self):
        self.tree = {}
        self.dataSet = []
        self.labels = []

    def getDumpData(self):
        data={}
        data["tree"]=self.tree
        data["labels"]=self.labels
        return data
    def loadDumpData(self,data):
        self.tree=data["tree"]
        self.labels=data["labels"]
        return self

    def train(self):
        labels = copy.deepcopy(self.labels)
        self.tree = self.buildTree(self.dataSet, labels)

    # 创建决策树主程序(递归)
    # dataList[[0,0,1,2,no],[0,1,0,2,yes]]训练数据集
    # labels['age','student'......]标签名称
    def buildTree(self, dataList, labels):
        cateList = [data[-1] for data in dataList]  # 获取决策标签

        # 程序终止条件1	: 如果cateList只有一种,继续分类没有意义结束递归,返回标签
        # len(dataList[0])>1
        if cateList.count(cateList[0]) == len(cateList):
            return cateList[0]

        # 程序终止条件2: 如果数据集的第一个决策标签只有一个 返回这个决策标签
        # len(dataList[0]) ==1 说明种类皆分类完毕
        # 不过到这一步说明当前分类下存在即是True也是False的值
        if len(dataList[0]) == 1:
            return self.maxCate(cateList)

        # 算法核心：
        bestFeatIndex = self.getBestFeat(dataList)  # 返回数据集的最优特征轴：index
        bestFeatLabel = labels[bestFeatIndex]  # 通过最优特征轴(index)获取Name
        tree = {bestFeatLabel: {}}
        # 将特征值移除list
        del (labels[bestFeatIndex])  # 里面应该是获取即labels第bestFeat列的引用(即labels[bestFeatIndex]),然后把这个引用删除(对象不删除引用计数-11)
        # 抽取最优特征下的分类
        uniqueVals = set([data[bestFeatIndex] for data in dataList])  # 获取最优特征下的分类
        for value in uniqueVals:
            subLabels = labels[:]  # 将labels复制一遍

            # 按最优特征列和值分割数据集[0,0,1,0,1,no]->[0,0,0,1,no]
            splitDataset = self.splitDataSet(dataList, bestFeatIndex, value)
            #返回dict
            #{'0':{xxx},"1":"yes"}这样
            subTree = self.buildTree(splitDataset, subLabels)  # 构建子树递归
            tree[bestFeatLabel][value] = subTree

        return tree

    def maxCate(self, catelist):  # 计算出现最多的类别标签
        return Counter(catelist).most_common().pop(0)[0]

    def getBestFeat(self, dataSet):
        # 计算特征向量维，其中最后一列用于类别标签，因此要减去
        numFeatureLength = len(dataSet[0]) - 1  # 特征向量维数= 行向量维度-1
        baseEntropy = self.computeEntropy(dataSet)  # 基础熵：源数据的香农熵
        bestInfoGain = 0.0  # 初始化最优的信息增益
        bestFeature = -1  # 初始化最优的特征轴
        # 外循环：遍历数据集各列,计算最优特征轴
        # indx 为数据集列索引：取值范围 0~(numFeatureLength-1)
        for indx in range(numFeatureLength):  # 抽取第i列的列向量
            uniqueSet = set([data[indx] for data in dataSet])  # 去重：该列的唯一值集
            newEntropy = 0.0  # 初始化该列的香农熵
            for value in uniqueSet:  # 内循环：按列和唯一值计算香农熵
                subDataSet = self.getCateList(dataSet, indx, value)  # 按选定列i和唯一值分隔数据集
                prob = len(subDataSet) / float(len(dataSet))  # (sx/S)
                newEntropy += prob * self.computeEntropy(subDataSet)  # (sx/S*I(s1x,s2x))
            infoGain = baseEntropy - newEntropy  # 计算最大增益
            if (infoGain > bestInfoGain):  # 如果信息增益>0;
                bestInfoGain = infoGain  # 用当前信息增益值替代之前的最优增益值
                bestFeature = indx  # 重置最优特征为当前列
        return bestFeature

    def computeEntropy(self, dataSet):  # 计算香农熵
        datalen = float(len(dataSet))
        cateList = [data[-1] for data in dataSet]  # 从数据集中得到类别标签
        items = dict(Counter(cateList))  # 得到类别为key，出现次数value的字典
        infoEntropy = 0.0  # 初始化香农熵
        for key in items:  # 计算香农熵
            prob = float(items[key]) / datalen
            infoEntropy += prob * math.log(1 / prob, 2)  # 香农熵：= - p*log2(p) --infoEntropy = -prob * log(prob,2)
        return infoEntropy

    # 分隔数据集：删除特征轴所在的数据列，返回剩余的数据集
    # dataSet：数据集;	indx：特征轴;	 value：特征轴的取值
    def splitDataSet(self, dataSet, indx, value):
        rtnList = []
        for featVec in dataSet:
            if featVec[indx] == value:
                rFeatVec = featVec[:indx]  # list操作 提取0~(axis-1)的元素
                rFeatVec.extend(featVec[indx + 1:])  # list操作 将特征轴（列）之后的元素加回
                rtnList.append(rFeatVec)
        return rtnList

    # 获取决策标签列
    def getCateList(self, dataSet, indx, value):
        cateList = []
        for featVec in dataSet:
            if featVec[indx] == value:
                cateList.append(featVec[-1])
        return cateList

    def predict(self, inputTree, testVec):  # 分类器
        root = list(inputTree.keys())[0]  # 树根节点
        secondDict = inputTree[root]  # value-子树结构或分类标签
        featIndex = self.labels.index(root)  # 根节点在分类标签集中的位置
        key = testVec[featIndex]  # 测试集数组取值
        valueOfFeat = secondDict[str(key)]
        if isinstance(valueOfFeat, dict):
            classLabel = self.predict(valueOfFeat, testVec)  # 递归分类
        else:
            classLabel = valueOfFeat
        return classLabel