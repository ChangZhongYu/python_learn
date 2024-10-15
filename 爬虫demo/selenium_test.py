"""
    selenium: 自动化测试工具
    环境搭建：
        pip install selenium
        下载对应浏览器的驱动，并将驱动放在python解释器所在的文件夹。
    对于加密数据，通过requests请求返回时数据形式很复杂，而通过浏览器自动化测试则可以直接获取数据，同时也可以防止部分反扒手段

"""
import time

# 导包
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
# 模拟键盘操作
from selenium.webdriver.common.keys import Keys
# 下拉列表操作包
from selenium.webdriver.support.select import Select
# 配置包
from selenium.webdriver.chrome.options import Options

# 设置配置参数
opt = Options()
# 静默运行（无窗口）
opt.add_argument("--headless")
opt.add_argument("--disbale-gpu")


# 创建浏览器对象
web = Chrome(options=opt)
# 打开url
web.get("https://bilibili.com")

# 模拟等待加载
time.sleep(2)

# 获取JS等解析后的页面，即所见页面
page = web.page_source
print(page)

# # 获取元素对象
# el = web.find_element(By.XPATH, '//*[@id="i_cecream"]/div[2]/div[1]/div[3]/div[1]/a[2]')
# # 点击事件
# el.click()

# 定位到搜索框
el = web.find_element(By.XPATH, '//*[@id="nav-searchform"]/div[1]/input')
# 录入检索内容后回车
el.send_keys("4k", Keys.ENTER)

# 窗口切换，跳转到最后一个窗口
web.switch_to.window(web.window_handles[-1])

# 模拟等待加载
time.sleep(5)

# 关闭登录弹窗
# e_1 = web.find_element(By.XPATH, '/html/body/div[6]/div/div/div[1]')
# e_1.click()

# 关闭当前窗口
web.close()

# 视角跳转回第一个窗口
web.switch_to.window(web.window_handles[-1])

# 处理iframe(内窗)，先定位到标签，再切换视窗到内窗，之后再获取数据
# 切换内窗
# web.switch_to.frame(iframe)
# 切回主窗
# web.switch_to.default_content()

# 下拉列表处理，定位标签后包装为下拉对象
# sel_el = web.find_element(By.XPATH, '//......')
# sel = Select(sel_el)
# 切换标签通常有三种方式
# sel.select_by_index() # 索引
# sel.select_by_value() # 值
# sel.select_by_visible_text() #文本
# for i in range(len(sel.options)):
#     # 按索引选择下拉选项
#     sel.select_by_index(i)
#     # 模拟等待加载
#     time.sleep(5)
#     # ......