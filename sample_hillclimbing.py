# 山登り法のサンプル
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


start = float(random.randint(0, 20))  # xをランダムで決めている
x = np.arange(0, 20, 0.1)
y = fx(x)
plt.plot(x, y)
plt.plot(start, fx(start), marker="o", markersize=10)
plt.xlabel("x")
plt.ylabel("y")


# 作るやつならクエリがxで検索順位がyになると言える
# stateが単語ベクトルになりそう。

class HillProblem(SearchProblem, ABC):
    def actions(self, state):
        list1 = []
        list1.append(min(state + 0.1, 20))  # よくわからないが右に1個進めることを書いている、おそらく最大である20を超えないためのコード
        list1.append(max(state - 0.1, 0))  # 範囲外に出ないようにしているだけ

        print("{:.3f} -> [{:.3f} {:.3f}]".format(state, list1[0], list1[1]))
        return list1

    def result(self, state, action):
        return action

    def value(self, state):
        v = fx(state)
        return v


problem = HillProblem(initial_state=start)
result = hill_climbing(problem)  # 結果は８であることに注意
