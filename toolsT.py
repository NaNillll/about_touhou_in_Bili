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
THREAD_PER_PROXY=10
MAXUID=458200000

#global
activeNum=0
thNum=0
nowNum=0
startRunTime=0
endRunTime=0
sleepTime=0.4
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
            req=requests.get(url,headers=headers,timeout=5,proxies=proxy)
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

def is_thp(uid,proxy={'http':None}):
    """
    return:0 means not activate; 1 means is thp; 2 means not thp; 3 means wrong; 

    1.Get all favorite videos to check if thv
    2.Get all submitted videos to check if thv
    3.Return

    """
    global activeNum,thNum,nowNum
    isActive =0
    isThp=0
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
                    res=is_thv_fid(uid,favList[j]['fid'],proxy)
                    if(res==3):
                        raise RequestException
                    if(res!=0):
                        if(isActive==0):
                            isActive=1
                            activeNum+=1
                    if(res==1):
                        isThp=1
                        thNum+=1
                        nowNum+=1
                        return 1
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
                            isThp=1
                            thNum+=1
                            nowNum+=1
                            return 1
                    else:
                        break
                    
        nowNum+=1
        if(isActive==0):
            return 0
        return 2
    
    except RequestException:
        print("What's Wrong?")
        if(isThp==1):
            thNum-=1
        if(isActive==1):
            activeNum-=1
        return 3

def is_thv_fid(uid,fid,proxy):
    """
    about favorate
    return:0 means not active, 1 means active and thv, 2 means active not thv, 3 means something wrong
    """
    isActive=0
    favPageUrl = 'https://api.bilibili.com/x/space/fav/arc?vmid={uid}&ps=100&fid={fid}&tid=0&keyword=&pn={page}&order=fav_time&jsonp=jsonp'.format(uid=uid,fid=fid,page=1)
    favPage = getJsonUrl(favPageUrl,proxy)
    if(favPage==None):
        return 3
    pageCount=favPage['data']['pagecount']
    for i in range(1, pageCount+1):
        if(i!=1):
            favPageUrl = 'https://api.bilibili.com/x/space/fav/arc?vmid={uid}&ps=100&fid={fid}&tid=0&keyword=&pn={page}&order=fav_time&jsonp=jsonp'.format(uid=uid,fid=fid,page=i)
            favPage = getJsonUrl(favPageUrl,proxy)
            if(favPage==None):
                return 3
        favList=favPage['data']['archives']
        for j in range(0,len(favList)):
            if(favList[j]['fav_at']>startTime):
                if(isActive==0):
                    isActive=1
                res=is_thv_aid(uid,favList[j]['aid'],proxy)
                if(res==2):
                    return 3
                if(res==1):
                    print(favList[j]['aid'])
                    return 1
            else:
                break
    if(isActive==0):
        return 0
    return 2        

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

def spider(proxy):
    global nowNum,errorThread
    while 1:
        tmpNum = nowNum
        isError =0
        if(tmpNum%50==1):
            print("Get{a},active{b},thp{c}".format(a=nowNum,b=activeNum,c=thNum))
        if(tmpNum%1000==1):
            print('\nStart refresh data\n')
            lock.acquire()  # 加锁  此区域的代码同一时刻只能一个线程执行
            with open('Out.txt', 'a+') as f:
                print("Get{a},active{b},thp{c}".format(a=nowNum,b=activeNum,c=thNum),file=f)
                print("Time: {time} min".format(time=(int(time.perf_counter())-startRunTime)/60),file=f)
                f.close()
                print("refresh 1")
            tmpThpList=thpList
            with open('ThpList', 'wb') as f:
                pickle.dump(tmpThpList,f)
                f.close()
                print("refresh 2")
            tmpActiveList=activeList
            with open('ActiveList', 'wb') as f:
                pickle.dump(tmpActiveList,f)
                f.close()
                print("refresh 3")
            lock.release()  # 释放锁
            print('\nEnd refresh data\n')
        if(tmpNum>=totalNum):
            print("Get{a},active{b},thp{c}".format(a=nowNum,b=activeNum,c=thNum))
            return
        uid=random.randint(1,MAXUID)
        while 1:
            res=is_thp(uid,proxy)
            if(res==1):
                thpList.append(uid)
                activeList.append(uid)
                if(isError==1):
                    errorThread-=1
                    isError=0
                    print("Ok, now errors={errorThread}".format(errorThread=errorThread))
                break
            elif(res==2):
                activeList.append(uid)
                if(isError==1):
                    errorThread-=1
                    isError=0
                    print("Ok, now errors={errorThread}".format(errorThread=errorThread))
                break
            elif(res==3):
                if(isError==0):
                    isError=1
                    errorThread+=1
                print("\nStop {proxy}, uid={uid}, errors={errorThread}\n".format(proxy=proxy,uid=uid,errorThread=errorThread))
                time.sleep(10)
                print("\nTry {proxy} again, uid={uid}\n".format(proxy=proxy,uid=uid))
                if(errorThread==10):
                    print("Long sleep")
                    time.sleep(600)
            elif(res==0):
                if(isError==1):
                    errorThread-=1
                    isError=0
                    print("Ok, now errors={errorThread}".format(errorThread=errorThread))
                break

def start():
    print('*'*5+"Start"+'*'*5)
    global startRunTime
    startRunTime==time.perf_counter()
    with open('Out.txt', 'w') as f:
        f.close()
    pool = ThreadPoolExecutor(max_workers=len(proxy)*THREAD_PER_PROXY)
    all_task=[]
    for p in proxy:
        for i in range(0,THREAD_PER_PROXY):
            try:
                all_task.append(pool.submit(spider,p))
                #print("Construct task{a} {b} !".format(a=p,b=i))
            except Exception:
                print("Can not construct task{a} {b} !".format(a=p,b=i))

    # for future in as_completed(all_task):
    #         data = future.result()
    #         print(data)
    #         print('*' * 50)
    wait(all_task)
    endRunTime=time.perf_counter()
    print("Finished!")
    print("finish! Get {a},active {b},thp {c},all {d}".format(a=nowNum,b=activeNum,c=thNum,d=totalNum))
    print("Total time:{t}s".format(t=(endRunTime-startRunTime)))
    return

def test():
    uid=[176929855,9210836,176929854,17896284]
    for u in uid:
        for p in proxy:
            print(is_thp(u,p))

def print_res(path):
    with open(path, 'rb') as f:
        data = pickle.load(f)
    for i in range(0,10):
        print(data[i])

def get_details(path):
    global details
    with open(path, 'rb') as f:
        data = pickle.load(f)


if __name__ == "__main__":
    start()
    print("Stop Main")
    print(thpList)
    print('*'*50)
    print(activeList)
    with open('ThpList.txt', 'wb',encoding='utf-8') as f:
        pickle.dump(thpList,f)
        f.close()
    with open('ActiveList.txt', 'wb',encoding='utf-8') as f:
        pickle.dump(activeList,f)
        f.close()
