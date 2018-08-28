# 导入贝叶斯包
from sklearn.naive_bayes import MultinomialNB
import os
import pickle
import numpy as np

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
predicted = clf.predict(testBunch.tdm)  # dimension mismatch

total = len(predicted)
rate = 0
for fileName, expctCate in zip(testBunch.fileNames, predicted):
    print("文件", fileName, "预测类别", expctCate)

from sklearn import metrics

"""
precision:精度(预测类型为xx,xx类型的预测准确率,越大说明该类型越容易进行预测)
recall:召回率/查准率(识别文件类型为xx,xx类型识别的准确率,越大说明该类型文件越容易被正确识别)
f1-score:又称平衡F分数（balanced F Score），它被定义为精确率和召回率的调和平均数。
support:对应类型的文件数

一个数据库有500个文档，其中有50个文档符合定义。系统检索到75个文档，但是实际只有45个符合定义。则：
召回率R=45/50=90%
精度P=45/75=60%
"""

print(metrics.classification_report(testBunch.label, predicted))
