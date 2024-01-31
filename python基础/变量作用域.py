"""
在Python中，临时变量(局域变量)使用后并未被释放，依旧可以访问，在规则上不允许，实际上仍可访问
"""

# for i in range(10):
#     print(i)
# i = 0
# print(i)

"""

从下面的代码来看，在Python中同名局部变量和全局变量并非指向同一地址
    
"""
# num = 200

def test_a():
    # global 关键字声明变量为全局变量
    global num
    num = 100
    # 就近原则取值
    print(num)
    return None

test_a()
print(num)


