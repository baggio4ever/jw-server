# coding: UTF-8
import csv
from datetime import date
import boto3
from time import sleep
from boto3.dynamodb.conditions import Key, Attr
import json
import decimal

# 指定した観測所の情報を取得する

dynamo = boto3.resource('dynamodb',region_name='ap-southeast-2')

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)


# 観測所
def get_observatory(place):
    TABLE_NAME = 'dev-jw-observatory'
    table = dynamo.Table(TABLE_NAME)

    response = table.query(
        KeyConditionExpression=Key('place').eq(place),
        ScanIndexForward=False,  #昇順か降順か（デフォルトは True=昇順）
        Limit=10
    )

    if response.get('Items'):
#        print('len(response["Items"] : {}'.format(len(response['Items'])))
        for i in response['Items']:
            print(i['place'] + ' ( ' + i['kana'] + ' ) : ' + i['address'])

#		print('response :' + json.dumps(response['Items'], cls=DecimalEncoder))
    else:
        print('あれれ。Itemsないみたい')


get_observatory('京田辺')
get_observatory('今津')