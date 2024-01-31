"""
Thread 线程类
    学习使用python的threading模块
    可以通过构造方法传入任务创建新的线程
    也可以通过继承Thread类来覆写run()方法创建新线程

"""

from threading import Thread


# 定义一个打印方法
def fanA():
    for i in range(100):
        print('fanA', i)


if __name__ == '__main__':
    # 创建一个新的线程，传入任务
    t = Thread(target=fanA)
    # 告知CPU这个线程已经就绪
    t.start()

    for i in range(100):
        print('main', i)
