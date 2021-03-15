#文献からストップワードを抽出するためのプログラム
#
#
#ストップワードの選定プログラム
#%%インポート
from __future__ import unicode_literals
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

# ori = "中医基本用語辞典" #正しい文献
# ori = "中医弁証学"
ori = "中医学４文献"

#ファイルの空白などを削除する(文字と文字の間が空いていたりするため削除しないと処理が難しいため)
openf = folder + ori + ".txt"
filename = folder + ori + "〇処理.txt"
savename = folder + ori + "〇空白処理.txt"
stopfile = folder + "Slothlib_japanese.txt"
#%%
with codecs.open(filename,"r","utf-8") as f:
    data = f.read()

#改行などを削除
data_=re.sub('[ \t\r\n\ufeff]+','',data)
#漢字抽出の際にどうしても出てしまう〇を文字列から削除するがただ消すと前後の単語が連結されてしまうため空白に置き換えてみる
data_2=re.sub('[〇◇,［］⇒[]]()]','',data_)
#%%
with codecs.open(savename,"w","utf-8") as f:
    f.write(data_2)

#%% 
with codecs.open(savename,"r","utf-8") as f:
    data_2 = f.read()
#%% ストップワードを考慮 Slothlibより得たストップワードのリストを作成
with codecs.open(stopfile,"r","utf-8") as f:
    stopword = f.read()

stoplist_temp = stopword.splitlines()
# print(stoplist)
stoplist = []

for s in stoplist_temp:
    if s != '':
        stoplist.append(s)

print(stoplist)
#%%
# t = MeCab.Tagger("-Ochasen -u C:/M_dic/kampotest.dic --unk-feature 未知語") #ここで未知語処理を入れてもすでに作っていた中医学用語辞書により漢字はしっかりと残るようになっている
t = MeCab.Tagger("-u C:/M_dic/kampotest.dic --unk-feature 未知語") #Ochasenを外して未知語処理を施してみる

select_conditions = ['動詞', '形容詞','名詞']

node = t.parseToNode(data_2)

terms = []

while node:
    #単語
    term = node.surface

    #品詞
    pos = node.feature.split(',')[0]

    #もし品詞が条件と一致したら
    if pos in select_conditions and term not in stoplist:
        terms.append(term)

    node = node.next

print(terms)
# #%%
# m = MeCab.Tagger("-Owakati -u C:/M_dic/kampotest.dic")

# l = m.parse(data_2).split(' ')

# print(l)

# %%
c = collections.Counter(terms)

d = dict(c.most_common(len(terms)))
print(d)

#%% jsonへ保存 
json_file = folder + ori + "_count_stopword_Slo_kai2" + ".json"
with codecs.open(json_file,'w','utf-8') as f:
    json.dump(d,f,indent=4,ensure_ascii=False)

# %%
