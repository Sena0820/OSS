import numpy as np
import requests
from bs4 import BeautifulSoup
from gensim.models import word2vec

model = word2vec.Word2Vec.load("word2vec.gensim.model")

v = model.wv['Ruby']

similar_word = model.wv.similar_by_vector(vector=v, topn=5, restrict_vocab=None)


website_title = '初心者がPythonで作れるもの5選！すぐに作れるものを徹底解説'
# 上位から何件までのサイトを抽出するか指定する

for i in similar_word:
    search_word = i[0]
    print(f'【検索ワード】{search_word}')
    pages_num = 40 + 1
    # Googleから検索結果ページを取得する
    url = f'https://www.google.co.jp/search?hl=ja&num={pages_num}&q={search_word}'
    request = requests.get(url)

    # Googleのページ解析を行う
    soup = BeautifulSoup(request.text, "html.parser")
    search_site_list = soup.select('div.kCrYT > a')

    # ページ解析と結果の出力
    for rank, site in zip(range(1, pages_num), search_site_list):
        try:
            site_title = site.select('h3.zBAuLc')[0].text
        except IndexError:
            # site_title = site.select('img')[0]['alt']
            site_url = site['href'].replace('/url?q=', '')
        # 結果を出力する
        if site_title == website_title:
            # print('「初心者がPythonで作れるもの5選！すぐに作れるものを徹底解説」' + 'の順位は' + str(rank))
            # print(str(rank) + "位: " + site_title)
            query_rank = rank
            print(query_rank)
