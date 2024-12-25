import json
import os
import sys
import pyperclip
import re
import tool as commonTool 
from DrissionPage import ChromiumPage,ChromiumOptions
from DrissionPage.errors import *
from DrissionPage.common import Actions
from DrissionPage.common import Keys

def aq_check(page):
    aq_check = False
    html = page.html

    aq_check = re.findall(r'安全检测', html)
    if aq_check:
        print('触发kimiAI验证,重新更新任务')
        page.wait(5)
        raise Exception("触发kimiAI验证")
    
    return True
    
page = None
co = ChromiumOptions() #配置文件
co.auto_port(False) #需要登录的平台
page = ChromiumPage(co)  #页面对象
page.set.window.max()
tool = commonTool.Tool(page)       
keyword = '棉城美食'               
page.set.load_mode.none()

with open('kimi.txt', 'r', encoding='utf-8') as file:
    zhilin = file.read()

orl_con = """
 社保怎么自己缴费补缴到60周岁 - 社保怎么自己缴费补缴
/uploads/keyimg/20241219/92a5e02fdbc677b8aa38c355d6b1eb3a13.jpg
/uploads/keyimg/20241219/9b6a532f6f5485e23b58758f0d2ef04f11.jpg

*个人是否可以补交社保*
个人可以补交社保，具体方法如下：
1、可以到当地的社会劳动保障局申请补缴；
2、如果之前没有交过的话，无法往前补交的，补交只存在于开养老账户后欠交的时段。另外如果是补交，滞纳金是一定会有的，按同期银行一年期定期存款利率计算。
个人补缴社保流程：
1、只能缴纳养老金和医疗保险这两部分。直接到户口所在地社保管理部门通常在乡镇社保部门（社区居委会）或县社保局提出申请办理社保；
2、携带个人身份证以及复印件、近期免冠一寸照片两张、保费和申请书等资料，提出申请即可。
法律依据：《中华人民共和国社会保险法》第六十二条
用人单位未按规定申报应当缴纳的社会保险费数额的，按照该单位上月缴费额的百分之一百一十确定
*我要怎么补缴中断了一年半的养老保险？（个人可以补吗？）
"""
if zhilin == '':
    raise Exception('AI指令外空，请在后台配置')
tool = commonTool.Tool(page)

page.set.load_mode.normal()
page.get("https://kimi.moonshot.cn/") 
page.wait.doc_loaded()
page.wait(1)

click_index = 5
while click_index:
    is_login = page.s_ele('.^loginLayout___')
    if is_login:
        raise Exception('AI没有登录！')
    chat = page.s_ele('.pop-content')
    if chat:
        print('指令输入成功')
        click_index = 0
        break
    else:
        click_index = click_index - 1
        page.wait.eles_loaded('.editor___KShcc editor___DSPKC')
        page.wait(2)
        input = page.ele('.editor___KShcc editor___DSPKC')
        tool.pyautoguiLocal(input)
        page.wait(1)
        ac = Actions(page)
        input.input(zhilin)
        page.wait(1)
        page.wait.eles_loaded('.^sendButton___')
        sendbtn = page.ele('.^sendButton___')
        sendbtn.click.multi(3)
        page.wait(5)
    if click_index == 0:
        raise Exception('对话失效') 

while True:
    page.wait.eles_loaded('.pop-content')
    chatList = page.eles('.pop-content')
    chat = chatList[-1]
    chatsize = chat.rect.size
    page.wait(5)
    if chatsize == chat.rect.size:
        print(chat.text)
        if chat.text == '':
            print('正在对话')
        else:
            print('对话结束')
            break
    else:
        print('正在对话')

click_index = 5
while click_index:
    page.wait.eles_loaded('.pop-content')
    chatList = page.eles('.pop-content')
    chatCount = len(chatList)
    if chatCount > 4:
        click_index = 0
        break
    else:
        click_index = click_index - 1
        page.wait.eles_loaded('.editor___KShcc editor___DSPKC')
        page.wait(2)
        input = page.ele('.editor___KShcc editor___DSPKC')
        tool.pyautoguiLocal(input)
        page.wait(1)
        input.clear()
        page.wait(1)
        ac = Actions(page)
        con = orl_con
        input.input(con)
        page.wait(2)
        page.wait.eles_loaded('.^sendButton___')
        sendbtn = page.ele('.^sendButton___')
        sendbtn.click.multi(3)
        page.wait(5)
    if click_index == 0:
        raise Exception('对话失效') 


while True:
    page.wait.eles_loaded('.pop-content')
    chatList = page.eles('.pop-content')
    chat = chatList[-1]
    chatCount = len(chatList)
    if chatCount == 5:
        if chat.text == '':
            print('正在对话')
        else:
            print('对话结束')
            break
    else:
        page.wait(3)


while True:
    page.wait.eles_loaded('.pop-content')
    chatList = page.eles('.pop-content')
    chat = chatList[-1]
    chatsize = chat.rect.size
    #print(chatsize)
    page.wait(5)
    #print(chat.rect.size)
    if chatsize == chat.rect.size:
        lwSelect = chat.s_ele('.^blockContainer___')
        if lwSelect:
            lwSelect = chat.ele('.^blockContainer___')
            chat = lwSelect.next()
            chatText = chat.text
        else:
            chatText = chat.text
        break
    else:
        pass
        #print('正在对话')
        
print(chatText)
if chatText == "尊敬的用户您好，让我们换个话题再聊聊吧。":
    raise Exception("采集内容被AI屏蔽，跳过任务")

print(chatText)
page.quit()
    
 