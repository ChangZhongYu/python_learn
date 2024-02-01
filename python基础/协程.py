"""
asyncio 协程类：
    在进行IO操作、request等时，线程会处于阻塞状态，此时可以通过协程让线程先处理其他事务，已达到高效利用CPU
"""

import asyncio
import time


async def print_1(time, name):
    print(name)
    await asyncio.sleep(time)
    print(name)


"""
# 通过async/await声明协程，简单地调用一个协程并不会使其被调度执行
async def main():
    print(f'开始时间：{time.strftime('%X')}')
    await print_1(1,'张三')
    await print_1(2,'李四')
    print(f'开始时间：{time.strftime('%X')}')

# asyncio.run() 函数用来运行最高层级的入口点"main()" 函数
asyncio.run(main())
"""


# asyncio.create_task() 函数用来并发运行作为 asyncio 任务 的多个协程。
# 输出显示代码段的运行时间比之前快了 1 秒,这里就体现了并发时多个协程可以切换执行
async def main():
    print(f'开始时间：{time.strftime('%X')}')
    tasks = [
        asyncio.create_task(print_1(1, '张三')),
        asyncio.create_task(print_1(2, '李四'))
    ]

    # 3.11 版本加入 asyncio.TaskGroup 类提供了 create_task() 的更现代化的替代。
    # async with asyncio.TaskGroup as at:
    #     tasks = [
    #         at.create_task(print_1(1, '张三')),
    #         at.create_task(print_1(2, '李四'))
    #     ]
    #     上下文管理器退出时，等待是隐含的
    await asyncio.wait(tasks)

    print(f'开始时间：{time.strftime('%X')}')


# asyncio.run() 函数用来运行最高层级的入口点"main()" 函数
asyncio.run(main())
