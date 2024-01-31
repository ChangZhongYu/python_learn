from playwright.sync_api import sync_playwright
'''
    playwright具有特殊功能：跟踪（tracing）

    playwright.exe codegen
    自帶的助手工具，可以根据浏览器操作生成简单的代码
'''
# 启动playwringht进程
p = sync_playwright().start()

# 创建浏览器对象 headless 控制浏览器是否后台运行，默认为后台,executable_paths 使用浏览器客户端
browser = p.chromium.launch(headless=False,
                            executable_path='C:/Users/Javen/AppData/Local/Google/Chrome/Application/chrome.exe')
# 启用跟踪
browser_context = browser.new_context()
browser_context.tracing.start(snapshots=True, sources=True, screenshots=True)

# 创建页面对象访问百度页面
page = browser_context.new_page()
page.goto('http://www.baidu.com')
print(page.title())

page.locator('#kw').fill('通讯')
page.locator('#su').click()

# 等待(毫秒)
page.wait_for_timeout(2000)

# 跟踪停止(日志保存在给定的路径)使用官方的网址或执行命令 playwright show-trace trace.zip打开
browser_context.tracing.stop(path='resource/trace.zip')

# 关闭浏览器
browser.close()
# 关闭进程
p.stop()
