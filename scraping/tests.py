# from django.test import TestCase
from django.core.management.base import BaseCommand, CommandError
# from scraping.models import Page, Advertisement
from selenium import webdriver
from time import sleep
import chromedriver_binary
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import re
import urllib
import requests
from collections import Counter
from urllib3 import request
# Create your tests here.


options = Options()
# options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
# ad_ids = [ad.ad_id for ad in Advertisement.objects.filter(parent=Page.objects.get(page_id=page_id))]
page_url = 'https://www.facebook.com/ads/library/?active_status=all&ad_type=all&country=JP&view_all_page_id=158139660914197&search_type=page'
driver.get(page_url)
sleep(5)
    
pre_scroll_top = -1
curr_scroll_top = 0
while pre_scroll_top != curr_scroll_top:
    pre_scroll_top = curr_scroll_top
    curr_scroll_top = driver.execute_script("return document.body.scrollTop || document.documentElement.scrollTop;")
    sleep(2)

html = driver.page_source.encode('utf-8')
soup = BeautifulSoup(html, features="html")

# いいねの数
likes = driver.find_element_by_css_selector("#content > div > div > div > div._7lcc > div._8n-_ > div:nth-child(1) > div > div > div:nth-child(1) > div > div > div > div > span:nth-child(2) > div > div:nth-child(2) > div:nth-child(2) > div:nth-child(1)")
likes = likes.text.split(' ')[0]
likes = int(re.sub(r"\D", "", likes))
print(likes)
# ページ名
page_name = driver.find_element_by_css_selector("#content > div > div > div > div._7lcc > div._8n-_ > div:nth-child(1) > div > div > div:nth-child(1) > div > div > div > div > div > div > div > a > div > span")
page_name = page_name.text
print(page_name)
# カテゴリ
category = driver.find_element_by_css_selector("#content > div > div > div > div._7lcc > div._8n-_ > div:nth-child(1) > div > div > div:nth-child(1) > div > div > div > div > span:nth-child(2) > div > div:nth-child(2) > div:nth-child(2) > div:nth-child(2)")
category = category.text
print(category)

def get_redirect_url(src_url):
    with urllib.request.urlopen(src_url) as res:
        url = res.geturl() # 最終的な URL を取得
    if src_url == url:
        return None # 指定された URL と同じなのでリダイレクトしていない
    else:
        return url # 指定された URL と異なるのでリダイレクトしている

advertisements = soup.find_all("div", class_="_99s5")

lps = []
for idx, ad in enumerate(advertisements[:10]):
    lp_url = ad.find("a", class_="d5rc5kzv chuaj5k6 l61y9joe j8otv06s a1itoznt fvlrrmdj svz86pwt aa8h9o0m jrvjs1jy jrkk970q").get("href")
    print(idx + 1)
    print(lp_url)
    print()
    lps.append(lp_url)

c = Counter(lps)
print(c)