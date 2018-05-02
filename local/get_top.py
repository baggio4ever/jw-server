# coding: UTF-8
import csv
from datetime import date
import boto3
from time import sleep
from boto3.dynamodb.conditions import Key, Attr
import json
import decimal

# 文字列として登録されている 気温や降水量、積雪量を数値属性で追加する
# あわせて不要な属性（prefectureなど）を削除


dynamo = boto3.resource('dynamodb',region_name='ap-southeast-2')

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)


# 降水量
def get_rainfall_top(year,month,day):
    TABLE_NAME = 'dev-jw-rain24h'
    table = dynamo.Table(TABLE_NAME)
    d = "{:04}/{:02}/{:02}".format(year,month,day)
    
    print('---')
    print('d : '+d)

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


# 降水量トップn
get_rainfall_top(2018,4,14)