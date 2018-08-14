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
def saveFile(savePath, content):
    content = content.encode(encoding='utf-8')#解码为字节码
    fp = open(savePath, "wb")
    fp.write(content)
    fp.close()


# 读取文件
def readFile(readPath):
    fp = open(readPath, "rb")
    content = fp.read()
    content = content.decode(encoding='utf-8')#解码为字符码
    fp.close()
    return content

'''
#转化语料库遍历提取语料
corpusPath = rootPath + "/train_corpus_small"  # 未分词语料路径
segPath = rootPath + "/train_corpus_seg"  # 已分词的语料路径

# 获取语料库下的文件路径
cateList = os.listdir(corpusPath)

for fileDir in cateList:
    classPath = corpusPath + "/" + fileDir + "/"
    testPath = segPath + "/" + fileDir + "/"
    if not os.path.exists(testPath):
        os.makedirs(testPath)  # 若不存在则创建目录
    fileList = os.listdir(classPath)  # 目录下所有文件
    for fileName in fileList:
        fullName = classPath + fileName  # 文件夹全名
        content = readFile(fullName).strip()
        content = content.replace("\r\n", "").strip()  # 删除换行与多余的空格
        content_seg = jieba.cut(content)
        saveFile(testPath + fileName, " ".join(content_seg))


'''
import pickle

from  sklearn.datasets.base import Bunch
wordbagPath=rootPath+"/train_word_bag/train_set.dat"


bunch=Bunch(target_name=[],label=[],fileNames=[],contents=[])
'''
segPath=rootPath+"/train_corpus_seg/"
cateList=os.listdir(segPath)#将分类信息保存至Bunch中
bunch.target_name.extend(cateList)#类别信息

for mydir in cateList:
    classPath=segPath+mydir
    fileList=os.listdir(classPath)
    for fileName in fileList:
        fullName=classPath+"/"+fileName
        bunch.label.append(mydir)#保存当前文件的分类标签
        bunch.fileNames.append(fullName)#当前文件路径
        bunch.contents.append(readFile(fullName).strip())

#Bunch对象持久化
fileObj=open(wordbagPath,'wb')
pickle.dump(bunch,fileObj)
print(bunch.label)
fileObj.close()

print("构建Bunch对象完成")

'''
#对象读取持久化序列
fileObj=open(wordbagPath,'rb')
bunch=pickle.load(fileObj)
# print(bunch.label)


stopworgPath=rootPath+"/train_word_bag/hlt_stop_words.txt"
stopList=readFile(stopworgPath).splitlines()
# print(stopList)

