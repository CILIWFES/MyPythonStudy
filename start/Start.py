import datetime
print("Python学习测试程序")

print("""运行开始
-------------------------------------------------------------------------------------\n""")
startTime=datetime.datetime.now()#起始时间
###################################################################################################################

# import dataStruct.list.list

# import  dataStruct.dict.dict

#import  dataStruct.tuple.tuple
# import  dataStruct.string.String
import grammar.grammar
###################################################################################################################
endTime=datetime.datetime.now()#终止时间
print("""\n-------------------------------------------------------------------------------------
运行结束
运行时间:""",endTime.microsecond-startTime.microsecond,"纳秒,即",(endTime-startTime).total_seconds(),"秒")




