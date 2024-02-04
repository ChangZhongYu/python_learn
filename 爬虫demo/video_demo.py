"""
    抓取视频案例
"""
import requests
import re
import json
# import asyncio
# import aiohttp
import aiofiles
import os
import logging
from yarl import URL
from concurrent.futures import ThreadPoolExecutor
import time

"""

"""


# 获取m3u8文件地址
# 下载m3u8文件，读取文件获取视频片段地址
# 采用异步方式下载视频片段
# 合并视频

# 获取包含该视频的所有m3u8的字典
def get_m3u8_url(url, headers):
    res_html = requests.get(url, headers=headers)
    # re_obj = re.compile(r'let obj = {"1":{"name":"1080P","url":"(?P<url>.*?)"', re.S)
    re_obj = re.compile(r'let obj =(?P<m3u8>.*?);', re.S)
    m3u8_url_dirc = json.loads(re_obj.findall(res_html.text)[0])
    return m3u8_url_dirc


# 下载m3u8文件
def download_m3u8(url, headers):
    res_m3u8 = requests.get(url, headers=headers)
    name = '../resources/video/' + url.split('/')[-1]
    with open(name, "wb") as f:
        f.write(res_m3u8.content)
    return name


# 读取m3u8文件获取视频片段地址
def read_m3u8(name, url, headers):
    video_url_list = []
    with open(name, mode='r', encoding="utf-8") as f:
        for line in f.readlines():
            line = line.strip()
            # 如果获取的文件中有.m3u8结尾，说明做了跳转。则需要再次处理
            if line.endswith(".m3u8"):
                # 字符串是不可变的
                url = url.replace('index.m3u8', line)
                print(url)
                m3u8_name = download_m3u8(url, headers)
                return read_m3u8(m3u8_name, url, headers)
            if line.startswith("#"):
                continue
            # 如果获取的文件不是https://开头，说明url地址不全，需要补全
            if line.startswith("https://"):
                video_url_list.append(line)
            else:
                video_url_list.append(url.replace('mixed.m3u8', line))
    return video_url_list


# 异步下载视频 采用异步请求时返回403，尝试了很多方法依旧不行，不确定是否是网站做了某种审核禁止异步访问
async def download_video(m3u8_url, headers, session):
    # res_video = requests.get(m3u8_url, headers=headers)
    async with session.get(URL(m3u8_url, encoded=False), headers=headers) as res:
        print(res.status)
        name = '../resources/video2/' + m3u8_url.split('/')[-1]
        async with aiofiles.open(name, mode="wb") as f:
            await f.write(await res.content.read())
    print(f'异步下载{name}完成')


def download_video_1(m3u8_url, headers):
    # 可能存在不可见的空白符
    m3u8_url = m3u8_url.strip()
    res_video = requests.get(m3u8_url, headers=headers)
    print(res_video.status_code)
    name = '../resources/video/' + m3u8_url.split('/')[-1]
    with open(name, mode='wb') as f:
        f.write(res_video.content)
    print(f'{name}下载完成')
    res_video.close()


def merge_m3u8_ts(name):
    dos = f'ffmpeg -f concat -safe 0 -i {name} -c copy A:/Download/movie/4.mp4'
    print(dos)
    os.system(dos)
    # os.system(f'copy /b {name} ../resources/video/1.mp4')
    print('视频合并完成')


# 程序入口
def mian():
    # 开启日志
    logging.basicConfig(level=logging.INFO)
    # 准备请求
    html_url = 'https://www.yingshi.tv/vod/play/id/200669/sid/1/nid/1.html'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
    }

    # 调用方法获取包含该视频的所有m3u8的字典
    m3u8_url_dirc = get_m3u8_url(html_url, headers)

    # 遍历字典
    video_url_list = []
    for key in m3u8_url_dirc.keys():
        # 获取该视频的所有m3u8文件地址
        m3u8_url = m3u8_url_dirc[key]["url"]
        # 掉用方法传入url下载m3u8文件并返回m3u8文件名
        m3u8_name = download_m3u8(m3u8_url, headers)
        # 调用方法，传入m3u8文件名，读取m3u8文件，获取该视屏所有切片的地址，存入list
        video_url_list = read_m3u8(m3u8_name, m3u8_url, headers)
        break  # 测试下载一个视频

    # tasks = []    #存储异步任务
    # 为了不频繁创建session，所以在外面创建好后传递给请求
    # async with aiohttp.ClientSession() as session:
    file_name = 'C:/Project/PycharmProjects/python_learn/resources/video/input.txt'
    headers.update({'Referer': 'https://www.yingshi.tv/', 'Origin': 'https://www.yingshi.tv'})
    with open(file_name, mode='w') as f:
        with ThreadPoolExecutor(16) as thread_pool:
            for video_url in video_url_list:
                print(video_url)
                # 将所有的切片文件名拼接，后续用于合并视频

                f.write("file '" + video_url.split("/")[-1] + "'" + "\n")
                # 多线程同步下载
                thread_pool.submit(download_video_1, m3u8_url=video_url, headers=headers)
                # 异步下载
                # tasks.append(asyncio.create_task(download_video(video_url, headers, session)))
                # break  # 测试下载一个切片
                # await asyncio.wait(tasks)
    merge_m3u8_ts(file_name)


if __name__ == '__main__':
    print(f'开始时间：{time.strftime('%X')}')
    mian()
    # with open('../resources/video/input.txt', 'r') as f:
    #     with open('../resources/video/output.txt', 'w') as o:
    #         for line in f.readlines():
    #             line = line.strip()
    #             if line.startswith("'"):
    #                 continue
    #             else:
    #                 o.write(line + "'"+'\n')
    # file_name = 'C:/Project/PycharmProjects/python_learn/resources/video/input.txt'
    # merge_m3u8_ts(file_name)
    print('程序结束')
    print(f'开始时间：{time.strftime('%X')}')
