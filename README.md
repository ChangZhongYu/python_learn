<center>用于不同的地方学习python爬虫之间的代码同步</center>


日志：
	     在video_demo.py案例中，抓取视频片段时用同步请求request服务器正常响应，但是使用异步请求aiohttp时服务器返回403拒绝响应。在网上查了很久，尝试了很多情况都不行，url被转、请求头、关闭SSL证书等都无效。单线程同步下载数量众多的切片非常慢，无法使用异步的话只能使用多线/进程改进



！！！字符串不可变！！！！
    

​		在网页爬取了一个m3u8文件，想将里面的.ts链接提取出来，输出的.ts链接鼠标点击可以正常访问，但接下来在代码里用get请求返回的结果却是404。可能是因为循环地给m3u8_url拼接的line中含有某些空白字符导致get请求无法顺利执行,这时候就要用到strip()函数来将m3u8_url链接前后看不见的隐形空白字符给去掉。

使用ffmpeg时要注意input文件是否和ts文件同层级否则会报以下错误

```
[concat @ 0000026a5ef86040] No files to concat
[in#0 @ 0000026a5ef85cc0] Error opening input: Invalid data found when processing input
Error opening input file C:/Project/PycharmProjects/Python_Instance/resources/input.txt.
Error opening input files: Invalid data found when processing input
```

2月5日，在继续优化video_demo时发现了两个问题：

- ```python
  concurrent.futures.wait(futures) 
  并不能等到所有子线程完成任务后执行
  ```

  ![image-20240205230702134](C:\Users\zhong\AppData\Roaming\Typora\typora-user-images\image-20240205230702134.png)

- 其次是有些视频切片合并时会出问题，尤其是B站的视频，应该和编码参数有关系