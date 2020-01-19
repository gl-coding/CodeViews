# coding=utf-8
import time
import urllib
from selenium import webdriver        
from bs4 import BeautifulSoup

def getProblemListPage(url):
    driver = webdriver.Chrome()
    driver.get(url)
    #歇两秒
    time.sleep(2)

    #找到入口xpath节点
    entrys = driver.find_elements_by_xpath("//div[@id='cnblogs_post_body']")
    #1.确定是否唯一
    print len(entrys)
    #2.确定使用的索引
    entry_idx = 0

    #分层，该用相对路径.//
    parts = entrys[entry_idx].find_elements_by_xpath(".//tr")
    #1.确定分层数
    print len(parts)

    #2.分层处理（多层处理用for循环）
    for part in parts:
        #不需要指定索引，用的是find_elements，node不是list类型
        try:
            nodes = part.find_elements_by_xpath(".//td")
            href  = part.find_element_by_xpath(".//a").get_attribute("href")
            score = nodes[0].text
            title = nodes[1].text
            print "\t".join([score, title, href])
        except:
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

def getPageDetail(filename):
    with open(filename) as f:
        for line in f:
            line = line.strip()
            idx, title, url = line.split("\t")
            path = "pages/" + idx + ".html"
            print "path:" + path
            #download problem page
            #detailPick(path, url)
            title, content = contentPick(path)
            print "title:" + title.encode("utf8")
            print content.encode("utf8")
            #break

if __name__ == '__main__':
    begin_url = "https://www.cnblogs.com/grandyang/p/4606334.html"

    #get leetcode problem idx title url
    #getProblemListPage(begin_url)

    #save problem html page
    getPageDetail("problem.idx")

