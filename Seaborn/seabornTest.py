import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# Seaborn其实是在matplotlib的基础上进行了更高级的API封装，从而使得作图更加容易，在大多数情况下使用seaborn就能做出很具有吸引力的图
# sns.set_style("dark")  # darkgrid, whitegrid, dark, white, ticks
# plt.plot(np.arange(10))
# plt.show()
#
# sns.set(style="white", palette="muted", color_codes=True)  # set( )设置主题，调色板更常用
# plt.plot(np.arange(10))
# plt.show()
#
# path2 = "E:\WorkSpace\PyCharm\MyPythonStudy\Support\\test.csv"
# df1 = pd.read_csv(path2, sep=';', low_memory=False, header=None)
# df1 = df1.dropna(axis=1, how='all')
# df1.head()  ## 获取前五行数据查看查看
# print(df1)
#
# fig, axes = plt.subplots(1, 2)
# sns.distplot(df1, ax=axes[0], kde=True, rug=True)  # kde 密度曲线  rug 边际毛毯
# sns.kdeplot(df1, ax=axes[1], shade=True)  # shade  阴影
# plt.show()

#
# sns.set(palette="muted", color_codes=True)
# rs = np.random.RandomState(10)
# d = rs.normal(size=100)  # 正态（高斯）分布中抽取随机样本
# # figsize每个图片尺寸
# f, axes = plt.subplots(2, 2, figsize=(7, 7), sharex=True)
# # ax 绘图区域   kds是否绘制高斯核密度估计默认True
# sns.distplot(d, kde=False, color="b", ax=axes[0, 0])
# # 是否绘制（标准化）直方图
# sns.distplot(d, hist=False, rug=True, color="r", ax=axes[0, 1])
#
# sns.distplot(d, hist=False, color="g", kde_kws={"shade": True}, ax=axes[1, 0])
#
# sns.distplot(d, color="m", ax=axes[1, 1])
# plt.show()
