# coding=utf-8
import time
import urllib
import sys
from selenium import webdriver        
from bs4 import BeautifulSoup

boke_problem_file = "boke_problem.idx"
boke_content_file = "boke_content.res"

def ropen(filename):
    return open(filename, "a+")

def getProblemListPage(url):
    log = ropen(boke_problem_file)
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
            print >> log, "\t".join([score, title, href])
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

def get_link(string, idx):
    pre = ""
    for line in string.split("\n"):
        line = line.strip()
        if pre.startswith(u"参考"):
            print idx, line
        pre = line

def getPageDetail(filename, download=False, writelog=False):
    log = ropen(boke_content_file)
    with open(filename) as f:
        for line in f:
            line = line.strip()
            idx, title, url = line.split("\t")
            path = "pages/" + idx + ".html"
            #download problem page
            if download:
                detailPick(path, url)

            title, content = contentPick(path)
            if writelog:
                print >> log, "path:" + path
                print >> log, "title:" + title.encode("utf8")
                print >> log, content.encode("utf8")

            #get_link(content, idx)
            #break

if __name__ == '__main__':
    begin_url = "https://www.cnblogs.com/grandyang/p/4606334.html"
    
    func = sys.argv[1]
    if func == "getidx":
        #get leetcode problem idx\ title\ url
        getProblemListPage(begin_url)
    elif func == "download":
        #save problem html page
        getPageDetail(boke_problem_file)
    else:
        print "argments error"

