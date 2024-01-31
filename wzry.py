"""
    抓取王者页面静态页面图片
"""
import requests
from pyquery import PyQuery


url = "https://pvp.qq.com/web201605/herolist.shtml"

html = requests.get(url).content

doc = PyQuery(html)

items = doc('.herolist>li').items()


for item in items:

    url = item.find('img').attr('src')
    urls = 'https:' + url
    print(urls)

    name = item.find('a').text()
    print(name)

    url_content = requests.get(urls).content

    with open("./resource/"+name+".jpg", "wb") as file:
        file.write(url_content)