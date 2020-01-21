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

def detailPick(filename):
    res = []
    res_item = []
    cate_dic = {}
    sim_dic  = []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if line.startswith("path:"):
                #print res_item
                if len(res_item) != 0:
                    res.append(res_item)

                flag, ret = categoryPick(res_item)
                if flag != None:
                    #print "\t".join(ret)
                    flag = int(flag)
                    for item in ret:
                        if item not in cate_dic:
                            cate_dic[item] = set([flag])
                        else:
                            cate_dic[item].add(flag)


                flag, ret = simPick(res_item)
                if flag != None:
                    #flag = int(flag)
                    #print "\t".join(ret)
                    sim_dic.append(ret)

                #print "\t".join(ret)
                res_item = []
            res_item.append(line)
    return cate_dic, sim_dic

def categoryPick(data_list):
    idx = data_list[0].replace("path:leet/", "").replace(".html", "")
    if not idx.isdigit():
        return None, []
    res = []
    flag = 0
    for item in data_list:
        if "相关标签" in item:
            res = []
            flag = 1
            continue
        if "相似题目" in item or "显示提示" in item or "题目列表" in item:
            break
        res.append(item.strip())
    if flag == 1:
        #print idx
        return idx, res
    else:
        return None, []

def simPick(data_list):
    idx = data_list[0].replace("path:leet/", "").replace(".html", "")
    if not idx.isdigit():
        return None, []
    res = []
    flag = 0
    for item in data_list:
        if "相似题目" in item:
            res = []
            flag = 1
            continue
        if "显示提示" in item or "题目列表" in item:
            break
        if "简单" in item or "中等" in item or "困难" in item:
            continue
        else:
            res.append(item.strip())
    if flag == 1:
        return idx, res
    else:
        return None, []

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

num_dic = {
        1: "一",
        2: "二",
        3: "三",
        4: "四",
        5: "五",
        6: "六",
        7: "七",
        8: "八",
        9: "九",
        10:"十",
        11:"十一",
        12:"十二",
        13:"十三",
        14:"十四",
        15:"十五",
        16:"十六",
        17:"十七",
        18:"十八",
        19:"十九",
        20:"二十",
        21:"二一",
        22:"二二",
        23:"二三",
        24:"二四",
        25:"二五",
        26:"二六",
        27:"二七",
        28:"二八",
        29:"二九",
        30:"三十",
        31:"三一",
        32:"三二",
        33:"三三",
        34:"三四",
        35:"三五",
        36:"三六",
        37:"三七",
        38:"三八",
        39:"三九"
        }

if __name__ == '__main__':
    begin_url = "https://leetcode-cn.com/problemset/all/"

    #get leetcode problem idx title url
    #getProblemListPage(begin_url)

    #save problem html page
    #getPageDetail("problem.idx")

    #getPageDetail("leetcode.idx", 204)

    cate_dic, sim_dic = detailPick("leet.log")

    print len(cate_dic)
    gcounter = 0
    print "* Summary\n"
    print "* [序](Abstract.md)"
    print "* [前言](README.md)"
    for k, v in cate_dic.items():
        gcounter += 1
        ch_counter = num_dic[gcounter]
        print "* [" + ch_counter + "、" + k + "](Chapter" + str(gcounter) +  "/README.md)"

        v = list(v)
        v = sorted(v)
        #print v

        res = []
        item_res = []
        counter = 0
        chapter = 1
        for item in v:
            counter += 1
            #print counter
            item_res.append(item)
            if counter == len(v):
                print "    * [第" + str(chapter) + "节](Chapter" + str(gcounter) + "/" + str(counter) + ".md)"
                print "\n".join([str(i) for i in item_res])
                res.append(item_res)
            if counter % 12 == 0:
                print "    * [第" + str(chapter) + "节](Chapter" + str(gcounter) + "/" + str(counter) + ".md)"
                chapter += 1
                print "\n".join([str(i) for i in item_res])
                res.append(item_res)
                item_res = []
            
            
