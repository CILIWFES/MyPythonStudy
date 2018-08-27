# -*- coding: utf-8 -*-
import numpy as np
import pickle
import os
import gc
import copy
from typing import List, Dict

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0] + "/Support/chapter02"
NBayesPath = rootPath + "/train_word_bag/NBayes.dat"


def writeBunch(path, bunch):
    fileObj = open(path, "wb")
    pickle.dump(bunch, fileObj)
    fileObj.close()


def loadDataSet():
    postingList = [['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
                   ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
                   ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him', 'my'],
                   ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                   ['mr', 'licks', 'ate', 'umy', 'steak', 'how', '84', '8stop', 'asawsx'],
                   ['mr554', 'licks', 'ate', 'umy', 'steak', 'how', 'ftdto', '8stop', 'asawsx'],
                   ['mr', 'licks', 'ate', 'umy', 'st55eak', 'how', 'ftdto', '8stop', 'asawsx'],
                   ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
    classVec = [0, 1, 0, 1, 3, 3, 3, 1]  # 1 is abusive, 0 not
    return postingList, classVec


# 写入bunch对象
def self(path, bunchobj):
    file_obj = open(path, "wb")
    pickle.dump(bunchobj, file_obj)
    file_obj.close()


isTFIDF = True


class ClassData(object):
    def __init__(self, classIndex, label, vocaLength, rate):
        self.label = label
        self.vocaLength = vocaLength
        self.classIndex = classIndex
        self.tfs = []
        self.rate = rate
        self.tdm = None

    def putTf(self, tf):
        self.tfs.append(tf)
        return self.tfs

    def calPXY(self, idf):
        self.tdm = np.zeros([1, self.vocaLength])
        for tf in self.tfs:
            self.tdm += np.multiply(tf, idf)
        if isTFIDF:
            self.tdm /= float(np.shape(self.tfs)[0])
        else:
            self.tdm /= float(np.shape(self.tfs)[0])

    def toPredict(self, testVec):

        if isTFIDF:
            weight = np.sum(np.multiply(self.tdm, testVec))  # 这种效果比上面好.上面的符合理论
        else:
            weight = np.sum(np.log(np.multiply(self.tdm, testVec) + 1)) * self.rate  # 朴素贝叶斯
        return weight


class NBayes(object):
    def __init__(self):
        self.vocabularys = []  # 词典
        self.vocabularyIndex = {}  # 字典表记录词典索引
        self.classMap = {}  # P(yi)--是个类别字典,结构Pcates[label]
        self.stopWordDict = None
        self.idf = None
        self.classIndex: Dict = None

    def makeTrain(self, trainMatrix, classVec):

        self.vocabularys = list(set([word for i in range(len(trainMatrix)) for word in trainMatrix[i]]))
        self.vocabularyIndex = {name: index for index, name in enumerate(self.vocabularys)}  # 索引序列

        self.makeClassMap(classVec)  # 计算每个分类在总类别集合中出现的概率：P(yi)
        if isTFIDF:
            self.calTfIdf(trainMatrix, classVec)  # 生成tf-idf权值
        else:
            self.calWordFreq(trainMatrix, classVec)  # 朴素贝叶斯

        gc.collect()
        self.makeTdm()  # 按分类累计向量空间的每维值：P(x|yi),X词在当前类别出现的次数/类别下所有词数(yi)

    # 生成 tf-idf
    def calTfIdf(self, trainMatrix, classVec):
        idf = np.zeros([len(self.classIndex), len(self.vocabularys)])

        for i in range(np.shape(trainMatrix)[0]):
            tf = np.zeros([1, len(self.vocabularys)])
            if i % 100 == 0:
                print("第", i + 1, "次运行")
            classData: ClassData = self.classMap[classVec[i]]
            for word in set(trainMatrix[i]):
                index = self.vocabularyIndex[word]
                tf[0, index] += trainMatrix[i].count(word)
                idf[self.classIndex[classVec[i]], index] += 1
            # 统计文本词频TF
            tf[0] = tf[0] / float(np.sum(tf[0]))
            classData.putTf(tf)
        self.idf = np.log(float(np.shape(trainMatrix)[0] + 1) / (np.sum(idf, axis=0)))  # 理论上要这个
        idf = idf.clip(max=1)
        idf = np.sum(idf, axis=0)
        self.idf *= np.log(float(len(self.classIndex) + 1) / (idf))  # 我加了这个

    """
    生成词频
    适配TFIDF
    """

    def calWordFreq(self, trainMatrix, classVec):
        self.idf = np.ones([1, len(self.vocabularys)])
        for i in range(np.shape(trainMatrix)[0]):
            tf = np.zeros([1, len(self.vocabularys)])
            if i % 100 == 0:
                print("第", i + 1, "次运行")
            classData: ClassData = self.classMap[classVec[i]]
            for word in set(trainMatrix[i]):
                index = self.vocabularyIndex[word]
                tf[0, index] += trainMatrix[i].count(word)
            tf[0, index] /= np.sum(tf[0, index])
            classData.putTf(tf)

    """
    生成分类字典,统计每个类别出现的概率P(yi)
    生成分类索引字典
    """

    def makeClassMap(self, classVec):
        classList = list(set(classVec))
        for index, label in enumerate(classList):  # 对分类进行去重遍历
            rate = float(classVec.count(label)) / float(np.alen(classVec))
            self.classMap[label] = ClassData(index, label, np.alen(self.vocabularys), rate)
        self.classIndex = {k: i for i, (k, v) in enumerate(self.classMap.items())}

    """
     按分类计算P(x|yi)
    """

    def makeTdm(self):
        print("构建分类权重")
        for label, classData in self.classMap.items():
            classData.calPXY(self.idf)
        print("分类权重构建完毕")

    def getDumpDate(self):
        dictData = {}
        dictData["vocabularys"] = self.vocabularys
        dictData["vocabularyIndex"] = self.vocabularyIndex
        for label, classData in self.classMap.items():
            classData.tfs = None
        dictData["classMap"] = self.classMap
        dictData["stopWordDict"] = self.stopWordDict
        return dictData

    def loadDumpDate(self, dictData):
        self.vocabularys = dictData["vocabularys"]
        self.vocabularyIndex = dictData["vocabularyIndex"]
        self.classMap = dictData["classMap"]
        self.stopWordDict = dictData["stopWordDict"]
        return self

    # 构建测试集合
    def makeTest(self):
        print("构造预测函数")

        def predict(testMatrix, nb: NBayes):
            print("准备预测")
            testMatrix = nb.deleteStopWord(testMatrix)
            testDetail = [{"matrixIndex": i, "all": 0, "notFind": 0} for i in range(np.shape(testMatrix)[0])]
            testTfMatrix = np.zeros([np.shape(testMatrix)[0], len(nb.vocabularys)])
            for i in range(np.shape(testTfMatrix)[0]):
                testDetail[i]["all"] = len(testMatrix[i])
                notFind = 0
                for word in testMatrix[i]:
                    index = nb.vocabularyIndex[word] if word in nb.vocabularyIndex else None
                    if index is not None:
                        testTfMatrix[i, index] += 1
                    else:
                        notFind += 1
                testDetail[i]["notFind"] = notFind

                testTfMatrix[i] = testTfMatrix[i] / float(np.sum(testTfMatrix[i]))

            testClassList = [0] * np.shape(testTfMatrix)[0]
            print("开始预测")
            for i in range(np.shape(testTfMatrix)[0]):
                predvalue = 0
                retClass = 0
                for label, classData in nb.classMap.items():
                    # P(x|yi)P(yi)
                    value = classData.toPredict(testTfMatrix[i])
                    if value > predvalue:
                        predvalue = value
                        retClass = label
                testClassList[i] = retClass
            print("预测结束")
            return testClassList, testDetail

        return predict

    """
    去除停用词
    """

    def deleteStopWord(self, matrix, stopWords=None):
        if (stopWords is not None):
            self.stopWordDict = set(stopWords)
            self.stopWordDict.add("")
            self.stopWordDict.add('\ufeff')
        print("正在删除停用词")
        for i in range(len(matrix)):
            for j in range(len(matrix[i]) - 1, -1, -1):
                word = matrix[i][j]
                if word in self.stopWordDict:
                    matrix[i].pop(j)

        print("停用词删除完毕")
        return matrix
