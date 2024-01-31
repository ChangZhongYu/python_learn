"""
css样式选择器中：
    #   ID
    .   class 如果有多个class，写法为.class1.class2
    tag 'tag'
    直接子元素 >
    后代元素 空格
    同级后续相邻 + 同级后续全部 ~   tag + span ; tag ~ span
    通用元素 tag（可缺省）[元素="值"] 值可缺省或部分（模糊匹配  *=包括 ，^= 开头 ，$=结尾） 多属性tag[][]
    组选择用,(逗号)隔开 .tag1, .tag2 
    locator 查找的内容如果是多个，则链式调用操作方法会报错
    locator API https://playwright.dev/python/docs/api/class-locator
"""

from playwright.sync_api import sync_playwright

# 启动playwright
p = sync_playwright().start()
# 创建浏览器对象
browser = p.chromium.launch(headless=False,
                            executable_path='C:/Users/Javen/AppData/Local/Google/Chrome/Application/chrome.exe')
browser_context = browser.new_context()

# 创建页面对象
page = browser_context.new_page()

page.goto("https://www.bilibili.com")
page.wait_for_timeout(2000)
print(page.title())

page.locator('.nav-search-input').fill('4k')
page.locator('.nav-search-btn').click()
page.wait_for_timeout(5000)
next_Page = browser_context.pages[1]
div_list = next_Page.locator('.bili-video-card').all()
n = 1
for div in div_list:
    print(n, div.locator('h3').get_attribute('title'))
    n += 1

next_button = page.locator('.vui_pagenation--btns button:nth-last-child(1)')
next_button.click()
print("*" * 30, "下一页", "*" * 30)
page.wait_for_timeout(5000)

div_list2 = next_Page.locator('.bili-video-card').all()
for div in div_list2:
    print(n, div.locator('h3').get_attribute('title'))
    n += 1

# 关闭
browser_context.close()
browser.close()
p.stop()
