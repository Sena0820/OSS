import numpy as np
import random
from simpleai.search import SearchProblem
from simpleai.search.local import genetic
from simpleai.search.viewers import ConsoleViewer
from gensim.models import KeyedVectors
# from gensim.models import word2vec
from gensim.models import word2vec
import requests
from bs4 import BeautifulSoup

# vectors: KeyedVectors = KeyedVectors.load("../chive-1.2-mc30_gensim/chive-1.2-mc30.kv")
vectors = model = word2vec.Word2Vec.load("word2vec.gensim.model")
# vectors: KeyedVectors = KeyedVectors.load("chive-1.2-mc30.kv")
start = ""
start_vector = vectors[start]

target = "クリスマス"
target_vector = vectors[target]

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
    def generate_random_state(self):
        new_vec = start_vector + np.random.standard_normal(size=start_vector.size)
        candidates = vectors.similar_by_vector(new_vec, topn=100)
        # return candidates[-1][0]
        return candidates[-1][0]
        # [-1]は最後の一個という意味
    def crossover(self, query1, query2):
        vec1 = vectors[query1]
        vec2 = vectors[query2]
        new_vec = (vec1 + vec2) / 2
        candidates = vectors.similar_by_vector(new_vec, topn=10)
        new_query = None
        for q, _ in candidates:
            if q != query1 and q != query2:
                new_query = q
                break
        return new_query

    def mutate(self, query): # 突然変異のこと
        vec = vectors[query]
        new_vec = vec + np.random.standard_normal(size=vec.size)
        candidates = vectors.similar_by_vector(new_vec, topn=10)
        new_query = None
        for q, _ in candidates:
            if q != query:
                new_query = q
                break

        return new_query

    # 状態の価値を計算
    # ここではベクトルの差（ノルム）の逆数を価値としている
    def value(self, curr_query):
        # v = 0
        v = return_semantic_rank(curr_query)
        # try:
        #     curr_vector = vectors[curr_query]
        #     # d = curr_vector - target_vector
        #     # v = 100.0 / (1.0 + np.linalg.norm(d))
        #     d = np.linalg.norm(curr_vector - target_vector) ** 2
        #     v = 100.0 / (1.0 + d)
        #     # np.linalg.normは距離を測る関数
        #     # これの意味聞く！
        # except Exception as e:
        #     print(e)
        #     print(curr_query)
        return v

'''
評価関数を３つにする。
➀検索順位
➁作成したリストの内いくつを含むか
③最初に選択した単語とのベクトル距離
これらの三つをバランス取る必要がある。傾斜的には➀＞③にしたい
➀＝1/50~1,➁=1~50,③=大体0.3~1
5:3:2くらいかな（検討必要）
chiveだけでも遅いのにスクレイピングまで入ったら処理長くなりそう
'''


problem = QuerySearchProblem()
# result = simulated_annealing(problem, iterations_limit=100, viewer=ConsoleViewer())
# result = genetic(problem, population_size=100, mutation_chance=0.5, iterations_limit=50, viewer=ConsoleViewer())
result = genetic(
    problem,
    population_size=100,
    crossover_rate=0.8,
    mutation_chance=0.1,
    iterations_limit=20,
    viewer=ConsoleViewer(),
)

print(result.state, result.path())