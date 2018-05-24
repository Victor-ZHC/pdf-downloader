# coding = UTF-8
# 爬取html链接中的PDF文档

import urllib.request
import re
import os

from bs4 import BeautifulSoup

# open the url and read
def getHtml(url):
    print("----------------------------", url, "---------------------------------")
    page = urllib.request.urlopen(url, timeout = 60)
    html = page.read()
    page.close()
    return html

# compile the regular expressions and find
# all stuff we need
def getDownloadList(html):
    soup = BeautifulSoup(html.decode('UTF-8'))
    span_list = soup.find_all('span', class_="srch-Title")
    download_list = map(lambda x: (x.a['href'], x.a.string), span_list)
    return download_list

def getFile(url, name):
    name = name.replace('/', '')
    file_name = name + '_' + url.split('/')[-1]
    print ("Begin to download %s from %s" % (file_name, url))
    u = urllib.request.urlopen(url, timeout=60)
    if not os.path.exists('download'):
        os.mkdir('download')
    f = open(os.path.join('download/', file_name), 'wb')

    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        f.write(buffer)
    f.close()
    print ("Sucessful to download %s from %s" % (file_name, url))

root_url = 'http://search.envir.cn/results.aspx?'  #下载地址中相同的部分

for i in range(115, 400):
    url = root_url + "k=%s&start1=%s"%(urllib.parse.quote("环评 pdf"), i * 10 + 1)
    try:
        html = getHtml(url)
    except Exception:
        print("Can't get html from %s" % url)
        f1 = open("pageErr", 'a+')
        f1.write(url + '\n')
        f1.close()
    else:
        download_list = getDownloadList(html)
        for download_url, name in download_list:
            try:
                getFile(download_url, name)
            except Exception:
                print("Unable to download from %s" % download_url)
                f2 = open("pdfErr", 'a+')
                f2.write(download_url + '\n')
                f2.close()

