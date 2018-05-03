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

 
s3 = boto3.client('s3')

dynamo = boto3.resource('dynamodb',region_name='ap-southeast-2')

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)



def get_highest_range(place,from_date,to_date):
    TABLE_NAME = 'dev-jw-highest'
    table = dynamo.Table(TABLE_NAME)
    
    print('-- 最高気温 range --')
    print('place : ' + place)
    print('from : ' + from_date)
    print('to : ' + to_date)
            
    response = table.query(
        KeyConditionExpression=Key('place').eq(place) & Key('date').between(from_date,to_date),
        Limit=65
    )
            
#            if len(response['Items']) == 0:
#                logger.info('あれれ。該当データないみたい')

    for i in response['Items']:
        print( i['date'] + ' : '+ i['temperature'])




get_highest_range('今津','2018/04/15','2018/05/01')
