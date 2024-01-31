import requests
from bs4 import BeautifulSoup

URL = 'https://bz.zzzmh.cn/index'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}
requests.get(URL, headers=headers)
