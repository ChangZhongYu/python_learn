# 定义list
my_list = ["zhangsan", 4, "李四"]

# 通过len(list)可以获取list的长度
print(len(my_list))
# 获取list中指定元素的索引
index = my_list.index("zhangsan")
print(index)
print(my_list[index])

# 在指定索引插入元素
my_list.insert(0, "one")
print(my_list)

# 末尾追加元素
my_list.append(2)
print(my_list)

# 将其他列表追加至尾部
my_list.extend(["王五", "赵六"])
print(my_list)

# 删除指定索引元素
del my_list[0]
print(my_list)

ele = my_list.pop(0)
print(ele)
print(my_list)

# 删除list中第一个匹配的指定元素
my_list.remove(4)
print(my_list)

# 清空列表
# my_list.clear()
# print(my_list)

# 统计指定元素在list中的个数
print(my_list.count("王五"))


