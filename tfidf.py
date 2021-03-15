#文献をテキスト化したものに対して空白を処理しながら単語を抽出するプログラム
#marukanji 〇を除いた漢字文字列の抽出
#
#%%インポート
from __future__ import unicode_literals
from sklearn.feature_extraction.text import TfidfVectorizer
import MeCab
import codecs
import pandas as pd
import collections
import re
import regex
import json

#対象とする文字数
# number = str(3)
folder = "../txt/"

ori = "中医基本用語辞典" #正しい文献
# ori = "中医弁証学"
ori2 = "中医弁証学"

#ファイルの空白などを削除する(文字と文字の間が空いていたりするため削除しないと処理が難しいため)
openf = folder + ori + ".txt"
filename = folder + ori + "〇処理.txt"
savename = folder + ori + "〇空白処理.txt"
stopfile = folder + "Slothlib_japanese.txt"
tfidffile = folder + ori + "_tfidf5.json"
openfile2 = folder + ori2 + "〇空白処理.txt"
#%% TFIDFの計算

docs = []

with codecs.open(savename,"r","utf-8") as f:
    data = f.read()

with codecs.open(openfile2,"r","utf-8") as f:
    data2 = f.read()

m = MeCab.Tagger("-Owakati -u C:/M_dic/kampotest.dic")

mdata = m.parse(data)
mdata2 = m.parse(data2)
# print(mdata)
#%%
docs.append(mdata)
docs.append(mdata2)

vectorizer = TfidfVectorizer(use_idf=False) #tf-idfの計算の準備 IDFを利用するか、ストップワードを使うかなど決めれる

tfidfs = vectorizer.fit_transform(docs) #TF-IDF計算の実行

terms = vectorizer.get_feature_names() #単語リストの取得

# print(terms[5000]) #単語リストの表示

# print('%s' % ' '.join(terms)) #単語リストの表示

# print(tfidfs.toarray()[0]) #0番目のドキュメントのTF-IDFの値を単語順に出力

savedata = []
for doc_id, vec in zip(range(len(docs)), tfidfs.toarray()): #ドキュメントの数だけ繰り返す
    print('doc_id:', doc_id)
    # savedata = []
    for id, tfidf in sorted(enumerate(vec), key = lambda x: x[1],reverse=True):
        lemma = terms[id] #単語
        savedata.append((lemma,tfidf))
        # print('\t{0:s}: {1:f}'.format(lemma, tfidf))
        # savedata.append('\t{0:s}: {1:f}'.format(lemma, tfidf))
tfd = dict(savedata)
# print(savedata)
# print(tfd)
#%%
with codecs.open(tfidffile,"w","utf-8") as f:
    json.dump(tfd,f,indent=4,ensure_ascii=False)



# %%
