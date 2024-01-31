"""
ThreadPoolExecutor 线程池类（进程池类同理）
    一次性开辟一定数量的线程，我们用户直接给线程池提交任务，线程任务的调度交给线程池来完成
"""

from concurrent.futures import ThreadPoolExecutor


def fan_task(name):
    for i in range(1000):
        print(name, i)


if __name__ == '__main__':
    # 创建线程池,提交任务，任务执行完成，回到主线程。涉及守护线程概念
    with ThreadPoolExecutor(10) as thread_pool:
        for i in range(100):
            thread_pool.submit(fan_task, name=f"线程{i}")

    print("任务执行完毕")
