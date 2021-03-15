#%%
import codecs
import json

folder = "../txt/"

ori = "中医基本用語辞典証dict"
# ori2 = "中医学４文献証dict"
ori2 = "合体+中医食療方証dict"

openjf = folder + ori + ".json"
openjf2 = folder + ori2 + ".json"

with codecs.open(openjf,"r","utf-8") as f:
    data = json.load(f)

with codecs.open(openjf2,"r","utf-8") as f2:
    data2 = json.load(f2)

print(type(data))
print(data)
# %%
wlist = []
wlist2 = []

for wkey in data.keys():
    wlist.append(wkey)

for wkey in data2.keys():
    wlist2.append(wkey)

# print(wlist)

print(len(wlist))
print(len(wlist2))
hikaku_list = set(wlist) - set(wlist2)
print(hikaku_list)
print(len(hikaku_list))
# %%
