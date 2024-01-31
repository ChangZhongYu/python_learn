# 安装requests模块
import requests

# 获取音乐URL
music_url ="https://webfs.hw.kugou.com/202312181103/60cf43e6718656bd18dea589b8fa52b4/KGTX/CLTX001/3805214793174a9ad1a241afdaa14ad8.mp3"

# 伪装浏览器访问
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

# 发送get请求
music_requesrs = requests.get(music_url,headers=headers)

# 将服务器的数据保存
with open('resource/1.mp3', 'wb') as file:
    file.write(music_requesrs.content)