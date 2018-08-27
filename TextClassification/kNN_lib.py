import numpy as np
from typing import Dict


# 夹角余弦距离公式
def cosdist(vector1, vector2):
    return np.dot(vector1, vector2) / (np.linalg.norm(vector1) * np.linalg.norm(vector2))


# kNN分类器
# 测试集：testdata
# 训练集：trainSet
# 类别标签：listClasses
# k:k个邻居数
def classify(testdata, trainSet, listClasses, k):
    # 返回样本集的行数
    dataSetSize = np.shape(trainSet)[0]
    # 计算测试集与训练集之间的距离：夹角余弦
    distances = np.array(np.zeros(dataSetSize))
    for indx in range(dataSetSize):
        distances[indx] = cosdist(testdata, trainSet[indx])
    # 5.根据生成的夹角余弦按从大到小排序,结果为索引号
    sortedDistIndicies = np.argsort(-distances)
    classCount = {}
    # 获取角度最小的前三项作为参考项
    for i in range(k):  # i = 0~(k-1)
        # 按序号顺序返回样本集对应的类别标签
        voteIlabel = listClasses[sortedDistIndicies[i]]
        # 为字典classCount赋值,相同key，其value加1
        # key:voteIlabel，value: 符合voteIlabel标签的训练集数
        classCount[voteIlabel] = classCount.get(voteIlabel, 0) + 1
    # 对分类字典classCount按value重新排序
    # sorted(data.iteritems(), key=operator.itemgetter(1), reverse=True)
    # 该句是按字典值排序的固定用法
    # classCount.iteritems()：字典迭代器函数
    # key：排序参数；operator.itemgetter(1)：多级排序
    sortedClassCount = sorted(classCount.items(), key=np.operator.itemgetter(1), reverse=True)
    # 返回序最高的一项
    return sortedClassCount[0][0]


class PointData(object):
    def __init__(self, fileIndex, label):
        self.fileIndex = fileIndex
        self.label = label
        self.tf = []

    def toPredict(self, testVec):
        return np.sqrt(np.sum(np.power(self.tf - testVec, 2)))


class kNN(object):
    def __init__(self):
        self.vocabularys = []  # 词典
        self.vocabularyIndex = {}  # 字典表记录词典索引
        self.stopWordDict = None
        self.classIndex = None
        self.classMap: Dict = None

    def makeTrain(self, trainMatrix, classVec):
        self.vocabularys = list(set([word for i in range(len(trainMatrix)) for word in trainMatrix[i]]))
        self.vocabularyIndex = {name: index for index, name in enumerate(self.vocabularys)}  # 索引序列
        self.makeClassMap(classVec)
        self.calWordFre(trainMatrix, classVec)

    def calWordFre(self, trainMatrix, classVec):
        self.idf = np.ones([1, len(self.vocabularys)])
        for i in range(np.shape(trainMatrix)[0]):
            tf = np.zeros([1, len(self.vocabularys)])
            if i % 100 == 0:
                print("第", i + 1, "次运行")
            pointData = PointData(i, classVec[i])
            for word in set(trainMatrix[i]):
                index = self.vocabularyIndex[word]
                tf[0, index] += trainMatrix[i].count(word)
            tf /= np.sum(tf)
            pointData.tf = tf
            self.classMap[classVec[i]].append(pointData)

        # 构建测试集合

    def makeTest(self):
        print("构造预测函数")

        def predict(testMatrix, knn:kNN,times):
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
                values=[]
                for label, pointData in knn.classMap.items():
                    # P(x|yi)P(yi)
                    value = pointData.toPredict(testTfMatrix[i])
                    if value > predvalue:
                        predvalue = value
                        retClass = label
                testClassList[i] = retClass
            print("预测结束")
            return testClassList, testDetail

        return predict
    """
       生成分类字典,统计每个类别出现的概率P(yi)
       生成分类索引字典
       """

    def makeClassMap(self, classVec):
        classList = list(set(classVec))
        for index, label in enumerate(classList):  # 对分类进行去重遍历
            self.classMap[label] = []
        self.classIndex = {k: i for i, (k, v) in enumerate(self.classMap.items())}

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
