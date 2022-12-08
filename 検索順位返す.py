# このプログラムはあるクエリで検索した際に指定したサイトで何位上位かを返してくれる
import requests
from bs4 import BeautifulSoup


# import numpy as np
# from gensim.models import word2vec
#
# model = word2vec.Word2Vec.load("word2vec.gensim.model")
# similar_python = model.wv.most_similar(positive = ['Python'])
# # print(similar_python)
# # print(similar_python[0][0])#これで一個目の類似単語が抜き出せる
# for i in range(len(similar_python)): #これで類似語検索した５つの単語をquery_wordに格納出来る！
#     query_word = similar_python[i][0]
#     print(query_word)

# Google検索するキーワードを設定

# search_word = 'python'
# website_title = '初心者がPythonで作れるもの5選！すぐに作れるものを徹底解説'
# # 上位から何件までのサイトを抽出するか指定する
# pages_num = 20 + 1
#
# print(f'【検索ワード】{search_word}')
#
# # Googleから検索結果ページを取得する
# url = f'https://www.google.co.jp/search?hl=ja&num={pages_num}&q={search_word}'
# request = requests.get(url)
#
# # Googleのページ解析を行う
# soup = BeautifulSoup(request.text, "html.parser")
# search_site_list = soup.select('div.kCrYT > a')
#
# # ページ解析と結果の出力
# for rank, site in zip(range(1, pages_num), search_site_list):
#     try:
#         site_title = site.select('h3.zBAuLc')[0].text
#     except IndexError:
#         #site_title = site.select('img')[0]['alt']
#         site_url = site['href'].replace('/url?q=', '')
#     # 結果を出力する
#     if site_title == website_title:
#         # print('「初心者がPythonで作れるもの5選！すぐに作れるものを徹底解説」' + 'の順位は' + str(rank))
#         # print(str(rank) + "位: " + site_title)
#         query_rank = rank
#         print(query_rank)
# これは確認ようなので後で消す
# このプログラムは入力したクエリで検索したら指定したサイトが何位かが「変数rank」に入るというプログラム

def return_rank(query):
    # 上位から何件までのサイトを抽出するか指定する
    search = query
    target = '初心者がPythonで作れるもの5選！すぐに作れるものを徹底解説'
    how_page = 30 + 1

    print(f'【検索ワード】{search}')

    # Googleから検索結果ページを取得する
    url = f'https://www.google.co.jp/search?hl=ja&num={how_page}&q={search}'
    request = requests.get(url)

    # Googleのページ解析を行う
    soup = BeautifulSoup(request.text, "html.parser")
    search_site_list = soup.select('div.kCrYT > a')

    # ページ解析と結果の出力
    for rank, site in zip(range(1, how_page), search_site_list):
        try:
            site_title = site.select('h3.zBAuLc')[0].text
        except IndexError:
            # site_title = site.select('img')[0]['alt']
            site_url = site['href'].replace('/url?q=', '')
        # 結果を出力する
        if site_title == target:
            # print('「初心者がPythonで作れるもの5選！すぐに作れるものを徹底解説」' + 'の順位は' + str(rank))
            # print(str(rank) + "位: " + site_title)
            query_rank = rank
            print(query_rank)


return_rank('Python')
