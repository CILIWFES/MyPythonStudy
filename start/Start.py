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

import random
def makeGenrator():
    lst=[i for i in range(10)]
    def foo(bb):
        genrator=lst
        if bb==1:
            for indx in genrator:
                yield indx
        else:
            x=yield len(genrator)
            print(x)
            yield 110

    return foo

fo2o=makeGenrator()
k=fo2o(2)
print(next(k))#获得len(genrator)
print(k.send(1))#x=1并往下走,返回110

###################################################################################################################
endTime = datetime.datetime.now()  # 终止时间

print("""\n-------------------------------------------------------------------------------------
运行结束
运行时间:""", endTime.microsecond - startTime.microsecond, "纳秒,即", (endTime - startTime).total_seconds(), "秒")
