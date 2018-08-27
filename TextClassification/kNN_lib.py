
# 配置utf-8输出环境


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
