#２つの文献を連結するプログラム
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
# ori2 = "中医弁証学"

# ori = "合体全訳中医診断学中医弁証学"
# ori2 = "中医食療方"

ori = "合体+中医食療方"
ori2 = "中医基本用語辞典"

#%%ファイルの空白などを削除する(文字と文字の間が空いていたりするため削除しないと処理が難しいため)
openf = folder + ori + ".txt"
openf2 = folder + ori2 + ".txt"
# filename = folder + "合体" + ori + ori2 + ".txt"
# filename = folder + "合体" + "+" + ori2 + ".txt"
filename = folder + "中医学４文献.txt"

with codecs.open(openf,"r","utf-8") as f:
    data = f.read()

with codecs.open(openf2,"r","utf-8") as f2:
    data2 = f2.read()

data3 = data + "\n" + data2

with codecs.open(filename,"w","utf-8") as f:
    f.write(data3)


# %%
