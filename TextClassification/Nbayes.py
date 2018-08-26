# -*- coding: utf-8 -*-
from TextClassification.Nbayes_lib import *
import pickle
import gc
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


# 配置utf-8输出环境
sys.getdefaultencoding()

trainPath = rootPath + "/train_word_bag/trainTfidfSpace.dat"
testPath = rootPath + "/test_word_bag/testTfidfSpace.dat"
trainBunch = readBunch(trainPath)  # 读取训练集的Bunch
testBunch = readBunch(testPath)  # 读取测试集的bunch

NBayesPath = rootPath + "/train_word_bag/NBayes.dat"

nb = NBayes()
# trainSet, classSet = loadDataSet()
# trainBunch.contents=trainSet
# trainBunch.label=classSet
#
# testBunch.contents=trainBunch.contents
# testBunch.label=trainBunch.label
# testBunch.fileNames=trainBunch.fileNames
if not os.path.exists(NBayesPath):  # 不是文件夹
    trainSet = nb.deleteStopWord(trainBunch.contents, stopList)
    nb.makeTrain(trainBunch.contents, trainBunch.label)
    print("开始序列化")
    gc.collect()
    writeBunch(NBayesPath, nb.getDumpDate())
    print("序列化完毕")
else:
    dictData = readBunch(NBayesPath)
    print("读取文件中")
    nb = nb.loadDumpDate(dictData)

print("加载成功")
gc.collect()
predict = nb.makeTest()
retClassList, testDetail = predict(testBunch.contents, nb)
print("完成预测,正在信息汇总")

printData = []
labelRDict = {word: 0 for word in testBunch.label}
labelEDict = {word: 0 for word in testBunch.label}

for dataDict in testDetail:
    printDict = {}
    index = dataDict['matrixIndex']
    printDict["fileName"] = testBunch.fileNames[index]
    printDict["className"] = retClassList[index]
    printDict["identRate"] = (dataDict['all'] - dataDict['notFind']) * 1.0 / dataDict['all']
    printData.append(printDict)
    index = dataDict['matrixIndex']
    if retClassList[index] == testBunch.label[index]:
        labelRDict[testBunch.label[index]] += 1
    else:
        labelEDict[testBunch.label[index]] += 1

for printDict in printData:
    print("文件:", printDict["fileName"], "预测类别:", printDict["className"], "识别率", printDict["identRate"] * 100, "%")

for word, i in labelRDict.items():
    print(word, "的准确率为:", labelRDict[word] / float(labelRDict[word] + labelEDict[word]) * 100, "%")
