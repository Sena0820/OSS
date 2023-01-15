import numpy as np
import random
from simpleai.search import SearchProblem
from simpleai.search.local import genetic
from simpleai.search.viewers import ConsoleViewer
from gensim.models import KeyedVectors
from gensim.models import word2vec
import requests
from bs4 import BeautifulSoup

vectors = KeyedVectors.load_word2vec_format("GoogleNews-vectors-negative300.bin", binary=True)

highrank_list = {}

# ↓ ↓ ↓ ↓　変える
pin_query = 'fish'  # 固定するクエリ
start_query = "water"  # 最初に指定するクエリ,これが最適クエリと離れすぎていたら無理かも
target_site = '2781.txt'  # 検索順位を上げたいターゲット
# この下で定めたクエリ（最適だと考えられるクエリで検索した時の検索結果のリストを作る）
good_queryA = 'fish'  # 正解リストにする際の検索クエリ
good_queryB = 'whale'
good_queryC = 'camel'
how_list = 50 + 1  # 何個のサイトを正解リストに入れるか指定
# ↑ ↑ ↑ ↑

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
    def generate_random_state(self):
        new_vec = start_vector + np.random.standard_normal(size=start_vector.size)
        candidates = vectors.similar_by_vector(new_vec, topn=100)
        return candidates[-1][0]

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

    def mutate(self, query):  # 突然変異のこと
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
        v2 = return_match_list(curr_query)
        print(f'クエリ：{curr_query}, 順位:{v}, 正解リストの合致数：{v2}, score:{1 / v + v2 / 200}')
        if v < 50 and curr_query not in highrank_list.keys():
            highrank_list[curr_query] = 1 / v + v2 / 200
        return 1 / v + v2 / 200


problem = QuerySearchProblem()
result = genetic(
    problem,
    population_size=50,
    crossover_rate=0.8,
    mutation_chance=0.3,
    iterations_limit=20,
    viewer=ConsoleViewer(),
)

print(f'最適と仮定したクエリ：「{good_queryA} {good_queryB} {good_queryC}」')
print(f'固定クエリ：{pin_query}')
print(result.state, result.path())
score_sorted = sorted(highrank_list.items(), key=lambda x:x[1], reverse=True)
print(f'検索クエリ改善過程：{score_sorted}')

