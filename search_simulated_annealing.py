from abc import ABC

import numpy as np
import random
from simpleai.search import SearchProblem
from simpleai.search.local import hill_climbing, simulated_annealing
from simpleai.search.viewers import ConsoleViewer
# from gensim.models import KeyedVectors
from gensim.models import word2vec
import requests
from bs4 import BeautifulSoup


def return_rank(query):
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
        # site_title = site.select('h3.zBAuLc')[0].text
        try:
            site_title = site.select('h3.zBAuLc')[0].text
            # print(site_title)
        except IndexError:
            # site_title = site.select('img')[0]['alt']
            site_title = 'abc'
            # site_url = site['href'].replace('/url?q=', '')
            # print('error')
            # print(site_title)
            # 結果を出力する
        if site_title == target:
            # print('「初心者がPythonで作れるもの5選！すぐに作れるものを徹底解説」' + 'の順位は' + str(rank))
            # print(str(rank) + "位: " + site_title)
            rank1 = 1 / rank
            return rank1
    return rank1


NUM_CANDIDATES = 2  # 一度に探索する単語の数

vectors = model = word2vec.Word2Vec.load("word2vec.gensim.model")


# target = "作成"
# target_vector = vectors[target]


class QuerySearchProblem(SearchProblem, ABC):
    # 次の状態に至るための action のリストを生成
    # ここでは次のクエリ候補を生成している
    def actions(self, curr_query):
        actions = []
        curr_vector = vectors.wv[curr_query]
        for _ in range(NUM_CANDIDATES):
            new_vector = curr_vector + (np.random.standard_normal(curr_vector.size))*0.2
            # new_vector = curr_vector + 0.3,これだと次のベクトルが変わらない可能性がある
            new_keywords = vectors.wv.similar_by_vector(new_vector)
            for k, _ in new_keywords:
                # 現在のqueryと異なり，かつすでにクエリ候補に入っていない単語をクエリ候補とする
                if k != curr_query and k not in actions:
                    actions.append(k)
                    break
        return actions

    # 状態にアクションを適用した際の次の状態を生成
    # アクション＝次のクエリ候補なのでそのまま戻す
    def result(self, curr_query, action):
        return action

    # 状態の価値を計算
    # ここではベクトルの差（ノルム）の逆数を価値としている
    def value(self, curr_query):
        # curr_vector = vectors[curr_query]
        # d = curr_vector - target_vector
        # v = 1.0 / (1.0 + np.linalg.norm(d))
        # print(f"query = {curr_query}, value={v}")
        v = return_rank(curr_query)
        print(f"検索ワード：Python 初心者 {curr_query},検索順位={1 / v}")
        return v


initial_query = "工作"
problem = QuerySearchProblem(initial_state=initial_query)
result = simulated_annealing(problem, iterations_limit=10, viewer=ConsoleViewer())
# result = hill_climbing(problem, iterations_limit=10, viewer=None)

print(result.path())
