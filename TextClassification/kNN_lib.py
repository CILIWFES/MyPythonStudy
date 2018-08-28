import numpy as np
from typing import Dict
from collections import Counter


class PointData(object):
    def __init__(self, fileIndex, label):
        self.fileIndex = fileIndex
        self.label = label
        self.tf = []

    def toPredict(self, testVec):
        testVec = np.mat(testVec)
        # return np.sqrt((self.tf[0] - testVec)*(self.tf[0] - testVec).T), self.label#欧式距离
        # return np.sum(np.abs(self.tf[0] - testVec)), self.label  # 曼哈顿距离
        # return np.max(np.abs(self.tf[0] - testVec)), self.label#切比雪夫距离
        return -self.tf * testVec.T / (np.linalg.norm(testVec) * np.linalg.norm(self.tf)), self.label#扣脚余弦


class kNN(object):
    def __init__(self):
        self.vocabularys = []  # 词典
        self.vocabularyIndex = {}  # 字典表记录词典索引
        self.stopWordDict = None
        self.points = []

    def getDumpData(self):
        dict = {}

        dict["vocabularys"] = self.vocabularys
        dict["vocabularyIndex"] = self.vocabularyIndex
        dict["stopWordDict"] = self.stopWordDict
        loadPoints = [(point.tf, point.label) for point in self.points]
        dict["points"] = loadPoints
        return dict

    def loadDumpData(self, dict):
        loadPoints = dict["points"]
        points = []
        for index, point in enumerate(loadPoints):
            temp = PointData(index, point[1])
            temp.tf = point[0]
            points.append(temp)
        self.points = points
        self.vocabularys = dict["vocabularys"]
        self.vocabularyIndex = dict["vocabularyIndex"]
        self.stopWordDict = dict["stopWordDict"]
        return self

    def makeTrain(self, trainMatrix, classVec):
        self.vocabularys = list(set([word for i in range(len(trainMatrix)) for word in trainMatrix[i]]))
        self.vocabularyIndex = {name: index for index, name in enumerate(self.vocabularys)}  # 索引序列
        self.calWordFre(trainMatrix, classVec)

    def calWordFre(self, trainMatrix, classVec):
        for i in range(np.shape(trainMatrix)[0]):
            tf = np.zeros([1, len(self.vocabularys)])
            if i % 100 == 0:
                print("第", i + 1, "次运行")
            for word in set(trainMatrix[i]):
                index = self.vocabularyIndex[word]
                tf[0, index] += trainMatrix[i].count(word)
            tf /= np.sum(tf)
            pointData = PointData(i, classVec[i])
            pointData.tf = tf
            self.points.append(pointData)

        # 构建测试集合

    def makeTest(self):
        print("构造预测函数")

        def predict(testMatrix, knn: kNN, times):
            print("准备预测")
            testMatrix = knn.deleteStopWord(testMatrix)
            testDetail = [{"matrixIndex": i, "all": 0, "notFind": 0} for i in range(np.shape(testMatrix)[0])]
            testTfMatrix = np.zeros([np.shape(testMatrix)[0], len(knn.vocabularys)])
            for i in range(np.shape(testTfMatrix)[0]):
                testDetail[i]["all"] = len(testMatrix[i])
                notFind = 0
                for word in testMatrix[i]:
                    index = knn.vocabularyIndex[word] if word in knn.vocabularyIndex else None
                    if index is not None:
                        testTfMatrix[i, index] += 1
                    else:
                        notFind += 1
                testDetail[i]["notFind"] = notFind

                testTfMatrix[i] = testTfMatrix[i] / float(np.sum(testTfMatrix[i]))

            testClassList = [0] * np.shape(testTfMatrix)[0]
            print("开始预测")
            for i in range(np.shape(testTfMatrix)[0]):
                print("第", i, "个文件开始预测")
                values = [(10000, 10000)] * times
                maxData = [10000, 0]  # val,index
                for pointData in knn.points:
                    # P(x|yi)P(yi)
                    value, label = pointData.toPredict(testTfMatrix[i])

                    if value < maxData[0]:
                        values[maxData[1]] = (value, label)
                        maxTemp = max(values, key=lambda x: x[0])
                        maxData[1] = values.index(maxTemp)
                        maxData[0] = maxTemp[0]
                values = [item[1] for item in values]

                testClassList[i] = Counter(values).most_common().pop(0)[0]
                print(testClassList[i])
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
