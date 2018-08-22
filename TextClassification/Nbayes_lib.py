# -*- coding: utf-8 -*-
import numpy as np
import pickle


def loadDataSet():
    postingList = [['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
                   ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
                   ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him', 'my'],
                   ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                   ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
                   ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
    classVec = [0, 1, 0, 1, 0, 1]  # 1 is abusive, 0 not
    return postingList, classVec


# 读取文件
def readfile(path):
    fp = open(path, "rb")
    content = fp.read()
    fp.close()
    return content


'''		
#计算分类精度：
def metrics_result(actual,predict):
	print '精度:{0:.3f}'.format(metrics.precision_score(actual,predict))  
	print '召回:{0:0.3f}'.format(metrics.recall_score(actual,predict))  
	print 'f1-score:{0:.3f}'.format(metrics.f1_score(actual,predict))  
'''


# 读取bunch对象
def readbunchobj(path):
    file_obj = open(path, "rb")
    bunch = pickle.load(file_obj)
    file_obj.close()
    return bunch


# 写入bunch对象
def writebunchobj(path, bunchobj):
    file_obj = open(path, "wb")
    pickle.dump(bunchobj, file_obj)
    file_obj.close()


class NBayes(object):
    def __init__(self):
        self.vocabulary = []  # 词典
        self.idf = 0  # 词典的idf权值向量
        self.tf = 0  # 训练集的权值矩阵
        self.tf_idf = 0  # tf_idf
        self.tdm = 0  # P(x|yi)
        self.Pcates = {}  # P(yi)--是个类别字典,结构Pcates[label]
        self.labels = []  # 对应每个文本的分类，是个外部导入的列表
        self.doclength = 0  # 文本训练集数
        self.vocablen = 0  # 词典词长

    #	加载训练集并生成词典，以及tf, idf值
    def train_set(self, trainSet, classVec):
        self.statisticalByClassVec(classVec)  # 计算每个分类在总类别集合中出现的概率：P(yi)
        self.doclength = len(trainSet)  # 统计文本数

        tempset = set()  # 建立集合
        [tempset.add(word) for trainVec in trainSet for word in trainVec]  # 生成词典集合

        self.vocabulary = list(tempset)  # 把字典集合转化为list放入字典顺序表
        self.vocablen = len(self.vocabulary)  # 记录总词数

        # 统计每个文本的词频,统计每个词的调用文件数
        self.calc_wordfreq(trainSet)
        self.tf_idf=self.tf
        self.calc_tfidf(trainSet)  # 生成tf-idf权值

        self.build_tdm()  # 按分类累计向量空间的每维值：P(x|yi),X词在当前类别出现的次数/类别下所有词数(yi)

    # 生成 tf-idf
    def calc_tfidf(self, trainSet):
        self.idf = np.zeros([1, self.vocablen])
        self.tf = np.zeros([self.doclength, self.vocablen])

        for i in range(self.doclength):
            for word in trainSet[i]:
                self.tf[i, self.vocabulary.index(word)] += 1
            # 统计文本词频TF
            self.tf[i] = self.tf[i] / float(len(trainSet[i]))
            for word in set(trainSet[i]):
                self.idf[0, self.vocabulary.index(word)] += 1
        self.idf = np.log(float(self.doclength) / self.idf)
        self.tf_idf = np.multiply(self.tf, self.idf)  # 矩阵与向量的点乘
        return self.tf_idf

    """
    生成普通的词频向量
    统计词频
    统计每个词的调用文件
    """

    def calc_wordfreq(self, trainSet):
        # idf为逆文件频率
        self.idf = np.zeros([1, self.vocablen])  # [[词0,词1,........,词n-1]]
        # 每个文件:每个词出现数
        self.tf = np.zeros([self.doclength, self.vocablen])  # 训练集文件数*词典数
        for i in range(self.doclength):  # 遍历所有的文本
            for word in trainSet[i]:  # 统计在第index+1个文件下每个单词的词频
                self.tf[i, self.vocabulary.index(word)] += 1  # 获取字典顺序表vocabulary下word的索引
            for word in set(trainSet[i]):  # 去重,遍历词,词调用频率+1
                self.idf[0, self.vocabulary.index(word)] += 1  # 记录逆文件权重的分母

    """
    生成分类字典,统计每个分类的概率P(yi)
    """

    def statisticalByClassVec(self, classVec):
        self.labels = classVec  # 写入
        for labeltemp in set(self.labels):  # 对分类进行去重遍历
            # 计算每个分类再classVec中的概率
            self.Pcates[labeltemp] = float(self.labels.count(labeltemp)) / float(len(self.labels))

    """
     按分类计算P(x|yi)
    """

    def build_tdm(self):
        self.tdm = np.zeros([len(self.Pcates), self.vocablen])  # 每个类别: 每个词的出现的概率
        sumlist = np.zeros([len(self.Pcates), 1])  # 统计每个类别在类别向量出现的总次数

        for i in range(self.doclength):  # 遍历每个文件
            self.tdm[self.labels[i]] += self.tf_idf[i]  # 按类别统计:每个词权重总数

        for i in range(len(self.tdm)):  # 遍历类别
            sumlist[self.labels[i]] = np.sum(self.tdm[self.labels[i]])  # 统计每个分类的所有词频

        self.tdm = self.tdm / sumlist  # P(x|yi)计算当前分类下X词出现的概率,X词在当前类别出现的次数/类别下所有词数(yi)

    # 构建测试集合
    def test_set(self, testSet):
        testDetail = [{"all": 0, "notFind": 0, "setIndex": i} for i in range(len(testSet))]
        testSetRet = np.zeros([1, self.vocablen])
        for i in range(len(testSet)):
            testDetail[i]["all"] = len(testSet[i])
            notFind = 0
            for word in testSet[i]:
                if word in self.vocabulary:
                    testSetRet[0, self.vocabulary.index(word)] += 1
                else:
                    notFind += 1
            testDetail[i]["notFind"] = notFind
        return testSetRet, testDetail

    # 输出分类类别
    def predict(self, testSet):
        if np.shape(testSet)[1] != self.vocablen:
            print("输入错误")
            exit(0)
        predClass = list()

        for i in range(np.shape(testSet)[0]):
            predvalue = 0
            retClass = 0
            for tdm_vect, keyclass in zip(self.tdm, self.Pcates):
                # P(x|yi)P(yi)
                temp = np.sum(np.multiply(testSet[i], tdm_vect) * self.Pcates[keyclass])
                if temp > predvalue:
                    predvalue = temp
                    retClass = keyclass
            predClass.append(retClass)

        return predClass
