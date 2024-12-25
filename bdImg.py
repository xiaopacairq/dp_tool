
from datetime import datetime
import os
import random
import secrets
import sys
import uuid
import requests
import tool as commonTool 

from DrissionPage import ChromiumPage,ChromiumOptions
from DrissionPage.errors import *


from PIL import Image

def pjImg(img_tmp_upfile,upfile_img_1):
    tmp_image_files = [os.path.join(img_tmp_upfile, f) for f in os.listdir(img_tmp_upfile) if f.lower().endswith(('.jpg'))]  

    # 检查图片数量是否为16  
    if len(tmp_image_files) >= 16:  
        tmp_image_files = random.sample(tmp_image_files, 16)

        new_img_width = 600  
        new_img_height = 350  
    
        cell_width = new_img_width // 4  
        cell_height = new_img_height // 4  
    
        new_img = Image.new('RGB', (new_img_width, new_img_height))  
    
        for i, img_path in enumerate(tmp_image_files):  
            img = Image.open(img_path)  
            img = img.resize((cell_width, cell_height), Image.BICUBIC)  
        
            x = (i % 4) * cell_width  
            y = (i // 4) * cell_height  
            
            new_img.paste(img, (x, y))  

        new_img.save(upfile_img_1)  
        
    else:  
        # pass
        print(f"The folder '' does not contain exactly 16 images.")
        raise Exception("采集图片少于16张")

page = None
co = ChromiumOptions() #配置文件
co.auto_port(False) #需要登录的平台
page = ChromiumPage(co)  #页面对象
page.set.window.max()
tool = commonTool.Tool(page)

bdimg_tmp = os.path.join('runtime','bdImg_tmp')
if not os.path.exists(bdimg_tmp):
    os.makedirs(bdimg_tmp)

# 释放临时文件
if os.path.exists(bdimg_tmp):
    for f_name in os.listdir(bdimg_tmp):  
        file_path = os.path.join(bdimg_tmp, f_name) 
        os.remove(file_path)

keyword = '潮阳棉城文化'

page.set.load_mode.normal()
page.get('https://image.baidu.com/') 
page.wait(1)

page.wait.eles_loaded('@placeholder:拖入图片/输入文字')
page.wait.eles_loaded('@type:submit')

input =page.ele('@placeholder:拖入图片/输入文字')

tool.pyautoguiLocal(input)
page.wait(1)
input.click()
page.wait(1)
input.input(keyword)
page.wait(1)

btn = page.ele('@type:submit')

tool.pyautoguiLocal(btn)
page.wait(1)
btn.click()
page.wait.load_start()
page.wait(1)

page.wait.eles_loaded('.main_img img-hover')
img_list = page.eles('.main_img img-hover')

keywordCount = len(keyword)
if len(img_list) < 16:
    keyWord = keyword
    while keywordCount:
        page.wait.eles_loaded('#kw')
        page.wait.eles_loaded('.s_btn_wr')
        
        input =page.ele('#kw')
        btn = page.ele('.s_btn_wr').child()
        keyWord = keyWord[:-1]
        input.clear()
        input.focus()
        input.input(keyWord)
        page.wait(1)
        btn.click()
        page.wait(1.5)
        img_list = page.eles('.main_img img-hover')
        if len(img_list) >= 16:
            img_list = page.eles('.main_img img-hover')
            break
        else:
            keywordCount = keywordCount - 1
        if keywordCount <= 4:
            raise Exception("该关键词没有图片，删除标题")
        
img_list = random.sample(img_list, 16)

for img in img_list:

    img_url = img.attr('data-imgurl')
    response = requests.get(img_url, stream=True)  
    
    if response.status_code == 200:    
        f_name= os.path.join(bdimg_tmp,str(uuid.uuid4())+".jpg" )
        with open(f_name, 'wb') as f:   
            for chunk in response.iter_content(1024):  
                if chunk:  
                    f.write(chunk)  
    else:  
        print(f"Failed to download {f_name}. Status code: {response.status_code}")
        
        
current_time = datetime.now().strftime('%Y%m%d')
uuidName = secrets.token_hex(16)

tmpdir = 'bgimg.jpg'

pjImg(bdimg_tmp,tmpdir)
# 释放临时文件
if os.path.exists(bdimg_tmp):
    for f_name in os.listdir(bdimg_tmp):  
        file_path = os.path.join(bdimg_tmp, f_name) 
        os.remove(file_path) 

# os.remove(tmpdir)
page.quit()