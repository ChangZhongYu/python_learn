"""
    抓取视频案例
"""
import concurrent

import requests
import re
import json
# import asyncio
# import aiohttp
import aiofiles
import logging
from yarl import URL
from concurrent.futures import ThreadPoolExecutor
import time
from mytool.MyFunction import MyFunction
import subprocess
import csv
import codecs


# 获取m3u8文件地址
# 下载m3u8文件，读取文件获取视频片段地址
# 采用异步方式下载视频片段
# 合并视频

# 获取包含该视频的所有m3u8的字典
def get_m3u8_url(url, headers):
    name = '-'.join(re.compile(r'\d+').findall(url))
    # 以下代码是防止debug频繁访问被封，基本的逻辑是record.csv中记录访问过的网址和时间，
    # 首次访问或者上次访问时间较长时则发起新的请求，否则读取上次请求的html页面
    read_file = codecs.open("../resources/record.csv", encoding="utf-8")
    line_dirc = csv.reader(read_file)
    dics = {}
    for line in line_dirc:
        if not line:
            continue
        dics.update({line[0]: line[1]})
    print(dics)
    read_file.close()
    # 首次访问或者上次访问以过5分钟以上则重新发送请求，将页面写到本地，并在record.csv记录，否注解读取本地html
    if url not in dics.keys() or round(int(time.time() * 1000)) - int(dics[url]) > 300 * 1000:
        res_html = requests.get(url, headers=headers)
        res_html.encoding = "utf-8"
        # 这里将请求页面写到本地，防止debug频繁访问被封 str>bytes encode(); bytes>str  decode()
        MyFunction.file_writing(f"../resources/{name}.html", res_html.text.encode())
        re_obj = re.compile(r'let obj =(?P<m3u8>.*?);', re.S)
        m3u8_url_dirc = json.loads(re_obj.findall(res_html.text)[0])
        # 将本次访问的URL和时间戳记录在record.csv
        writer_fiel = open("../resources/record.csv", "a", encoding="utf-8", newline="")
        writer_obj = csv.writer(writer_fiel)
        writer_obj.writerow([url, str(round(int(time.time() * 1000)))])
        writer_fiel.close()
        return m3u8_url_dirc
    else:
        with open(f"../resources/{name}.html", "r", encoding="utf-8") as r:
            re_obj = re.compile(r'let obj =(?P<m3u8>.*?);', re.S)
            m3u8_url_dirc = json.loads(re_obj.findall(r.read())[0])
        return m3u8_url_dirc


# 下载m3u8文件
def download_m3u8(url, path, headers):
    res_m3u8 = requests.get(url, headers=headers)
    name = path + url.split('/')[-1]
    with open(name, "wb") as f:
        f.write(res_m3u8.content)
    return name


# 读取m3u8文件获取视频片段地址
def read_m3u8(name, url, tspath, headers):
    video_url_list = []
    with open(name, mode='r', encoding="utf-8") as f:
        for line in f.readlines():
            line = line.strip()
            # 如果获取的文件中有.m3u8结尾，说明做了跳转。则需要再次处理
            if line.endswith(".m3u8"):
                # 字符串是不可变的
                url = url.replace('index.m3u8', line)
                print(url)
                m3u8_name = download_m3u8(url, tspath, headers)
                return read_m3u8(m3u8_name, url, tspath, headers)
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


def download_video_1(m3u8_url, file_path, file_name, headers):
    # 可能存在不可见的空白符
    m3u8_url = m3u8_url.strip()
    res_video = requests.get(m3u8_url, headers=headers)
    print(res_video.status_code)
    name = file_path + file_name + "." + m3u8_url.split('.')[-1]
    with open(name, mode='wb') as f:
        f.write(res_video.content)
    print(f'{name}下载完成')
    res_video.close()


