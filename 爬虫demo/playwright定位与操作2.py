"""
playwright推荐以用户的视角去定位：
    get_by_xxxx()

playwright page.locator(tag).操作:
    inner_text()/all_inner_text() 获取定位元素的可见文本
    text_content()/all_text_content() 获取定位元素的文本内容，会忽略行内HTML标签
    get_attribute() 获取属性值
    inner_html() 获取HTML文本页面
    click()/dblclick 单击/双击
    hover() 悬停
    wait_for() 等待标签元素加载完成
    is_visible() 定位元素是否可见（存在）不会等待
    fill() 在文本框输入内容
    clear() 清空文本框内容
    input_value() 获取文本框内文本内容
    set_input_files([路径1, 路径2]) 上传文件
    check()/uncheck()/is_checked 选定（点选）/取消选定/是否为选定
    select_option([]|string|index|value|label) []空置，多选,隔开
    locator(tag | option:checked) 定位所有选中的项
    screenshot() 截屏标签内容

浏览器网页操作page.操作
    goto(url)/reload/go_back/go_forward 打开网址/重载/前进/后退
    content() 获取网页文本
    title() 标题
    set_viewport_size() 可见窗口大小
    bring_to_front() 将视窗切换到操作页
    screenshot(path, full_page=True) 截屏当前页面可见内容 full_page=True 整个网页
    close() 关闭当前标签页

iframe/frame(frameset)内嵌网页标签
    page.frame_locator() 定位到内嵌网页，生成内嵌网页对象FrameLocator，类同Page类

跳转新标签页Browser类对象操作
    context.pages[index] index按照网页打开时间顺序排序


"""
from playwright.sync_api import sync_playwright

p = sync_playwright().start()
context = p.chromium.launch(headless=False,
                            executable_path='C:/Users/Javen/AppData/Local/Google/Chrome/Application/chrome.exe').new_context()
# 设置默认等待元素时长（毫秒）
context.set_default_timeout(5000)
page = context.new_page()
page.goto('http://www.bilibili.com')
page.screenshot(path='/resource/test.png', full_page=True)
# print(page.content())


