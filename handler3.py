# coding: UTF-8
import json
import urllib.request
import csv
from datetime import date,datetime,timedelta,timezone
import os
import logging
import datetime
import base64
import codecs
import boto3
import decimal
from boto3.dynamodb.conditions import Key, Attr

logger = logging.getLogger()
logger.setLevel(logging.INFO)
 
s3 = boto3.client('s3')
BUCKET_NAME = os.environ['bucketName']

dynamo = boto3.resource('dynamodb',region_name='ap-southeast-2')

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)


# 観測ポイント名 の 開始日から終了日までのデータを取得する（最大65日）
# from : 開始日
# to  : 終了日
# name : 観測ポイント名

def get_highest_range(event, context):
    TABLE_NAME = 'dev-jw-highest'
    table = dynamo.Table(TABLE_NAME)

    if( event.get('queryStringParameters')):
        params = event.get('queryStringParameters')

        name = params.get('name')
        from_date = params.get('from')
        to_date = params.get('to')
        if name and from_date and to_date:
            logger.info('-- 最高気温 range --')
            logger.info('name : ' + name)
            logger.info('from : ' + from_date)
            logger.info('to : ' + to_date)
            
            response = table.query(
                KeyConditionExpression=Key('place').eq(name) & Key('date').between(from_date,to_date),
                Limit=65
            )
            
            if len(response['Items']) == 0:
                logger.info('あれれ。該当データないみたい')
            
            results = response['Items']
        else:
            results = []
    else:
        results = []
        
    body = {
        "Items": results
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body, cls=DecimalEncoder),
        "headers": {
            "Access-Control-Allow-Origin":"*"
        }
    }
    
    logger.info(response)

    return response
