"""
使用异步方式改良程序
    异步请求 aiohttp
    异步IO aiofiles

"""
import asyncio
import requests
from lxml import etree
import aiohttp
import aiofiles


# 创建对象


def get_img_info(url, headers):
    print('-' * 30, '开始抓取图片信息', '-' * 30)
    url_list = []
    response = requests.get(url, headers=headers)
    html = etree.HTML(response.text)
    ul_list = html.xpath('//*[@id="index_ajax_list"]/li/div')
    for ul in ul_list:
        img_url = ul.xpath("./a/@href")[0]
        title = ul.xpath("./a/@title")[0]
        viewing_count = ul.xpath('./div[@class="postmeta-box"]/span[1]/text()')[0]
        like_count = ul.xpath('./div[@class="postmeta-box"]/span[2]/text()')[0]

        url_list.append({"img_url": img_url, "title": title, "viewing_count": viewing_count, "like_count": like_count})
        print(f">>标题：{title}，<< >>浏览数量：{viewing_count}，<< >>点赞数量：{like_count}<<")
    print('-' * 30, '图片信息抓取完成', '-' * 30)
    return url_list


# 采用异步请求获取具体图片页面
async def get_img_url(list, headers):
    img_url_lists = []

    for img_info in list:
        url = img_info["img_url"]
        title = img_info["title"]
        viewing_count = img_info["viewing_count"]
        like_count = img_info["like_count"]

        # 如果图片点赞数量大于20 或者浏览数量大于2000，则下载图组
        if int(like_count) > 20 or int(viewing_count) > 2000:
            print(f"开始抓取高人气图组链接：{title}")
            # 这里采用异步请求获取页面
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as res:
                    etree_html = etree.HTML(await res.text())
                    img_url_lists += etree_html.xpath('//*[@id="content"]/div//img/@src')
            print(f"高人气图组链接抓取完成：{title}")
    return img_url_lists


# 采用异步请求和异步写入
async def download_img(url, headers):
    # 下载图片
    name = url.split("/")[-1]
    print(f"开始下载：{name}")
    # 采用异步请求
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            # 采用异步写入
            async with aiofiles.open("../resources/img/" + name, "wb") as f:
                await f.write(await response.content.read())
    print(f"下载完成：{name}")


async def main():
    URL = "https://dimtown.com/jk"
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    tasks = []
    img_info_list = get_img_info(URL, headers)

    img_url_lists = get_img_url(img_info_list, headers)
    for img_url in await img_url_lists:
        tasks.append(asyncio.create_task(download_img(img_url, headers)))
    await asyncio.wait(tasks)


if __name__ == '__main__':
    asyncio.run(main())
    print('程序结束')
