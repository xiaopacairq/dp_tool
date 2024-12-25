import random
import re  
import pyautogui
from watermarker.marker import add_mark

# 工具类
# 1.鼠标轨迹模拟
# 2.滚动页面模拟
# 3.图片处理：
## 3.1 图片添加水印
## 3.2 图片拼接

class Tool:  
    def __init__(self,page):  
        """  
        :param page: 页面元素
        """  
        self.page = page  # 当前页面 
        
    def add_sy(self,imgtext,file,out):  
        add_mark(
            file=file,
            out=out, 
            color='#e4007f',
            mark= imgtext, 
            opacity= 0.2, 
            angle= 30, 
            space= 70
            )    
        
    def pyautoguiLocal(self,ele):
        pyautogui.FAILSAFE = False
        eleLocal = ele.rect.screen_location
        pyautogui.moveTo(eleLocal[0],eleLocal[1])

    def to_scroll_target_ele(self,url):
        self.page.scroll.to_see(url)
        
    def to_scroll_page(self): 
        footLocal = self.page.rect.size
        if footLocal[1] < 1080:
            count = 0
        else:
            count = (footLocal[1] - 1080) // 350
        while count:
            count = count - 1 
            self.page.scroll.down(300 + random.randint(10,20))
            self.page.wait(random.randint(1,2)/20)
            self.move_mouse()
            
        self.page.scroll.to_bottom()
        self.page.wait(1)
            
        if footLocal[1] < 1080:
            count = 0
        else:
            count = (footLocal[1] - 1080) // 350
        while count:
            count = count - 1 
            self.page.scroll.up(300 + random.randint(10,20))
            self.page.wait(random.randint(1,2)/20)
            self.move_mouse()
            
        self.page.scroll.to_top()
    def move_mouse(self): 
        pyautogui.FAILSAFE = False
        pyautogui.moveTo(random.randint(200, 400), random.randint(200, 400), duration=random.uniform(0.25, 1))  
        
    def clear_trim(self,text):
        cleaned_text = ' '.join(text.split()).strip()
        final_text = re.sub(r'\n+', '\n', cleaned_text)
        
        return final_text
    
     
    
       