# 导入贝叶斯包
from sklearn.naive_bayes import MultinomialNB
import sys
import os
from sklearn.datasets.base import Bunch
import pickle

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0] + "/Support/chapter02"


def readBunch(path):
    fileObj = open(path, "rb")
    bunch = pickle.load(fileObj)
    fileObj.close()
    return bunch


def writeBunch(path, bunch):
    fileObj = open(path, "wb")
    pickle.dump(bunch, fileObj)
    fileObj.close()


trainPath = rootPath + "/train_word_bag/trainTfidfSpace.dat"
testPath = rootPath + "/test_word_bag/testTfidfSpace.dat"
trainBunch = readBunch(trainPath)  # 读取训练集的Bunch
testBunch = readBunch(testPath)  # 读取测试集的bunch
# 应用朴素贝叶斯算法
# alpha:0.001,alpha越小,遍历次数越高
clf = MultinomialNB(alpha=0.001).fit(trainBunch.tdm, trainBunch.label)

# 预测分类结果
predicted = clf.predict(testBunch.tdm)#dimension mismatch
total = len(predicted)
rate = 0
for label, fileName, expctCate in zip(testBunch.label, testBunch.fileNames, predicted):
    if label != expctCate:
        rate += 1
        print("文件", fileName, "实际类别:", label, "预测类别", expctCate)

import numpy as np
from sklearn import metrics


# 定义分类精度函数
def metricsResult(actual, predict):
    print("精度:", metrics.precision_score(actual, predict))
    print("召回率:", metrics.recall_score(actual, predict))
    print("F-Score:", metrics.f1_score(actual, predict))


metricsResult(testBunch.label, predicted)
