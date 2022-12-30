import numpy as np
import random
from simpleai.search import SearchProblem
from simpleai.search.local import genetic
from simpleai.search.viewers import ConsoleViewer
from gensim.models import KeyedVectors
from gensim.models import word2vec

# vectors: KeyedVectors = KeyedVectors.load("../chive-1.2-mc30_gensim/chive-1.2-mc30.kv")
# vectors = model = word2vec.Word2Vec.load("word2vec.gensim.model")
vectors: KeyedVectors = KeyedVectors.load("chive-1.2-mc30.kv")
start = "若者"
start_vector = vectors[start]

target = "クリスマス"
target_vector = vectors[target]


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
        v = 0
        try:
            curr_vector = vectors[curr_query]
            d = curr_vector - target_vector
            v = 100.0 / (1.0 + np.linalg.norm(d))
            # np.linalg.normは距離を測る関数
            # これの意味聞く！
        except Exception as e:
            print(e)
            print(curr_query)
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
result = genetic(problem, population_size=100, mutation_chance=0.5, iterations_limit=50, viewer=ConsoleViewer())

print(result.state, result.path())