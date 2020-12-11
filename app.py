#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 必要なライブラリのインポート
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib.parse
import time
import datetime
import sys
import traceback
import readfile

args = sys.argv#コマンドの引数
####################設定####################

#１日にいいね！できる最大値。この数を超えたら処理終了
max_limit_likes_counter = 500

#自動いいね！時、エラーがこの数を超えたら処理終了
max_limit_error_cnt = 10

#Instagramログイン用 ID PASS
username = "XXXXXXXXXXXXXXXXXXXX"
password = "XXXXXXXXXXXXXXXXXXXX"

#読み込みファイル名
file_words = "words_" + str(args[1]) +".txt"
file_l_cnt = "likes_cnt.txt"
file_alu = "already_likes_url.txt"

#################いいね！したいワードをファイルから取得
words = readfile.readWords( file_words )

#############本日、いいね！している数をファイルから取得
today = datetime.date.today()
today = str(today)
likes_cnt,data_other_than_today = readfile.getLikesCntToday(today,file_l_cnt)

######################すでにいいね！したURLの読み込み
already_likes_url = readfile.readAlreadyLikesURL(file_alu)

#Chromeを起動
driver = webdriver.Chrome()

#Instagram ログインURL
login_url = "https://www.instagram.com/"

#ログインボタン
#login_path = '//*[@id="react-root"]/section/main/article/div[2]/div[2]/p/a'

#ログイン用フォームへのパス
username_path = '//form//div[1]//input'
password_path = '//form//div[2]//input'

#いいね！ボタン取得用
like_x_path = '//main//section//button'

#Instagramのサイトを開く
driver.get(login_url)
time.sleep(3)

#ログインページへ ( Webページの構造が変化しており、↓の処理はいらなくなった。2020.04.04 確認 ) 
#driver.find_element_by_xpath(login_path).click()
#time.sleep(3)

#ユーザー名とパスワードを入力してリターンキーを押す
usernameField = driver.find_element_by_xpath(username_path)
usernameField.send_keys(username)
time.sleep(1)
passwordField = driver.find_element_by_xpath(password_path)
passwordField.send_keys(password)
passwordField.send_keys(Keys.RETURN)
time.sleep(3)

if "アカウントが不正使用されました" in driver.page_source:
    print(driver.page_source)
    print("ブロックされました。パスワードを変更する必要があります。")
    print("処理を終了します。")
    exit()

#####################ハッシュタグ毎のループ
#ハッシュタグ検索用のURL
tag_search_url = "https://www.instagram.com/explore/tags/{}/?hl=ja"
off = False #処理を終了する切り替えスイッチ
error_cnt = 0
for word in words:

    if off:
        break
    print("http req get hashtag page: " + tag_search_url.format(word))
    driver.get(tag_search_url.format(word))
    time.sleep(3)
    driver.implicitly_wait(10)

    #リンクのhref属性の値を取得
    mediaList = driver.find_elements_by_tag_name("a")
    hrefList = []

    #1つのハッシュタグに表示された画像のhrefを配列に格納
    for media in mediaList:
        href = media.get_attribute("href")
        if "/p/" in href:
            hrefList.append(href)

    #画像のhrefを格納した配列でループ処理
    for href in hrefList:
	#すでにいいね！していた場合はスルー
        if href in already_likes_url:
            print("[いいね！済]" + href)
        else:
            driver.get(href)
            time.sleep(2)
            try:
                driver.find_element_by_xpath(like_x_path).click()
                time.sleep(2)
                #print(driver.page_source)
                if "ブロックされています" in driver.page_source:
                    print("ブロックされました。処理を終了します。")
                    off = True
                    break

                likes_cnt += 1
                print('いいね！ {}'.format(likes_cnt))
                flc = open(file_l_cnt,'w')
                flc.write(data_other_than_today + today + '\t'  + str(likes_cnt) + '\n')
                flc.close()

                fa = open(file_alu,'a')
                fa.write(href + '\n')
                fa.close()
		
		#この地点を通過する時にいいね！"max_limit_likes_counter"回超えてたら終了
		#BAN防止
                if likes_cnt >= max_limit_likes_counter:
                    print("いいね！の上限回数({})を超えました。処理を終了します。".format(max_limit_likes_counter))
                    off = True

            except Exception as e:
                ex, ms, tb = sys.exc_info()
                print(ex)
                print(ms)
                traceback.print_tb(tb)
                error_cnt += 1
                time.sleep(5)
                if error_cnt > max_limit_error_cnt:
                    print("エラーが{}回を超えました。処理を終了します。".format(max_limit_error_cnt))
                    off = True

            if off:
                break

print("本日のいいね！回数 {}".format(likes_cnt))
#ブラウザを閉じる
#driver.quit()
