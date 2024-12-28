import subprocess
import sys
import time  
from DrissionPage.common import Actions
from DrissionPage.common import Keys

from DrissionPage import ChromiumPage,ChromiumOptions
from DrissionPage.errors import *

tmp_dir = './tmp'
config_dir = './configs.ini'
wxUrl = 'https://mp.weixin.qq.com/'
apiDoname = 'http://fwz.sttyyy.com/'

while True:
    try:
        page = None
        wxyyurlfile = 'wxyyurl.txt'
        with open(wxyyurlfile, 'r', encoding='utf-8') as file:
            url = file.read()
        
        co = ChromiumOptions() #配置文件
        # co.set_user_data_path(r'C:\Users\Administrator\AppData\Local\Google\Chrome\wx_gzh_'+user)
        co.auto_port(False) #需要登录的平台
        page = ChromiumPage(co)  #页面对象
   
        con = page.s_eles('#answer_text_id')
        if con:
            conlen = len(con)
            # print(conlen)
            if conlen > 10:
                with open(wxyyurlfile, 'w', encoding='utf-8') as file:
                    file.write("https://yiyan.baidu.com/")
            
        
        page.set.load_mode.normal()
        page.set.window.max()
        page.get(url)
        
        page.wait.doc_loaded()
        
        login = page.s_ele('text:登录')
        if login:
            raise Exception('页面没有登录')
            # page.wait(30)
        
        ac = Actions(page)
        
        adcolse = page.s_ele('.ant-modal-close')
        if adcolse:
            adcolse = page.ele('.ant-modal-close')
            ac.move_to(adcolse).click()
        
        page.wait.ele_displayed('.^yc-editor-container')
        input = page.ele('.^yc-editor-container')
        page.wait(1)
        ac.move_to(input)
        page.wait(1)
        # ac.click().input('宫颈疾病怎么治疗，帮我上今日头条搜索一下，给出结果，要条理清晰')
        ac.click().type((Keys.LEFT, '汕头潮阳棉城美食'))
        page.wait(1,3)
        ac.click().type(', 有哪些?')
        page.wait(1,3)
        ac.click().type('\n')
        page.wait(10)
        
        
        page.wait.eles_loaded('.custom-html md-stream md-stream-desktop')
        
        while True:
            gc_con = page.ele('.custom-html md-stream md-stream-desktop')
            if gc_con:
                page.wait(2)
            else:
                break
        
        
        con = page.ele('#answer_text_id')
        if con:
            conhtml = con.text
            print(conhtml)
                
            with open(wxyyurlfile, 'w', encoding='utf-8') as file:
                file.write(page.url)
        else:
            print('没有结果')
        page.quit()
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
                # page.quit()
                pass
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
                # page.quit()
                pass
        except Exception as e:
            subprocess.run(["taskkill", "/F", "/IM", "chrome.exe"], check=True)

        time.sleep(3)
