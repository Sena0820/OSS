import numpy as np

import requests
from bs4 import BeautifulSoup
from gensim.models import word2vec
from simpleai.search import SearchProblem, hill_climbing
import random


# この関数はあるクエリで検索した際に指定したサイトで何位上位かを返してくれる
def return_rank(query):
    # 上位から何件までのサイトを抽出するか指定する
    global site_title
    search = query
    target = '初心者がPythonで作れるもの5選！すぐに作れるものを徹底解説'
    how_page = 50 + 1

    # print(f'【検索ワード】{search}')

    # Googleから検索結果ページを取得する
    url = f'https://www.google.co.jp/search?hl=ja&num={how_page}&q={search}'
    request = requests.get(url)

    # Googleのページ解析を行う
    soup = BeautifulSoup(request.text, "html.parser")
    search_site_list = soup.select('div.kCrYT > a')
    # num2 = random.randint(1,10)
    # ページ解析と結果の出力
    num = random.randint(1, 10)
    for rank, site in zip(range(1, how_page), search_site_list):
        # site_title = site.select('h3.zBAuLc')[0].text
        try:
            site_title = site.select('h3.zBAuLc')[0].text
        except IndexError:
            # site_title = site.select('img')[0]['alt']
            site_url = site['href'].replace('/url?q=', '')
        # 結果を出力する
        if site_title == target:
            # print('「初心者がPythonで作れるもの5選！すぐに作れるものを徹底解説」' + 'の順位は' + str(rank))
            # print(str(rank) + "位: " + site_title)
            return rank
    return 50 - num


model = word2vec.Word2Vec.load("word2vec.gensim.model")

first_word = 'Ruby'
start = model.wv[first_word]

# ここから自分で山登り法実装してみる
# next_vector1 = start
# next_vector2 = start
start.flags.writeable = True
winner_list = []
max_rank = return_rank(first_word)
for i in range(5):
    next_vector = start
    # print(start)
    next_vector1 = start
    next_vector1 += 0.06
    # print(f"next_vector1:{next_vector1}")
    word1 = model.wv.similar_by_vector(vector=next_vector1, topn=2, restrict_vocab=None)[1][0]
    print(f"word1は{word1}")
    next_vector2 = start
    next_vector2 -= 0.06
    # print(f"next_vector2:{next_vector2}")
    word2 = model.wv.similar_by_vector(vector=next_vector2, topn=2, restrict_vocab=None)[1][0]
    print(f"word2は{word2}")
    if return_rank(word1) > return_rank(word2):
        start = next_vector1
        print(f"winnerは{word1}")
        print(start)
    else:
        start = next_vector2
        print(f"winnerは{word2}")
        # print(start)