def merge_m3u8_ts(inpath, outpath):
    dos = f'ffmpeg -f concat -i {inpath} -c copy {outpath}{str(round(int(time.time() * 1000)))}.mp4'
    dos_cmd = dos.replace("'", "")
    out_path = f'{outpath}{str(round(int(time.time() * 1000)))}.mp4'
    ffmpeg_command = [
        'ffmpeg',  # FFmpeg可执行文件名，如果已加入环境变量则可以直接使用
        '-i', inpath,  # 输入部分，指定待合并的ts文件列表
        '-c', 'copy',  # 复制音视频流，不进行转码（假设源文件编码一致）
        '-bsf:a', 'aac_adtstoasc',  # 对于某些AAC音频流，需要添加此选项才能正确合并
        out_path  # 输出文件路径
    ]
    print(dos_cmd)
    if subprocess.run(dos_cmd, text=True).returncode == 0:
        print("TS文件合并成功")
    else:
        print("TS文件合并过程中发生错误！")


# 程序入口
def mian():
    # 开启日志
    logging.basicConfig(level=logging.INFO)
    # 配置参数
    config = MyFunction.read_file_config()
    # 调用方法获取包含该视频的所有m3u8的字典
    m3u8_url_dirc = get_m3u8_url(config.html_url, config.headers)

    # 遍历字典，获取到每个视频的所有ts文件下载地址
    videos_url_list = []
    flag = 0
    for key in m3u8_url_dirc.keys():
        # 获取该视频的所有m3u8文件地址
        m3u8_url = m3u8_url_dirc[key]["url"]
        # 掉用方法传入url下载m3u8文件并返回m3u8文件名
        m3u8_name = download_m3u8(m3u8_url, config.ts_path, config.headers)
        # 调用方法，传入m3u8文件名，读取m3u8文件，获取该视屏所有切片的地址，存入list
        videos_url_list.append(read_m3u8(m3u8_name, m3u8_url, config.ts_path, config.headers))
        flag += 1
        if flag < 2:
            break

    # tasks = []    #存储异步任务
    # 为了不频繁创建session，所以在外面创建好后传递给请求
    # async with aiohttp.ClientSession() as session:

    config.headers.update({'Referer': 'https://www.yingshi.tv/', 'Origin': 'https://www.yingshi.tv'})
    tag = 1
    with ThreadPoolExecutor(16) as thread_pool:
        for video_url_list in videos_url_list:
            with open(config.input_path + f"input{tag}.txt", mode='w') as f:
                tag2 = 1
                file_names = []
                for video_url in video_url_list:
                    file_name = f"{str(tag)}-{str(tag2)}"
                    file_names.append(file_name)
                    # 将所有的切片文件名拼接，后续用于合并视频
                    f.write(f"file '{config.relative_path}" + file_name + "." + video_url.split(".")[-1] + "'" + "\n")
                    # 单线程下载
                    # download_video_1(video_url, headers=config.headers)
                    # 多线程同步下载
                    print(video_url)
                    thread_pool.submit(download_video_1, video_url, config.ts_path, file_name, config.headers)
                    tag2 += 1
                    # break  # 测试下载一个切片
                    # 异步下载
                    # tasks.append(asyncio.create_task(download_video(video_url, headers, session)))
                    # await asyncio.wait(tasks)
                # 等待所有子线程完成任务
                thread_pool.shutdown(True)
                merge_m3u8_ts(config.input_path + f"input{tag}.txt", config.output_path)
                tag += 1
                # if tag > 2:
                #     break


if __name__ == '__main__':
    print(f'开始时间：{time.strftime('%X')}')
    mian()

    # config = MyFunction.read_file_config()
    # m3u8_url_dirc = get_m3u8_url(config.html_url, config.headers)
    # for key in m3u8_url_dirc.keys():
    #     print(m3u8_url_dirc[key])

    # ffmpeg_command = 'ffmpeg -f concat -i C:/Project/PycharmProjects/Python_Instance/resources/input1.txt -c copy C:/Project/PycharmProjects/Python_Instance/resources/video2/1707238312086.mp4'
    #
    # if subprocess.run(ffmpeg_command, text=True).returncode == 0:
    #     print("TS文件合并成功")
    # else:
    #     print("TS文件合并过程中发生错误！")

    print('程序结束')
    print(f'开始时间：{time.strftime('%X')}')
