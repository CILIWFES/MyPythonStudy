from collections import Counter


class DataBean:
    def __init__(self, trainSet, rows, featurs, featureIndexReal, featuresValue, isLeft=None, beforDataBean=None):
        # 不为空表示数组即将拆分
        self.featuresInfo = {}
        self.rows = rows
        self.trainSet = trainSet
        self.features = featurs
        self.featureIndexReal = featureIndexReal
        self.featuresValue = featuresValue
        self.aMax = -1
        if beforDataBean is not None:
            if isLeft:
                self.rows = [row for row in beforDataBean.rows if trainSet[row][featureIndexReal] is featuresValue]
            else:
                # 提高搜索效率
                tempDic = {key: index for index, key in enumerate(featuresValue)}
                self.rows = [row for row in beforDataBean.rows if trainSet[row][featureIndexReal] in tempDic]
            self.features = beforDataBean.features[:]
            # 删除自身结点
            self.features.remove(featureIndexReal)
        self.labelInfo = None
        self.choiceFeatureDataBean: DataBean = None
        self.choiceFeatureOtherDataBean: DataBean = None
        self.choiceFeatureIndex = None  # 判断是否为叶子节点的标志

    # 获取行的长度
    def lenRow(self):
        return len(self.rows)

    # 获取列的长度
    def lenFeaturs(self):
        return len(self.features)

    # 获取真实坐标
    def getRow(self, fakeIndex):
        return self.rows[fakeIndex]

    # 获取真实特征坐标
    def getFeature(self, fakeIndex):
        return self.features[fakeIndex]

    # 获取0-n行
    def iterRows(self, fakeIndex):
        rows = self.rows
        trainSet = self.trainSet

        # 生成一个生成器
        def genrator(fakeIndex):
            while fakeIndex < len(rows):
                ret = trainSet[rows[fakeIndex]]
                fakeIndex += 1
                yield ret

        # 生成一个生成器
        return genrator(fakeIndex)

    def iterFeature(self, fakeIndex):
        while fakeIndex < len(self.rows):
            ret = self.trainSet[self.rows[fakeIndex]][self.features[fakeIndex]]
            fakeIndex += 1
            return ret

    # 特征值信息统计
    def featureInfo(self, fakeIndex):
        if self.features[fakeIndex] not in self.featuresInfo:
            self.featuresInfo[self.features[fakeIndex]] = self.__getFeatureInfo(self.features[fakeIndex])
        return self.featuresInfo[
            self.features[fakeIndex]]  # {"2wa":{"all":5,"1":3,"2":2}, "XX":{"all":50,"2":49,"3":1}}

    def featureCnt(self, realIndex):
        if self.features[realIndex] not in self.featuresInfo:
            self.featuresInfo[self.features[realIndex]] = self.__getFeatureInfo(self.features[realIndex])
        return [(k, v["all"]) for k, v in self.featuresInfo[self.features[realIndex]].items()]

    def getLabelInfo(self) -> Counter:
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
