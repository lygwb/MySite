import time
import sched
from .get_fault import faults_todb

# 初始化sched模块的scheduler类
# 第一个参数是一个可以返回时间戳的函数，第二个参数可以在定时未到达之前阻塞。
s = sched.scheduler(time.time, time.sleep)


# 被周期性调度触发的函数
def perform1(inc):
    s.enter(inc, 0, perform1, (inc,))
    faults_todb()


def my_timer(func, inc=2):
    if func == '1':
        s.enter(0, 0, perform1, (60,))


# 每10秒钟执行perform1
def my_timer_interface():
    my_timer('1')
    s.run()
