# coding: UTF-8
import csv
from datetime import date
import boto3
from time import sleep

TABLE_NAME = 'dev-jw-observatory'

dynamo = boto3.resource('dynamodb',region_name='ap-southeast-2')
table = dynamo.Table(TABLE_NAME)

fn ='ame_master_utf8.csv'

with open(fn,newline='',encoding='utf-8') as html:
	re = csv.reader(html,delimiter=',',quotechar='"')
	with table.batch_writer() as batch:
		count = 0
		a = set()
		# l = []
		for row in re:
			if count>0:
				#     場所           地域            住所
		#		print(row[3] + ' ' + row[0] + ' : ' + row[5])
				str = '{:10}{:10}'.format(row[3],row[0])
				print(str)

				if not row[3] in a: # 重複チェック（同じ 観測所名、観測所番号 の行が存在する）
					batch.put_item(
						Item={
							"place": row[3],
							"prefecture": row[0],
							"address": row[5],
							"place_no": row[1],
							"kana": row[4],
							"type": row[2],
							"latitude": row[6], # 緯度（度）
							"latitude_min": row[7],  # 緯度（分）
							"longitude": row[8], # 経度（度）
							"longitude_min": row[9]  # 経度（分）
						})
					a.add(row[3])

				# if not row[0] in l:
				#	l.append(row[0])

			count += 1

		# DynamoDB にはチビチビ登録。
		# if count % 10 == 0:
		#	sleep(1)

print('-----')
print('読み取り行数: {}'.format(count))
# print( a )
# print( len(a) )
# print( l )
# print( len(l) )

# http://minus9d.hatenablog.com/entry/2015/07/07/225304

# 気象庁
# http://www.data.jma.go.jp/obd/stats/data/mdrr/docs/csv_dl_readme.html
