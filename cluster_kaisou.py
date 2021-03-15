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
from scipy.cluster.hierarchy import ward,dendrogram, linkage, fcluster

#%%変数定義
# model_path = "../model/4book.model"
model_path = "../model/4book.model"

#%%モデルの読み込み
m = Doc2Vec.load(model_path)

#%%モデル確認
print(m.wv.vocab.keys())

#%%クラスタリングする単語の厳選
kampo_vocab = []
with codecs.open("../dict_txt/中医学用語のみ.txt","r","utf-8") as f:
    kanji_data = f.read()

kanji_list = kanji_data.split("\n") #改行で区切っていたテキストだったので改行を除いて要素をリストに抽出した
kanji_list.pop(-1)#一ついらない要素があったから除いた
# print(kanji_list)
vectors = [] #単語ベクトルを格納するリスト
cluster_word_list = [] #単語を格納するリスト
KeyError_word_list = [] #KeyErrorを吐いた単語を格納しておくリスト　確認用
for word in kanji_list: #中医学用語のみ.txtの中の単語すべてに対してDoc2vecによるモデルにある単語を抽出する
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

#%%
print(len(vectors))
print(vectors[0])
#%%クラスタリングしてみる
# n_clusters = 10
# Kmeans_model = KMeans(n_clusters=n_clusters, verbose=1, random_state=1, n_jobs=-1)
# Kmeans_model.fit(vectors)

##ward法　初回失敗例
# ward = ward(vectors)
# print(ward)
# dendrogram(ward,leaf_font_size=8)
# plt.show()

# ward法　linkage使ってみる
cluster = linkage(vectors, method="ward",metric="euclidean")
#%%
# print(cluster)
print(cluster_word_list)
#%%階層ツリーの作成
# pにクラスタ数を入れてtruncate_modeをlastpにするとクラスタ数をどうするか決めることができる
dendrogram(cluster, p=100, truncate_mode='lastp', labels=None, leaf_font_size=8)

#%%　クラスタリングされた単語を抽出する
# t = 0.7*max(cluster[:,2])
t = 2
# t = 13
c = fcluster(cluster, t, criterion="distance") #クラスタの作成　樹形図=dendrogramをどこで区切るか決める　そして各単語の順番通りに度のクラスタに属しているか出力する

#%%
c_n = max(c) #クラスタ数を格納
print(c_n)
#%%
print(c)

#%%
cluster_to_words = defaultdict(list)
for cluster_id, word in zip(c, cluster_word_list):
    cluster_to_words[cluster_id].append(word)

#%%
print(cluster_to_words[3][:10])
print(len(cluster_to_words))
#%% 各クラスタの中の単語をファイルに保存する
savefolder_name = "../cluster_txt/kaisou_clusters_t=" + str(c_n)
print(savefolder_name)
try:
    os.mkdir(savefolder_name)
except FileExistsError:
    print("すでに"+ savefolder_name + "フォルダーは作成されています。")
    pass

# print(cluster_list[1])
# print(len(cluster_list))
# print(cluster_to_words[10])
for cluster_n in range(len(cluster_to_words)):
    savefilename = savefolder_name + "/cluster" + str(cluster_n) + ".txt"
    with codecs.open(savefilename,"w","utf-8") as f:
    # print(cluster_n)
        for w in cluster_to_words[cluster_n]:
            f.write("%s\n" % w)

# %%
