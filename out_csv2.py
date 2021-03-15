#%%
import csv
import json
import codecs
read_folder = "../txt/"
write_folder = "../csv/"
# filename = "中医基本用語辞典marumecabdict"
filename = "中医学４文献marudict"
savefilename = "4kanpo_book"
#%%jsonファイルの読み込み#################################


openf = read_folder + filename + ".json"

with codecs.open(openf,"r","utf-8") as rf:
    # data = f.read()
    data = json.load(rf)

# json_open = open('')


# dict_data = list(data) 
print(data)
print(type(data))
##########################################################

# %%csvに書き込み#########################################

writef = write_folder + savefilename + ".csv"
data_list = list(data)
print(data_list)


csv_data = data_list ##csvのデータ
#%%
with codecs.open(writef,"w","utf-8") as wf:
    writer = csv.writer(wf)
    # writer = csv.writer(wf, delimiter='\t')
    # writer.writerows(data_list)
    # writer = csv.DictWriter(wf, data)
    # writer.writeheader()
    # writer.writerow(data[])
    for d in data_list:
        writer.writerow([d,'','','1','名詞','一般','*','*','*','*','','',''])

# %%
