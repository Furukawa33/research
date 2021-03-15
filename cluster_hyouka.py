#形態素解析用に作成した中医学用辞書の評価を行うプログラム
#中医学用語辞書に追加する中医学用語の候補の中から無作為に100個の単語を抽出して
#テキストファイルに出力する。
#人力で出力した単語群の中から中医学用語にふさわしくない単語があったらカウントして割合を出す。
#%%
import codecs
import json
import random

folder = "../cluster_txt/kaisou_clusters_t=10/"
n_s = 6 #始めのクラスタ
n_e = 7 #まとめ終わるクラスタ
t = n_e - n_s + 1 #ファイルを読み込む回数
data = []
sum_data = []
for i in range(t): 
    n = n_s + i
    ori = "cluster" + str(n)
    opentxt = folder + ori + ".txt"
    # save_json_file = folder + "/cluster" + str(n) + "/cluster" + str(n) + "_hyouka.json"
    with codecs.open(opentxt,"r","utf-8") as f:
        txt_data = f.read()
        d = txt_data.split("\n")
        d.pop(-1) #最後の改行で作られた空要素を除く
        sum_data = sum_data + d
    data.append(d)
# print(type(data))
# print(len(data[0]))
# print(data[0])
# print(data[1])
print(len(sum_data))
# %%
r_w = random.sample(sum_data, 100)
print(r_w)

# %%
save_json_file = folder + "clusterB.json"
with codecs.open(save_json_file,'w','utf-8') as f:
    json.dump(r_w,f,indent=4,ensure_ascii=False)
# %%

# %%
