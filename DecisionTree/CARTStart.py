from DecisionTree.CARTTree import *
import os
import pickle
# 树与分类结构的可视化
import treePlotter.treePlotter as tp

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0] + "/Support/chapter03"
CARTLoadPath = rootPath + "/dataset.dat"
CARTSavePath = rootPath + "/CARTTree.dat"


def loadDataSet(path):
    fp = open(path, "rb")  # 读取文件内容
    content = fp.read()
    content = content.decode(encoding='utf-8')  # 解码为字符码
    fp.close()
    rowlist = content.splitlines()  # 按行转换为一维表
    recordlist = [row.split("\t") for row in rowlist if row.strip()]
    return recordlist


def saveDump(path, obj):
    file = open(path, "wb")
    pickle.dump(obj, file)
    file.close()


def readDump(path):
    file = open(path, "rb")
    data = pickle.load(file)
    file.close()
    return data


dtree = CARTTree()
if not os.path.exists(CARTSavePath):  # 不是文件夹
    print("生成数据")
    dataSet = loadDataSet(CARTLoadPath)
    labels = ["age", "revenue", "student", "credit"]
    print("训练数据")
    dtree.train(dataSet,labels,True)
    print("持久化数据")
    saveDump(CARTSavePath, dtree.getDumpData())
    print("正在生成树")
    tp.createPlot(dtree.tree)
else:
    print("读取持久化")
    dtree.loadDumpData(readDump(CARTSavePath))

tp.createPlot(dtree.tree)
print("预测结果为:", dtree.predict(dtree.tree, [0, 0, 1, 1]))