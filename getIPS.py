
"""
__author__:俺没文化（小易）
__create_time__:2018-3-24
"""
import requests
import time
from bs4 import BeautifulSoup
from os import path
import os
from lxml import etree
import re


#程序执行时长装饰器
def userdTime(fun):
    def wrapper(*args, **kwargs):
        start = time.time()
        fun(*args, **kwargs)
        end = time.time()
        return fun(*args, **kwargs), "{}s".format(round(end - start,2))
    return wrapper

#获取代理IP的类
class GetProxy:
    # 类初始化
    def __init__(self):
        self.heades = {
            'Host': 'www.xicidaili.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36'
        }
        self.url = 'http://www.xicidaili.com/nn/{}'

    # 西刺高匿代理IP爬虫
    def getHtml(self, pagenum):
        try:
            response = requests.get(self.url.format(pagenum), headers=self.heades)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(e)
            return

    #获取最大页码
    def getMaxPageNum(self):
        maxnum = []
        html = self.getHtml(1)
        if html:
            root = etree.HTML(html)
            pagenum = root.xpath('//a[contains(@href,"nn")]/text()')
            for item in pagenum:
                if re.findall('\d+',item):
                    maxnum.append(int(item))
            return max(maxnum)
        else:
            return

    #得到IP地址和端口号
    def getIp(self, html_response):
        proxy_info = []
        if html_response:
            soup = BeautifulSoup(html_response, 'lxml')
            table = soup.find_all('table', id='ip_list')
            tr_info = table[0].find_all('tr',class_=True)
            for item in tr_info:
                info = item.find_all('td')
                ip_info = ip_address,ip_port,q_http = info[5].get_text(),info[1].get_text(),info[2].get_text()
                proxy_info.append(ip_info)
            return proxy_info
        else:
            return

    #验证是否可用
    @userdTime
    def isAlive(self,proxy_addr,proxy_port,q_http):
        proxy_url = 'http://{}:{}'.format(proxy_addr,proxy_port)
        url = 'https://www.baidu.com/'
        proxies = {q_http: proxy_url}
        r = requests.get(url,proxies=proxies,timeout=4)
        if r.status_code == 200:
            return True
        else:
            print(r.status_code)
            return False

    #将可用的写入文本备用
    def write_proxies(self,info):
        with open('ips.txt','a') as f:
            f.write(info)
            f.write('\n')

    #主程序
    def main(self):
        if path.isfile('ips.txt'):
            os.remove('ips.txt')
        proxies = GetProxy()
        maxnum = proxies.getMaxPageNum()
        if maxnum:
            for i in range(1, maxnum+1):
                html = proxies.getHtml(1)
                info = proxies.getIp(html)
                for item in info:
                    if proxies.isAlive(*item)[0]:
                        print(["OK ",*item, proxies.isAlive(*item)[1]])
                        proxies.write_proxies(" ".join(item))
        else:
            print('最大页码获取失败')
            return

if __name__ == '__main__':
    Proiexs = GetProxy()
    Proiexs.main()

