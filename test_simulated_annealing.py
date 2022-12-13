import numpy as np
import random
from simpleai.search import SearchProblem
from simpleai.search.local import hill_climbing, simulated_annealing
from simpleai.search.viewers import ConsoleViewer
from gensim.models import KeyedVectors
from gensim.models import word2vec
import requests
from bs4 import BeautifulSoup


NUM_CANDIDATES = 3  # 一度に探索する単語の数

vectors = word2vec.Word2Vec.load("word2vec.gensim.model")

target = "初心者"
target_vector = vectors[target]


class QuerySearchProblem(SearchProblem):
    # 次の状態に至るための action のリストを生成
    # ここでは次のクエリ候補を生成している
    def actions(self, curr_query):
        actions = []
        curr_vector = vectors.wv[curr_query]
        for _ in range(NUM_CANDIDATES):
            new_vector = curr_vector + (np.random.standard_normal(curr_vector.size))* 0.2
            # new_vector = curr_vector + np.random.randint(0, 0.5, size=curr_vector.size)
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
        curr_vector = vectors.wv[curr_query]
        d = curr_vector - target_vector
        v = 1.0 / (1.0 + np.linalg.norm(d))
        print(f"query = {curr_query}, value={v}")
        # v = return_rank(curr_query)
        # print(f"検索ワード：Python {curr_query},検索順位={v*50}")
        return v


initial_query = "若手"
problem = QuerySearchProblem(initial_state=initial_query)
result = simulated_annealing(problem, iterations_limit=10, viewer=ConsoleViewer())
# result = hill_climbing(problem, iterations_limit=50, viewer=ConsoleViewer())

# print(result.path())
