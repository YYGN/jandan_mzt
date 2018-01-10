# !/usr/bin/env python
# -*- coding: utf-8 -*-

'''
这是一个用selenium+PhantomJS绕过http://jandan.net/ooxx
网站的反爬机制，直接存储图片的爬虫程序。
'''

# 导入基本库
import os
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
from hashlib import md5
from multiprocessing import Pool


# 用selenium方法取得网页完整的html文件
def get_html(url):
    driver = webdriver.PhantomJS()
    driver.get(url)
    pages = driver.find_element_by_css_selector('.current-comment-page').text.strip('[]')
    # 返回网页完整html
    html = driver.page_source
    print('现在开始下载%s的图片！' % driver.current_url)
    driver.quit()
    return html
		

# 解析得到的html
def parse_html(html):
    # 采用beautifulsoup来解析网页，也可以用其他的解析器
    soup = BeautifulSoup(html, 'lxml')
    lis = soup.select('.view_img_link')
    link_list = ['http:' + li.get('href') for li in lis]
    return link_list


# 根据得到的图片链接用requests存储图片
def save_img(link):
    # 设置存储路径
    img_path = r'D:\Mzitu'
    os.chdir(img_path)
    # 请求得到图片的二进制文件
    content = requests.get(link).content
    filename = md5(content).hexdigest() + link[-4:]
    # 采用md5的方式对重复图片进行筛选
    if not os.path.exists(filename):
        with open(filename, 'wb') as f:
            f.write(content)
            print('%s 保存成功！' % filename)
            f.close()
        return None
    else:
        print('%s 文件已经存在了!' % filename)
        return None




def spider(url):
    html = get_html(url)
    for link in parse_html(html):
        save_img(link)

if __name__ == '__main__':
    base_url = 'http://jandan.net/ooxx/'
    url_list = sorted([base_url + 'page-%s#comments' % str(page) for page in range(1, 500)], reverse=True)
    # 开启多进程
    pool = Pool()
    pool.map(spider, url_list)
    pool.close()
    pool.join()