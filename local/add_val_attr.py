# coding: UTF-8
import csv
from datetime import date
import boto3
from time import sleep
from boto3.dynamodb.conditions import Key, Attr
import json
import decimal

# 文字列として登録されている 気温や降水量、積雪量を数値属性で追加する


dynamo = boto3.resource('dynamodb',region_name='ap-southeast-2')

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)


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

	c0 = 0
	c1 = 0
	if response.get('Items'):
		for i in response['Items']:
			if i.get('prefecture'):
				i.pop('prefecture')
			if i.get('place_no'):
				i.pop('place_no')
			if i.get('international_place_no'):
				i.pop('international_place_no')
			print(i['date'], ":", i['rainfall_amount'])
			if i['rainfall_amount']=='-':
				i['rainfall_amount_val'] = decimal.Decimal("-999.9")
				c0 += 1
			else:
				i['rainfall_amount_val'] = decimal.Decimal(i['rainfall_amount'])
				c1 += 1
		
		print('len(response["Items"] : {}'.format(len(response['Items'])))
		print( 'c0: {}, c1: {}'.format(c0,c1) )

		print('response :' + json.dumps(response, cls=DecimalEncoder))

		with table.batch_writer() as batch:
			for i in response['Items']:
				batch.put_item(
						Item=i
				)

	else:
		print('あれれ。Itemsないみたい')


def append_highest_temperature_val(year,month,day):
	TABLE_NAME = 'dev-jw-highest'
	table = dynamo.Table(TABLE_NAME)
	d = "{:04}/{:02}/{:02}".format(year,month,day)

	print('---')
	print('d : '+d)

	response = table.query(
		IndexName='globalIndex1',
	    KeyConditionExpression=Key('date').eq(d)
	)

	c0 = 0
	c1 = 0
	if response.get('Items'):
		for i in response['Items']:
			if i.get('prefecture'):
				i.pop('prefecture')
			if i.get('place_no'):
				i.pop('place_no')
			if i.get('international_place_no'):
				i.pop('international_place_no')
			
			print(i['date'], ":", i['temperature'])
			if i['temperature']=='-':
				i['temperature_val'] = decimal.Decimal("-999.9")
				c0 += 1
			else:
				i['temperature_val'] = decimal.Decimal(i['temperature'])
				c1 += 1
		
		print('len(response["Items"] : {}'.format(len(response['Items'])))
		print( 'c0: {}, c1: {}'.format(c0,c1) )

		print('response :' + json.dumps(response, cls=DecimalEncoder))

		with table.batch_writer() as batch:
			for i in response['Items']:
				batch.put_item(
						Item=i
				)

	else:
		print('あれれ。Itemsないみたい')


# append_rainfall_amount_val(2018,4,8)
# append_rainfall_amount_val(2018,4,9)
# append_rainfall_amount_val(2018,4,10)
# append_rainfall_amount_val(2018,4,11)
# append_rainfall_amount_val(2018,4,12)
append_rainfall_amount_val(2018,4,13)
