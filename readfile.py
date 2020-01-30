#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import urllib.parse

#いいね！するワード（ハッシュタグ）を格納する配列を作成する関数
#numにはコマンド実行時の引数１が入る
def readWords(file_words):

    file_check = os.path.isfile(file_words)
    if file_check:#ファイルが存在した
        print("######################################################################")
        print(file_words + "を読み込みました。以下ワードのハッシュタグ付き投稿をいいねします。")
        words = []
        with open(file_words,'r') as f:
            for row in f:
                if row != "":
                    word = row.strip()
                    print(word + ",",end="")
                    #URLにそのまま日本語は入れられないので、エンコードする
                    words.append(urllib.parse.quote(word))
        print("\n######################################################################")
    else:#ファイルが存在しなかった
        print( file_words + "が見つかりません。処理を終了します。" )
        exit()

    return words


#本日のいいね！した回数を取得する関数
def getLikesCntToday(today,file_l_cnt):

    likes_cnt = ""
    data_other_than_today = ""
    file_check = os.path.isfile(file_l_cnt)
    if file_check:#ファイルが存在した

        with open(file_l_cnt,'r') as f:
        	for row in f:
        		if row != "":
        			date,num = row.split('\t')
        			#print(date)
                    #print(likes_cnt)
        			if date == today:
        				likes_cnt = int(num.strip())
        			else:
        				data_other_than_today += row
        f.close()
        #ファイル内に本日の日付が見つからなかった場合
        if likes_cnt == "":
        	f = open(file_l_cnt,'a')
        	f.write(today + '\t0\n')
        	likes_cnt = 0
        	f.close()

    else:#ファイルが存在しなかった
        f = open(file_l_cnt,'w')
        f.write(today + '\t0\n')
        likes_cnt = 0
        f.close()

    print("本日（{0}）すでにいいね！している数 : {1}".format(today,likes_cnt))
    return likes_cnt,data_other_than_today


#すでにいいね！したURLの読み込み、2回目のいいね！はいいね！キャンセルとなってしまうため、防止機能用
def readAlreadyLikesURL(file_alu):

    already_likes_url = []
    f = open(file_alu,'r')
    for row in f:
        if row.strip() == "":
            continue
        already_likes_url.append(row.strip())
    f.close()
    return already_likes_url
