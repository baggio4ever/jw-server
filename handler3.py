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

dynamo = boto3.resource('dynamodb',region_name='ap-southeast-2')

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)



def getResponse(results):
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


DEFAULT_LIMIT = 65

def query(event,table_name):
    table = dynamo.Table(table_name)

    if( event.get('queryStringParameters')):
        params = event.get('queryStringParameters')

        place = params.get('place')
        from_date = params.get('from')
        to_date = params.get('to')
        if place and from_date and to_date:
            logger.info( place + '  ' + from_date + ' - ' + to_date )
            
            response = table.query(
                KeyConditionExpression=Key('place').eq(place) & Key('date').between(from_date,to_date),
                Limit=DEFAULT_LIMIT
            )
            
            if len(response['Items']) == 0:
                logger.info('あれれ。該当データないみたい')
            
            results = response['Items']
        else:
            results = []
    else:
        results = []

    return results

    
# 観測ポイント名 の 開始日から終了日までのデータを取得する（最大65日）
# from : 開始日
# to  : 終了日
# name : 観測ポイント名

def get_highest_range(event, context):
    TABLE_NAME = 'dev-jw-highest'
#    table = dynamo.Table(TABLE_NAME)
    results = query(event,TABLE_NAME)
    '''
    if( event.get('queryStringParameters')):
        params = event.get('queryStringParameters')

        place = params.get('place')
        from_date = params.get('from')
        to_date = params.get('to')
        if place and from_date and to_date:
            logger.info( place + '  ' + from_date + ' - ' + to_date )
            
            response = table.query(
                KeyConditionExpression=Key('place').eq(place) & Key('date').between(from_date,to_date),
                Limit=DEFAULT_LIMIT
            )
            
            if len(response['Items']) == 0:
                logger.info('あれれ。該当データないみたい')
            
            results = response['Items']
        else:
            results = []
    else:
        results = []
    '''    
    return getResponse(results)
#    body = {
#        "Items": results
#    }

#    response = {
#        "statusCode": 200,
#        "body": json.dumps(body, cls=DecimalEncoder),
#        "headers": {
#            "Access-Control-Allow-Origin":"*"
#        }
#    }
#    
#    logger.info(response)

#    return response


def get_lowest_range(event, context):
    TABLE_NAME = 'dev-jw-lowest'
#    table = dynamo.Table(TABLE_NAME)
    results = query(event,TABLE_NAME)
    '''
    if( event.get('queryStringParameters')):
        params = event.get('queryStringParameters')

        place = params.get('place')
        from_date = params.get('from')
        to_date = params.get('to')
        if place and from_date and to_date:
            logger.info( place + '  ' + from_date + ' - ' + to_date )
            
            response = table.query(
                KeyConditionExpression=Key('place').eq(place) & Key('date').between(from_date,to_date),
                Limit=DEFAULT_LIMIT
            )
            
            if len(response['Items']) == 0:
                logger.info('あれれ。該当データないみたい')
            
            results = response['Items']
        else:
            results = []
    else:
        results = []
    '''        
    return getResponse(results)
#    body = {
#        "Items": results
#    }

#    response = {
#        "statusCode": 200,
#        "body": json.dumps(body, cls=DecimalEncoder),
#        "headers": {
#            "Access-Control-Allow-Origin":"*"
#        }
#    }
    
#    logger.info(response)
#
#    return response

def get_rain24h_range(event, context):
    TABLE_NAME = 'dev-jw-rain24h'

    results = query(event,TABLE_NAME)
        
    return getResponse(results)


def get_snow_range(event, context):
    TABLE_NAME = 'dev-jw-snow'

    results = query(event,TABLE_NAME)
        
    return getResponse(results)
