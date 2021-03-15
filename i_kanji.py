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
# ori = "全訳中医診断学"
# ori = "中医弁証学"
# ori = "合体全訳中医診断学中医弁証学"
# ori = "合体+中医食療方"
ori = "中医基本用語辞典" #正しい文献
# ori = "中医学４文献"

#%%ファイルの空白などを削除する(文字と文字の間が空いていたりするため削除しないと処理が難しいため)
openf = folder + ori + ".txt"
filename = folder + ori + "〇処理.txt"
#%%
with codecs.open(openf,"r","utf-8") as f:
    data = f.read()

#改行などを削除
data_=re.sub('[ \t\r\n\ufeff]+','',data)
#漢字抽出の際にどうしても出てしまう〇を文字列から削除するがただ消すと前後の単語が連結されてしまうため空白に置き換えてみる
data_2=re.sub('[〇]',' ',data_)
with codecs.open(filename,"w","utf-8") as f:
    f.write(data_2)

#%% 漢字の文字列を抽出
with codecs.open(filename,"r","utf-8") as f:
    data_2 = f.read()

k_data=regex.findall(r'\p{Han}+',data_2)
pass

l=[]
for w in k_data:
    if len(w) > 1:
        l.append(w)
    

# %%
c = collections.Counter(l)

d = dict(c.most_common(len(l)))
print(d)

#%% jsonへ保存
json_file = folder + ori + "maru" + "kanji.json"
with codecs.open(json_file,'w','utf-8') as f:
    json.dump(d,f,indent=4,ensure_ascii=False)

# # %%確認用
# # words, counts = zip(*list(d))
# m = MeCab.Tagger("-Owakati")
# mecabdata = []
# i=0
# # for word in d:
# number = 1
# word = list(d)
# print(word[number])
# p = m.parse(word[number])
# print(p)
# print(len(p)-2)
# print(len(word[number]))
# if len(p) >= len(word)*2+1:
#     mecabdata.append((word,d[word]))
#     # i = i+1
# # #%%
# # print(mecabdata[1])
# # # %%
# di = dict(mecabdata)

#%% 確認用プログラム　mecabによって１文字に分割された単語（誤字候補）を抽出する
m = MeCab.Tagger("-Owakati")
# w = "発痒"
# w = "息切れ"
w = "精神疲労"
p = m.parse(w)

print(p)
print(len(p.split()))

#%%
mecabdata = []
# i=0
flag = True
for word in d:
    p = m.parse(word)
    l = p.split()
    for w in l:
        if len(w) == 1:
            flag = False
    if len(l) >= 2 and flag == False:         
        mecabdata.append((word,d[word]))
        flag = True

di = dict(mecabdata)

mecab_file = folder + ori + "誤字確認" + "maru" + "mecabdict.json"
with codecs.open(mecab_file,'w','utf-8') as f:
    json.dump(di,f,indent=4,ensure_ascii=False)

# %%誤字確認用助詞とか削除
#mecabで形態素解析を行うことによって一部単語は助詞と一緒の形態素になるその単語に関してはいらないので除去
m2 = MeCab.Tagger("-Owakati")
p2 = m2.parse(data_)
print(p2)
list_out = p2.split(' ')
print(list_out)
j_data=regex.findall(r'\p{Han}+'r'\p{Hiragana}+',p2)
print(j_data)
#助詞を含んだ漢字の文字列（削除対象）
j_data_set = set([regex.sub(r'\p{Hiragana}+','',d) for d in j_data])

ans = []
for word in di:
    if word not in j_data_set:
        ans.append((word,di[word]))
print(ans)

#%% jsonへ保存
mecab_file = folder + ori + "誤字確認" + "maru" + "dict.json"
with codecs.open(mecab_file,'w','utf-8') as f:
    json.dump(dict(ans),f,indent=4,ensure_ascii=False)


# %%
# words, counts = zip(*list(d))
m = MeCab.Tagger("-Owakati")
mecabdata = []
i=0
for word in d:
    p = m.parse(word)
    if len(p.split()) >= 2:   
        mecabdata.append((word,d[word]))

di = dict(mecabdata)
# # %%　MeCabに含まれているかの条件で文字数ではなく分裂したかで見るようにできたためそっちにする
# # words, counts = zip(*list(d))
# m = MeCab.Tagger("-Owakati")
# mecabdata = []
# i=0
# for word in d:
#     p = m.parse(word)
#     if (len(p)-2) >= len(word)+1:   ##余計な文字が２文字つくようだから２文字削除したうえで行っている
#         mecabdata.append((word,d[word]))

# di = dict(mecabdata)
#%% jsonへ保存
# mecab_file = "mecabdict" + number + ".json"
mecab_file = folder + ori + "maru" + "mecabdict.json"
with codecs.open(mecab_file,'w','utf-8') as f:
    json.dump(di,f,indent=4,ensure_ascii=False)

#必要なさそう_たぶんmecabで排除する単語の条件を変更したためだと思われる
# %%助詞とか削除
#mecabで形態素解析を行うことによって一部単語は助詞と一緒の形態素になるその単語に関してはいらないので除去
m2 = MeCab.Tagger("-Owakati")
p2 = m2.parse(data_)
print(p2)
list_out = p2.split(' ')
print(list_out)
j_data=regex.findall(r'\p{Han}+'r'\p{Hiragana}+',p2)
print(j_data)
#助詞を含んだ漢字の文字列（削除対象）
j_data_set = set([regex.sub(r'\p{Hiragana}+','',d) for d in j_data])

ans = []
for word in di:
    if word not in j_data_set:
        ans.append((word,di[word]))
print(ans)

#%% jsonへ保存
mecab_file = folder + ori + "maru" + "dict.json"
with codecs.open(mecab_file,'w','utf-8') as f:
    json.dump(dict(ans),f,indent=4,ensure_ascii=False)

#%%
word_list = []
shou_list = []
for w,c in ans:
    if w.endswith('証'):
        word_list.append(w)
        shou_list.append((w,c))
print(word_list)
print(shou_list)

shou_file = folder + ori + "証" + "dict.json"
with codecs.open(shou_file,'w','utf-8') as f:
    json.dump(dict(shou_list),f,indent=4,ensure_ascii=False)
#%%リストから〇〇証を抽出


# %%
