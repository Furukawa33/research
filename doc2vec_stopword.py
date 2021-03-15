#%%
import MeCab
from gensim.models.doc2vec import Doc2Vec
from gensim.models.doc2vec import TaggedDocument
import codecs
import json
from sklearn.cluster import KMeans
import csv
import regex
import re

folder = "../txt/"
csv_folder = "../csv/"
# ori = "中医基本用語辞典〇処理" #分散表現する対象のテキスト名
ori = "中医学４文献〇空白処理" #分散表現する対象のテキスト名
# model_name = "../model/doc2vec_stopword2.model"
# model_name = "../model/doc2vec_4doc_stopword_unk.model"
model_name = "../model/4book.model"
# dict_filename = "中医基本用語辞典marumecabdict"
dict_filename = "中医学４文献marudict"
openfile = folder + ori + ".txt"
opendict = folder + dict_filename + ".json"
opendict2 = csv_folder + "word_kanpou_tr.csv"
kanji_list_name = "../dict_txt/中医学用語のみ.txt"
#%%ファイルを開く
with codecs.open(openfile,"r","utf-8") as f:
    data = f.read()

#%% ストップワード以外を通す　今回は名詞、動詞、形容詞、記号を通す。未知語も省く
# t = MeCab.Tagger("-Ochasen -u C:/M_dic/kampotest.dic --unk-feature 未知語")
# t = MeCab.Tagger("-u C:/M_dic/kampotest.dic --unk-feature 未知語")
t = MeCab.Tagger("--unk-feature 未知語") #ユーザー辞書にkampotest.dicを追加しないと奥山さんの奴とかが反映されないから仕方なくやったので指定しなくてよい
select_conditions = ['動詞', '形容詞','名詞']

node = t.parseToNode(data)
print(node)
terms = []

while node:
    #単語
    term = node.surface

    #品詞
    pos = node.feature.split(',')[0]

    #もし品詞が条件と一致したら
    #もし単語が。だったら
    if pos in select_conditions or term == '。':
        terms.append(term)

    node = node.next

# print(terms)

sentence_data = ''.join(terms)
# print(sentence_data)
print(type(sentence_data))
print('胃陰不足' in sentence_data) #しっかり胃陰不足は含まれていた
#%%　。で区切って各文に対して形態素解析をする    
m = MeCab.Tagger("-Owakati")
# m = MeCab.Tagger("-Owakati -u C:/M_dic/kampotest.dic")
p = m.parse("胃気上逆")
print(p)

#%% 文に分割
sentence_list = sentence_data.split('。')
training_docs = []
for i,sentence in enumerate(sentence_list):
    p_sentence = m.parse(sentence).split()
    text = TaggedDocument(words = p_sentence, tags = [i])
    training_docs.append(text)

print(training_docs)
    # p_data = [TaggedDocument(words = data.split('。'),tags = [i]) for i,data in enumerate(f)]

    # p_data = [TaggedDocument(words = data.split('。'),tags = [i]) for i,data in enumerate(f)]
    # print(p_data)

#%%モデルの学習
model = Doc2Vec(documents = training_docs, dm = 1, size=300, window=8, min_count=1, workers=4)
# model_name = "../model/doc2vec_stopword.model"
model.save(model_name)

#%% モデルのロード
model = Doc2Vec.load(model_name)

#%% モデルの単語数をカウント
model_len = len(model.wv.vocab)
print(model_len)#単語数を出す
# %%
print(model.most_similar(positive=['胃陰不足'],topn=10)[0][0])

# %%
print(model.most_similar(positive=['胃気上逆'],topn=10))

# %% 中医学用語辞書に入っている単語のみベクトルを表示する。

with codecs.open(opendict,"r","utf-8") as f:
    dict_data = json.load(f)

print(type(dict_data.keys()))
dict_data1 = list(dict_data)
print(type(dict_data1))
# dict_data1 = []
# for i in range(len(dict_data)):
#     dict_data2.append(dict_data[i][0])
# print(dict_data)
#%%
#奥山さんの辞書はcsv形式なのでdict型で読み込む
# dict_data2 = []
with codecs.open(opendict2,"r","utf-8") as f:
    reader = csv.reader(f)
    l = [row for row in reader]
    # print(l)
    # for row in reader:
    #     dict_data2.append(row)

dict_data2 = []
for i in range(len(l)):
    if len(l[i][0]) >=2: 
        dict_data2.append(l[i][0])
print(dict_data2)

#%%奥山さんの奴から漢字の文字列のみ抽出 ひらがなが含まれていたら除くように処理
pattern = regex.compile(r'\p{Han}+')
kanji_list = []
for kanji_word in dict_data2:
    if pattern.fullmatch(kanji_word):
        kanji_list.append(kanji_word)

# print(kanji_list)
print(dict_data1)
#%%奥山さんの作った辞書と合体している
ex_dict = dict_data1+dict_data2
kanji_dict = dict_data1+kanji_list
#
# print(dict_data2)
# print(ex_dict)
print(kanji_dict)

#%%奥山さんの奴と俺の辞書を合体させて漢字の文字列のみファイル出力
with codecs.open(kanji_list_name,"w","utf-8") as f:
    for w in kanji_dict:
        f.write("%s\n" % w)
#%%
# print(dict_data.keys()) #辞書の中の漢字リストの出し方
print(model.most_similar(positive=['胃陰不足'],topn=10))
# %%
test = dict(model.most_similar(positive=['胃陰不足'],topn=model_len))
print(test.keys())

# %% for文で回してベクトルを表示する奴から漢字辞書の奴のみ表示するようにする。
# mostruiji = model.most_similar(positive=['胃気上逆'],topn=15)
mostruiji = model.most_similar(positive=['胃陰不足'],topn=model_len)
wv_list = []

for word_vec in mostruiji:
    if word_vec[0] in ex_dict:
        wv_list.append(word_vec)

print(wv_list)


# %%
print(wv_list[0])
# %%
