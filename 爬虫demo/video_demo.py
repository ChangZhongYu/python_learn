"""
    抓取视频案例
"""
import requests
import re
import json
import asyncio
import aiohttp
import aiofiles
import os

"""

"""


# 获取m3u8文件地址
# 下载m3u8文件，读取文件获取视频片段地址
# 采用异步方式下载视频片段
# 合并视频

# 获取m3u8文件地址
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
def read_m3u8(name):
    video_url_list = []
    with open(name, mode='r', encoding="utf-8") as f:
        for line in f.readlines():
            if line.startswith("#"):
                continue
            video_url_list.append(line.strip())
    return video_url_list


# 异步下载视频
async def download_video(m3u8_url, headers, session):
    # res_video = requests.get(m3u8_url, headers=headers)
    async with session.get(m3u8_url, headers=headers) as res:
        name = '../resources/video/' + m3u8_url.split('/')[-1]
        async with aiofiles.open(name, mode="wb") as f:
            await f.write(await res.content.read())
    print(f'异步下载{name}完成')


def download_video_1(m3u8_url, headers):
    res_video = requests.get(m3u8_url, headers=headers)
    name = '../resources/video/' + m3u8_url.split('/')[-1]
    with open(name, mode='wb') as f:
        f.write(res_video.content)
    print(f'{name}下载完成')


def merge_m3u8_ts(name):
    # print(f'copy /b {name} 1.mp4')
    # os.system(f'copy /b {name} ../resources/video/1.mp4')
    os.system(r'copy /b ../resources/video/*.ts 2.mp4')
    print('视频合并完成')


# 程序入口
async def mian():
    html_url = 'https://www.yingshi.tv/vod/play/id/197245/sid/1/nid/1.html'
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    }
    # m3u8_url_dirc = get_m3u8_url(html_url, headers)
    # m3u8_url_list = []
    # for key in m3u8_url_dirc.keys():
    #     m3u8_url_list.append(m3u8_url_dirc[key]["url"])
    #
    # download_m3u8(m3u8_url_list[0], headers)
    # 这里为了方便直接给了文件名，文件名可以通过download_m3u8()返回
    name = '../resources/video/f790c290a82ef3e46cc44fb42e5f0f7f5a0080055abdb275613ac02413ded5969921f11e97d0da21.m3u8'
    video_url_list = read_m3u8(name)
    # 为了不频繁创建session，所以在外面创建好后传递给方法
    tasks = []
    async with aiohttp.ClientSession() as session:
        file_name = []
        for video_url in video_url_list:
            # download_video_1(video_url, headers)
            file_name.append("../resources/video/" + video_url.split("/")[-1])
            # tasks.append(asyncio.create_task(download_video(video_url, headers, session)))
            # break  # 测试用
        # await asyncio.wait(tasks)
        video_name = " ".join(file_name)
        merge_m3u8_ts(video_name)


if __name__ == '__main__':
    asyncio.run(mian())
    print('程序结束')
