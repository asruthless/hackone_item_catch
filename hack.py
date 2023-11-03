import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import requests_html
import os
from bs4 import BeautifulSoup
import time
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys  # 模仿键盘,操作下拉框的
from selenium.common.exceptions  import TimeoutException
import re
import numpy as np
from selenium.webdriver.common.by import By
import pandas as pd
import shutil

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--proxy-server=http://127.0.0.1:7890')
chrome_options.add_argument(
    'User-Agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36')

# 创建Chrome实例 。
chrome_path1 = r"C:\Users\12936\Downloads\chromedriver-win64 (1)\chromedriver-win64\chromedriver.exe"
browser = webdriver.Chrome(options = chrome_options,executable_path=chrome_path1)
browser.maximize_window()
def pulldown():
    url = "https://hackerone.com/opportunities/all/search?bbp=true&asset_types=CIDR%2CURL%2COTHER_IPA%2COTHER%2CHARDWARE%2CIP_ADDRESS%2CWILDCARD&ordering=Newest+programs"
    browser.get(url)
    browser.refresh()
    browser.set_page_load_timeout(3)
    #页面加载向下拖动
    browser.refresh()
    t = True
    i = 1
    while t:
        try:
            check_height = browser.execute_script("return document.body.scrollHeight;")
            for r in range(20):
                t = random.uniform(1, 2)
                browser.execute_script("window.scrollBy(0,document.body.scrollHeight)")
                time.sleep(t)
            check_height1 = browser.execute_script("return document.body.scrollHeight;")
        except TimeoutException:
            print("1232132321321321")
            browser.refresh()
            continue
        if check_height == check_height1:
            if check_height1 > 24400:
                print(check_height)
                t = False
            else:
                browser.refresh()
                continue
    check_height = browser.execute_script("return document.body.scrollHeight;")
    for r in range(20):
        t = random.uniform(1, 2)
        browser.execute_script("window.scrollBy(0,document.body.scrollHeight)")
        time.sleep(t)
    check_height1 = browser.execute_script("return document.body.scrollHeight;")



page_source = browser.page_source

listcompany = []
listurl = []
money = [[0 for i in range(2)] for j in range(200)]


def company_name_and_url():
    with open('test.txt', 'w',encoding='utf-8') as f:
        f.write(page_source)
    with open( 'test.txt', 'r' ) as f:
        r=f.read()
        rs = re.findall(r'<span.*?w-0.*?>(.*?)</span>', r, re.S)
        for j in rs:
            listcompany.append(j)
        url2 = re.findall(r'<a.?data-testid.*?href="(.*?)">', r, re.S)
        print(rs)
        url1 = "https://hackerone.com"
        for i in url2[1:]:
            listurl.append(url1+i)
    with open('company_name.txt','w',encoding='utf-8') as f:
        for k in listcompany:
            f.write(k+'\n')
    with open('company_url.txt','w',encoding='utf-8') as f:
        for k in listurl:
            f.write(k+'\n')

time.sleep(4)

listcompanyname = []
def write_company_name():   #别关
    with open('company_name.txt', 'r') as f:
            a = f.readline().replace("\n","")
            while a is not None and a != '':
                listcompanyname.append(a)
                a = f.readline().replace("\n", "")  # 读取下一行
write_company_name()

def get_company_first_list():   # 保存每个首页地址内容
    with open('company_url.txt', 'r') as f:
        a = f.readlines()
        count = -1
        for i in a:
            count += 1
            try:
                browser.get(i)
                browser.set_page_load_timeout(3)
                time.sleep(3)
            except TimeoutException:
                print("重试")
                browser.refresh()
                browser.set_page_load_timeout(2)
                continue
            page_source = browser.page_source
            with open(f'file/{listcompanyname[count]}.txt', 'w', encoding='utf-8') as f:
                f.write(page_source)




def get_average_money_of_company():
            count=-1
            length=0
            list1 = -1
            for i in listcompanyname:

                list1+=1
                count+=1
                with open(f'file/{i}.txt', 'r', encoding='utf-8') as f:
                    r = f.read()
                    rc = re.findall(
                        r'<div class="sc-aXZVg cYeGpe flex--left-border">.*?<div class="flex margin-24--right team-cta__wrapper flex-col gap-sm.*?>',
                        r, re.S)
                with open(f'file/testmoney.txt', 'w', encoding='utf-8') as f:
                    for i in rc:
                        f.write(i)

                with open(f'file/testmoney.txt', 'r', encoding='utf-8') as f:
                    r = f.read()
                    rs = re.findall(r'<span>(.?\d+)</span>', r, re.S)
                count1 = 0
                for j in rs:
                    money[count][count1] = j
                    count1 += 1
                    length+=1
get_average_money_of_company()

