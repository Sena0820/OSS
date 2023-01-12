from abc import ABC

import numpy as np
import random
from simpleai.search import SearchProblem
from simpleai.search.local import hill_climbing_stochastic, simulated_annealing
from simpleai.search.viewers import ConsoleViewer
from gensim.models import KeyedVectors
from gensim.models import word2vec
import requests
from bs4 import BeautifulSoup

# ↓ ↓ ↓ ↓　変える
NUM_CANDIDATES = 5  # 一度に探索する単語の数
pin_query = 'fish'
target_site = '2781.txt'
start_query = "sorry"
# この下で定めたクエリ（最適だと考えられるクエリで検索した時の検索結果のリストを作る）
good_queryA = 'whale'
good_queryB = 'fish'
good_queryC = 'camel'
how_list = 10 + 1  # 何個のサイトにするか指定
# ↑ ↑ ↑ ↑

vectors = KeyedVectors.load_word2vec_format("enwiki_20180420_100d.txt", binary=False)

highrank_list = {}

start_vector = vectors[start_query]
best_page_url = f'http://yoda.cla.kobe-u.ac.jp:8080/search/?&s={how_list}view=list&zoom=years&q={good_queryA}+{good_queryB}+{good_queryC}'
request2 = requests.get(best_page_url)
soup2 = BeautifulSoup(request2.text, "html.parser")
search_site_list2 = soup2.find_all('a', class_='title')
good_site_list = []
for site2 in search_site_list2:
    site_title2 = site2.text
    good_site_list.append(site_title2)

def return_match_list(query):
    global site_title
    search = query
    # print(f'【検索ワード】{search}') # ここにランクも出力したい
    point_page = [1, 11, 21, 31, 41]
    list_points = 0
    for s in point_page:
        url = f'http://yoda.cla.kobe-u.ac.jp:8080/search/?&s={s}view=list&zoom=years&q={pin_query}+{search}'
        request = requests.get(url)
        soup = BeautifulSoup(request.text, "html.parser")
        search_site_list = soup.find_all('a', class_='title')
        for rank, site in zip(range(1, 10), search_site_list):
            try:
                site_title = site.text
            except IndexError:
                site_url = site['href'].replace('/url?q=', '')
            # 結果を出力する
            if site_title in good_site_list:
                list_points += 1
    return list_points


def return_semantic_rank(query):
    global site_title
    global query_rank
    search = query
    point_page = [1, 11, 21, 31, 41]
    for s in point_page:
        url = f'http://yoda.cla.kobe-u.ac.jp:8080/search/?&s={s}view=list&zoom=years&q={pin_query}+{search}'
        request = requests.get(url)
        soup = BeautifulSoup(request.text, "html.parser")
        search_site_list = soup.find_all('a', class_='title')
        query_rank = 50
        for rank, site in zip(range(1, 10), search_site_list):
            try:
                site_title = site.text
            except IndexError:
                site_url = site['href'].replace('/url?q=', '')
            # 結果を出力する
            if site_title == target_site:
                query_rank = rank
                if s == 11:
                    query_rank += 10
                if s == 21:
                    query_rank += 20
                if s == 31:
                    query_rank += 30
                if s == 41:
                    query_rank += 40
                return query_rank
    return query_rank


class QuerySearchProblem(SearchProblem):
    # 次の状態に至るための action のリストを生成
    # ここでは次のクエリ候補を生成している
    def actions(self, curr_query):
        actions = [curr_query]
        curr_vector = vectors[curr_query]
        for _ in range(NUM_CANDIDATES):
            new_vector = curr_vector + np.random.uniform(size=curr_vector.size, low=-0.5, high=0.5)
            new_keywords = vectors.similar_by_vector(new_vector, topn=NUM_CANDIDATES)
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

    def value(self, curr_query):
        # v = 0
        v = return_semantic_rank(curr_query)
        v2 = return_match_list(curr_query)
        print(f'クエリ：{curr_query}, 順位:{v}, 正解リストの合致数：{v2}, score:{1 / v + v2 / 130}')
        if v < 40 and curr_query not in highrank_list.keys():
            highrank_list[curr_query] = 1 / v + v2 / 130
        return 1 / v + v2 / 130

problem = QuerySearchProblem(initial_state=start_query)
result = hill_climbing_stochastic(problem, iterations_limit=50, viewer=ConsoleViewer())
score_sorted = sorted(highrank_list.items(), key=lambda x:x[1], reverse=True)
print(f'最適と仮定したクエリ：「{good_queryA} {good_queryB} {good_queryC}」')
print(f'初期クエリでの検索順位:34位')
print(f'検索クエリ改善過程：{score_sorted}')