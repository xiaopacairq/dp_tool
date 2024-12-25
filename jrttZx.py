import random
import re
import tool as commonTool 
from DrissionPage import ChromiumPage,ChromiumOptions
from DrissionPage.errors import *


def aq_check(page):
    aq_check = False
    html = page.html

    aq_check = re.findall(r'请完成下列验证(.*?)', html)
    if aq_check:
        print('触发今日头条安全验证,重新更新任务')
        page.wait(5)
        raise Exception("触发今日头条安全验证,重新更新任务")

    return True


page = None
co = ChromiumOptions() #配置文件
co.auto_port(False) #需要登录的平台
page = ChromiumPage(co)  #页面对象
page.set.window.max()
tool = commonTool.Tool(page)       
keyword = '棉城美食'               
page.set.load_mode.none()
page.get("https://so.toutiao.com/search?dvpf=pc&source=search_subtab_switch&keyword=" + keyword + "&pd=information") 

keywordCount = len(keyword)
keyWord = keyword
while keywordCount:

    listBox = page.s_ele('.s-result-list')
    if listBox:
        list = page.ele('.s-result-list').eles('.result-content')[:-2]

        if len(list) == 0 :
            keyWord = keyWord[:-1]
            page.get("https://so.toutiao.com/search?dvpf=pc&source=search_subtab_switch&keyword=" + keyWord + "&pd=information")
            keywordCount = keywordCount - 1
        else:
            break
    else:
        keyWord = keyWord[:-1]
        page.get("https://so.toutiao.com/search?dvpf=pc&source=search_subtab_switch&keyword=" + keyWord + "&pd=information") 
        keywordCount = keywordCount - 1
    
    if keywordCount <= 4:
        page.wait(5)
        raise Exception("今日头条结果为空，跳过该任务")
            
index = len(list)
while index:
    newlist = random.sample(list, 1)
        
    for res in newlist:    
        tool.to_scroll_target_ele(res)
        page.wait(1)
        tool.pyautoguiLocal(res)
        page.wait(1)

        new_tab = res.ele('tag:a').click.for_new_tab()
        tool = commonTool.Tool(new_tab)
        
        new_tab.wait.load_start()
        # if check.check(new_tab,self.id,self.task_id).aq_check():raise Exception("触发安全警告")
        new_tab.wait.eles_loaded('.article-content')
        
        ask_title = new_tab.s_ele('.article-content').s_ele('tag:h1').text
        ask_title = '*'+ask_title+'*'
        answer = new_tab.s_ele('.article-content').s_ele('.syl-article-base tt-article-content syl-page-article syl-device-pc')
        if answer:
            answer_list=answer.text
            answer_list = answer_list.split('\n')[:6]
            answer_list = '\n'.join(answer_list)
            index = 0
            break
        else:
            print(index)
            index = index - 1
            new_tab.close()
        if index == 0:
            raise Exception("今日头条结果为空，跳过该任务")
    print(ask_title)
    print(answer_list)
    new_tab.wait(2)
    new_tab.close()
    page.quit()

    