import sys
import os
from sklearn.datasets.base import Bunch
import pickle
from sklearn.feature_extraction.text import TfidfTransformer, TfidfVectorizer

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0] + "/Support/chapter02"


# 读取文件
def readFile(readPath):
    fp = open(readPath, "rb")
    content = fp.read()
    content = content.decode(encoding='utf-8')  # 解码为字符码
    fp.close()
    return content


print(sys.getdefaultencoding())

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


# 将bunch转化成TF-IDF权重矩阵
def makeTfidfSpace(bunch):
    tfidfSpace = Bunch(targetName=bunch.targetName, label=bunch.label, fileNames=bunch.fileNames,
                       contents=bunch.contents,
                       tdm=[], vocabulary=[])
    '''
    max_df：这个给定特征可以应用在 tf-idf 矩阵中，用以描述单词在文档中的最高出现率。假设一个词（term）在 80% 的文档中都出现过了，那它也许（在剧情简介的语境里）只携带非常少信息。
    min_df：可以是一个整数（例如5）。意味着单词必须在 5 个以上的文档中出现才会被纳入考虑。设置为 0.2；即单词至少在 20% 的文档中出现 。
    sublinear_tf:应用子线性tf缩放，即用1 + log（tf）替换tf。
    '''
    vectorizer = TfidfVectorizer(stop_words=stopList, sublinear_tf=True, max_df=0.5)

    '''
    第一种方法是在用CountVectorizer类向量化之后再调用TfidfTransformer类进行预处理。
    第二种方法是直接用TfidfVectorizer完成向量化与TF-IDF预处理。
    这里是用第二种
    '''
    # transformer = TfidfTransformer()
    contents=list()
    for content in  bunch.contents:
        contents.append(str(content))
    # 词频矩阵(TF-IDF)
    tfidfSpace.tdm = vectorizer.fit_transform(contents)#list(str)
    # Tf-idf-weighted  tf-idf的逆文件权重:  (第i-1个文件,vocabulary索引)  权重   的结构

    # print(tfidfSpace.tdm.todense())#所有的词向量如0.74, 0.11, 0,0 0,0 0 0,0.54,0.55,0.001,0.052

    tfidfSpace.vocabulary = vectorizer.vocabulary_  # 所有的词向量索引,如"xx":1表示上面对应的0.11项的词是"xx"

    new_dict = {v: k for k, v in tfidfSpace.vocabulary.items()}  # 转置字典索引
    # new_dict[57514] '石像'
    return tfidfSpace


'''
写入训练集的tfidfSpace
'''
path = rootPath + "/train_word_bag/trainSpace.dat"
bunch = readBunch(path)  # 读取bunch
tfidfSpace = makeTfidfSpace(bunch)  # 获取TF-IDF
spacePath = rootPath + "/train_word_bag/trainTfidfSpace.dat"
writeBunch(spacePath, tfidfSpace)  # 序列化

'''
写入测试集的tfidfSpace
'''

path = rootPath + "/test_word_bag/testSpace.dat"
bunch = readBunch(path)  # 读取bunch
tfidfSpace = makeTfidfSpace(bunch)  # 获取TF-IDF
spacePath = rootPath + "/test_word_bag/testTfidfSpace.dat"
writeBunch(spacePath, tfidfSpace)  # 序列化
