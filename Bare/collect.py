import urllib.request
import re
import threading
import time
import os.path
import random

class Collect:
    _content = ''
    def get(self, url):
        data = urllib.request.urlopen(url).read()
        self._content = str(data.decode('gbk'))
        return self
    def getHtml(self, url):
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        #'Accept':'text/html;q=0.9,*/*;q=0.8',
        #'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        #'Accept-Encoding':'gzip',
        #'Connection':'close',
        'Referer':'https://www.baidu.com/' #注意如果依然不能抓取的话，这里可以设置抓取网站的host
        }
        opener = urllib.request.build_opener()
        opener.addheaders = [headers]
        data = opener.open(url).read()
        self._content = str(data.decode('gbk'))
        return self
    def getMatch(self, reg):
        m = re.search(reg, self._content)
        if m:
            return m.groups()[0]
        else:
            return
    def getMatchAll(self, reg):
        m = re.findall(reg, self._content, re.MULTILINE)
        if m:
            return m
        else:
            return
    def download(self, url, filename):
        dir = os.path.dirname(filename)
        if not os.path.exists(dir):
            os.makedirs(dir)
        urllib.request.urlretrieve(url, filename)

if __name__=="__main__":
    cc = Collect()
    '''
    url = "http://tieba.baidu.com/f?kw=%B0%A2%C9%AD%C4%C9"
    res = cc.get(url).getMatch('src="([^"]+)"')
    print(res)
    res = cc.getMatchAll('src="([^"]+jpg)"')
    print(len(res))
    threads = []
    timestart = time.time()
    print(time.time())
    for i in range(len(res)):
        threads.append(threading.Thread(target=cc.download,args=(res[i], '../jpg/%s.jpg' % i)))
        #cc.download(res[i], '../jpg/%s.jpg' % i)
        #print(i)
    for t in threads:
        t.setDaemon(True)
        t.start()
        t.join()
    timeend = time.time()
    print(timeend - timestart)
    '''

    url = 'http://www.xiaoshuo77.com/page_allvisit_1.html'
    url_name = cc.getHtml(url).getMatchAll('<div class="con3"><a\s*class="tit" href="([^"]*)" title="([^"]*)" target="_blank">[^"]*</a>\s*/\s*<a href="[^"]*" title="[^"]*" target="_blank">[^"]*</a></div>')
    for val in url_name:
        print(val[0])
        print(val[1])
    print(len(url_name))
