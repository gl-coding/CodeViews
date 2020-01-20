# coding=utf-8
import time
import urllib
import traceback
from selenium import webdriver        
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def getProblemListPage(url):
    driver = webdriver.Chrome()
    driver.get(url)
    #歇两秒
    time.sleep(2)

    #找到入口xpath节点
    entrys = driver.find_elements_by_xpath("//div[@class='table-responsive question-list-table']")
    #1.确定是否唯一
    print len(entrys)
    time.sleep(10)

    #2.确定使用的索引
    entry_idx = 0

    #分层，该用相对路径.//
    parts = entrys[entry_idx].find_elements_by_xpath(".//tr")
    #1.确定分层数
    print len(parts)

    #2.分层处理（多层处理用for循环）
    counter = 0
    for part in parts:
        counter += 1
        #不需要指定索引，用的是find_elements，node不是list类型
        try:
            #href  = part.get_attribute("href")
            nodes = part.find_elements_by_xpath(".//td")
            flag = nodes[0].find_elements_by_xpath(".//i")
            typ = 0
            if len(flag) == 0:
                typ = 1
            typ = str(typ)
            num = nodes[1].text
            url = nodes[2].find_element_by_xpath(".//a").get_attribute("href")
            tit = nodes[2].find_element_by_xpath(".//a").text
            lev = nodes[5].text
            print "\t".join([typ, num, url, tit, lev]).encode("utf8")
            #print "\t".join([score, title, href])
        except:
            traceback.print_exc()
            continue

    #完成，退出
    driver.quit()

def detailPick(filename, url):
    html = urllib.urlopen(url).read()
    with open(filename, "w+") as f:
        f.write(html)

def contentPick(path):
    htmlfile = open(path, 'r')
    soup = BeautifulSoup(htmlfile, 'lxml')
    entrys = soup.find_all('div', id='cnblogs_post_body')
    title = soup.find('a', class_='postTitle2')
    return title.string, entrys[0].text

def get_link(string, idx):
    pre = ""
    for line in string.split("\n"):
        line = line.strip()
        if pre.startswith(u"参考"):
            print idx, line
        pre = line

def getPageDetail(filename, begin_idx=0):
    #driver = webdriver.Chrome()
    options = webdriver.ChromeOptions()
    options.set_headless()
    driver = webdriver.Chrome(chrome_options=options)
    with open(filename) as f:
        counter = 0
        for line in f:
            counter += 1
            line = line.strip()
            #print line
            #print counter
            if counter <= begin_idx:
                continue
            flag, idx, url, title, typ = line.split("\t")
            print flag
            if flag == "0":
                continue
            path = "leet/" + idx + ".html"
            print "path:" + path
            #download problem page
            #detailPick(path, url)
            driver.get(url)
            print url
            entrys = driver.find_elements_by_xpath("//div[@class='side-tools__3mLh']")
            if len(entrys) == 0:
                continue
            tag = driver.find_elements_by_xpath("//div[@class='header__22S7']")
            if len(tag) != 0:
                try:
                    tag[0].click()
                except:
                    time.sleep(1)
                    continue
            sim = driver.find_elements_by_xpath("//div[@class='header___3eQ']")
            if len(sim) != 0:
                try:
                    sim[0].click()
                except:
                    time.sleep(1)
                    continue
            #print len(entrys)
            time.sleep(1)
            print entrys[0].text
            #time.sleep(1)
            #title, content = contentPick(path)
            #print "title:" + title.encode("utf8")
            #print content.encode("utf8")
            #get_link(content, idx)
            #break
    #driver.quit()

if __name__ == '__main__':
    begin_url = "https://leetcode-cn.com/problemset/all/"

    #get leetcode problem idx title url
    #getProblemListPage(begin_url)

    #save problem html page
    #getPageDetail("problem.idx")

    getPageDetail("leetcode.idx", 204)

