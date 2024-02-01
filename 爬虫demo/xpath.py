# xpath是在xml中查找元素的工具
# html是xml的子集
# pip install lxml
"""
    /text() 获取元素的文本
    // 获取后代的全部元素
    ./ 从当前元素开始查找
    @属性 获取元素的属性值

"""
import time
import requests
from lxml import etree

# 创建对象

URL = "https://dimtown.com/cosplay/page/2"
headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
response = requests.get(URL, headers=headers)
# print(response.text)

html = etree.HTML(response.text)
ul_list = html.xpath('//*[@id="index_ajax_list"]/li/div')
url_list = []
print('开始抓取图片地址：')
for ul in ul_list:
    url_zi = ul.xpath("./a/@href")
    title = ul.xpath("./a/@title")[0]
    viewing_count = ul.xpath('./div[@class="postmeta-box"]/span[1]/text()')[0]
    like_count = ul.xpath('./div[@class="postmeta-box"]/span[2]/text()')[0]
    print(f"标题：{title}，浏览数量：{viewing_count}，点赞数量：{like_count}")

    # 如果图片点赞数量大于20 或者浏览数量大于2000，则下载图组
    if int(like_count) > 20 or int(viewing_count) > 2000:
        print(f"开始下载图组：{title}")
        res = requests.get(url_zi[0], headers=headers)
        etree_html = etree.HTML(res.text)
        # 获取图组节点
        img_node_list = etree_html.xpath('//*[@id="content"]/div//img')
        # 便利遍图组节点，获取图片地址
        for img_node in img_node_list:
            img_url = img_node.xpath('./@src')[0]
            # 下载图片
            res_img = requests.get(img_url, headers=headers)
            name = img_url.split("/")[-1]
            with open("../resources/img2/" + name, "wb") as f:
                f.write(res_img.content)
            print(f"下载完成：{name}")

            res_img.close()
            # 防止爬虫速度过快
            # time.sleep(1)
            # break 用于测试
        print(f"*********************下载图组完成：{title}***********************")
        res.close()
print('程序结束')
response.close()
