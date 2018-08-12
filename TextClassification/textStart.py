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
# print(text)


# 初识别jieba
import jieba

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


# 保存文件
def saveFile(savePath, content):
    fp = open(savePath, "wb")
    fp.write(content)
    fp.close()

#读取文件
def readFile(readPath, content):
    fp = open(readPath, "rb")
    content = fp.read()
    fp.close()
    return content


