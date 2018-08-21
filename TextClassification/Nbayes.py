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
nb.map2vocab(contentSet[3])
print(nb.predict(nb.testset))
