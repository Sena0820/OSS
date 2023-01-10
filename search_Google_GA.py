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
start = "構成"
start_vector = vectors[start]

target = "コツ"
target_vector = vectors[target]

def return_rank(query):
    # 上位から何件までのサイトを抽出するか指定する
    global site_title
    global same_query1
    same_query1 = '卒論'
    global same_query2
    # same_query2 = '書きかた'
    # same_query1 = '健康'
    search = query
    target = '卒論の書き方と構成・項目別サンプル・卒論計画書の書き方'
    # target = 'https://www.e-life.jp/column/trend/2282/'
    how_page = 50 + 1

    # print(f'【検索ワード】{search}')

    # Googleから検索結果ページを取得する
    url = f'https://www.google.co.jp/search?hl=ja&num={how_page}&q={same_query1}+{search}'
    request = requests.get(url)

    # Googleのページ解析を行う
    soup = BeautifulSoup(request.text, "html.parser")
    search_site_list = soup.select('div.kCrYT > a')

    # num = random.randint(1, 10)
    # rank1 = 1 / (50 + num)
    rank1 = 1/50
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


highrank_list = {}

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
        v = return_rank(curr_query)
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
        print(f'クエリ：{curr_query}, 順位:{1/v}')
        if 1/v < 40 and curr_query not in highrank_list.keys():
            highrank_list[curr_query] = 1/v
        return v

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
score_sorted = sorted(highrank_list.items(), key=lambda x:x[1])
print(f'high_rank リスト：{score_sorted}')
