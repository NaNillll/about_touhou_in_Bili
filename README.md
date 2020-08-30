# about_touhou_in_Bili
## getKey.py
1. 用于获得uidList中用户的所有投稿的tag，和每个tag的出现次数,并保存
2. 使用aiohttp库进行并发，并发数为MAXTHREADS，默认为10
3. 结果为dict，pickle文件默认储存在keyWords
4. 直接运行即可
## toolsT.py
1. 多线程随机选取用户进行判断，总量达到totalNum时停止。可以使用代理，每个代理对应MAXTHREADS个线程，默认为10。在proxy中添加代理
2. 访问过的活跃用户，爱好者的uid分别以List形式储存在pickle文件中，为ActiveList和ThpList，运行情况记录在Out.txt
3. 直接运行即可
## toolsC.py
1. 整合path路径下所有ThpList，保存为pickle文件，文件名Total，依照Total中保存uid依次查找该用户相关视频出现次数，uid与次数一一对应保存在dict中，储存在pickle文件中，文件名details
2. 多线程随机选取用户进行判断，可以使用代理，每个代理对应MAXTHREADS个线程，默认为10。在proxy中添加代理
3. 给path赋值后，直接运行即可



*这个代码写的真是惨不忍睹。。。当时写的时候连进程都不知道是什么。。。*
