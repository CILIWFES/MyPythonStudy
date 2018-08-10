import sys
import os
import numpy as np

print(sys.getdefaultencoding())


def fillToMatrix(path,delimiter):
    recordlist=[]
    fp=open(path,"rb")
    content=fp.read()
    fp.close()
    rowlist=content.splitlines()
    recordlist=[map(eval,row.split(delimiter)) for row in rowlist if row.strip()]