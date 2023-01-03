# TripBuilder Algorithm Team

import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import urllib.request
import json
import re
import time

from selenium import webdriver
from selenium.webdriver.common.by import By

# 네이버 검색/블로그/플레이스 등
class NaverCrawler:
    def __init__(self):
        self.API_keys = [{"client_id":"0mK4JnoFJM1CPYWNlG80","client_secret":"UMINhUjvKQ"},
                    {"client_id":"HSGXhbVLnjvb31S9N_cB","client_secret":"4r9gnASzKU"}]
        self.HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"}
    def HELP(self):
        print("[get_BlogURL]:input=query,num\n  -query:검색어\n  -num:크롤링 할 글 수 결정\n  >>output:[url1, url2, ...]\n")
        print("[get_BlogInfo]:input=url,image\n  -url:블로그 링크\n  -image:TRUE/FALSE,이미지까지 크롤링할지 결정\n  >>output:\"안녕하세요. 오늘은 ...\", [img1, img2, ...]\n")
        print("[get_NaverPlace]:input=location,name\n  -location:장소 위치\n  -name:장소명\n  >>output:[category, tel_num, review, extra_inform]")
    def get_BlogURL(self,query,num):
        keyword = ["상권분석", "부동산", "방문자리뷰수", "리뷰수", "소셜커머스", "금리", "매물", "매매", "급등", "광고"]
        Search = urllib.parse.quote(query)

        start = 1; size = num
        url = f"https://openapi.naver.com/v1/search/blog?query={Search}&start={start}&display={size}"  # json 결과

        for API in self.API_keys:
            request = urllib.request.Request(url)
            request.add_header("X-Naver-Client-Id", API["client_id"])
            request.add_header("X-Naver-Client-Secret", API["client_secret"])
            response = urllib.request.urlopen(request)
            rescode = response.getcode()
            blog_url = []
            if (rescode == 200):
                response_body = response.read()
                msg = response_body.decode('utf-8')
                blog = json.loads(msg)['items']
                for blog_info in blog:
                    for word in keyword:
                        if (word in blog_info['title'].split(" ")):
                            continue
                    blog_url.append(blog_info['link'])
                break
            else:
                continue

        return blog_url
    def get_BlogInfo(self,url,img=False):
        cont = ''; imgs = []
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            ifra = soup.find('iframe', id='mainFrame')
            post_url = 'https://blog.naver.com' + ifra['src']
            res = requests.get(post_url)
            soup2 = BeautifulSoup(res.text, 'html.parser')

            txt_contents = soup2.find_all('div', {'class': "se-module se-module-text"})

            for p_span in txt_contents:
                for txt in p_span.find_all('span'):
                    cont += txt.get_text()
                if(img==True):
                    imgs = soup2.find_all('img', class_='se-image-resource')
        except:
            pass
        return cont, imgs
    def get_NaverPlace(self,location,name):
        url = "https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=" + f"{quote(location)}+{quote(name)}"
        res = requests.get(url, headers=self.HEADERS)
        soup = BeautifulSoup(res.text, "lxml")
        naver_place = soup.find_all("div", attrs={"class": "api_subject_bx"})[0]

        # 카테고리 가져오기
        category = naver_place.find("span", attrs={"class": "DJJvD"}).get_text()
        # 전화번호 가져오기
        try:
            tel = naver_place.find("li", attrs={"class": "SF_Mq SjF5j Xprhw"})
            tel_num = tel.find("span", attrs={"class": "dry01"}).get_text()
        except:
            tel_num = None
        # 방문자 리뷰 가져오기
        try:
            rev = naver_place.find("ul", attrs={"class": "flicking-camera"})
            reviews = rev.find_all("li", attrs={"class": "nbD78"})
            # num_review = len(reviews)
            txt = []
            for review in reviews:
                txt.append(review.find("span", attrs={"class": "nWiXa"}).get_text()[1:-2])
        except:
            txt.append(None)
        # 기타 부가 정보
        try:
            extra = naver_place.find("div", attrs={"class": "xHaT3"})
            etc = extra.find("span", attrs={"class": "zPfVt"}).get_text()
        except:
            etc = None

        inform = [category, tel_num, txt, etc]
        return inform #

# 카카오 맵
class KakaoCrawler:
    def __init__(self):
        self.API_KEY = "bc5c15facbf4450fd684f4894286c377"
    def get_Detail(self, location, name):
        url = f"https://dapi.kakao.com/v2/local/search/keyword.json?query={location + ' ' + name}"

        result = requests.get(url, headers={"Authorization": f"KakaoAK {self.API_KEY}"})
        json_obj = result.json()

        try:
            x_position = json_obj['documents'][0]['x']
            y_position = json_obj['documents'][0]['y']
            place_url = json_obj['documents'][0]['place_url']
            detail_category = json_obj['documents'][0]['category_name']
            position_XY = [x_position, y_position]
        except:
            position_XY = [np.nan, np.nan]
            place_url = np.nan
            detail_category = np.nan

        return position_XY, place_url, detail_category
    def get_PosXY(self,location,name):
        url = f"https://dapi.kakao.com/v2/local/search/keyword.json?query={location + ' ' + name}"

        result = requests.get(url, headers={"Authorization": f"KakaoAK {self.API_KEY}"})
        json_obj = result.json()

        try:
            x_position = json_obj['documents'][0]['x']
            y_position = json_obj['documents'][0]['y']
            position_XY = [x_position, y_position]
        except:
            position_XY = [np.nan, np.nan]
        return position_XY
    def get_PlaceInfo(self):
        return 0

# 트위터
class TwitCrawler:
    def __init__(self):
        self.API_keys = {"Key":"9eOpfLcdERN8yvwkCmOzm5s5C",
                         "Secret":"YpKspw0SVTIZVpSipBLyiwnAmsjNmpeTiTlVGb4uXQm8CdZ7Na",
                        "Bearer":"AAAAAAAAAAAAAAAAAAAAAAPfgwEAAAAAtR5Rp9Zp2faQ80zwQ42tg9cnpY8%3D6uV8tn95JW5qq0lAyftKxwp9dIY13x60JpK6MD3ajQJ1PiAlRs"}
        self.ACCOUNT = {"id":"teamtripbuilder@gmail.com",
                     "pw":"unist2021!"}
        print("WARNING: The [TwitCrawler] is still under development.")

# 구글 맵
class GoogleMap:
    def __init__(self):
        self.API_Key = "AIzaSyBhcuH45NaLJEqVuqGG7EmPqPPIJq9kumc"
        print("WARNING: The [GoogleMap] is still under development.")

# 기상청 API
class ExtraCrawler:
    def __init__(self):
        self.API_Key = "bejQ3PaK3jyOBGfWQDVAd6GFLmvUtQ7ppZhrs7IBiF7TuwiD0xb5JEdjb9JEPFTlDZna8U84TjhCUILWeP7n3Q%3D%3D"
        print("WARNING: The [ExtraCrawler] is still under development.")
    def getWeather(self,place,date):
        return place, date

########[EXAMPLE CODE]########
#crawler = NaverCrawler()
#crawler.HELP()
