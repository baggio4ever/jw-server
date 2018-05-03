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
    print(place + '  ' + from_date + ' - ' + to_date)
            
    response = table.query(
        KeyConditionExpression=Key('place').eq(place) & Key('date').between(from_date,to_date),
        Limit=65
    )
            
    for i in response['Items']:
        print( i['date'] + ' : '+ i['temperature'])


def get_lowest_range(place,from_date,to_date):
    TABLE_NAME = 'dev-jw-lowest'
    table = dynamo.Table(TABLE_NAME)
    
    print('-- 最低気温 range --')
    print(place + '  ' + from_date + ' - ' + to_date)
            
    response = table.query(
        KeyConditionExpression=Key('place').eq(place) & Key('date').between(from_date,to_date),
        Limit=65
    )
            
    for i in response['Items']:
        print( i['date'] + ' : '+ i['temperature'])


def get_rain24h_range(place,from_date,to_date):
    TABLE_NAME = 'dev-jw-rain24h'
    table = dynamo.Table(TABLE_NAME)
    
    print('-- 降水量 range --')
    print(place + '  ' + from_date + ' - ' + to_date)
            
    response = table.query(
        KeyConditionExpression=Key('place').eq(place) & Key('date').between(from_date,to_date),
        Limit=65
    )
            
    for i in response['Items']:
        print( i['date'] + ' : '+ i['rainfall_amount'])


def get_snow_range(place,from_date,to_date):
    TABLE_NAME = 'dev-jw-snow'
    table = dynamo.Table(TABLE_NAME)
    
    print('-- 積雪量 range --')
    print(place + '  ' + from_date + ' - ' + to_date)
            
    response = table.query(
        KeyConditionExpression=Key('place').eq(place) & Key('date').between(from_date,to_date),
        Limit=65
    )
            
    for i in response['Items']:
        print( i['date'] + ' : '+ i['snow_depth'])




get_highest_range('今津','2018/04/15','2018/05/02')
print('')
get_lowest_range('今津','2018/04/15','2018/05/02')
print('')
get_rain24h_range('今津','2018/04/15','2018/05/02')
print('')
get_snow_range('今津','2018/04/15','2018/05/02')
print('')
