# -*- coding: utf-8 -*-
"""
获取豆瓣电影排行榜所有评论
豆瓣电影排行榜url: https://movie.douban.com/chart
"""

from scrapy.http import Request
import random
# import sys
# import numpy as np
import scrapy
import re
# from copy import deepcopy
import time
from math import ceil
from .selenium_login import getCookies


class DoubanSpider(scrapy.Spider):
    start_urls = []
    url_list = []
    # 加载需要爬取的豆瓣用户观影记录首页
    with open('user_movie.csv') as file:
        num = 0
        userurl = file.readlines()
        for line in userurl:
            if num == 0:
                start_urls.append(line.replace("\n", ""))
                num += 1
            else:
                url_list.append(line.replace("\n", ""))
    flag = -1
    name = 'douban'
    allowed_domains = ['movie.douban.com']

    # 手动登录 获取cookies
    cookies = getCookies()

    # 重载start_requests方法
    def start_requests(self):
        # 指定cookies 再次请求到详情页，并且声明回调函数callback
        yield Request(self.start_urls[0], cookies=self.cookies, callback=self.parse)

    def parse(self, response):
        #  处理页面内容
        movies_num = response.xpath(
            '//*[@id="db-usr-profile"]/div[2]/h1').extract()[0]
        user_url = response.url
        pattern = r'\((\d+)\)'

        #  记录当前用户链接
        print(user_url)

        # 获取用户观影记录数量， 进行随机页面选择， 大于350部，进行采样
        watchedMovie = int(re.findall(pattern, movies_num)[0])
        page_num = ceil(watchedMovie / 15)
        if watchedMovie > 350:
            chioce_page_num = random.sample(range(1, page_num), 22)
        else:
            chioce_page_num = random.sample(range(1, page_num+1), page_num)

        self.writeUserAndRandomInfo(
            user_url+","+str(watchedMovie)+","+str(chioce_page_num))

        for index in chioce_page_num:
            url = str(user_url) + '?start=' + str((index-1)*15) + \
                '&sort=time&rating=all&filter=all&mode=grid'
            time.sleep(random.choice([2, 1.9, 2.5]))
            yield scrapy.Request(
                url=url,
                callback=self.parse_page_url,
                meta={"index": index, "User_url": user_url}
            )

        next_url = self.getNextURl()

        time.sleep(random.choice([2.5, 2]))
        yield scrapy.Request(
            url=next_url,
            callback=self.parse
        )

    def writeUserAndRandomInfo(self, item):
        with open('UserAndRandomInfo.csv', 'a', encoding='utf-8') as file:
            file.write(item + "\n")

    def parse_page_url(self, response):
        User_url = response.meta.get('User_url')  # 取出值
        movie_url_info = response.xpath(
            '//*[@id="content"]/div[2]/div[1]/div[2]/div/div[2]/ul/li[1]/a').extract()
        movie_rate = response.xpath(
            '//*[@id="content"]/div[2]/div[1]/div[2]/div/div[2]/ul/li[3]/span[1]').extract()
        pattern = r'href="(.*?)"'
        i = 0
        for url in movie_url_info:
            movie_url = re.findall(pattern, url)
            self.writeMovieURL(
                movie_url[0]+","+User_url+","+str(movie_rate[i]))
            i += 1

    def writeMovieURL(self, item):
        with open('MovieURL.csv', 'a', encoding='utf-8') as file:
            file.write(item + "\n")

    def getNextURl(self):
        self.flag += 1
        return self.url_list[self.flag]
