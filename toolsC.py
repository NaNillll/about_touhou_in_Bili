from urllib.request import urlopen
import json
import re
import time
import sys
import logging
import pickle
import time
import requests
import time
from concurrent.futures import ThreadPoolExecutor,wait, ALL_COMPLETED, FIRST_COMPLETED,as_completed
import threading
from requests.exceptions import RequestException
import random
import threading
import os
lock = threading.Lock()

startTime=1546272000
endTime=1579881600
totalNum=1000000

keyList=['东方PROJECT','东方MMD','东方','东方project','东方Project']
THREAD_PER_PROXY=5
MAXUID=458200000

#global
activeNum=0
thNum=0
nowNum=0
startRunTime=0
endRunTime=0
sleepTime=0.5
errorThread=0

keys={}
tagCount=0
aidList=[]
thpList=[]
activeList=[]
details={}

proxy=[
    {'http':None}
]

totalUids=[]
user_agents =  [
    'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
    # Opera
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60",
    "Opera/8.0 (Windows NT 5.1; U; en)",
    "Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50",
    # Firefox
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
    # Safari
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2",
    # chrome
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16",
    # 360
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    ]

def getJsonUrl(url,proxy):
    '''
    If fav no data, no 'data'

    1.Can not get: return None
    2.Status!=200: wrong, return None
    3.json['code']!=0, too fast

    '''
    try:
        headers = {'User-Agent':random.choice(user_agents),"X-Requested-With": "XMLHttpRequest"}
        try:
            req=requests.get(url,headers=headers,timeout=5)
        except Exception:
            print('Requests error,url={url},proxy={proxy}'.format(url=url,proxy=proxy))
            return None

        time.sleep(sleepTime)
        if(req.status_code==200):
            json = req.json()
            if(json['code']==-400):
                print("Maybe too fast,url={url},proxy={proxy}".format(url=url,proxy=proxy))
                raise RequestException
            else:

                return json
        else:
            print('Can not connect,url={url},proxy={proxy}'.format(url=url,proxy=proxy))
            raise RequestException
    except RequestException:
        return None

def is_thv_aid(uid,aid,proxy):
    """
    about submit
    return:1 means is thv, 0 means not thv, 2 means something wrong
    """
    submittedUrl='https://api.bilibili.com/x/tag/archive/tags?aid={aid}&jsonp=jsonp'.format(aid=aid)
    submittedInfo=getJsonUrl(submittedUrl,proxy)
    if(submittedInfo==None):
        return 2
    if('data' not in submittedInfo):
        return 0
    tagList=submittedInfo['data']
    for i in range(0,len(tagList)):
        if(tagList[i]['tag_name'] in keyList):
            return 1
    return 0

def is_thTag(tag):
    """
    return:1 means th Tag, 0 means not  
    """
    for t in keyList:
        if(tag==t):
            return 1
    return 0

def get_details(i):
    '''
    Get a single details from file of path one by one
    Save in details
    '''
    global details,totalUids
    size=int(len(totalUids)/THREAD_PER_PROXY)
    print(i)
    startID=size*i
    endID=min(size*i+size,len(totalUids))
    for i in range(startID,endID):
        print(totalUids[i])
        while 1:
            num=is_thpC(totalUids[i])
            if(num!=-1):
                break
            print("error")
            time.sleep(5)
        if(details.__contains__(totalUids[i])==0):
            details[totalUids[i]]=num
        print("Finish {a}/{b}".format(a=1+i-startID,b=endID-startID))
    return

