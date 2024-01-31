import xlwt
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

driver = webdriver.Chrome()
# 设置窗口尺寸
driver.set_window_size(640, 320)
# 设置等待元素操作
wait = WebDriverWait(driver, 10)

book = xlwt.Workbook(encoding='UTF-8', style_compression=0)
sheet = book.add_sheet('B站python视屏', cell_overwrite_ok=True)
sheet.write(0, 0, '标题')
sheet.write(0, 1, 'UP')
sheet.write(0, 2, '播放量')
sheet.write(0, 3, '弹幕数')
sheet.write(0, 4, '时长')
sheet.write(0, 5, '上传时间')
sheet.write(0, 6, '链接')
n = 1


# 获取给定页面的数据后保存到本地xlsx
def get_source():
    # 获取页面内容
    html_page = driver.page_source
    # 解析页面
    soup_page = BeautifulSoup(html_page, 'lxml')
    # lists = soup_page.find_all(class_='bili-video-card')
    lists = soup_page.find_all('div', {'class': 'bili-video-card__wrap'})
    global n

    for li in lists:
        # 值得注意的是，通过find查找返回的值仍然是<class 'bs4.element.Tag'>
        try:
            link = li.find('a')['href']  # 也可以透过get('href')获取属性的值
            # class_是为了区分python中的class的写法，其它同理,.string获取内容
            title = li.find('h3').get('title')
            tag = li.findAll('span', {'class': 'bili-video-card__stats--item'})
            # 不一定有弹幕数据
            bofangliang = tag[0].find('span').string
            if len(tag) != 1:
                danmu_count = tag[1].find('span').string
            else:
                danmu_count = 0
            # 不一定有时长
            timelong = li.find('span', {'class': "bili-video-card__stats__duration"}).string
            up_bilibili = li.find('span', {'class': "bili-video-card__info--author"}).string
            # 不一定有上传时间
            date = li.find('span', {'class': "bili-video-card__info--date"}).string
            print('正在抓取：', title)
            sheet.write(n, 0, title)
            sheet.write(n, 1, up_bilibili)
            sheet.write(n, 2, bofangliang)
            sheet.write(n, 3, danmu_count)
            sheet.write(n, 4, timelong)
            sheet.write(n, 5, date)
            sheet.write(n, 6, link)
            n += 1
            print('*' * 60)
        except AttributeError:
            print('节点数据集异常')


def search(url, content):
    # 访问URL，搜索conten，提交
    driver.get(url)
    input_souso = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="nav-searchform"]/div[1]/input')))
    input_souso.send_keys(content)
    input_souso.submit()

    try:
        # 搜索执行后，跳转新窗口，获取所有窗口
        all_handles = driver.window_handles

        # 跳转到第二个页面，等待指定元素加载完成，获取页面
        driver.switch_to.window(all_handles[1])
        wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="i_cecream"]/div/div[2]/div[2]/div/div/div/div[3]')))

        # 获取页面内容到后写入本地
        get_source()

        # 获取检索内容的总页面数
        total = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="i_cecream"]/div/div[2]/div[2]/div/div/div/div[4]/div/div/button[9]')))
        page_total = total.text

        return page_total
    except TimeoutException:
        return None


def nextPage(page):
    try:
        next_button = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="i_cecream"]/div/div[2]/div[2]/div/div/div/div[4]/div/div/button[10]')))
        next_button.click()

        # 猜测是等页码元素加载完成
        wait.until(EC.text_to_be_present_in_element(
            (By.XPATH, '//*[@id="i_cecream"]/div/div[2]/div[2]/div/div/div/div[4]/div/div/button[2]',), str(page)))

        print("开始获取数据，页面：", page)
        get_source()
    except TimeoutException:
        return nextPage(page)


def mian():
    url = 'https://www.bilibili.com/'
    content = 'drissionpage'
    try:
        total = search(url, content)
        # print(int(total))

        # for i in range(2, int(total) + 1):
        #     print('跳转页码：', i)
        #     nextPage(i)
    finally:
        driver.quit()


if __name__ == '__main__':
    mian()
    book.save(u'B站drissionpage视频.xlsx')
