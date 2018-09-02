import datetime
import sys
import os
import numpy as np
import treePlotter

# curPath = os.path.abspath(os.path.dirname(__file__))
# rootPath = os.path.split(curPath)[0]
# sys.path.append(rootPath)


print("Python学习测试程序")

print("""运行开始
-------------------------------------------------------------------------------------\n""")
startTime = datetime.datetime.now()  # 起始时间

###################################################################################################################

# import dataStruct.list.list

# import  dataStruct.dict.dict

# import  dataStruct.tuple.tuple
# import  dataStruct.string.String
# import grammar.grammar
# import classTest.classTest
# import Thread.thread
# import ioTest.io

# import modelTest.allTest
# import modelTest.Numpy.matrix

# import distance.Distance
# import dataVisualization.DataVisualization
# import TextClassification.textStart


a = ['2', 5]
a = [eval(str(item)) for item in a]
print(sum(a) / len(a))

a = ['s', '2']
b = ['s', '2']
print(a + b)

import numpy as np
from collections import Counter
saaa = np.mat([[0, 2, 5, 7, 3], [5, 8, 9, 7, 4], [5, 8, 9, 7, 4], [5, 8, 9, 7, 4], [5, 8, 9, 7, 4]])

print(saaa.item(5))
###################################################################################################################
endTime = datetime.datetime.now()  # 终止时间

print("""\n-------------------------------------------------------------------------------------
运行结束
运行时间:""", endTime.microsecond - startTime.microsecond, "纳秒,即", (endTime - startTime).total_seconds(), "秒")
