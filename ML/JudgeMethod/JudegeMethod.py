import numpy as np
import matplotlib.pyplot as plt
from prettytable import PrettyTable


class JudegeMethod:
    def __init__(self):
        # 这些是坐标
        self.TP = 0  # 真正例,当前正确预测
        self.FP = 1  # 假正例,当前错误预测
        self.TN = 2  # 真反例,其他错误预测
        self.FN = 3  # 假反例,其他正确预测
        self.PRECISION = 4  # 查准率
        self.RECALL = 5  # 查全率
        self.dataDict = {}

    def Judege(self, predictions, realClass):
        if len(predictions) is not len(realClass):
            raise Exception("预测值与实际值长度不一")
        dic = {}
        for index in range(len(realClass)):
            realName = realClass[index]
            preName = predictions[index]

            if realName not in dic:
                dic[realName] = [0, 0, 0, 0, 0, 0]
            if preName not in dic:
                dic[preName] = [0, 0, 0, 0, 0, 0]

            if realName == preName:
                dic[realName][self.TP] += 1  # 正确,真正例+1
            elif realName != preName:
                dic[realName][self.FP] += 1  # 错误,假正例+1
                dic[preName][self.TN] += 1  # 其他错误,真反例

        allCnt = len(predictions)
        precisions = []
        recalls = []

        for k, lst in dic.items():  # 计算假反例
            lst[self.FN] = allCnt - sum(lst)  # 假反例,其他正确预测
            lst[self.PRECISION] = lst[self.TP] / (float(lst[self.TP] + lst[self.TN]))
            lst[self.RECALL] = lst[self.TP] / (float(lst[self.TP] + lst[self.FP]))  # 假反例,其他正确预测
            precisions.append(lst[self.PRECISION])
            recalls.append(lst[self.RECALL])
        self.dataDict = dic
        self.printData()
        self.showFigure(predictions, recalls)

    def printData(self):
        table = PrettyTable(["类名", "查准率", "查全率"])

        table.align["查准率"] = "c"  # 以name字段左对齐
        table.align["查全率"] = "c"  # 以name字段左对齐
        table.padding_width = 2  # 填充宽度
        for k, lst in self.dataDict.items():  # 计算假反例
            table.add_row([k, "{0:.2f}".format(lst[self.PRECISION]), "{0:.2f}".format(lst[self.RECALL])])
        print(table)

    def showFigure(self, precisions, recalls):
        # 绘图
        fig = plt.figure()
        # 把画布分成1行1列 1x1块,当前画布处于第1块
        ax = fig.add_subplot(1, 1, 1)
        # 绘制散点图x=查全,y=查准
        ax.scatter(recalls, precisions, s=10, color='blue', marker='o')
        # 绘制图线
        ax.plot(recalls, precisions, color='r')
