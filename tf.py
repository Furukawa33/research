# #%%インポート
# from __future__ import unicode_literals
# from sklearn.feature_extraction.text import TfidfVectorizer
# import MeCab
# import codecs
# import pandas as pd
# import collections
# import re
# import regex
# import json

# def calc_tf(b_idx, w_idx):
#     """b_idx 番目のブログの WORD[w_idx] の TF値を算出する"""
#     # WORD[w_idx] の出現回数の和
#     word_count = BLOG[b_idx]["bow"][w_idx]
#     if word_count == 0:
#         return 0.0
#     # 全単語の出現回数の和
#     sum_of_words = sum(BLOG[b_idx]["bow"])
#     # TF値計計算
#     return word_count/float(sum_of_words)