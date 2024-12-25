import os
import pyperclip
import re
import tool as commonTool 
from DrissionPage import ChromiumPage,ChromiumOptions
from DrissionPage.errors import *

def aq_check(page):
    aq_check = False
    html = page.html

    aq_check = re.findall(r'检测到你电脑或网络的流量高于往常', html)
    if aq_check:
        print('触发bing安全验证,重新更新任务')
        page.wait(5)
        raise Exception("触发bing安全验证,重新更新任务")

    return True

org_con = """
*潮阳美食特色*
1、潮阳的特产其实都带有比较明显的地域性美食特产比如最有名的鲎裸，以棉城出产为主，其他地方基本没有海门糕仔，去莲花峰玩的人经常会带一点回家此外还有贵屿朥饼，和平葱饼
仙城束沙农作物特产西胪乌酥杨梅。
2、2，肠粉 肠粉虽然发源于广州西关，但在汕头潮阳形成了自己的特色，在棉城，从事出售肠粉的店家有很多，也各有各的特点，但在棉城，制作肠粉的主料一般是主料米浆，猪肉或
肉，虾仁，青菜，鸡蛋，菜脯粒香菇等3。
3、1西胪乌酥杨梅 潮阳区西胪镇地处榕江下游西岸，依山傍海，土地肥沃，向来是潮汕平原的“鱼米之乡”，也是孕育有“岭南佳果”美称的乌酥杨梅之地2金玉三捻橄榄 原产于汕头市潮阳
金灶镇，是该地特产其
"""
 
page = None
co = ChromiumOptions() #配置文件
co.auto_port(False) #需要登录的平台
page = ChromiumPage(co)  #页面对象
page.set.window.max()
tool = commonTool.Tool(page)

fanyi_con = os.path.join('runtime','fanyi_tmp.txt')

page.set.load_mode.normal()
page.get("https://cn.bing.com/translator") 
page.wait.doc_loaded()
page.wait(1)
page.wait.eles_loaded('#tta_input_ta')
page.wait.eles_loaded('#tta_revIcon')
page.wait(2)

textarea = page.ele('#tta_input_ta')
qh_btn = page.ele('#tta_revIcon')


tool.to_scroll_target_ele(qh_btn)
page.wait(1)
tool.pyautoguiLocal(qh_btn)
page.wait(1)

qh_btn.click.at(20,20)

tool.to_scroll_target_ele(textarea)
page.wait(1)
tool.pyautoguiLocal(textarea)
page.wait(1)

textarea.clear()
textarea.focus()
page.wait(1)
textarea.input(org_con)
aq_check(page)
page.wait(3)


click_index = 4
while click_index:
    page.wait.eles_loaded('#tta_copyIcon')
    copy = page.ele('#tta_copyIcon')
    #print(copy)
    tool.to_scroll_target_ele(copy)
    page.wait(1)
    tool.pyautoguiLocal(copy)
    page.wait(1)
    copy.click(by_js=None)
    tmp_con = pyperclip.paste()
    if tmp_con == '':
        print('没有复制到内容，请重试')
        click_index = click_index - 1
        page.wait(3)
    else:
        break
    if click_index == 0:
        raise Exception("没有复制到内容，任务失败")
    
with open(fanyi_con, 'w', encoding='utf-8') as file:
    file.write(tmp_con) 
page.wait(1)
tmp_con = ''
pyperclip.copy('')

page.wait(1)
page.wait.eles_loaded('#tta_input_ta')
page.wait.eles_loaded('#tta_revIcon')

tool.to_scroll_target_ele(textarea)
page.wait(1)
tool.pyautoguiLocal(textarea)
page.wait(1)

textarea.clear()

tool.to_scroll_target_ele(qh_btn)
page.wait(1)
tool.pyautoguiLocal(qh_btn)
page.wait(1)

qh_btn.click(by_js=None)
page.wait(1)

tool.to_scroll_target_ele(textarea)
page.wait(1)
tool.pyautoguiLocal(textarea)
page.wait(1)

textarea.focus()
page.wait(1)
with open(fanyi_con, 'r', encoding='utf-8') as file:
    content = file.readlines()
    
content = [line for line in content if line.strip() != '']
textarea.input(content)
page.wait(2)
page.wait.eles_loaded('#tta_copyIcon')
copy = page.ele('#tta_copyIcon')


click_index = 4
while click_index:
    
    tool.to_scroll_target_ele(copy)
    page.wait(1)
    tool.pyautoguiLocal(copy)
    page.wait(1)
    copy.click(by_js=None)
    tmp_con = pyperclip.paste()
    if tmp_con == '':
        print('没有复制到内容，请重试')
        click_index = click_index - 1
    else:
        break
    if click_index == 0:
        raise Exception("没有复制到内容，任务失败")        

print(tmp_con)

page.quit()




