# このプログラムは、検索するクエリを最初の言葉からどんどんランダムに変化させていく手法である

import numpy as np
# from sklearn.decomposition import PCA
# import matplotlib.pyplot as plt
import random
from gensim.models import word2vec

model = word2vec.Word2Vec.load("word2vec.gensim.model")
# print(model.wv['cat'])
similar_python = model.wv.most_similar(positive=['Python'])
# print(similar_python)
# print(similar_python[0][0])#これで一個目の類似単語が抜き出せる
# for i in range(len(similar_python)):  # これで類似語検索した５つの単語をquery_wordに格納出来る！
#     query_word = similar_python[i][0]
#     print(query_word)

first_word = model.wv['Ruby']


# similar_word1 = model.wv.similar_by_vector(vector=first_word, topn=5, restrict_vocab=None)
# for i in range(5):
#     v2 = similar_word1[i][0]
#
#
#     similar_word2 = model.wv.similar_by_vector(vector=v2, topn=5, restrict_vocab=None)
#
#     all_word = model.wv.index2word
#     random_word = random.choice(all_word)
#     a = model.wv.most_similar(positive=[first_word, random_word])
#     for k in range(len(a)):
#         new_query = a[k][0]
#         print(new_query)

# 下の関数は10個のランダムの単語を返す
def make_random_word():
    all_word = model.wv.index2word
    random_word = random.choice(all_word)
    new_word = model.wv.most_similar(positive=[first_word, random_word])
    new_word2 = model.wv.most_similar(positive=[new_word[9][0], random_word])
    random_word2 = random.choice(all_word)
    new_word3 = model.wv.most_similar(positive=[new_word2[9][0], random_word2])
    for q in range(len(new_word)):
        print(new_word[q][0])
    for w in range(len(new_word2)):
        print(new_word2[w][0])
    for e in range(len(new_word3)):
        print(new_word3[e][0])
    # print(new_word)
    # print(new_word2)
    # print(new_word3)


# for i in range(10):
#     print(make_new_word())
# make_random_wo
# print(first_word)
a = first_word + 0.3
similar_word2 = model.wv.similar_by_vector(vector=a, topn=5, restrict_vocab=None)
print(similar_word2)