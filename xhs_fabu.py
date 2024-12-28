import os              
import subprocess
import sys
import time  
import pyautogui
import tool as commonTool 

from DrissionPage import ChromiumPage,ChromiumOptions
from DrissionPage.errors import *

pyautogui.FAILSAFE = False

tmp_dir = './tmp'
xhsUrl = 'https://creator.xiaohongshu.com/new/home'
# apiDoname = 'http://fwz.sttyyy.com/'
img_dir = './img'
entries = os.listdir(img_dir)
file_list = [entry for entry in entries if os.path.isfile(os.path.join(img_dir, entry))]
for index,file in enumerate(file_list):
    file_list[index] = os.path.join(img_dir, file)
    
title = '测试标题1'
content = '测试内容1'

while True:
    try:
        
        co = ChromiumOptions() #配置文件
        co.auto_port(False) #需要登录的平台
        # co.set_user_data_path(r'C:\Users\Administrator\AppData\Local\Google\Chrome\xhs_'+user)
        page = ChromiumPage(co)  #页面对象
        tool = commonTool.Tool(page)       
        
        page.set.load_mode.normal()
        page.set.window.max()
        page.get(xhsUrl)
        page.wait.doc_loaded()
        
        loginBox = page.s_ele(".login-box-container")
        if loginBox:
            # print('未登录状态，正在扫码登录')
            raise Exception('未登录状态，请扫码登录')
            
        page.wait.eles_loaded('.group-list')
        conBtn =page.ele('.group-list')
        if conBtn:
            conBtn = conBtn.ele('.publish-card')
        page.wait(1)
        tool.pyautoguiLocal(conBtn)
        page.wait(1)
        
        conBtn.click.to_upload(file_list)
        
        
        page.wait.eles_loaded('.d-input --color-text-title --color-bg-fill')
        titleinput =page.ele('.d-input --color-text-title --color-bg-fill')
        tool.pyautoguiLocal(titleinput)
        page.wait(1)
        titleinput.focus()
        page.wait(1)
        titleinput.input(title)
        page.wait(1)
        
        
        page.wait.eles_loaded('.ql-editor ql-blank')
        coninput =page.ele('.ql-editor ql-blank')
        tool.pyautoguiLocal(coninput)
        page.wait(1)
        coninput.focus()
        page.wait(1)
        coninput.input(content)
        page.wait(1)
        
        page.wait.eles_loaded('.submit')
        sendBtn =page.ele('.submit')
        tool.pyautoguiLocal(sendBtn)
        page.wait(1)
        # sendBtn.click(by_js=None)
        
        sys.exit(0)
          

    except (ElementNotFoundError,AlertExistsError,ContextLostError,ElementLostError,CDPError,
                    PageDisconnectedError,JavaScriptError,NoRectError,BrowserConnectError,NoResourceError,
                    CanNotClickError,GetDocumentError,WaitTimeoutError,WrongURLError,StorageError,CookieFormatError) as e:
        print(e,',3s后重连')
        time.sleep(2)

        try:
            if page is None:
                pass
            else:
                pass
                # page.quit()
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
                pass
                # page.quit()
        except Exception as e:
            subprocess.run(["taskkill", "/F", "/IM", "chrome.exe"], check=True)

        time.sleep(3)
