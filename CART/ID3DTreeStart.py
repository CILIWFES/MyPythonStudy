from CART.ID3DTree import *
import os
# 树与分类结构的可视化
import treePlotter.treePlotter as tp


curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0] + "/Support/chapter03"
ID3Path = rootPath + "/dataset.dat"

dtree = ID3DTree()
dtree.loadDataSet(ID3Path, ["age", "revenue", "student", "credit"])
dtree.train()
tp.createPlot(dtree.tree)
