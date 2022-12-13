import random

import requests
from bs4 import BeautifulSoup
from gensim.models import word2vec


# この関数はあるクエリで検索した際に指定したサイトで何位上位かを返してくれる
def return_rank(query):
    # 上位から何件までのサイトを抽出するか指定する
    search = query
    target = '初心者がPythonで作れるもの5選！すぐに作れるものを徹底解説'
    how_page = 50 + 1

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
            return rank
    return 0


model = word2vec.Word2Vec.load("word2vec.gensim.model")

first_word = model.wv['Ruby']


# 下の関数はランダムの単語の2次元配列を返す（単語とベクトルが一個の配列に入っている)
def make_random_word(select_word):
    select_vector = model.wv[select_word]
    all_word = model.wv.index2word
    random_word = random.choice(all_word)
    new_word = model.wv.most_similar(positive=[select_vector, random_word])
    return new_word


# 類似語2次元配列を返す（使うときはfor文で)
def make_similar_word(sec_word):
    sec_word_vector = model.wv[sec_word]
    similar_word = model.wv.similar_by_vector(vector=sec_word_vector, topn=10, restrict_vocab=None)
    return similar_word


def make_next_word(select_word):
    select_vector = model.wv[select_word]
    next_word_vector = select_vector + 0.2
    next_word = model.wv.similar_by_vector(vector=next_word_vector, topn=10, restrict_vocab=None)
    return next_word[0][0]


def return_rank2(query):
    # 上位から何件までのサイトを抽出するか指定する
    global site_title
    same_query1 = 'Python'
    same_query2 = '初心者'
    search = query
    target = '初心者がPythonで作れるもの5選！すぐに作れるものを徹底解説'
    how_page = 50 + 1

    # print(f'【検索ワード】{search}')

    # Googleから検索結果ページを取得する
    url = f'https://www.google.co.jp/search?hl=ja&num={how_page}&q={same_query1}+{same_query2}+{search}'
    request = requests.get(url)

    # Googleのページ解析を行う
    soup = BeautifulSoup(request.text, "html.parser")
    search_site_list = soup.select('div.kCrYT > a')

    num = random.randint(1, 10)
    rank1 = 1 / (50 + num)

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
            rank1 = 1 / rank
            return rank1
    return rank1



print(1/return_rank2('　'))
