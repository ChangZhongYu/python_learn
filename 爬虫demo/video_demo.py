# https:\/\/v.cdnlz3.com\/20240126\/22925_ab576153\/index.m3u8
# https://v.cdnlz3.com/20240126/22925_ab576153/index.m3u8
"""
练习抓取视频并合并

"""
import requests
import re


# 获取视频地址
# 获取m3u8文件地址
# 下载m3u8文件
# 解析m3u8文件获取地址
# 下载ts文件
# 解密合并视频


# 通过给定视频连接，获取m3u8的初见地址
def get_m3u8_address_1(url, header):
    res_html = requests.get(url, headers=header)
    print(res_html.text)
    obj = re.compile(r"let obj =.*?:(?P<url>.*?)from", re.S)
    m3u8_url_1 = obj.search(res_html.text).group(url)
    print(m3u8_url_1)


def main():
    pass


if __name__ == '__main__':
    html_url = "https://www.yingshi.tv/vod/play/id/200851/sid/1/nid/1.html"
    headers = {
        'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
    }
    get_m3u8_address_1(html_url, headers)
