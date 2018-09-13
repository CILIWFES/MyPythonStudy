from collections import Counter
class DataBean:
    def __init__(self, trainSet, rows, featurs, featureIndexReal, featuresValue, isLeft=None, beforDataBean=None):
        # 不为空表示数组即将拆分
        self.featursInfo = {}
        self.rows = rows
        self.trainSet = trainSet
        self.featurs = featurs
        self.featureIndexReal = featureIndexReal
        self.featuresValue = featuresValue
        if beforDataBean is not None:
            if isLeft:
                self.rows = [row for row in beforDataBean.rows if trainSet[row][featureIndexReal] is featuresValue]
            else:
                self.rows = [row for row in beforDataBean.rows if trainSet[row][featureIndexReal] is not featuresValue]
            self.featurs = beforDataBean.featurs[:]
            # 删除自身结点
            self.featurs.remove(featureIndexReal)
        self.labelInfo = None
        self.choiceFeatureValue = None
        self.choiceFeatureOtherValue = None
        self.choiceFeatureIndx = None

    # 获取行的长度
    def lenRow(self):
        return len(self.rows)

    # 获取列的长度
    def lenFeaturs(self):
        return len(self.featurs)

    # 获取真实坐标
    def getRow(self,fakeIndex):
        return self.rows[fakeIndex]

    # 获取真实特征坐标
    def getFeature(self,fakeIndex):
        return self.featurs[fakeIndex]

    # 获取0-n行
    def iterRows(self,fakeIndex):
        rows=self.rows
        trainSet=self.trainSet
        #生成一个生成器
        def genrator(fakeIndex):
            while fakeIndex < len(rows):
                ret = trainSet[rows[fakeIndex]]
                fakeIndex += 1
                yield ret
        #生成一个生成器
        return genrator(fakeIndex)

    def iterFeature(self,fakeIndex):
        while fakeIndex < len(self.rows):
            ret = self.trainSet[self.rows[fakeIndex]][self.featurs[fakeIndex]]
            fakeIndex += 1
            return ret
    #特征值信息统计
    def featureInfo(self,fakeIndex):
        if self.featurs[fakeIndex] not in self.featursInfo:
            self.featursInfo[self.featurs[fakeIndex]] = self.__getFeatureInfo(self.featurs[fakeIndex])
        return self.featursInfo[self.featurs[fakeIndex]]  # {"2wa":{"all":5,"1":3,"2":2}, "XX":{"all":50,"2":49,"3":1}}


    def featureCnt(self,realIndex):
        if self.featurs[realIndex] not in self.featursInfo:
            self.featursInfo[self.featurs[realIndex]] = self.__getFeatureInfo(self.featurs[realIndex])
        return [(k, v["all"]) for k, v in self.featursInfo[self.featurs[realIndex]].items()]

    def getLabelInfo(self):
        if self.labelInfo is None:
            self.labelInfo = self.__getLabelInfo()
        return self.labelInfo


    def __getFeatureInfo(self, realIndex):
        retDic = {}
        for index in self.rows:
            item = self.trainSet[index][realIndex]
            label = self.trainSet[index][-1]

            if item in retDic:
                retDic[item]["all"] += 1
            else:
                retDic[item] = {"all": 1}

            if label in retDic[item]:
                retDic[item][label] += 1
            else:
                retDic[item][label] = 1
        return retDic

    def __getLabelInfo(self):
        retDic = Counter([self.trainSet[index][-1] for index in self.rows])
        return retDic