def is_thpC(uid,proxy={'http':None}):
    """
    return:0 means not activate; 1 means is thp; 2 means not thp; 3 means wrong; 

    1.Get all favorite videos to check if thv
    2.Get all submitted videos to check if thv
    3.Return

    """
    global activeNum,thNum,nowNum
    isActive =0
    isThp=0
    thvNum=0
    #print("uid={uid},nowNum={nowNum}".format(uid=uid,nowNum=nowNum))
    try:
        #Get favorite list and check
        favFileUrl = 'https://api.bilibili.com/medialist/gateway/base/created?pn={page}&ps=100&up_mid={uid}&is_space=0&jsonp=jsonp'.format(page=1,uid=uid)
        favFileJson = getJsonUrl(favFileUrl,proxy)
        if(favFileJson==None):
            raise RequestException
        if('data' in favFileJson):
            favFileNum=favFileJson['data']['count']
            for i in range(1,(favFileNum//100)+2):
                if(i!=1):
                    favFileUrl = 'https://api.bilibili.com/medialist/gateway/base/created?pn={page}&ps=100&up_mid={uid}&is_space=0&jsonp=jsonp'.format(page=i,uid=uid)
                    favFileJson = getJsonUrl(favFileUrl,proxy)
                if(favFileJson==None):
                    raise RequestException
                favList=favFileJson['data']['list']   
                for j in range(0,len(favList)):
                    res=is_thv_fidC(uid,favList[j]['fid'],proxy)
                    thvNum+=res
        
        subListUrl='https://api.bilibili.com/x/space/arc/search?mid={uid}&ps=100&tid=0&pn={page}&keyword=&order=pubdate&jsonp=jsonp'.format(uid=uid,page=1)
        subListJson=getJsonUrl(subListUrl,proxy)
        if(subListJson==None):
            raise RequestException
        if('data' in subListJson):
            count=subListJson['data']['page']['count']
            for i in range(1,(count//100)+2):
                if(i!=1):
                    subListUrl='https://api.bilibili.com/x/space/arc/search?mid={uid}&ps=100&tid=0&pn={page}&keyword=&order=pubdate&jsonp=jsonp'.format(uid=uid,page=i)
                    subListJson=getJsonUrl(subListUrl,proxy)
                if(subListJson==None):
                    raise RequestException
                videoList=subListJson['data']['list']['vlist']
                for j in range(0,len(videoList)):
                    if(videoList[j]['created']>startTime):
                        if(isActive==0):
                            isActive=1
                            activeNum+=1
                        res=is_thv_aid(uid,videoList[j]['aid'],proxy)
                        if(res==2):
                            raise RequestException
                        if(res==1):
                            thvNum+=1
                    else:
                        break       
        return thvNum
    except RequestException:
        print("What's Wrong?")
        return -1

def is_thv_fidC(uid,fid,proxy):
    """
    about favorate
    return:0 means not active, 1 means active and thv, 2 means active not thv, 3 means something wrong
    """
    isActive=0
    thvNum=0
    favPageUrl = 'https://api.bilibili.com/x/space/fav/arc?vmid={uid}&ps=100&fid={fid}&tid=0&keyword=&pn={page}&order=fav_time&jsonp=jsonp'.format(uid=uid,fid=fid,page=1)
    favPage = getJsonUrl(favPageUrl,proxy)
    if(favPage==None):
        return -1
    pageCount=favPage['data']['pagecount']
    for i in range(1, pageCount+1):
        if(i!=1):
            favPageUrl = 'https://api.bilibili.com/x/space/fav/arc?vmid={uid}&ps=100&fid={fid}&tid=0&keyword=&pn={page}&order=fav_time&jsonp=jsonp'.format(uid=uid,fid=fid,page=i)
            favPage = getJsonUrl(favPageUrl,proxy)
            if(favPage==None):
                return -1
        favList=favPage['data']['archives']
        for j in range(0,len(favList)):
            if(favList[j]['fav_at']>startTime):
                res=is_thv_aid(uid,favList[j]['aid'],proxy)
                if(res==1):
                    thvNum+=1
            else:
                break
    return thvNum     

def get_total_uid(path):
    fileList = os.listdir(path)
    res=[]
    i=0
    for f in fileList:
        fileName=path+'/'+f
        with open(fileName, 'rb') as file:
            data = pickle.load(file)
        for t in data:
            if(t not in res):
                res.append(t)
        i+=1
    with open('Total', 'wb') as f:
        pickle.dump(res,f)
        f.close()

def startC():
    global totalUids,details
    with open('Total', 'rb') as f:
        totalUids=pickle.load(f)
        f.close()
    print(len(totalUids))
    pool = ThreadPoolExecutor(max_workers=15)
    all_task=[]
    for i in range(0,THREAD_PER_PROXY+1):
        try:
            all_task.append(pool.submit(get_details,i))
            time.sleep(0.3)
        except Exception:
            print("Can not construct task{i}!".format(i=i))
    '''
     pool = ThreadPoolExecutor(max_workers=len(proxy)*THREAD_PER_PROXY)
    all_task=[]
    for p in proxy:
        for i in range(0,THREAD_PER_PROXY):
            try:
                all_task.append(pool.submit(spider,p))
                #print("Construct task{a} {b} !".format(a=p,b=i))
            except Exception:
                print("Can not construct task{a} {b} !".format(a=p,b=i))
    '''
    wait(all_task)
    oneNum=0
    twoNum=0
    moreNum=0
    tmp=details
    for (uid,num) in tmp.items():
        if(num==0):
            print("error")
        elif(num==1):
            oneNum+=1
        elif(num==2):
            twoNum+=1
        else:
            moreNum+=1
    print(oneNum,twoNum,moreNum)
    with open('details', 'wb') as f:
        pickle.dump(tmp,f)
        f.close()
    print("Finished")
    return

if __name__ == "__main__":
    path=
    get_total_uid(path)
    startC()

