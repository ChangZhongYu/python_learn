import requests
import httpx

"""
    演示对比两张请求发送方式
"""
# 传统request
# response = requests.get("https://www.baidu.com")
# print(response.text)

# python3引进的httpx
response = httpx.get("https://www.bilibili.com")
print(response.text)
