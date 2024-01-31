"""
导入模块：
    关键字
        import 包名 [as 别名]；导入整个包
        form 包名 import [模块|类|变量|方法名|*][as 别名] ；导入包内指定方法
"""
# import time
# flag = 0
# while flag < 5:
#     print(flag)
#     time.sleep(1)
#     flag += 1

from time import sleep

flag = 0
while flag < 10:
    print(flag)
    sleep(1)
    flag += 1

# 调试标志
# if __name__ == '__main__':

# __all__ = [] 通过此标志可以控制 import * 的访问内容

