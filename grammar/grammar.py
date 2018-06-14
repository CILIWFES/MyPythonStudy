x,y,z=1,2,3
print(x,y,z)

dict={"da":8,"dada":5}
print(dict)

x,y,z={5,8,7}


#闭包
def function(arr):
    def test():
        print(arr)
    return  test
a=function("dassadsas")

print(a)