policyurl = []
def get_policy_url():
    with open(f'company_url.txt', 'r', encoding='utf-8') as f:
        a = f.readline().replace("?type=team", "/policy_scopes")
        while a is not None and a != '':
            policyurl.append(a)
            a = f.readline().replace("?type=team", "/policy_scopes")
get_policy_url()

def get_csv_file_url():
    csv_url = []
    with open(f'company_url.txt', 'r', encoding='utf-8') as f:
        a = f.readline().replace("https://hackerone.com", "https://hackerone.com/teams").replace("?type=team\n","/assets/download_csv.csv")
        while a is not None and a != '':
            csv_url.append(a)
            a = f.readline().replace("https://hackerone.com", "https://hackerone.com/teams").replace("?type=team\n","/assets/download_csv.csv")
    with open(f'download_csv_url.txt', 'w', encoding='utf-8') as f:
        for i in csv_url:
            f.write(i + '\n')


csvlist = []
def uselist_for_csv_url():
    with open(f'download_csv_url.txt', 'r', encoding='utf-8') as f:
        a = f.readline().replace("\n", "")
        while a is not None and a != '':
            csvlist.append(a)
            a = f.readline().replace("\n", "")  # 读取下一行
    print("创建完成")
uselist_for_csv_url()


def update_policy_page():
    shutil.rmtree(r'D:\python\csv')  # 清空并创建文件夹
    os.mkdir(r'D:\python\csv')
    chrome2_options = webdriver.ChromeOptions()
    chrome2_options.add_argument('--proxy-server=http://127.0.0.1:7890')
    chrome2_options.add_argument(
        'User-Agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36')
    chrome2_options.add_argument('--headless')
    prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': 'D:\\python\\csv'}
    chrome2_options.add_experimental_option('prefs', prefs)
    chrome_path2 = r"C:\Users\12936\Downloads\chromedriver-win64 (1)\chromedriver-win64\chromedriver.exe"
    browser2 = webdriver.Chrome(options = chrome2_options,executable_path=chrome_path2)
    browser2.minimize_window()
    for i in csvlist:
        try:
            browser2.get(i)
            time.sleep(3)
            time.sleep(3)
        except TimeoutException:
             print("超时")
             time.sleep(3)
             continue
    browser2.quit()



def read_detail_for_item():
    name1 = input("输入想要查看的项目名称: ")
    item_name = name1.lower()
    path = r"D:\python\csv"
    datanames = os.listdir(path)
    for i in datanames:
        a=(os.path.splitext(i)[0]).split('_')[2]
        if item_name == a:
            csvfilepath=path+"\\"+i
            reader = pd.read_csv(csvfilepath,keep_default_na=False)
            pd.set_option('display.unicode.ambiguous_as_wide', True)
            pd.set_option('display.unicode.east_asian_width', True)
            pd.set_option('display.max_columns', None)
            pd.set_option('display.max_rows', None)
            pd.set_option('display.width', None)

            reader["eligible_for_bounty"]=reader["eligible_for_bounty"].astype(str)
            print(reader[reader["eligible_for_bounty"].str.contains('T')])


def oupput_item_and_money():
    count = 0
    x=30
    for i in  listcompanyname[0:x]:
        print(f"名称：{listcompanyname[count]},平均赏金:{money[count][0]}---{money[count][1]}")
        count+=1
    a = input("输入回车继续显示：")
    if a=='':
        for i in listcompanyname[x:]:
            print(f"名称：{listcompanyname[count]},平均赏金:{money[count][0]}---{money[count][1]}")
            count += 1


if __name__ == "__main__":
    print("输入对应值: \n update : 更新所有项目内容\n itemlist: 列出所有项目名称和平均赏金 \n itemdetail:查看想要项目的详细内容 \n exit: 退出 ")


    def updateitem():
        pulldown()
        print("重新抓取首页完毕------（1/6）")
        company_name_and_url()
        print("更新url和内容完毕------（2/6）")
        print("项目列表内容读取完毕-----（3/6）")
        get_company_first_list()
        print("项目首页读取完毕-----（4/6）")
        get_csv_file_url()
        print("获取csv文件下载地址-----（5/6）")
        update_policy_page()
        print("csv文件更新完毕-----（6/6）")
   # updateitem()


    def default():  # 执行默认函数
        print('No such  fun')


    def out():
        exit()

    while True:
        switch_dict = {
            'update': updateitem,
            'itemlist': oupput_item_and_money,
            'itemdetail': read_detail_for_item,
            'exit': out,
        }

        a = input("")
        switch_dict.get(a, default)()  # 根据key执行对应的函数，如果没有就执行默认的函数
        print("输入对应值: \n update : 更新所有项目内容\n itemlist: 列出所有项目名称和平均赏金 \n itemdetail:查看想要项目的详细内容 \n exit: 退出 ")