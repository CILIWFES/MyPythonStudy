import numpy as np

myZero = np.zeros([5, 6])  # 生成一个5x6的矩阵,初始值为0
print(type(myZero))
print(myZero)

myOnes = np.ones([5, 4])  # 生成一个5x4的矩阵,初始值为1
print(type(myOnes))
print(myOnes)

myRand = np.random.rand(5, 4)  # 生成一个5x4的矩阵,初始值为随机值,(0~1)
print(type(myRand))
print(myRand)

myEye = np.eye(5)  # 生成5x5单位矩阵
print(type(myEye))  # <class 'numpy.ndarray'>
print(myEye)

# list转化为矩阵
testList = [[1, 2, 3, 4, 5], [1, 5, 7, 8, 9], [1, 4, 7, 8, 5], [1, 2, 2, 2, 2], [2, 1, 5, 3, 6]]
myMatrix = np.mat(testList)
print(type(myMatrix))  # <class 'numpy.matrixlib.defmatrix.matrix'>
print(myMatrix)

print()
print("""矩阵操作""", end='\n\n')

# 矩阵数加
print(6 + myEye)
# 矩阵相加
print(myOnes + myRand)
# print(myOnes+myEye)#相加失败,行列数不一致

# 矩阵数乘
print(10 * myRand)

# 矩阵求和(逐个列向量求和)
print(np.sum(myRand))

print(np.sum(myMatrix))

print(np.sum(myEye))

# 矩阵乘积
myMatrix1 = np.eye(5)
myMatrix2 = np.random.rand(5, 5)
print(myMatrix2)
print(2 * myMatrix1 * myMatrix2)
# 两个类型相同的矩阵乘积,最后类型还是对于矩阵
print(type(2 * myMatrix1 * myMatrix2))  # <class 'numpy.ndarray'>
print(myMatrix * myMatrix1)
# 两个类型不同的矩阵乘积类型是下列矩阵
print(type(myMatrix * myMatrix1))  # <class 'numpy.matrixlib.defmatrix.matrix'>

# 矩阵中各个元素乘积
print(myMatrix)
print(np.multiply(myMatrix, myMatrix))
print(np.multiply(myMatrix, myMatrix1))

# 矩阵的n次幂
print(myMatrix)
print(np.power(myMatrix, 3))

# 矩阵的转置
print(myMatrix)
print(myMatrix.T)
print(myMatrix.transpose())
print(np.random.rand(5, 3).transpose())

print(end="\n\n")
# 矩阵的操作

print(myMatrix)

print(myMatrix)
[m, n] = np.shape(myMatrix)
print("矩阵的行数与列数:", m, n)
print("按行切片:", myMatrix[2])
print("按列切片:", myMatrix.T[2])

# 矩阵元素比较
print(myMatrix1 > myMatrix)

# 复制矩阵
tempMatrix = myMatrix.copy()
print(tempMatrix == myMatrix)
print(id(tempMatrix) == id(myMatrix))

# 矩阵的合并
tempMatrix = np.append(myMatrix, np.random.rand(1, 5), 0)  # 为myMatrix添加一行
print(tempMatrix)
tempMatrix = np.append(myMatrix, np.random.rand(5, 1), 1)  # 为myMatrix添加一列
print(tempMatrix)

# 矩阵的删除
print(myMatrix)
tempMatrix = np.delete(myMatrix, [1, 2, 3], 0)  # 删除myMatrix的第2,3,4行
print(tempMatrix)  # 删除后的矩阵

print(myMatrix)  # 删除前的矩阵

tempMatrix = np.delete(myMatrix, 2, 0)  # 删除myMatrix的第三行
print(tempMatrix)
print(myMatrix)  # 删除前的矩阵

tempMatrix = np.delete(myMatrix, 1, 1)  # 删除myMatrix的第三列
print(tempMatrix)


#矩阵的行列式
print(myMatrix)
print(np.linalg.det(myMatrix))

#矩阵的逆矩阵
print(np.linalg.inv(myMatrix))
print(myMatrix*np.linalg.inv(myMatrix))

#矩阵的对称
print(myMatrix)
print(myMatrix*myMatrix.T)

#矩阵的秩
print(np.linalg.matrix_rank(myMatrix))

#可逆矩阵求解
y=[0,0,0,0,5]
print(np.linalg.solve(myMatrix,y))
print(sum(np.multiply(myMatrix,np.linalg.solve(myMatrix,y)).T))