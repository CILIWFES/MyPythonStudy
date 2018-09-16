# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeRegressor

# Create a random dataset
def plotfigure(X,X_test,y,yp):
	plt.figure()
	plt.scatter(X.tolist(), y,  color='blue', marker='o', label="data")
	plt.plot(X_test, yp, c="r", label="max_depth=5", linewidth=2)
	plt.xlabel("data")
	plt.ylabel("target")
	plt.title("Decision Tree Regression")
	plt.legend()
	plt.show()

x = np.linspace(-5,5,200)
siny = np.sin(x)    # 给出y与x的基本关系
X = np.mat(x).T
y = siny+np.random.rand(1,len(siny))*1.5	# 加入噪声的点集
y = y.tolist()[0]
# Fit regression model
clf = DecisionTreeRegressor(max_depth=3)
clf.fit(X, y)

# Predict
X_test = np.arange(-5.0, 5.0, 0.05)[:, np.newaxis]
yp = clf.predict(X_test)

plotfigure(X,X_test,y,yp)