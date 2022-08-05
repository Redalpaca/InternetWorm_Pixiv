from bs4 import BeautifulSoup
import re
import requests
import os
import PixivClass
from PixivClass import Image
import json
import imageio

pixivHeaders = {
'method':'GET',
'cookie':'first_visit_datetime_pc=2022-07-30+21:56:08; p_ab_id=4; p_ab_id_2=8; p_ab_d_id=24300274; _fbp=fb.1.1659185776163.1855011282; __utma=235335808.723299299.1659185772.1659185778.1659185778.1; __utmc=235335808; __utmz=235335808.1659185778.1.1.utmcsr=zhidao.baidu.com|utmccn=(referral)|utmcmd=referral|utmcct=/question/551945585.html; __utmt=1; yuid_b=IUJHmSQ; _gid=GA1.2.1027644613.1659185789; _im_vid=01G97JW02M164KTW505MYQ3ZTS; PHPSESSID=13748038_jko4pfRHJRYIu9LKEtZovKMqvuo1K4HL; device_token=95fc0a113a28a9a3111c2f36b135bded; c_type=102; privacy_policy_agreement=0; privacy_policy_notification=0; a_type=0; b_type=1; __utmv=235335808.|3=plan=normal=1^5=gender=male=1^6=user_id=13748038=1^11=lang=zh=1; QSI_S_ZN_5hF4My7Ad6VNNAi=v:0:0; cto_bundle=I_OMcF9halBZeHlhSks0V0RqWlN3YU11WXc1S1dGRVo2M3d1N3lZTWtnYVJDODRzWEd6UURZajZ5UmJlRjA4WnM3MzVCUkJCU0klMkJ2ZGJsY20xM1FuNnIyZzNCMTcwZUhKczQwMmN2d0t0WmhuUDFZTm1OV3ZZazV1UmVOSjA1ZnFJM29VZjF3UGlIb2VJVjcxTEpXOTBFemxDdyUzRCUzRA; tag_view_ranking=0xsDLqCEW6~F1AKdqvivA~jEthU99Q2P~3gc3uGrU1V~KN7uxuR89w~cb91hphOyK~jGhu1L3S_w~K8qOt_bKU_~OlC0hKTA-T; categorized_tags=F1AKdqvivA~b8b4-hqot7; tags_sended=1; adr_id=pbbFDZ5croUEokQgxIpfQ1uWpIE8Q4aasA98brGSDs9r6qWM; _ga=GA1.1.723299299.1659185772; __cf_bm=zKtpRSo9jyvD31OFWcOtu3h.AZgUNnc.zA074plHiLs-1659186275-0-AdR4pgiYO1DUZAji/o16gt1Vp5eS5Yx6LJwa5SwC1GQLySRb8ovK2+BLPnQho3l9pLpml843qk7Ahql55h7L2ykPUejfzCcl9In7CYCXRUSEDbvv1wRWeJvHLoK8Ete0BFFh8EG3YzHbUm3wzyU9y+nF/GhKbI5OdgTtPcmyC1fC8bdyRyFvgIdq/Mv99Pqssw==; __utmb=235335808.9.10.1659185778; _ga_75BBYNYN9J=GS1.1.1659185771.1.1.1659186276.0; _im_uid.3929=i.7J3ajAqLSFSB5u7_4INsdQ',
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
'referer':'https://www.pixiv.net'
}
pixivDownloadHeaders = {
'method':'GET',
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
'referer':'https://www.pixiv.net'
}
proxies = {#在梯子底下能翻到,用的本地地址和本地端口
'http':'http://127.0.0.1:19180',
'https':'http://127.0.0.1:19180'
}

#状态码是否合法
def Status(status_code:str):
    modeStr = re.compile('2..')
    res = re.search(modeStr, status_code)
    if(res != None):
        return True
    return False

#以下是Gif图的下载函数
#GifSave的辅助函数, 参数duration是图片播放间隔
def GifCreate(image_list, gif_name, duration):
    frames = []
    for image_name in image_list:
        frames.append(imageio.imread(image_name))
    imageio.mimsave(gif_name, frames, 'GIF', duration=duration)
    return
#location是序列图片文件夹的路径
def GifSave(path_gif = 'E:/WormDownloadLib/PixivImage/GifTest/GifSave/test.gif', path_image = 'E:/WormDownloadLib/PixivImage/GifTest/ImageSave/test/', duration = 0.04):
    files = os.listdir(path_image) #获取图像序列
    image_list = []
    for file in files:
        path = path_image + file
        image_list.append(path)  
    GifCreate(image_list, path_gif, duration)   #创建动态图
    #os.remove('E:/WormDownloadLib/PixivImage/GifTest/ImageSave/test')
    print('Over')
#解压函数, 指定zip文件, 并指定一个路径存储
def Unzip(path_zip, path_save):
    commad = f'unzip {path_zip} -d {path_save}'
    os.system(commad)
    pass
