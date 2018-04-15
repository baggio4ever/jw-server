# coding: UTF-8
import csv
from datetime import date
import boto3
from time import sleep
from boto3.dynamodb.conditions import Key, Attr
import json

# 文字列として登録されている 気温や降水量、積雪量を数値属性で追加する


dynamo = boto3.resource('dynamodb',region_name='ap-southeast-2')

def append_rainfall_amount_val(year,month,day):
	TABLE_NAME = 'dev-jw-rain24h'
	table = dynamo.Table(TABLE_NAME)
	d = "{:04}/{:02}/{:02}".format(year,month,day)

	print('---')
	print('d : '+d)

	response = table.query(
		IndexName='globalIndex1',
	    KeyConditionExpression=Key('date').eq(d)
	)

	if response.get('Items'):
		for i in response['Items']:
		    print(i['date'], ":", i['rainfall_amount'])
		
		print('len(response["Items"] : {}'.format(len(response['Items'])))
	else:
		print('あれれ。Itemsないみたい')
		print('response :' + json.dumps(response))

append_rainfall_amount_val(2018,4,8)
