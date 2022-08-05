
from bs4 import BeautifulSoup
import re
import requests
import os
def Status(status_code:str):
    modeStr = re.compile('2..')
    res = re.search(modeStr, status_code)
    if(res != None):
        return True
    return False
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


url = 'https://www.pixiv.net/artworks/97894564'
#url_1 = 'https://www.google.com'

proxies = {#在梯子底下能翻到,用的本地地址和本地端口
'http':'http://127.0.0.1:19180',
'https':'http://127.0.0.1:19180'
}
DefaultDir = 'C:/Users/DELL/Desktop/pixiv/'
DefaultDir = 'E:/WormDownloadLib/PixivImage/test/'

#找到获取图片的apiURL,需要三个参数
#获取原图
modeURL_origin = 'https://i.pximg.net/img-original/img/{Time}/{ID}_p{index}.jpg'
#获取压缩过的图
modeURL = 'https://i.pximg.net/img-master/img/{Time}/{ID}_p{index}_master1200.jpg'

imageID = '94218245'
url = 'https://www.pixiv.net/artworks/{ID}'.format(ID = imageID)

#创建新文件夹
path = DefaultDir + imageID
if(not os.path.exists(path)):
    os.makedirs(path)

#打开初始URL
res = requests.get(url, headers=pixivHeaders, proxies=proxies)
print(res)
html = res.text
#获取作者的ID (通过搜索ID本身定位到的)
mode = re.compile('\"authorId\":\"(.*?)\"')
authorID = re.search(mode, html).group(1)

#获取发布时间 (通过复制其本身得到的)
mode = re.compile('img-master/img/(.*?)/{ID}_p'.format(ID= imageID))
Time = re.search(mode,html).group(1)



"""
count = 0
while(True):
    imageURL = modeURL.format(Time = Time, ID = imageID, index = count)
    #print(imageURL)
    try:
        res = requests.get(imageURL, headers=pixivDownloadHeaders, proxies=proxies)
        if not Status(str(res.status_code)) :
            break
    except Exception as error:
        break
    
    with open(DefaultDir + imageID + '/%d.jpg'%count, 'wb') as f:
        f.write(res.content)
    print('Count:%d'%(count+1))
    count += 1
    pass
print('Download Over.')
"""
"""
imageURL = 'https://i.pximg.net/img-master/img/2022/04/26/17/14/47/97894564_p44_master1200.jpg'
res = requests.get(imageURL, headers=pixivDownloadHeaders, proxies=proxies)
with open(DefaultDir + 'adsfasdfaaaa.jpg', 'wb') as f:
        f.write(res.content)
print('Down')
"""








#从这个api可以获取日期
"""
TimeapiURL_mode = 'https://www.pixiv.net/ajax/user/{userID}/illusts?ids%5B%5D={imageID}'
TimeapiURL = TimeapiURL_mode.format(userID = authorID, imageID = imageID)
res_1 = requests.get(TimeapiURL, headers=pixivHeaders, proxies=proxies)
html = res.text
"""

"""
res = requests.get(url, headers=pixivHeaders, proxies=proxies)
print(res)
html = res.text
soup = BeautifulSoup(html, 'lxml')
print(soup.find(name='body'))
mode = re.compile('')
print(re.search('62720177', html))
"""





 





