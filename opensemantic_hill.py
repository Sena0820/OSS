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

NUM_CANDIDATES = 5  # 一度に探索する単語の数

vectors = word2vec.Word2Vec.load("word2vec.gensim.model")

# target = "初心者"
# target_vector = vectors[target]

def return_semantic_rank(query):
    global site_title
    search = query
    target = 'wiki_68'
    print(f'【検索ワード】{search}')
    point_page = [1, 11, 21, 31, 41]
    for s in point_page:
        url = f'http://yoda.cla.kobe-u.ac.jp:8080/search/?&s={s}view=list&zoom=years&q={search}'
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
            if site_title == target:
                query_rank = rank
                # print(query_rank)
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

    # 状態の価値を計算
    # ここではベクトルの差（ノルム）の逆数を価値としている
    def value(self, curr_query):
        # curr_vector = vectors[curr_query]
        # d = curr_vector - target_vector
        # v = 1.0 / (1.0 + np.linalg.norm(d))
        v = 1/return_semantic_rank(curr_query)
        print(f"query = {curr_query} 順位={1/v}")
        return v


initial_query = "警察"
problem = QuerySearchProblem(initial_state=initial_query)
# result = simulated_annealing(problem, iterations_limit=100, viewer=ConsoleViewer())
result = hill_climbing_stochastic(problem, iterations_limit=50, viewer=ConsoleViewer())