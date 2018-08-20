from lxml import etree, html
import os
import sys

print(sys.getdefaultencoding())

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0] + "/Support/chapter02"

# 初识别lxml
# path = rootPath + '/1.html'
# content = open(path, 'rb').read()
# page = html.document_fromstring(content)  # 解析文件
# text = page.text_content()  # 去除标签
import jieba

'''
# 初识别jieba

# 默认切分
segList = jieba.cut("张三1996年毕业于北京五道口职业大学", cut_all=False)
print("Default Mode:", " ".join(segList))  # segList为序列," "与序列每个元素拼接
# 默认的和上面一样
segList = jieba.cut("张三1996年毕业于北京五道口职业大学")
print(" ".join(segList))
# 全切分
segList = jieba.cut("张三1996年毕业于北京五道口职业大学", cut_all=True)
print("Full Mode:", " ".join(segList))
# 搜索引擎模式切分
segList = jieba.cut_for_search("小明毕业于中国科学院计算机所,后在日本京都大学深造")
print(" ".join(segList))

'''


# print(text)


# 保存文件
def saveFile(savePath, fileName, content):
    if not os.path.exists(savePath):
        os.makedirs(savePath)  # 若不存在则创建目录
    content = content.encode(encoding='utf-8')  # 解码为字节码
    fp = open(savePath + fileName, "wb")
    fp.write(content)
    fp.close()


# 读取文件
def readFile(classPath, fileNamme):
    fp = open(classPath + fileNamme, "rb")
    content = fp.read()
    content = content.decode(encoding='utf-8')  # 解码为字符码
    fp.close()
    return content


"""
将文件夹下二级文件进行分词,并保存
searchPath:搜索路径,xx/xx/
savePath:保存路径xx/xx/
"""


def searchFileToJieba(searchPath, savePath):
    cateList = os.listdir(searchPath)
    for dir in cateList:
        if not os.path.exists(searchPath + dir + '/'):  # 不是文件夹
            content = readFile(searchPath, dir).strip()
            content = content.replace("\r\n", "").strip()  # 删除换行与多余的空格
            content_seg = jieba.cut(content)
            saveFile(savePath, dir, " ".join(content_seg))
        else:
            tempSearchPath = searchPath + dir + "/"
            tempSavePath = savePath + dir + "/"
            searchFileToJieba(tempSearchPath, tempSavePath)


# 转化语料库遍历提取语料
seachPath = rootPath + "/train_corpus_small/"  # 未分词语料路径
savePath = rootPath + "/train_corpus_seg/"  # 已分词的语料路径
searchFileToJieba(seachPath, seachPath)

seachPath = rootPath + "/test_corpus_small/"  # 未分词语料路径
savePath = rootPath + "/test_corpus_seg/"  # 已分词的语料路径
searchFileToJieba(seachPath, seachPath)

import pickle

from sklearn.datasets.base import Bunch

"""
一级:总文件夹
二级:label文件夹
三级:分类文件
通过词包下二级文件进行解析,获取标签和对应的内容
seachPath:一级地址
"""


def makeBunch(seachPath):
    # 将分类信息保存至Bunch中
    bunch = Bunch(targetName=[], label=[], fileNames=[], contents=[])
    cateList = os.listdir(seachPath)
    bunch.targetName.extend(cateList)  # 类别信息
    for mydir in cateList:
        classPath = seachPath + mydir + '/'
        fileList = os.listdir(classPath)
        for fileName in fileList:
            bunch.label.append(mydir)  # 保存当前文件的分类标签
            bunch.fileNames.append(mydir + "/" + fileName)  # 当前 标签/文件名
            bunch.contents.append(readFile(classPath, fileName).strip())  # 文本内容
    return bunch

searchPath = rootPath + "/train_corpus_seg/"
bunch = makeBunch(searchPath)

savePath = rootPath + "/train_word_bag/trainSpace.dat"
# Bunch对象持久化
fileObj = open(savePath, 'wb')
pickle.dump(bunch, fileObj)
fileObj.close()

searchPath = rootPath + "/test_corpus_seg/"
bunch = makeBunch(searchPath)

savePath = rootPath + "/test_word_bag/testSpace.dat"
# Bunch对象持久化
fileObj = open(savePath, 'wb')
pickle.dump(bunch, fileObj)
fileObj.close()
