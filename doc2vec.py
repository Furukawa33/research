#%%
import MeCab
from gensim.models.doc2vec import Doc2Vec
from gensim.models.doc2vec import TaggedDocument
import codecs

folder = "../txt/"
ori = "中医基本用語辞典〇処理" #分散表現する対象のテキスト名

openfile = folder + ori + ".txt"

#%%ファイルを開く
with codecs.open(openfile,"r","utf-8") as f:
    data = f.read()

#%%　。で区切って各文に対して形態素解析をする    
m = MeCab.Tagger("-Owakati")
sentence_list = data.split('。')
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
model = Doc2Vec(documents = training_docs, dm = 1, size=300, window=8, min_count=2, workers=4)

model.save("../model/doc2vec.model")

#%% モデルのロード
model = Doc2Vec.load('../model/doc2vec.model')


# %%
print(model.most_similar(positive=['胃陰不足'],topn=10))

# %%
print(model.most_similar(positive=['胃気上逆'],topn=10))

# %%
