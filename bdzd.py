import random
import re
import tool as commonTool 

from DrissionPage import ChromiumPage,ChromiumOptions
from DrissionPage.errors import *
from urllib.parse import urlparse


def aq_check(page):
    aq_check = False
    html = page.html

    aq_check = re.findall(r'百度安全验证', html)
    if aq_check:
        print('触发百度安全验证,重新更新任务')
        page.wait(5)
        raise Exception("触发百度安全验证,重新更新任务")
    

    return True
        


page = None
co = ChromiumOptions() #配置文件
co.auto_port(False) #需要登录的平台
page = ChromiumPage(co)  #页面对象
page.set.window.max()
tool = commonTool.Tool(page)
keyword = '棉城美食'
        
page.set.load_mode.normal()

page.get("https://www.baidu.com/")
page.wait(1)

page.get("https://zhidao.baidu.com/search?lm=0&rn=10&pn=0&fr=search&dyTabStr=null&word="+keyword) 
aq_check(page)
page.wait(1)

keywordCount = len(keyword)
keyWord = keyword
while keywordCount:
    listBox = page.s_ele('#wgt-list')
    if listBox:
        list = page.ele('#wgt-list').eles('.dl')
        page.wait(1)
        if len(list) == 0:
            keyWord = keyWord[:-1]
            page.get("https://zhidao.baidu.com/search?lm=0&rn=10&pn=0&fr=search&dyTabStr=null&word="+keyWord) 
            keywordCount = keywordCount - 1
        else:
            break
    else:   
        keyWord = keyWord[:-1]
        page.get("https://zhidao.baidu.com/search?lm=0&rn=10&pn=0&fr=search&dyTabStr=null&word="+keyWord) 
        keywordCount = keywordCount - 1
    if keywordCount <= 4:
        print('百度搜索结果为空')
        page.wait(5)
        raise Exception("百度搜索结果为空，跳过该任务1")
    
index11 = 4
while index11: 

    list = random.sample(list, 1)

    for item in list:
        domain = urlparse(item.child().child().link).netloc.split(':')[0]
        # print(domain)
        # print(list)
        if domain == 'zhidao.baidu.com':
            
            page.wait(1)
            tool.pyautoguiLocal(item)
            page.wait(1)

            new_tab = item.child().child().click.for_new_tab()
            new_tab.wait.load_start()  
            tool = commonTool.Tool(new_tab)

            ask_title = '*' + new_tab.s_ele('.ask-title').text + '*'
            answer_list = new_tab.s_eles('.rich-content-container rich-text-')
            target_index = None
            for index,item in enumerate(answer_list):
                res = item.s_ele('.wgt-replyer-all-follow-box')
                if res:
                    target_index = index
                    break
                    
            if target_index is not None:
                answer_list = answer_list[index]
            else:
                answer_list = random.sample(answer_list, 1)[0]
                
            answer_text = answer_list.text[:300]
            
            print(ask_title)
            print(answer_text)

            new_tab.wait(2)
            new_tab.close()
            aq_check(page)
            page.quit()
                
            index11 = 0
        else:
            index11 = index11 -1
            if index11 == 1:
                raise Exception("百度搜索结果为空，跳过该任务2")