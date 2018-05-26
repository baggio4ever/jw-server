# coding: UTF-8
import csv
from datetime import date
from time import sleep
import json

# 気象庁のサイトからダウンロードしたAMeDAS一覧のCSVファイルを,JSONに変換する
#  {key:value}
#     観測所名:カナ
# の形でJSON化。
# 都府県振興局、および観測所名の登場順は、気象庁からダウンロードしたファイル内の登場順通り

fn ='ame_master_utf8.csv'

with open(fn,newline='',encoding='utf-8') as html:
	re = csv.reader(html,delimiter=',',quotechar='"')

	count = 0
	count2 = 0
	a = set()

	autocompleteDict = {}

	for row in re:
		if count>0:
			#                         地域      カナ
			str = '{:10}{:10}'.format(row[3],row[4])
			print(str)

#			if not row[0] in prectureDict.keys():
#				prectureDict[row[0]] = []

#			if not row[3] in autocompleteDict.keys():
#				autocompleteDict[row[3]] = row[3]

			if not row[4] in autocompleteDict.keys():
				autocompleteDict[row[3]] = row[4]
				count2 += 1

		count += 1


print('-----')
print('読み取り行数: {}'.format(count))
print('書き込み行数: {}'.format(count2))

print('-----')
for i in autocompleteDict.keys():
	print(i)


# Pythonオブジェクトをファイル書き込み
savepath = 'observatory_autocompleteDict.json'
with open(savepath, 'w') as outfile:
    json.dump(autocompleteDict, outfile)


# http://minus9d.hatenablog.com/entry/2015/07/07/225304

# 気象庁
# http://www.data.jma.go.jp/obd/stats/data/mdrr/docs/csv_dl_readme.html
