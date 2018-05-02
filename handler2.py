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

logger = logging.getLogger()
logger.setLevel(logging.INFO)
 
s3 = boto3.client('s3')
BUCKET_NAME = os.environ['bucketName']

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)


def get_highest_top(event, context):
    response = {
        "statusCode": 200,
        "body": "",
        "headers": {
            "Access-Control-Allow-Origin":"*"
        }
    }
    
    logger.info(response)

    return response

