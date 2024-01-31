"""
requests 发送请求模块
BeautifulSoup 解析http文本
xlwt 操作WPS
"""
import requests
from bs4 import BeautifulSoup
import xlwt

book = xlwt.Workbook(encoding='UTF-8', style_compression=0)
sheet = book.add_sheet('当当图书TOP500', cell_overwrite_ok=True)
sheet.write(0, 0, '排名')
sheet.write(0, 1, '书名')
sheet.write(0, 2, '作者')
sheet.write(0, 3, '评分')
sheet.write(0, 4, '图片')
n = 1


# 给指定的url发送请求，如果响应正常，返回http页面文本
def request_dangdang(url, i):
    haeders = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    url = url + str(i)
    try:
        response_dd = requests.get(url, headers=haeders)
        if response_dd.status_code == 200:
            return response_dd.text
    except requests.RequestException:
        print('请求异常')
        return None


# 将返回的页面解析获取需要的数据并写入表格。
def main(url):
    for i in range(1, 26):
        html = request_dangdang(url, i)
        soup = BeautifulSoup(html, "lxml")
        lists = soup.find(class_='bang_list clearfix bang_list_mode').find_all('li')
        global n
        for item in lists:
            try:
                item_index = item.find(class_='list_num').string
                item_name = item.find(class_='pic').find('img').get('title')
                autor = item.find(class_='publisher_info').find('a').get('title')
                item_star = item.find(class_='star').find('a').string
                item_pic = item.find(class_='pic').find('img').get('src')
                jigou = item.find(class_='publisher_info').find('a').string

                print("开始写入数据：", item_index[0:-1], item_name, item_pic, item_star, autor)
                sheet.write(n, 0, item_index)
                sheet.write(n, 1, item_name)
                sheet.write(n, 2, autor)
                sheet.write(n, 3, item_star)
                sheet.write(n, 4, item_pic)
                print("写入完成")
                n += 1
            except Exception:
                print("获取数据异常")
    book.save(u'当当图书TOP500.xlsx')


if __name__ == '__main__':
    url = 'http://bang.dangdang.com/books/fivestars/01.00.00.00.00.00-all-0-0-1-'
    main(url)
