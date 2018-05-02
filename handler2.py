# coding: UTF-8
import json
import urllib.request
import csv
# from bs4 import BeautifulSoup
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


DEFAULT_TOP = 10

def getToday():
    JST = timezone(timedelta(hours=+9),'JST') # 日本時刻大切
    now = datetime.datetime.now(JST)
    return now
    
def getYesterday():
    today = getToday()
    t = timedelta(days=1)
    return (today-t)

def format_date2(d):
    return "{:04}/{:02}/{:02}".format(d.year,d.month,d.day)


# date : 取得する日（記述ない時は、昨日。今のところ日が変わる直前にデータを気象庁から取得しているので）
# top  : トップ幾つまで取得するか（記述ない時は、10）

def get_highest_top(event, context):
    TABLE_NAME = 'dev-jw-highest'
    table = dynamo.Table(TABLE_NAME)

    if( event.get('queryStringParameters')):
        params = event.get('queryStringParameters')

        dd = params.get('date')
        if dd is not None:
            d = dd
        else:
            # now = getYesterday()
            # d = "{:04}/{:02}/{:02}".format(now.year,now.month,now.day)
            d = format_date2( getYesterday() )

        ttop = params.get('top')
        if ttop is not None:
            top = int(ttop)
        else:
            top = DEFAULT_TOP
    else:
        # now = getYesterday()
        # d = "{:04}/{:02}/{:02}".format(now.year,now.month,now.day)
        d = format_date2(getYesterday())
        top = DEFAULT_TOP
    
    logger.info('-- 最高気温 --')
    logger.info('date : '+d)

    response = table.query(
        IndexName='globalIndex2',
        KeyConditionExpression=Key('date').eq(d),
        ScanIndexForward=False,  #昇順か降順か（デフォルトは True=昇順）
        Limit=top
    )

#    if response.get('Items'):
#        for i in response['Items']:
#            logger.info(i['place'] + ' : ' + str(i['temperature_val']))

#    else:
#        logger.info('あれれ。Itemsないみたい')

    if len(response['Items']) == 0:
        logger.info('あれれ。該当データないみたい')


    body = {
        "ret": response['Items'],
        "input": event
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


def get_lowest_top(event, context):
    response = {
        "statusCode": 200,
        "body": "",
        "headers": {
            "Access-Control-Allow-Origin":"*"
        }
    }
    
    logger.info(response)

    return response

