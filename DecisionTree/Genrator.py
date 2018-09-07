from collections import Counter


# 二维数组,类别索引字典,  行/列,
def makeGenrator(trainSet, labelIndexs, rows, featurs, featurNames, beforGenerator):
    # 创造迭代器
    def generator(choice, data1, data2):
        featursInfo = {}
        labelInfo = None

        if choice is "lenR":  # 获取行的长度
            yield len(rows)

        elif choice is "lenF":  # 获取列的长度
            yield len(featurs)



        elif choice is "getRealR":  # 获取真实坐标
            yield rows[data1]



        elif choice is "getRealF":  # 获取真实特征坐标
            yield featurs[data1]


        elif choice is "iterF":  # 获取某一列的0-n行
            while data1 < len(rows):
                ret = trainSet[rows[data1]][featurs[data2]]
                data1 += 1
                yield ret



        elif choice is "iterR":  # 获取0-n行

            while data1 < len(rows):
                ret = trainSet[rows[data1]]
                data1 += 1
                yield ret




        elif choice is "getFeatureInfo":  # data1是当前坐标,需要转化未真实坐标
            if featurs[data1] not in featursInfo:
                featursInfo[featurs[data1]] = getFeatureInfo(trainSet, rows, featurs[data1])

            yield featursInfo[featurs[data1]]  # {"2wa":{"all":5,"1":3,"2":2}, "XX":{"all":50,"2":49,"3":1}}

        elif choice is "featureCnt":  # 获取每一个的列数量
            if featurs[data1] not in featursInfo:
                featursInfo[featurs[data1]] = getFeatureInfo(trainSet, rows, featurs[data1])
            yield [(k, v["all"]) for k, v in featursInfo[featurs[data1]].items()]



        elif choice is "labelInfo":  # 获取标签统计
            if labelInfo is None:
                labelInfo = getLabelInfo(trainSet, rows)
            yield labelInfo


def getFeatureInfo(trainSet, rows, featurIndex):
    retDic = {}
    for index in rows:
        item = trainSet[index][featurIndex]
        label = trainSet[index][-1]

        if item in retDic:
            retDic[item]["all"] += 1
        else:
            retDic[item] = {"all": 1}

        if label in retDic[item]:
            retDic[item][label] += 1
        else:
            retDic[item][label] = 1
    return retDic


def getLabelInfo(trainSet, rows):
    retDic = {}
    for index in rows:
        item = trainSet[index][-1]

        if item in retDic:
            retDic[item] += 1
        else:
            retDic[item] = 1

    return retDic
