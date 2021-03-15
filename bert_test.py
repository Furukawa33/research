#%%インポート
import numpy as np
import json

#%%単語の埋込ベクトルを取り出す
with open(r'C:/bert/json/output.json', 'r') as f:
    lines = f.readlines()

objs = []
for l in lines:
    objs.append(json.loads(l))

#%%単語の確認
print(objs[1]['features'][1]['token'])

#%%すべての文の各単語埋込ベクトルを取得
words = []
for o in objs: ##文の数だけ繰り返す
    dic = {}
    for feature in o['features']: ##単語の数だけ繰りかえす
        token = feature['token'] ##tokenに単語を挿入
        dic[token] = np.array(feature['layers'][0]['values']) ##ベクトルをくっつける
    words.append(dic)

#%%埋込ベクトルの表示
print(words[0]['ガンダム']) ##最初の変数で文を指定、2変数目で単語を指定そのベクトルを出力

# %%　コサイン類似度の定義
def cos_sim(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
# %%コサイン類似度の計算例 単語動詞の類似度
print(cos_sim(words[0]['ガンダム'], words[1]['モビルスーツ']))
print(cos_sim(words[1]['ザク'], words[1]['モビルスーツ']))
print(cos_sim(words[0]['ロボット'], words[1]['モビルスーツ']))
print(cos_sim(words[4]['イチゴ'], words[1]['モビルスーツ']))

# %%　文脈を考慮した類似度計算
print(cos_sim(words[2]['彗星'], words[2]['シャア']))
print(cos_sim(words[3]['彗星'], words[2]['シャア']))
# %% 単語の埋込ベクトルの演算
print(cos_sim(words[1]['ザク'] + words[4]['赤い'], words[2]['シャア']))
print(cos_sim(words[1]['ザク'] + words[4]['甘い'], words[2]['シャア']))