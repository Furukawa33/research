#%%
import MeCab
# m = MeCab.Tagger("-u C:/M_dic/NEologd.20191205-u.dic C:/M_dic/word_kanpo_tr-u.dic --unk-feature 未知語")
m = MeCab.Tagger("-u C:/M_dic/kampotest.dic --unk-feature 未知語")
# m = MeCab.Tagger("--unk-feature 未知語")
# m = MeCab.Tagger("-Owakati")
# m = MeCab.Tagger("-Ochasen")
p = m.parse("湿熱黄疸証湿熱黄疸証")
# p = m.parse("肢冷躍臥")
print(p)
# %%
