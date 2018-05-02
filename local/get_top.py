# coding: UTF-8
import csv
from datetime import date
import boto3
from time import sleep
from boto3.dynamodb.conditions import Key, Attr
import json
import decimal

# 指定日のトップnのデータを取得する

dynamo = boto3.resource('dynamodb',region_name='ap-southeast-2')

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)


# 最高気温
def get_highest_top(year,month,day):
    TABLE_NAME = 'dev-jw-highest'
    table = dynamo.Table(TABLE_NAME)
    d = "{:04}/{:02}/{:02}".format(year,month,day)
    
    print('-- 最高気温 --')
    print('date : '+d)

    response = table.query(
        IndexName='globalIndex2',
        KeyConditionExpression=Key('date').eq(d),
        ScanIndexForward=False,  #昇順か降順か（デフォルトは True=昇順）
        Limit=10
    )

    if response.get('Items'):
        print('len(response["Items"] : {}'.format(len(response['Items'])))
        for i in response['Items']:
            print(i['place'] + ' : ' + str(i['temperature_val']))

#		print('response :' + json.dumps(response['Items'], cls=DecimalEncoder))
    else:
        print('あれれ。Itemsないみたい')


# 最低気温
def get_lowest_top(year,month,day):
    TABLE_NAME = 'dev-jw-lowest'
    table = dynamo.Table(TABLE_NAME)
    d = "{:04}/{:02}/{:02}".format(year,month,day)
    
    print('-- 最低気温 --')
    print('date : '+d)

    response = table.query(
        IndexName='globalIndex2',
        KeyConditionExpression=Key('date').eq(d),
        ScanIndexForward=True,  #昇順か降順か（デフォルトは True=昇順）
        Limit=10
    )

    if response.get('Items'):
        print('len(response["Items"] : {}'.format(len(response['Items'])))
        for i in response['Items']:
            print(i['place'] + ' : ' + str(i['temperature_val']))

#		print('response :' + json.dumps(response['Items'], cls=DecimalEncoder))
    else:
        print('あれれ。Itemsないみたい')


# 降水量
def get_rainfall_top(year,month,day):
    TABLE_NAME = 'dev-jw-rain24h'
    table = dynamo.Table(TABLE_NAME)
    d = "{:04}/{:02}/{:02}".format(year,month,day)
    
    print('-- 降水量(24h) --')
    print('date : '+d)

    response = table.query(
        IndexName='globalIndex2',
        KeyConditionExpression=Key('date').eq(d),
        ScanIndexForward=False,  #昇順か降順か（デフォルトは True=昇順）
        Limit=10
    )

    if response.get('Items'):
        print('len(response["Items"] : {}'.format(len(response['Items'])))
        for i in response['Items']:
            print(i['place'] + ' : ' + str(i['rainfall_amount_val']))

#		print('response :' + json.dumps(response['Items'], cls=DecimalEncoder))
    else:
        print('あれれ。Itemsないみたい')


# 積雪量
def get_snow_depth_top(year,month,day):
    TABLE_NAME = 'dev-jw-snow'
    table = dynamo.Table(TABLE_NAME)
    d = "{:04}/{:02}/{:02}".format(year,month,day)
    
    print('-- 積雪量 --')
    print('date : '+d)

    response = table.query(
        IndexName='globalIndex2',
        KeyConditionExpression=Key('date').eq(d),
        ScanIndexForward=False,  #昇順か降順か（デフォルトは True=昇順）
        Limit=10
    )

    if response.get('Items'):
        print('len(response["Items"] : {}'.format(len(response['Items'])))
        for i in response['Items']:
            print(i['place'] + ' : ' + str(i['snow_depth_val']))

#		print('response :' + json.dumps(response['Items'], cls=DecimalEncoder))
    else:
        print('あれれ。Itemsないみたい')


# 降水量トップn
# get_rainfall_top(2018,4,14)

get_snow_depth_top(2018,4,14)