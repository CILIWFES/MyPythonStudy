# -*- coding: utf-8 -*-
import os
import numpy as np
import pickle
import sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0] + "/Support/chapter02"


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

def deleteStopWord( matrix, stopWords=None):
    stopWordDict = set(stopWords)
    print("正在删除停用词")
    for i in range(len(matrix)):
        while '' in matrix[i]:
            matrix[i].remove('')
        while '\ufeff' in matrix[i]:
            matrix[i].remove('\ufeff')
        for j in range(len(matrix[i]) - 1, -1, -1):
            word = matrix[i][j]
            if word in stopWordDict:
                matrix[i].pop(j)
    print("停用词删除完毕")
    return matrix


# 配置utf-8输出环境
sys.getdefaultencoding()

trainPath = rootPath + "/train_word_bag/trainTfidfSpace.dat"
testPath = rootPath + "/test_word_bag/testTfidfSpace.dat"
trainBunch = readBunch(trainPath)  # 读取训练集的Bunch
testBunch = readBunch(testPath)  # 读取测试集的bunch



k = 10
testdata = deleteStopWord(testBunch.contents,stopList)
dataSet, labels = deleteStopWord(trainBunch.contents,stopList), trainBunch.label
print(classify(testdata, dataSet, labels, k))
# dataSet, listClasses = loadDataSet()
# nb = NBayes()
# nb.train_set(dataSet, listClasses)
# print(classify(nb.tf[3], nb.tf, listClasses, k))
