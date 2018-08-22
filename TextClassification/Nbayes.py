# -*- coding: utf-8 -*-

import sys  
import os 
import time
from numpy import *
import numpy as np
from TextClassification.Nbayes_lib import *


# 配置utf-8输出环境
sys.getdefaultencoding()

contentSet, classSet = loadDataSet()
nb = NBayes()
nb.train_set(contentSet, classSet)
testSet=[['BBB','stop', 'posting', 'stupid', 'worthless', 'garbage']]
testSet,testDetail=nb.test_set(testSet)
print(nb.predict(testSet))
