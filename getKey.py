#from urllib.request import urlopen
import json
import re
import time
import sys
import logging
import pickle
#import requests
import asyncio
import aiohttp
import time
import random
headers = {
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36"
    "(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
}

MAXTHREADS=10
#global
activeNum=0
thNum=0
nowNum=0
keys={}
tagCount=0
aidList=[]
uidList=[149592,170864189,8712297,605769,1879254,
        28980856,184568,86865890,24867677,448823,10863253,
        184568,942357,23581010]
    
async def getJsonUrl(url):
    await asyncio.sleep(0.5)
    async with asyncio.Semaphore(MAXTHREADS):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as html:
                while 1:
                    text = await html.text(encoding="utf-8")
                    jsonData =json.loads(text)
                    if(jsonData['data']==-400):
                        print("something wrong when connect "+url)
                        await asyncio.sleep(5)
                    else:
                        return jsonData

async def getKey():
    global aidList,keys,uidList
    start=time.time()
    with open('keyWords', 'wb') as f:
        #Get all aids
        for uid in uidList:
            subListUrl='https://api.bilibili.com/x/space/arc/search?mid={uid}&ps=100&tid=0&pn={page}&keyword=&order=pubdate&jsonp=jsonp'.format(uid=uid,page=1)
            subListJson =await getJsonUrl(subListUrl)
            count=subListJson['data']['page']['count']
            for i in range(1,(count//100)+2):
                print("{a}/{b}".format(a=i,b=(count//100)+2))
                if(i!=1):
                    subListUrl='https://api.bilibili.com/x/space/arc/search?mid={uid}&ps=100&tid=0&pn={page}&keyword=&order=pubdate&jsonp=jsonp'.format(uid=uid,page=i)
                    subListJson =await getJsonUrl(subListUrl)
                videoList=subListJson['data']['list']['vlist']
                for j in range(0,len(videoList)):
                    aid=videoList[j]['aid']
                    aidList.append(aid)
        #Get all tag from all aid
        task=[]    
        for aid in aidList:
            task.append(add_tag(aid))
            if(len(task)>MAXTHREADS):
                await asyncio.gather(*task)
                task=[]
        await asyncio.gather(*task)
        pickle.dump(keys,f)
        f.close()
        print("cost:{}s".format(time.time() - start))

async def add_tag(aid):
    global tagCount,aidList
    submittedUrl='http://api.bilibili.com/x/tag/archive/tags?aid={aid}&jsonp=jsonp'.format(aid=aid)
    submittedInfo=await getJsonUrl(submittedUrl)
    tagList=submittedInfo['data']
    for k in range(0,len(tagList)):
        if(keys.__contains__(tagList[k]["tag_name"])==0):
            keys[tagList[k]["tag_name"]]=1
            #print(tagList[k]["tag_name"])
        else:
             keys[tagList[k]["tag_name"]]+=1
    tagCount+=1
    if((tagCount+1)%30==0):
        print("{}/{}".format(tagCount+1,len(aidList)))

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(getKey())
    with open('keyWords', 'rb') as f:
        tmp=pickle.load(f)
        for (tag,num) in tmp.items():
            if(num>=500):
                print(tag,num)
        f.close()
    