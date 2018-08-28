# -*- coding: utf-8 -*-
import os
import numpy as np
import pickle
import sys
import gc
from TextClassification.kNN_lib import *
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0] + "/Support/chapter02"

kNNPath = rootPath + "/train_word_bag/kNN.dat"

# 读取文件
def readFile(readPath):
    fp = open(readPath, "rb")
    content = fp.read()
    content = content.decode(encoding='utf-8')  # 解码为字符码
    fp.close()
    return content


# 读取停用词
stopworgPath = rootPath + "/train_word_bag/hlt_stop_words.txt"
stopList = readFile(stopworgPath).splitlines()


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

# testBunch.contents=trainBunch.contents
# testBunch.label=trainBunch.label
# testBunch.fileNames=trainBunch.fileNames

times = 5
knn=kNN()

if not os.path.exists(kNNPath):  # 不是文件夹
    trainSet = knn.deleteStopWord(trainBunch.contents, stopList)
    knn.makeTrain(trainBunch.contents, trainBunch.label)
    print("开始序列化")
    gc.collect()
    writeBunch(kNNPath, knn.getDumpData())
    print("序列化完毕")
else:
    dictData = readBunch(kNNPath)
    print("读取文件中")
    knn = knn.loadDumpData(dictData)

print("加载成功")
gc.collect()
predict = knn.makeTest()
retClassList, testDetail = predict(testBunch.contents, knn,times)
print("完成预测,正在信息汇总")


from sklearn import metrics
#classification_report函数构建了一个文本报告，用于展示主要的分类metrics
print(metrics.classification_report(testBunch.label, retClassList))

