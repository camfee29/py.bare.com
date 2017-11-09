import urllib.request
import re
import os.path

class Collect:
    _content = ''
    def get(self, url):
        data = urllib.request.urlopen(url).read()
        self._content = str(data.decode('gbk'))
        return self
    def getHtml(self, url):
        headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Referer':'https://www.baidu.com/' # 注意如果依然不能抓取的话，这里可以设置抓取网站的host
        }
        opener = urllib.request.build_opener()
        opener.addheaders = [headers]
        data = opener.open(url).read()
        self._content = str(data.decode('gbk'))
        return self
    def getMatch(self, reg, flag = re.M|re.S):
        m = re.search(reg, self._content, flag)
        if m:
            return m.groups()[0]
        else:
            return
    def getMatchAll(self, reg, flag = re.M|re.I):
        m = re.findall(reg, self._content, flag)
        if m:
            return m
        else:
            return
    def download(self, url, filename):
        dir = os.path.dirname(filename)
        if not os.path.exists(dir):
            os.makedirs(dir)
        urllib.request.urlretrieve(url, filename)

if __name__ == "__main__":
    print('采集封装类')
