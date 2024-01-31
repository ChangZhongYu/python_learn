"""
Process 进程类
    通过构造方法Process(target = fun)创造新的进程
    也可通过覆写父类
"""
from multiprocessing import Process
def fanA():
    for i in range(1000):
        print('子进程', i)


if __name__ == '__main__':
    # 创建一个新的进程，传入任务
    t = Process(target=fanA)
    # 告知CPU这个进程已经就绪
    t.start()

    for i in range(1000):
        print('主进程', i)
