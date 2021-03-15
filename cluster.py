#%%インポート
from matplotlib import pyplot as plt
from sklearn import datasets, preprocessing
from sklearn.cluster import KMeans
from gensim.models.doc2vec import Doc2Vec
from gensim.models.doc2vec import TaggedDocument
import numpy as np 
import pandas as pd
import sys
from collections import defaultdict
import MeCab
import codecs
import os

#%%変数定義
model_path = "../model/4book.model"

#%%モデルの読み込み
m = Doc2Vec.load(model_path)

#%%モデル確認
print(m.wv.vocab.keys())

#%%クラスタリングする単語の厳選
kampo_vocab = []
with codecs.open("../dict_txt/中医学用語のみ.txt","r","utf-8") as f:
    kanji_data = f.read()

kanji_list = kanji_data.split("\n")
kanji_list.pop(-1)
# print(kanji_list)
vectors = []
cluster_word_list = []
KeyError_word_list = []
for word in kanji_list:
    try:
        vectors.append(m.wv[word])
        cluster_word_list.append(word)
    except KeyError:
        KeyError_word_list.append(word)
        print("Not in Vocabulary" + word + "\n")
# vectors = [m.wv[word] for word in kanji_list]
print(len(cluster_word_list))
print(len(KeyError_word_list))
print(KeyError_word_list)

#%%クラスタリングしてみる
n_clusters = 10
Kmeans_model = KMeans(n_clusters=n_clusters, verbose=1, random_state=1, n_jobs=-1)
Kmeans_model.fit(vectors)

#%%クラスタリングして割り当てたクラス情報を使って単語をまとめ上げる
cluster_labels = Kmeans_model.labels_
cluster_to_words = defaultdict(list)
for cluster_id, word in zip(cluster_labels, cluster_word_list):
    cluster_to_words[cluster_id].append(word)

#%%クラスタリングの結果を見る
cluster_list = []  
for words in cluster_to_words.values():
    print(len(words))
    print(words[:10])
    cluster_list.append(words)

# print(cluster_list[0][:10])  #[]1つめにクラスタ名が来る、次にクラスタの中の変数が来る

#%% 各クラスタの中の単語をファイルに保存する
savefolder_name = "../cluster_txt/n_clusters=" + str(n_clusters)
print(savefolder_name)
try:
    os.mkdir(savefolder_name)
except FileExistsError:
    print("すでに"+ savefolder_name + "フォルダーは作成されています。")
    pass

# print(cluster_list[1])
# print(len(cluster_list))
for cluster_n in range(len(cluster_list)):
    savefilename = savefolder_name + "/cluster" + str(cluster_n) + ".txt"
    with codecs.open(savefilename,"w","utf-8") as f:
        for w in cluster_list[cluster_n]:
            f.write("%s\n" % w)

#%%ベクトルをリストに格納する
# vectors_list = [m.docvecs[n] for n in range(len(m.docvecs))]

# #%%ドキュメント番号のリスト
# doc_nums = range(200,200+len(m.docvecs))

#%%クラスタリング設定
#   クラスター数を変えたい場合はn_clustersを変える
# n_clusters = 8
# kmeans_model = KMeans(n_clusters=n_clusters, verbose=1, random_state=1, n_jobs=-1)

# #%%クラスタリング実行
# kmeans_model.fit(vectors)

# #%%クラスタリングデータにラベル付け
# labels=kmeans_model.labels_

# #%%ラベルとドキュメント番号の辞書作り
# cluster_to_docs = defaultdict(list)
# for cluster_id, doc_num in zip(labels, doc_nums):
#     cluster_to_docs[cluster_id].append(doc_num)

# #%%クラスター出力
# for docs in cluster_to_docs.values():
#     print(docs)

# #%%どんなクラスタリングになったか、棒グラフ出力する
# #x軸ラベル
# x_label_name = []
# for i in range(n_clusters):
#     x_label_name.append("Cluster"+str(i))

# #x=left , y=heightデータ. ここではx=クラスター名、y=クラスター内の文書数
# left = range(n_clusters)
# height = []
# for docs in cluster_to_docs.values():
#     height.append(len(docs))
# print(height,left,x_label_name)

# #%%棒グラフ設定
# plt.bar(left,height,color="#FF5B70",tick_label=x_label_name,align="center")
# plt.title("Document clusters")
# plt.xlabel("cluster name")
# plt.ylabel("number of docments")
# plt.grid(True)
# plt.show()
# %%
