# -*- coding: utf-8 -*-
import numpy as np
import pickle
import sys
import os
import gc

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
                   ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
                   ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
    classVec = [0, 1, 0, 1, 0, 1]  # 1 is abusive, 0 not
    return postingList, classVec


# 写入bunch对象
def self(path, bunchobj):
    file_obj = open(path, "wb")
    pickle.dump(bunchobj, file_obj)
    file_obj.close()


class NBayes(object):
    def __init__(self):
        self.vocabularys = []  # 词典
        self.vocabularyIndex = {}  # 字典表记录词典索引
        self.idf = 0  # 词典的idf权值向量
        self.tf = 0  # 训练集的权值矩阵
        self.tf_idf = 0  # tf_idf
        self.tdm = 0  # P(x|yi)
        self.classRateMap = {}  # P(yi)--是个类别字典,结构Pcates[label]
        self.classList = []
        self.classVec = []  # 对应每个文本的分类，是个外部导入的列表
        self.doclength = 0  # 文本训练集数
        self.vocablen = 0  # 词典词长

    #	加载训练集并生成词典，以及tf, idf值
    def makeTrain(self, trainMatrix, classVec):
        self.makeByClassMap(classVec)  # 计算每个分类在总类别集合中出现的概率：P(yi)
        self.doclength = np.shape(trainMatrix)[0]  # 统计文本数
        vocabularySet = set()
        for trainVec in trainMatrix:
            for word in trainVec:  # 把字典集合转化为list放入字典顺序表
                vocabularySet.add(word)
        self.vocabularys =list(vocabularySet)
        del vocabularySet
        self.vocabularyIndex = {name: index for index, name in enumerate(self.vocabularys)}  # 索引序列
        self.vocablen = len(self.vocabularys)  # 记录总词数

        # 统计每个文本的词频,统计每个词的调用文件数
        # self.calc_wordfreq(trainSet)
        gc.collect()
        self.calTf_Idf(trainMatrix)  # 生成tf-idf权值
        gc.collect()
        self.makeTdm()  # 按分类累计向量空间的每维值：P(x|yi),X词在当前类别出现的次数/类别下所有词数(yi)

    # 生成 tf-idf
    def calTf_Idf(self, trainMatrix):
        self.idf = np.zeros([1, self.vocablen])
        self.tf = np.zeros([self.doclength, self.vocablen])

        for i in range(self.doclength):
            if i % 100 == 0:
                print("第", i + 1, "次运行")
            for word in set(trainMatrix[i]):
                index = self.vocabularyIndex[word]
                self.tf[i, index] += trainMatrix[i].count(word)
                self.idf[0, index] += 1
            # 统计文本词频TF
            self.tf[i] = self.tf[i] / float(np.alen(trainMatrix[i]))
        self.idf = np.log(float(self.doclength) / self.idf)
        self.tf_idf = np.multiply(self.tf, self.idf)  # 矩阵与向量的点乘
        return self.tf_idf

    """
    生成普通的词频向量
    统计词频
    统计每个词的调用文件
    """

    def calc_wordfreq(self, trainMatrix):
        # idf为逆文件频率
        self.idf = np.zeros([1, self.vocablen])  # [[词0,词1,........,词n-1]]
        # 每个文件:每个词出现数
        self.tf = np.zeros([self.doclength, self.vocablen])  # 训练集文件数*词典数
        for i in range(self.doclength):  # 遍历所有的文本
            if i % 100 == 0:
                print("第", i + 1, "次运行")
            for word in set(trainMatrix[i]):
                index = self.vocabularyIndex[word]
                self.tf[i, index] += trainMatrix[i].count(word)
                self.idf[0, index] += 1

        self.tf_idf = self.tf

    """
    生成分类字典,统计每个类别出现的概率P(yi)
    生成分类索引字典
    """

    def makeByClassMap(self, classVec):
        self.classVec = classVec  # 写入
        classSet = set(self.classVec)
        self.classList = list(classSet)
        for label in classSet:  # 对分类进行去重遍历
            # 计算每个分类再classVec中的概率
            self.classRateMap[label] = float(self.classVec.count(label)) / float(np.alen(self.classVec))

    """
     按分类计算P(x|yi)
    """

    def makeTdm(self):
        self.tdm = np.zeros([len(self.classList), self.vocablen])  # 每个类别: 每个词的出现的概率
        sumlist = np.zeros([len(self.classList), 1])  # 统计每个类别在类别向量出现的总次数

        for i in range(self.doclength):  # 遍历每个文件
            self.tdm[self.classList.index(self.classVec[i])] += self.tf_idf[i]  # 按类别统计:每个词权重总数

        for i in range(len(self.classList)):  # 遍历类别
            sumlist[i] = np.sum(self.tdm[i])  # 统计每个分类的所有词频

        self.tdm = self.tdm / sumlist  # P(x|yi)计算当前分类下X词出现的概率,X词在当前类别出现的次数/类别下所有词数(yi)

    # 构建测试集合
    def makeTest(self, testMatrix):
        testDetail = [{"all": 0, "notFind": 0, "setIndex": i} for i in range(np.shape(testMatrix)[0])]
        testTfMatrix = np.zeros([np.shape(testMatrix)[0], self.vocablen])
        for i in range(len(testMatrix)):
            testDetail[i]["all"] = len(testMatrix[i])
            notFind = 0
            for word in testMatrix[i]:
                index = self.vocabularyIndex[word] if word in self.vocabularyIndex else None
                if index != None:
                    testTfMatrix[i, index] += 1
                else:
                    notFind += 1
            testDetail[i]["notFind"] = notFind
        return testTfMatrix, testDetail

    # 输出分类类别
    def predict(self, testTfMatrix):
        predClass = list()

        for i in range(np.shape(testTfMatrix)[0]):
            predvalue = 0
            retClass = 0
            for tdmVect, keyClass in zip(self.tdm, self.classList):
                # P(x|yi)P(yi)
                temp = np.sum(np.multiply(testTfMatrix[i], tdmVect) * self.classRateMap[keyClass])
                if temp > predvalue:
                    predvalue = temp
                    retClass = keyClass
            predClass.append(retClass)

        return predClass

    """
    去除停用词
    """

    def deleteStopWord(self, trainSet, stopWords):
        stopWordSet=set(stopWords)
        for i in range(len(trainSet)):
            for word in trainSet[i]:
                if word in stopWordSet or len(word)<=0:
                    trainSet[i].remove(word)
        return trainSet
