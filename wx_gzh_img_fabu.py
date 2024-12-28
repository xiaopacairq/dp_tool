import os              
import subprocess
import sys
import time  
import pyautogui
import requests
import tool as commonTool 
from DrissionPage.common import Actions
from DrissionPage.common import Keys

from DrissionPage import ChromiumPage,ChromiumOptions

from DrissionPage.errors import *

pyautogui.FAILSAFE = False


wxUrl = 'https://mp.weixin.qq.com/'
img_dir = './img'
entries = os.listdir(img_dir)
file_list = [entry for entry in entries if os.path.isfile(os.path.join(img_dir, entry))]

for index,file in enumerate(file_list):
    file_list[index] = os.path.join(img_dir, file)
    
while True:
    try:        
        
        co = ChromiumOptions() #配置文件
        page = ChromiumPage(co)  #页面对象
        co.auto_port(False) #需要登录的平台
        page.set.load_mode.normal()
        page.set.window.max()
        page.get(wxUrl) 
        tool = commonTool.Tool(page)       
        
        page.wait.eles_loaded('.new-creation__menu-item')
        btnList =page.eles('.new-creation__menu-item')
        conBtn = btnList[2]
        page.wait(1)
        tool.pyautoguiLocal(conBtn)
        page.wait(1)
        tool.pyautoguiLocal(conBtn)
        page.wait(1)
        new_tab = conBtn.click.for_new_tab()
        new_tab.wait.load_start()
        tool = commonTool.Tool(new_tab)       
                        
        new_tab.wait.eles_loaded('.pop-opr__group pop-opr__group-select-image')
        add_img_btn = new_tab.ele('.pop-opr__group pop-opr__group-select-image')
        tool.to_scroll_target_ele(add_img_btn)
        tool.pyautoguiLocal(add_img_btn)
        new_tab.wait(1)
        
        new_tab.wait.eles_loaded('.weui-desktop-upload pop-opr__item')
        upload_img = new_tab.ele('.weui-desktop-upload pop-opr__item')
        tool.to_scroll_target_ele(upload_img)
        tool.pyautoguiLocal(upload_img)
        new_tab.wait(1)
        
        new_tab.set.upload_files(file_list)
        # 点击触发文件选择框按钮
        upload_img.click()
        # 等待路径填入
        new_tab.wait.upload_paths_inputted()

        new_tab.wait.eles_loaded('#title')
        title_input = new_tab.ele('#title')
        tool.pyautoguiLocal(title_input)
        new_tab.wait(1)
        title_input.clear()
        new_tab.wait(1)
        title_input.focus()
        new_tab.wait(1)
        title_input.input('标题测试1')
        new_tab.wait(1)
        
        new_tab.wait.eles_loaded('#guide_words_main')
        art_input = new_tab.ele('#guide_words_main')
        tool.pyautoguiLocal(art_input)
        new_tab.wait(1)
        art_input.clear()
        new_tab.wait(1)
        art_input.focus()
        new_tab.wait(1)
        art_input.input('内容测试1')
        new_tab.wait(1)
            
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
