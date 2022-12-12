import numpy as np
from gensim.models import word2vec

vectors = word2vec.Word2Vec.load("word2vec.gensim.model")

first_vector = vectors['新人']
first_vector.flags['WRITEABLE'] = True
for i in range(30):
    # first_vector += np.random.standard_normal(first_vector.size)
    first_vector += 0.003
    print(np.average(first_vector))
    next_words = vectors.similar_by_vector(first_vector)[2][0]
    print(next_words)
print(first_vector)
# 次は近い単語を羅列させてみる
# similar_vector50 = vectors.wv.most_similar(positive=['新人'], topn = 30, restrict_vocab=None)
# for i in similar_vector50:
#     print(i)
# # print(similar_vector50)
# print(f"初心者のベクトル：{vectors['初心者']}")
# print(f"若手のベクトル：{vectors['若手']}")
# print(f"引き算ベクトル：{vectors.wv.most_similar(positive=['初心者'],negative=['若手'],topn = 10, restrict_vocab=None)}")
# print(vectors.wv.most_similar(positive=['初心者'], topn=30, restrict_vocab=None))
