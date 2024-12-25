import re
import subprocess
import time
import tool as commonTool 

from DrissionPage import ChromiumPage,ChromiumOptions
from DrissionPage.errors import *

def aq_check(page):
    aq_check = False

    html = page.html

    aq_check = re.findall(r'百度安全验证', html)
    if aq_check:
        print('触发百度安全验证,重新更新任务')
        page.wait(5)
        raise Exception("触发百度安全验证,重新更新任务")

    return False

try:
    page = None
    co = ChromiumOptions() #配置文件
    co.auto_port(False) #需要登录的平台
    page = ChromiumPage(co)  #页面对象
    page.set.window.max()
    page.set.load_mode.normal()
    tool = commonTool.Tool(page)

    keyword = '潮阳棉城肠粉'

    page.get("https://www.baidu.com/")
    page.wait(1)

    page.wait.eles_loaded('#kw')
    input =page.ele('#kw')

    tool.pyautoguiLocal(input)

    input.clear()
    input.focus()
    page.wait(1)
    input.input(keyword)
    page.wait(1)

    aq_check(page)

    keywordCount = len(keyword)
    cwc = ''
    cwcBox = page.s_ele('#normalSugSearchUl')
    if not cwcBox:
        keyWord = keyword
        while keywordCount:
            keyWord = keyWord[:-1]
            input.clear()
            input.focus()
            input.input(keyWord)
            page.wait(1.5)
            is_cwc = page.s_ele('#normalSugSearchUl')
            if is_cwc:
                cwc = page.s_ele('#normalSugSearchUl').child().text
                break
            else:
                keywordCount = keywordCount - 1
            if keywordCount <= 4:
                raise Exception("该关键词没有长尾词")
    else:
        cwc = page.s_ele('#normalSugSearchUl').child().text

    newkeyword = cwc +' - '+ keyword

    print(newkeyword)
    
    page.quit()
except (ElementNotFoundError,AlertExistsError,ContextLostError,ElementLostError,CDPError,
                PageDisconnectedError,JavaScriptError,NoRectError,BrowserConnectError,NoResourceError,
                CanNotClickError,GetDocumentError,WaitTimeoutError,WrongURLError,StorageError,CookieFormatError) as e:
    print(e,',3s后重连')
    time.sleep(2)

    try:
        if page is None:
            pass
        else:
            page.quit()
    except Exception as e:
        subprocess.run(["taskkill", "/F", "/IM", "chrome.exe"], check=True)

        time.sleep(3)

except Exception as e:
    print(e,',3s后重连')
    time.sleep(2)

    try:
        if page is None:
            pass
        else:
            page.quit()
    except Exception as e:
        subprocess.run(["taskkill", "/F", "/IM", "chrome.exe"], check=True)

    time.sleep(3)




            
