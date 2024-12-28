import os              
import re
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

tmp_dir = './tmp'
wxUrl = 'https://mp.weixin.qq.com/'

while True:
    try:
        page = None
            
        user = '作者'
        img_html = os.path.abspath('./wx_gzh/img.html')
        con_html = os.path.abspath('./wx_gzh/content.html')
        
        co = ChromiumOptions() #配置文件
        co.auto_port(False) #需要登录的平台
        page = ChromiumPage(co)  #页面对象
        page.set.load_mode.normal()
        page.set.window.max()
        tool = commonTool.Tool(page)       
        
        chromList = page.get_tabs()
        # print(chromList)
        if len(chromList) > 1:
            for index,chrom in enumerate(chromList):
                if index == 0:
                    continue
                else:
                    print('关闭多余页面')
                    chrom.close()
                
        page.get(wxUrl)
        print('进入微信公众号页面')
        
        qh_btn =page.s_ele('.login__type__container__select-type')
        if qh_btn:
            raise Exception('微信公众号未登录')

        page.wait.doc_loaded()
        page.wait.eles_loaded('.new-creation__menu-item')
        conBtn =page.ele('.new-creation__menu-item')
        page.wait(1)
        tool.pyautoguiLocal(conBtn)
        page.wait(1)
        
        new_tab = conBtn.click.for_new_tab()
        new_tab.wait.doc_loaded()
        print('跳转进入文章页')
        new_tab.wait(5)
        
    
        tool = commonTool.Tool(new_tab)       

        new_tab.wait(1)
        new_tab.wait.eles_loaded('#title')
        title_input = new_tab.ele('#title')
        tool.pyautoguiLocal(title_input)
        new_tab.wait(1)
        title_input.clear()
        new_tab.wait(1)
        title_input.input('标题1')
        new_tab.wait(1)
        print('标题写入成功')
        
        new_tab.wait.eles_loaded('#author')
        name_input = new_tab.ele('#author')
        tool.pyautoguiLocal(name_input)
        new_tab.wait(1)
        name_input.clear()
        new_tab.wait(1)
        name_input.input('作者1')
        new_tab.wait(1)
        print('作者写入成功')
        
        
        imgindex = 3
        while imgindex:
            img_tab = page.new_tab()
            img_tab.get(img_html)
            img_tab.wait.doc_loaded()
            img_tab.wait.eles_loaded('tag:img')
            ac = Actions(img_tab)
            ac.type(Keys.CTRL_A)
            ac.type(Keys.CTRL_C)
            img_tab.wait(2)
            print('进入图片html')
            img_tab.close()
            
            ac = Actions(new_tab)
            new_tab.wait.eles_loaded('#edui1_iframeholder')
            art_input = new_tab.ele('#edui1_iframeholder')
            tool.pyautoguiLocal(art_input)
            new_tab.wait(1)
            art_input.clear()
            new_tab.wait(1)
            art_input.focus()
            new_tab.wait(1)
            art_input.input(Keys.CTRL_V)
            print('复制封面图')
            new_tab.wait(5)
            arthtml = new_tab.ele('.page_msg mini with_closed js_catch_tips')
            if arthtml:
                arthtml = arthtml.states.is_displayed
            
            # print(arthtml)
            if arthtml:
                print('封面图插入失败')
                new_tab.wait.eles_loaded('#edui1_iframeholder')
                art_input = new_tab.ele('#edui1_iframeholder')
                tool.pyautoguiLocal(art_input)
                art_input.focus()
                ac.type(Keys.BACKSPACE)
                imgindex = imgindex - 1
            else:
                new_tab.wait(3)
                clickindex = 5
                while clickindex:
                    add_local_img_btn = new_tab.eles('.pop-opr__button js_selectCoverFromContent')[-1]
                    if add_local_img_btn:
                        new_tab.wait(2)
                        is_click = add_local_img_btn.states.is_displayed
                        if is_click:
                            print('使用正文封面图')
                            add_local_img_btn = new_tab.eles('.pop-opr__button js_selectCoverFromContent')[-1]
                            tool.pyautoguiLocal(add_local_img_btn)
                            add_local_img_btn.click(by_js=None)
                            new_tab.wait(1)
                            clickindex = 0
                            break
                        else:
                            print('鼠标选择封面图')
                            new_tab.wait(1)
                            new_tab.wait.eles_loaded('.icon20_common add_cover')
                            add_img_btn = new_tab.ele('.icon20_common add_cover')
                            tool.pyautoguiLocal(add_img_btn)
                            clickindex = clickindex - 1
                    else:
                        print('鼠标选择封面图')
                        new_tab.wait(1)
                        new_tab.wait.eles_loaded('.icon20_common add_cover')
                        add_img_btn = new_tab.ele('.icon20_common add_cover')
                        tool.pyautoguiLocal(add_img_btn)
                        clickindex = clickindex - 1
                        
                noneimg = new_tab.s_ele('text:正文中无可用做封面的图片和视频封面')
                if noneimg == None:
                    # 有图片，进入剪图片选择
                    print('正文有封面图，开始选择封面图')
                    new_tab.wait.eles_loaded('.appmsg_content_img_item')
                    select_one_img = new_tab.ele('.appmsg_content_img_item')
                    tool.to_scroll_target_ele(select_one_img)
                    tool.pyautoguiLocal(select_one_img)
                    new_tab.wait(1)
                    select_one_img.click(by_js=None)
                    new_tab.wait(1)
                    
                    new_tab.wait.eles_loaded('下一步')
                    xyb_btn = new_tab.ele('下一步')
                    tool.to_scroll_target_ele(xyb_btn)
                    tool.pyautoguiLocal(xyb_btn)
                    new_tab.wait(1)
                    xyb_btn.click(by_js=None)
                    new_tab.wait(1)
                    
                    new_tab.wait.eles_loaded('上一步')
                    wc_btn = new_tab.ele('上一步').parent().next().child()
                    tool.to_scroll_target_ele(wc_btn)
                    tool.pyautoguiLocal(wc_btn)
                    new_tab.wait(1)
                    wc_btn.click(by_js=None)
                    new_tab.wait(5)
                    
                    fm = new_tab.ele('.^js_cover_preview_new select-cover__preview')
                    fmimg = fm.attr('style')
                    pattern = r'url\("([^"]*)"\)'
                    match = re.search(pattern, fmimg)
                    isfm = True
                    if match:
                        url_content = match.group(1) 
                        isfm = not bool(url_content.strip())
                    else:
                        isfm = True
                    if isfm:
                        print('图片裁剪失败,可能是网络问题')
                        imgindex = imgindex - 1
                    else:
                        print('图片裁剪成功')
                        imgindex = 0
                        break
                else:
                    print('正文无封面图，重新提取封面图')
                    quitbtn = new_tab.ele('.weui-desktop-dialog__wrp weui-desktop-dialog_img-picker').ele('.weui-desktop-icon-btn weui-desktop-dialog__close-btn')
                    tool.pyautoguiLocal(quitbtn)
                    quitbtn.click(by_js=None)
                    new_tab.wait(1)
                    imgindex = imgindex - 1


            if imgindex == 0:
                raise Exception('封面图选泽失败，删除文章')
        
            
        new_tab.wait(5)
        
        fm = new_tab.ele('.^js_cover_preview_new select-cover__preview')
        fmimg = fm.attr('style')
        pattern = r'url\("([^"]*)"\)'
        match = re.search(pattern, fmimg)
        isfm = True
        if match:
            url_content = match.group(1) 
            isfm = not bool(url_content.strip())
        else:
            isfm = True
        if isfm:
            raise Exception('没有检测到封面图，删除文章')
        
        clear_index = 5
        while clear_index:
            new_tab.wait.eles_loaded('#edui1_iframeholder')
            art_input = new_tab.ele('#edui1_iframeholder')
            art_input = art_input.ele('tag:img')
            # print(art_input)
            ac = Actions(new_tab)
            tool.pyautoguiLocal(art_input)
            new_tab.scroll.to_top()
            new_tab.wait(2)
            art_input.click.at(50, 150,count=3)
            new_tab.wait(1)
            ac.type(Keys.BACKSPACE)
            new_tab.wait(1)
            is_clear = new_tab.ele('.editor_content_placeholder edui-default ProseMirror-widget')
            if is_clear:
                print('正文清空成功')
                clear_index = 0
                break
            else:
                print('正文清空失败，正在重试！！！')
                clear_index = clear_index - 1
                new_tab.wait(2)
            if clear_index == 0:
                raise Exception('正文清空失败，请联系管理员')
                
        conindex = 3
        while conindex:    
            con_tab = page.new_tab()
            print('打开文章的html')
            con_tab.get(con_html)
            con_tab.wait.doc_loaded()
            rect = con_tab.rect.size
            ac = Actions(con_tab)
            ac.type(Keys.CTRL_A)
            ac.type(Keys.CTRL_C)
            con_tab.wait(2)
            con_tab.close()
    
            ac = Actions(new_tab)
            art_input.input(Keys.CTRL_V)
            print('粘贴文章的html')
            new_tab.wait(5)
            arthtml = new_tab.ele('.page_msg mini with_closed js_catch_tips')
            if arthtml:
                arthtml = arthtml.states.is_displayed
            if arthtml:
                print('粘贴文章的html失败，正在重试！！！')
                
                clear_index = 5
                while clear_index:
                    new_tab.wait.eles_loaded('#edui1_iframeholder')
                    art_input = new_tab.ele('#edui1_iframeholder')
                    tool.pyautoguiLocal(art_input)
                    art_input.focus()
                    ac.type(Keys.CTRL_A)
                    new_tab.wait(1)
                    ac.type(Keys.BACKSPACE)
                    is_clear = new_tab.ele('.editor_content_placeholder edui-default ProseMirror-widget')
                    if is_clear:
                        print('正文清空成功')
                        clear_index = 0
                        break
                    else:
                        print('正文清空失败，正在重试！！！')
                        clear_index = clear_index - 1
                        new_tab.wait(2)
                if clear_index == 0:
                    raise Exception('正文清空失败，请联系管理员')
                        
                conindex =conindex - 1
            else:
                conindex = 0
                break
            
            if conindex == 0:
                raise Exception('粘贴文章的html失败，删除该文章')
        
        ac = Actions(new_tab)
        new_tab.wait.eles_loaded('#js_description')
        description_input = new_tab.ele('#js_description')
        tool.to_scroll_target_ele(description_input)
        tool.pyautoguiLocal(description_input)
        new_tab.wait(1)
        description_input.clear()
        new_tab.wait(1)
        description_input.focus()
        new_tab.wait(1)
        ac.type(('文章简介', ' '))
        new_tab.wait(1)
        
            
        print('文章简介插入成功')
        
        new_tab.wait.eles_loaded('.allow_click_opr js_article_tags_label')
        tags_btn = new_tab.ele('.allow_click_opr js_article_tags_label')
        tool.pyautoguiLocal(tags_btn)
        tags_btn.click(by_js=None)
        tags = ['合集1','合集2']
        tagindex = 5
        
        new_tab.wait.eles_loaded('.weui-desktop-form-tag__input__label')
        tags_input = new_tab.ele('.weui-desktop-form-tag__input__label')
        tool.pyautoguiLocal(tags_input)
        tags_input.focus()
        for tag in tags:
            tags_input.input(tag+'\n')
            tagindex = tagindex - 1
            if tagindex == 0:
                break
        
        tagaddbtn = new_tab.ele('.weui-desktop-dialog__wrp article_tags_dialog js_article_tags_dialog').ele('.weui-desktop-dialog__ft').ele('tag:button')
        tagaddbtn.click(by_js=None)
        print('文章写入合集成功')
        
        
        print('文章写入原文链接')
        new_tab.wait.eles_loaded('.allow_click_opr js_article_url_allow_click')
        orglink_btn = new_tab.ele('.allow_click_opr js_article_url_allow_click')
        tool.pyautoguiLocal(orglink_btn)
        new_tab.wait(1)
        orglink_btn.click(by_js=None)
        new_tab.wait(1)
        
        
        new_tab.wait.eles_loaded('.weui-desktop-form__input js_url js_field')
        orglink_input = new_tab.ele('.weui-desktop-form__input js_url js_field')
        orglink_input.focus()
        new_tab.wait(1)
        orglink_input.input('www.baidu.com')
        new_tab.wait(1)
        
        new_tab.wait.eles_loaded('.btn btn_primary jsPopoverBt')
        orglink_btn = new_tab.ele('.btn btn_primary jsPopoverBt')
        new_tab.wait(1)
        orglink_btn.click(by_js=None)
        new_tab.wait(1)
        print('文章写入原文链接成功')
        

        arthtml = new_tab.ele('.page_msg mini with_closed js_catch_tips')
        if arthtml:
            arthtml = arthtml.states.is_displayed
        if arthtml:
            print('正文插入失败')
            new_tab.wait.eles_loaded('#edui1_iframeholder')
            art_input = new_tab.ele('#edui1_iframeholder')
            tool.pyautoguiLocal(art_input)
            art_input.focus()
            ac.type(Keys.BACKSPACE)
                
        print('文章编写结束，进入发送阶段')
        new_tab.wait.eles_loaded('.mass_send')
        sendBtn =  new_tab.ele('.mass_send')
        tool.pyautoguiLocal(sendBtn)
        new_tab.wait(1)
        sendBtn.click(by_js=None)
        new_tab.wait(2)
        
        err = new_tab.ele('.page_msg mini with_closed js_title_error js_error_msg edui-default')
        if err:
            err = err.states.is_displayed
            errmsg = '标题不存在'
            
        err2 = new_tab.ele('.frm_msg fail js_cover_error js_error_msg')
        if err2:
            err2 = err2.states.is_displayed
            errmsg = '封面图不存在'
            
        err3 = new_tab.ele('.frm_msg fail js_desc_error')
        if err3:
            err3 = err3.states.is_displayed
            errmsg = '简介错误'
            
        if err or err2 or err3:
            raise Exception(errmsg)
        else:

            new_tab.wait.eles_loaded('.mass-send__footer')
            sendBtn = new_tab.ele('.mass-send__footer')
            if sendBtn:
                sendBtn1 = new_tab.ele('.mass-send__footer').ele('.weui-desktop-btn weui-desktop-btn_primary')
                tool.pyautoguiLocal(sendBtn1)
                new_tab.wait(1)
                sendBtn1.click(by_js=None)
                new_tab.wait(5)
                
                new_tab.wait.eles_loaded('.double_check_dialog')
                sendBtn2 = new_tab.ele('.double_check_dialog')
                if sendBtn2:
                    sendBtn2 = new_tab.ele('.mass-send__footer').ele('.weui-desktop-btn weui-desktop-btn_primary')
                    tool.pyautoguiLocal(sendBtn2)
                    new_tab.wait(2)
                    sendBtn2.click(by_js=None)
                    new_tab.wait(15)
                    
                    orgUrl = new_tab.url
                    
                    print('文章发送成功')
                # sys.exit(0)

                
            new_tab.close()
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
