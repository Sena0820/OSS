from abc import ABC

import numpy as np
import matplotlib.pyplot as plt
import random
import requests
from bs4 import BeautifulSoup
from simpleai.search import SearchProblem, hill_climbing


def fx(x):
    y = -(x - 10) ** 2
    return y


def return_rank(query):
    # 上位から何件までのサイトを抽出するか指定する
    search = query
    target = '初心者がPythonで作れるもの5選！すぐに作れるものを徹底解説'
    how_page = 30 + 1

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
            # print(query_rank)


start = float(random.randint(0, 20))  # xをランダムで決めている
x = np.arange(0, 20, 0.1)
y = fx(x)
plt.plot(x, y)
plt.plot(start, fx(start), marker="o", markersize=10)
plt.xlabel("x")
plt.ylabel("y")


# 作るやつならクエリがxで検索順位がyになると言える

# class HillProblem(SearchProblem, ABC):
#     def actions(self, state):
#         list1 = []
#         list1.append(min(state + 0.1, 20))  # よくわからないが右に1個進めることを書いている、おそらく最大である20を超えないためのコード
#         list1.append(max(state - 0.1, 0))
#
#         print("{:.3f} -> [{:.3f} {:.3f}]".format(state, list1[0], list1[1]))
#         return list1
#
#     def result(self, state, action):
#         return action
#
#     def value(self, state):
#         v = fx(state)
#         return v

class HillProblem(SearchProblem, ABC):
    def actions(self, state):
        list1 = []
        list1.append(min(state + 0.1, 20))  # よくわからないが右に1個進めることを書いている、おそらく最大である20を超えないためのコード
        list1.append(max(state - 0.1, 0))

        print("{:.3f} -> [{:.3f} {:.3f}]".format(state, list1[0], list1[1]))
        return list1

    def result(self, state, action):
        return action

    def value(self, state, query):
        how_rank = return_rank(query)
        return how_rank


problem = HillProblem(initial_state=start)
result = hill_climbing(problem)  # 結果は８であることに注意
