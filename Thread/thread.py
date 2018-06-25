
import time
import _thread as thread
"""
def run(time1):
    print("启动")
    time.sleep(time1)
    print("准备停止")
    thread.exit_thread()
print(__name__)
thread.start_new_thread(run,(10000,))#单个元组要加,

"""

import  threading
class threadTest(threading.Thread):
    def __init__(self,interval,sleepTime):
        threading.Thread.__init__(self)
        self.interval=interval
        self.sleepTime=sleepTime
        self.__stop=True
    def run(self):
        while self.interval>0 and self.__stop:#变量定义一定要精确
            print('time.ctime=',time.ctime())#时间打印
            self.interval-=1
            time.sleep(self.sleepTime)
    def stop(self):#暂停
        print("线程暂停")
        self.__stop=False


test=threadTest(100,0.02)#表示秒
test.start()
time.sleep(0.2)
test.stop()
a=5
