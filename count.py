#文献をテキスト化したものに対して空白を処理しながら単語を抽出するプログラム
#marukanji 〇を除いた漢字文字列の抽出
#
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

ori = "中医基本用語辞典" #正しい文献


#%%ファイルの空白などを削除する(文字と文字の間が空いていたりするため削除しないと処理が難しいため)
openf = folder + ori + ".txt"
filename = folder + ori + "〇処理.txt"

with codecs.open(openf,"r","utf-8") as f:
    data = f.read()

#改行などを削除
data_=re.sub('[ \t\r\n\ufeff]+','',data)
#漢字抽出の際にどうしても出てしまう〇を文字列から削除するがただ消すと前後の単語が連結されてしまうため空白に置き換えてみる
data_2=re.sub('[〇]','',data_)
with codecs.open(filename,"w","utf-8") as f:
    f.write(data_2)

m = MeCab.Tagger("-Owakati -u C:/M_dic/kampotest.dic")
l = m.parse(data_2).split(' ')

print(l)

# %%
c = collections.Counter(l)

d = dict(c.most_common(len(l)))
print(d)

#%% jsonへ保存
json_file = folder + ori + "_count2" + ".json"
with codecs.open(json_file,'w','utf-8') as f:
    json.dump(d,f,indent=4,ensure_ascii=False)


# %%
