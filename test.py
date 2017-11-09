import sys
import time
import threading
import os.path
#sys.path.append(r'Bare')
#from mysqldb import MysqlDB
#from redisdb import RedisDB
#from memcachedb import MemcacheDB
from Bare.mysqldb import MysqlDB
#import Bare.mysqldb as mysqldb
import Bare.redisdb as redisdb
import Bare.memcachedb as memcachedb
import Classes.collect as collect

#DB = mysqldb.MysqlDB()
DB = MysqlDB()
#data = DB.query("SHOW TABLES")
#print ( data )
#DB.selectDB('mysql')
#data = DB.query("SHOW TABLES")
#print ( data )
DB.selectDB('29shu_book')
res = DB.find('Book',{'BookId':['>', 5]},'*', '', [5,5])
print (res)

rds = redisdb.RedisDB()
#res = rds.get('mykey1')
#print(res)
#rds.set('age', 28)
#res = rds.get('age')
#print(res)
#rds.set({'age':28,'sex':'男','time':time.time()})
#res = rds.get(['sex','age'])
#rds.rpush('list', 1,2,3)
#res = rds.lrange('list')
#res = rds.rpop('list')
#res = rds.lindex('list')
#rds.rpush('list', 'a','b','c')
#res = rds.llen('list')
#rds.delete('list')
#rds.move('list',1)
#rds.selectDB(1)
#res = rds.exists('list')
#print(res)
#rds.decr('age')
#res = rds.get('age')
#rds.hset('camfee',{'age':28,'sex':'男','time':time.time()})
#res = rds.hget('camfee', ['sex','age'])
#res = rds.hscan('camfee',1)
#rds.sadd('set1', {'aa':11, 'cc': 23, 'dd': 323})
#res = rds.smembers('set1')
#rds.srem('set1',{'aa':11, 'cc': 23, 'dd': 323})
#res = rds.scard('set1')
#res = rds.spop('set1')
#print(res)

mem = memcachedb.MemcacheDB()
#mem.set({'age':28,'sex':'男','time':time.time()})
#res = mem.get(['age','sex'])
#mem.set('age',28)
#res = mem.get('time')
#print(res)

# 采集示例
cc = collect.Collect()
'''
url = 'http://www.xiaoshuo77.com/page_allvisit_1.html'
url_name = cc.getHtml(url).getMatchAll('<div class="con3"><a\s*class="tit" href="([^"]*)" title="([^"]*)" target="_blank">[^"]*</a>\s*/\s*<a href="[^"]*" title="[^"]*" target="_blank">[^"]*</a></div>')
for val in url_name:
    print(val[0])
    print(val[1])
print(len(url_name))
'''
'''
def getList(url):
    url_title = cc.getHtml(url).getMatchAll("<a test=a href='([^']+)' target='_blank'>([^(</a>)]+)</a>")
    dir = 'news/' + os.path.splitext(os.path.basename(url))[0]
    if not os.path.exists(dir):
        os.makedirs(dir)
    i = 0
    for v in url_title:
        f = open(dir + '/' + str(i) + '.txt', 'w')
        print(v[1] , file = f)
        threading.Thread(target=getContent,args=(v[0], f, dir)).start()
        #getContent(v[0], f, dir)
        i += 1
def getContent(url, f, dir = '.'):
    content = cc.getHtml(url).getMatch('<div itemprop="articleBody">(.+)<div class="new_hot1">')
    print(content, file = f)
url = 'http://wei.sohu.com/roll/'
timestart = time.time()
print(timestart)
getList(url + 'index.shtml')
for i in range(851, 949):
    print(url + 'index_' + str(i) + '.shtml');
    getList(url + 'index_' + str(i) + '.shtml')
timeend = time.time()
print(timeend)
print(timeend - timestart)
'''
