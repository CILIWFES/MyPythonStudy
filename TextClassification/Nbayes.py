# -*- coding: utf-8 -*-
from TextClassification.Nbayes_lib import *
import pickle
import gc

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

# nb = readBunch(NBayesPath)
# trainSet, classSet = loadDataSet()
nb = NBayes()
trainSet = nb.deleteStopWord(trainBunch.contents, stopList)
nb.makeTrain(trainBunch.contents, trainBunch.label)

testTfMatrix, testDetail = nb.makeTest(testBunch.contents)
print("预测为:", nb.predict(testTfMatrix))
print(testDetail)

gc.collect()
writeBunch(NBayesPath, nb)
print("序列化成功!")
