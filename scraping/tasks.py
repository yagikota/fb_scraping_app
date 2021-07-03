from __future__ import absolute_import, unicode_literals
from django.core.management.base import BaseCommand, CommandError
from .models import Page, Advertisement
from selenium import webdriver
from time import sleep
import chromedriver_binary
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import re
import concurrent.futures
from celery import shared_task

page_ids = {page.page_id for page in Page.objects.all()}

@shared_task
def scraping():
    page_ids = {page.page_id for page in Page.objects.all()}
    def _scrape(page_id):
        options = Options()
        # options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
        page_url = 'https://www.facebook.com/ads/library/?active_status=all&ad_type=all&country=JP&view_all_page_id='+str(page_id)+'&search_type=page'
        driver.get(page_url)
        sleep(5)

        # 最下部までスクロール
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # pre_scroll_top = -1
        # curr_scroll_top = 0
        # print(pre_scroll_top)
        # print(curr_scroll_top)
        # while pre_scroll_top != curr_scroll_top:
        #     pre_scroll_top = curr_scroll_top
        #     curr_scroll_top = driver.execute_script("return document.body.scrollTop || document.documentElement.scrollTop;")
        #     sleep(5)
        #     print(pre_scroll_top)
        #     print(curr_scroll_top)

        html = driver.page_source.encode('utf-8')
        soup = BeautifulSoup(html, features="html")

        # いいねの数
        likes = driver.find_element_by_css_selector("#content > div > div > div > div._7lcc > div._8n-_ > div:nth-child(1) > div > div > div:nth-child(1) > div > div > div > div > span:nth-child(2) > div > div:nth-child(2) > div:nth-child(2) > div:nth-child(1)")
        likes = likes.text.split(' ')[0]
        likes = int(re.sub(r"\D", "", likes))
        # print(likes)
        # ページ名
        page_name = driver.find_element_by_css_selector("#content > div > div > div > div._7lcc > div._8n-_ > div:nth-child(1) > div > div > div:nth-child(1) > div > div > div > div > div > div > div > a > div > span")
        page_name = page_name.text
        # print(page_name)
        # カテゴリ
        category = driver.find_element_by_css_selector("#content > div > div > div > div._7lcc > div._8n-_ > div:nth-child(1) > div > div > div:nth-child(1) > div > div > div > div > span:nth-child(2) > div > div:nth-child(2) > div:nth-child(2) > div:nth-child(2)")
        category = category.text
        # print(category)

        parent = Page.objects.create(name=page_name, page_id=page_id, likes=likes, category=category)

        # #全ての広告を取得
        advertisements = soup.find_all("div", class_="_99s5")
        ad_queries = []
        i = 1

        for ad in advertisements:
            # ID
            ad_id = int(ad.find("span", class_="l61y9joe jdeypxg0 and5a8ls te7ihjl9 svz86pwt jrvjs1jy a53abz89").text[4:])
            # ステータス
            status = ad.find("div", class_="_9cd2").text
            # 掲載開始日
            started_running_on = ad.find_all("span", class_="l61y9joe jdeypxg0 and5a8ls te7ihjl9 svz86pwt ippphs35 a53abz89")[1].text
            # ID
            ad_id = int(ad.find("span", class_="l61y9joe jdeypxg0 and5a8ls te7ihjl9 svz86pwt jrvjs1jy a53abz89").text[4:])
            # メインテキスト
            main_text = ad.find_all("div", class_="_4ik4 _4ik5")[1].text
            # 画像
            # 画像, 動画
            image_url = ad.find("img", class_="_7jys img")
            # print(image_url)
            if image_url is not None:
                image_url = image_url.get("src")
            else:
                image_url = ad.find("video")
                if image_url is not None:
                    image_url = ad.find("video").get("src")
            lp_url = ad.find("a", class_="d5rc5kzv chuaj5k6 l61y9joe j8otv06s a1itoznt fvlrrmdj svz86pwt aa8h9o0m jrvjs1jy jrkk970q").get("href")

            # Advertisement.objects.create(parent=parent, status = status, started_running_on = started_running_on, main_text=main_text, ad_id=ad_id, image_url=image_url, lp_url=lp_url)
            ad = Advertisement(parent=parent, status = status, started_running_on = started_running_on, main_text=main_text, ad_id=ad_id, image_url=image_url, lp_url=lp_url)
            ad_queries.append(ad)
            i += 1
        Advertisement.objects.bulk_create(ad_queries)
        print(i)
        driver.quit()

    # 並列処理
    executor = concurrent.futures.ThreadPoolExecutor()
    for page_id in page_ids:
        executor.submit(_scrape, page_id)


