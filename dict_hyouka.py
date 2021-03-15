#形態素解析用に作成した中医学用辞書の評価を行うプログラム
#中医学用語辞書に追加する中医学用語の候補の中から無作為に100個の単語を抽出して
#テキストファイルに出力する。
#人力で出力した単語群の中から中医学用語にふさわしくない単語があったらカウントして割合を出す。
#%%
import codecs
import json
import random

folder = "../txt/"

ori = "中医基本用語辞典marudict"
# ori = "中医学４文献marudict"
# ori = "中医基本用語辞典証dict"
# # ori2 = "中医学４文献証dict"
# ori2 = "合体+中医食療方証dict"

openjf = folder + ori + ".json"
# openjf2 = folder + ori2 + ".json"

save_json_file = "../json/中医基本用語辞典/dict_hyouka3.json"

with codecs.open(openjf,"r","utf-8") as f:
    data = json.load(f)

# with codecs.open(openjf2,"r","utf-8") as f2:
#     data2 = json.load(f2)

print(type(data))
print(data)
# %%
wlist = []
# wlist2 = []

for wkey in data.keys():
    wlist.append(wkey)

# for wkey in data2.keys():
#     wlist2.append(wkey)

r_w = random.sample(wlist, 100)
print(r_w)
# print(wlist)

# print(len(wlist))
# print(len(wlist2))
# hikaku_list = set(wlist) - set(wlist2)
# print(hikaku_list)
# print(len(hikaku_list))
# %%
with codecs.open(save_json_file,'w','utf-8') as f:
    json.dump(r_w,f,indent=4,ensure_ascii=False)
# %%