#Gif下载函数
def GifDownload(imageID):
    #包含图片文件zip的api
    gif_apiURL_mode = 'https://www.pixiv.net/ajax/illust/{imageID}/ugoira_meta?lang=zh'
    gif_apiURL = gif_apiURL_mode.format(imageID = imageID)
    #指定路径
    path_zip = f'E:/WormDownloadLib/PixivImage/GifTest/ZipSave/{imageID}.zip'
    path_image = f'E:/WormDownloadLib/PixivImage/GifTest/ImageSave/{imageID}/'
    path_gif = f'E:/WormDownloadLib/PixivImage/GifTest/GifSave/{imageID}.gif'
    if os.path.exists(path_gif):
        print('%s already exist.'%path_gif)
        return
    #从api网页中获取zip文件的下载链接
    res = requests.get(gif_apiURL, headers=pixivHeaders, proxies=proxies)
    if res.status_code != 200:
        print('ERROR status_code: [%s]'%res.status_code)
        return
    html = res.text
    dict_0 = json.loads(html)
    zipURL = dict_0['body']['src']
    #zipURL_origin = dict_0['body']['originalSrc']
    print(dict_0['body']['src'])
    #下载zip文件
    res = requests.get(zipURL, headers= pixivDownloadHeaders, proxies= proxies)
    print(res)
    with open(path_zip, 'wb') as f:
        f.write(res.content)
    print('.zip download over.')
    #解压zip文件为图片, 存储至特定路径
    Unzip(path_zip, path_image)
    print('Unzip over.')
    #将图片合成为GIF
    GifSave(path_gif=path_gif, path_image=path_image)
    print(f'{imageID}.gif successfully saved.')

#以下是下载pixiv个人收藏的代码
#查询收藏项数
def TotalBookmarkAmount(userID, private = False):
    url = f'https://www.pixiv.net/ajax/user/{userID}/illusts/bookmark/tags?lang=zh'
    res = requests.get(url, headers=pixivHeaders, proxies=proxies)
    dict_0 = json.loads(res.text)
    publicCount = dict_0['body']['public'][0]['cnt']
    if(not private):
        return publicCount
    else:
        privateCount = dict_0['body']['private'][0]['cnt']
        return privateCount
#下载个人的公开收藏, 允许GIF下载(保存在其他目录)
def DownPublicBookmark(userID, high_quality:int = 0, path = 'E:/WormDownloadLib/PixivImage/alpaca/', BeginPage = 1):
    #begin参数是从第几项收藏开始，Limit是一页显示几项
    BookmarkURL_mode = 'https://www.pixiv.net/ajax/user/{userID}/illusts/bookmarks?tag=&offset={Begin}&limit={Limit}&rest=show&lang=zh' 
    #暂时只考虑公共收藏
    TotalAmount = TotalBookmarkAmount(userID)
    #下载总数
    TotalCount = 1
    BeginIndex = (BeginPage-1)*48
    for i in range(BeginIndex, TotalAmount, 48): #第一页是0
        #BookmarkURL是pixiv的api, 用以存储书签信息 (JSON格式的数据)
        BookmarkURL = BookmarkURL_mode.format(Begin = str(i), Limit = '48', userID = userID)
        res = requests.get(BookmarkURL, headers=pixivHeaders, proxies=proxies)
        print(res)
        html = res.text
        dict0 = json.loads(html)
        works = dict0['body']['works']
        #works[i]存储一个书签的信息, 'id'key保存imageID, 提取出来存在列表中
        List = []
        try: #防止数组越界
            for j in range(0,48,1):
                imageID = works[j]['id']
                List.append(imageID)
        except:
            pass
        print(List)
        #通过列表中的imageID进行批量下载
        BookmarkCount = 1
        for imageID in List:
            print('Downloading: %s'%imageID, end='   ')
            print('BookmarkCount:%d'%BookmarkCount,end='   ')
            print('TotalCount:%d'%TotalCount)
            BookmarkCount += 1 
            TotalCount += 1 
            image = Image(imageID)
            #ImageDownload方法可以自动检测是否为gif
            image.ImageDownload(high_quality= high_quality, path= path)
    pass

def DownAuthorIllst(authorID):
    pass

DownPublicBookmark(userID='13748038', path='E:/WormDownloadLib/PixivImage/alpaca/', BeginPage=7)























"""
userID = '13748038'
#begin参数是从第几项收藏开始, Limit是一页显示几项
BookmarkURL_mode = 'https://www.pixiv.net/ajax/user/{userID}/illusts/bookmarks?tag=&offset={Begin}&limit={Limit}&rest=show&lang=zh' 
#暂时只考虑公共收藏
TotalAmount = TotalBookmarkAmount(userID)['public']
#正式下载代码
TotalCount = 1
for i in range(288, TotalAmount, 48): #第一页是0
    #BookmarkURL是pixiv的api, 用以存储书签信息 (JSON格式的数据)
    BookmarkURL = BookmarkURL_mode.format(Begin = str(i), Limit = '48', userID = userID)
    res = requests.get(BookmarkURL, headers=pixivHeaders, proxies=proxies)
    print(res)
    html = res.text
    dict0 = json.loads(html)
    works = dict0['body']['works']
    #works[i]存储一个书签的信息, 'id'key保存imageID
    List = []
    try: #防止数组越界
        for j in range(0,48,1):
            imageID = works[j]['id']
            List.append(imageID)
    except:
        pass
    print(List)
    #通过列表中的imageID进行批量下载
    BookmarkCount = 1
    for imageID in List:
        print('Downloading: %s'%imageID, end='   ')
        print('BookmarkCount:%d'%BookmarkCount,end='   ')
        print('TotalCount:%d'%TotalCount)
        BookmarkCount += 1 
        TotalCount += 1
        image = Image(imageID)
        image.ImageDownload()
"""















