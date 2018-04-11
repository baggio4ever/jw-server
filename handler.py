# coding: UTF-8
import json
import urllib.request
import csv
# from bs4 import BeautifulSoup
from datetime import date
import os
import logging
import datetime
import base64
import codecs
import boto3
from decimal import Decimal

logger = logging.getLogger()
logger.setLevel(logging.INFO)
 
s3 = boto3.client('s3')
BUCKET_NAME = os.environ['bucketName']

# http://minus9d.hatenablog.com/entry/2015/07/07/225304

# 気象庁
# http://www.data.jma.go.jp/obd/stats/data/mdrr/docs/csv_dl_readme.html

# アクセスするURL
# 最高気温
url_highest = "http://www.data.jma.go.jp/obd/stats/data/mdrr/tem_rct/alltable/mxtemsadext00_rct.csv"

# 最低気温
url_lowest = "http://www.data.jma.go.jp/obd/stats/data/mdrr/tem_rct/alltable/mntemsadext00_rct.csv"

# 24時間降水量
url_rain24h = "http://www.data.jma.go.jp/obd/stats/data/mdrr/pre_rct/alltable/pre24h00_rct.csv"

# 積雪量
url_snow = "http://www.data.jma.go.jp/obd/stats/data/mdrr/snc_rct/alltable/snc00_rct.csv"


def hello(event, context):
    
    download_csv_upload_to_s3( url_highest,'highest')
    download_csv_upload_to_s3( url_lowest,'lowest')

    '''
    # URLにアクセスする
    now = date.today()
    fn = now.strftime('%Y%m%d') + '.csv'
    fn_utf8 = now.strftime('%Y%m%d') + '_utf8.csv'
    full_fn = '/tmp/' + fn
    urllib.request.urlretrieve(url_highest,full_fn)
#    html = urllib.request.urlopen(url)

    s3.upload_file(full_fn, BUCKET_NAME, fn)

    utf8_full_fn = convert_sjis_to_utf8(full_fn)

    s3.upload_file(utf8_full_fn, BUCKET_NAME, fn_utf8)

    os.remove(full_fn)
    os.remove(utf8_full_fn)
    '''

    body = {
        # "message": "Go Serverless v1.0! Your function executed successfully!",
        # "filename": fn,
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body),
        "headers": {
            "Access-Control-Allow-Origin":"*"
        }
    }
    
    logger.info(response)

    return response

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """

def download_highest_temperature(event, context):
    
    s3filename = download_csv_upload_to_s3( url_highest,'highest')
    # ret = scrape_highest_temperature(s3filename)

    body = {
        # "message": "Go Serverless v1.0! Your function executed successfully!",
        # "ret":"gj",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body),
        "headers": {
            "Access-Control-Allow-Origin":"*"
        }
    }
    
    logger.info(response)

    return response


def download_lowest_temperature(event, context):
    
    s3filename = download_csv_upload_to_s3( url_lowest,'lowest')

    body = {
        # "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body),
        "headers": {
            "Access-Control-Allow-Origin":"*"
        }
    }
    
    logger.info(response)

    return response


def download_snow(event, context):
    
    s3filename = download_csv_upload_to_s3( url_snow,'snow')

    body = {
        # "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body),
        "headers": {
            "Access-Control-Allow-Origin":"*"
        }
    }
    
    logger.info(response)

    return response


def download_rain24h(event, context):
    
    s3filename = download_csv_upload_to_s3( url_rain24h,'rain24h')

    body = {
        # "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body),
        "headers": {
            "Access-Control-Allow-Origin":"*"
        }
    }
    
    logger.info(response)

    return response



def get_s3_file(year,month,day,attr):
    # ファイル名
    fn_utf8 = "{:04}{:02}{:02}_{}.csv".format(year,month,day,attr)

    # S3保存用パス付きファイル名 年/月のフォルダを作る
    s3_full_fn_utf8 = "{}/{}/{}".format(year,month,fn_utf8)

    return (s3_full_fn_utf8,fn_utf8)
    

def get_date_to_scrape(event):
    b = event.get("body")
    if b is not None:
        yy = json.loads(event["body"])

        year = yy["year"]
        month = yy["month"]
        day = yy["day"]
    else:
        now = date.today()

        year = now.year
        month = now.month
        day = now.day

    return (year,month,day)


def scrape_highest(event, context):
    '''
    b = event.get("body")
    if b is not None:
        yy = json.loads(event["body"])

        year = yy["year"]
        month = yy["month"]
        day = yy["day"]
    else:
        now = date.today()

        year = now.year
        month = now.month
        day = now.day
    '''

    year,month,day = get_date_to_scrape(event)

    '''
    # ファイル名
    fn_utf8 = now.strftime('%Y%m%d') + '_'+'highest'+'.csv'

    # S3保存用パス付きファイル名 年/月のフォルダを作る
    s3_full_fn_utf8 = "{}/{}/{}".format(now.year,now.month,fn_utf8)

    ret = scrape_highest_temperature(s3_full_fn_utf8,fn_utf8)
    '''
    s3_full,s3_fn = get_s3_file(year,month,day,'highest')

    logger.info(s3_full)
    
    ret = scrape_highest_temperature(s3_full,s3_fn)
    
    body = {
        # "message": "Go Serverless v1.0! Your function executed successfully!",
        "ret":ret,
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body),
        "headers": {
            "Access-Control-Allow-Origin":"*"
        }
    }
    
    logger.info(response)

    return response



def scrape_lowest(event, context):
    
    # now = date.today()
    year,month,day = get_date_to_scrape(event)

    '''
    # ファイル名
    fn_utf8 = now.strftime('%Y%m%d') + '_'+'lowest'+'.csv'

    # S3保存用パス付きファイル名 年/月のフォルダを作る
    s3_full_fn_utf8 = "{}/{}/{}".format(now.year,now.month,fn_utf8)

    ret = scrape_lowest_temperature(s3_full_fn_utf8,fn_utf8)
    '''
    s3_full,s3_fn = get_s3_file(year,month,day,'lowest')

    logger.info(s3_full)

    ret = scrape_lowest_temperature(s3_full,s3_fn)

    body = {
        # "message": "Go Serverless v1.0! Your function executed successfully!",
        "ret":ret,
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body),
        "headers": {
            "Access-Control-Allow-Origin":"*"
        }
    }
    
    logger.info(response)

    return response


def scrape_sn(event, context):
    
    # now = date.today()
    year,month,day = get_date_to_scrape(event)

    '''
    # ファイル名
    fn_utf8 = now.strftime('%Y%m%d') + '_'+'snow'+'.csv'

    # S3保存用パス付きファイル名 年/月のフォルダを作る
    s3_full_fn_utf8 = "{}/{}/{}".format(now.year,now.month,fn_utf8)

    ret = scrape_snow(s3_full_fn_utf8,fn_utf8)
    '''
    s3_full,s3_fn = get_s3_file(year,month,day,'snow')

    logger.info(s3_full)

    ret = scrape_snow(s3_full,s3_fn)
    
    body = {
        # "message": "Go Serverless v1.0! Your function executed successfully!",
        "ret":ret,
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body),
        "headers": {
            "Access-Control-Allow-Origin":"*"
        }
    }
    
    logger.info(response)

    return response



def scrape_rain(event, context):
    
    # now = date.today()
    year,month,day = get_date_to_scrape(event)

    '''
    # ファイル名
    fn_utf8 = now.strftime('%Y%m%d') + '_'+'rain24h'+'.csv'

    # S3保存用パス付きファイル名 年/月のフォルダを作る
    s3_full_fn_utf8 = "{}/{}/{}".format(now.year,now.month,fn_utf8)

    ret = scrape_rain24h(s3_full_fn_utf8,fn_utf8)
    '''
    s3_full,s3_fn = get_s3_file(year,month,day,'rain24h')

    logger.info(s3_full)

    ret = scrape_rain24h(s3_full,s3_fn)
    
    body = {
        # "message": "Go Serverless v1.0! Your function executed successfully!",
        "ret":ret,
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body),
        "headers": {
            "Access-Control-Allow-Origin":"*"
        }
    }
    
    logger.info(response)

    return response



def scrape_highest_temperature(s3_full_fn,fn):
    tempFile = '/tmp/'+fn
    s3.download_file(BUCKET_NAME,s3_full_fn,tempFile)

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table( 'dev-jw-highest' )

    count=0
    with open(tempFile,newline='') as html:
        re = csv.reader(html,delimiter=',',quotechar='|')
        for row in re:
            if count>0:
    	        #     県             地域             最高温度
		        #	print(row[1] + ' ' + row[2] + ' : ' + row[9])
                # str = '{:20}{:12} : {:6}'.format(row[1],row[2],row[9])
                # logger.info(str)

                place = row[2]
                year = row[4]
                month = row[5]  # csvファイルに0詰めで入っている
                day = row[6]  # csvファイルに0詰めで入っている
                date = "{}/{}/{}".format(year,month,day)
                temperature = row[9]
                if temperature:
                    temperature_val = Decimal(float(temperature))
                else:
                    temperature = '-'
                    temperature_val = Decimal(-999.0)
                prefecture = row[1]

                place_no = row[0]
                international_place_no = row[3]
                if not international_place_no:
                    international_place_no = '-'
                time = "{}:{}".format(row[11],row[12])

                table.put_item(
                    Item={
                        "place": place,
                        "date": date,
                        "temperature": temperature,
                        # "temperature_val": temperature_val,
                        # "prefecture": prefecture,

                        # "place_no": place_no,
                        # "international_place_no": international_place_no,
                        "time": time
                    }
                )
            count+=1

    os.remove(tempFile)

    return [count]


def scrape_lowest_temperature(s3_full_fn,fn):
    tempFile = '/tmp/'+fn
    s3.download_file(BUCKET_NAME,s3_full_fn,tempFile)

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table( 'dev-jw-lowest' )

    count=0
    with open(tempFile,newline='') as html:
        re = csv.reader(html,delimiter=',',quotechar='|')
        for row in re:
            if count>0:
    	        #     県             地域             最高温度
		        #	print(row[1] + ' ' + row[2] + ' : ' + row[9])
                # str = '{:20}{:12} : {:6}'.format(row[1],row[2],row[9])
                # logger.info(str)

                place = row[2]
                year = row[4]
                month = row[5]  # csvファイルに0詰めで入っている
                day = row[6]  # csvファイルに0詰めで入っている
                date = "{}/{}/{}".format(year,month,day)
                temperature = row[9]
                if temperature:
                    temperature_val = Decimal( float(temperature) )
                else:
                    temperature = '-'
                    temperature_val = Decimal( -999.0 )
                prefecture = row[1]

                place_no = row[0]
                international_place_no = row[3]
                if not international_place_no:
                    international_place_no = '-'
                time = "{}:{}".format(row[11],row[12])

                table.put_item(
                    Item={
                        "place": place,
                        "date": date,
                        "temperature": temperature,
                        # "temperature_val": temperature_val,
                        # "prefecture": prefecture,

                        # "place_no": place_no,
                        # "international_place_no": international_place_no,
                        "time": time
                    }
                )
            count+=1

    os.remove(tempFile)

    return [count]


def scrape_snow(s3_full_fn,fn):
    tempFile = '/tmp/'+fn
    s3.download_file(BUCKET_NAME,s3_full_fn,tempFile)

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table( 'dev-jw-snow' )

    count=0
    with open(tempFile,newline='') as html:
        re = csv.reader(html,delimiter=',',quotechar='|')
        for row in re:
            if count>0:
    	        #     県             地域             最高温度
		        #	print(row[1] + ' ' + row[2] + ' : ' + row[9])
                # str = '{:20}{:12} : {:6}'.format(row[1],row[2],row[9])
                # logger.info(str)

                place = row[2]
                year = row[4]
                month = row[5]  # csvファイルに0詰めで入っている
                day = row[6]  # csvファイルに0詰めで入っている
                date = "{}/{}/{}".format(year,month,day)
                depth = row[9]
                if depth:
                    depth_val = Decimal(float(depth))
                else:
                    depth = '-'
                    depth_val = Decimal(-999.0)
                prefecture = row[1]

                place_no = row[0]
                international_place_no = row[3]
                if not international_place_no:
                    international_place_no = '-'
                time = "{}:{}".format(row[7],row[8])

                table.put_item(
                    Item={
                        "place": place,
                        "date": date,
                        "snow_depth": depth,
                        # "snow_depth_val": depth_val,
                        # "prefecture": prefecture,

                        # "place_no": place_no,
                        # "international_place_no": international_place_no,
                        "time": time
                    }
                )
            count+=1

    os.remove(tempFile)

    return [count]



def scrape_rain24h(s3_full_fn,fn):
    tempFile = '/tmp/'+fn
    s3.download_file(BUCKET_NAME,s3_full_fn,tempFile)

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table( 'dev-jw-rain24h' )

    count=0
    with open(tempFile,newline='') as html:
        re = csv.reader(html,delimiter=',',quotechar='|')
        for row in re:
            if count>0:
    	        #     県             地域             最高温度
		        #	print(row[1] + ' ' + row[2] + ' : ' + row[9])
                # str = '{:20}{:12} : {:6}'.format(row[1],row[2],row[9])
                # logger.info(str)

                place = row[2]
                year = row[4]
                month = row[5]  # csvファイルに0詰めで入っている
                day = row[6]  # csvファイルに0詰めで入っている
                date = "{}/{}/{}".format(year,month,day)
                amount = row[11]
                if amount:
                    amount_val = Decimal(float(amount))
                else:
                    amount = '-'
                    amount_val = Decimal(-999.0)
                prefecture = row[1]

                place_no = row[0]
                international_place_no = row[3]
                if not international_place_no:
                    international_place_no = '-'
                time = "{}:{}".format(row[13],row[14])

                table.put_item(
                    Item={
                        "place": place,
                        "date": date,
                        "rainfall_amount": amount,
                        # "rainfall_amount_val": amount_val,
                        # "prefecture": prefecture,

                        # "place_no": place_no,
                        # "international_place_no": international_place_no,
                        "time": time
                    }
                )
            count+=1

    os.remove(tempFile)

    return [count]




def download_csv_upload_to_s3(download_url,attr):

    now = date.today()

    # ファイル名
    fn = now.strftime('%Y%m%d') + '_'+attr+'_sjis.csv'
    fn_utf8 = now.strftime('%Y%m%d') + '_'+attr+'.csv'

    # lambdaローカル保存用パス付きファイル名
    full_fn = '/tmp/' + fn
    full_fn_utf8 = '/tmp/' + fn_utf8

    # URLにアクセスしてファイルに保存
    urllib.request.urlretrieve(download_url,full_fn)
#    html = urllib.request.urlopen(url)

    # S3保存用パス付きファイル名 年/月のフォルダを作る
    s3_full_fn = "{}/{}/{}".format(now.year,now.month,fn)
    s3_full_fn_utf8 = "{}/{}/{}".format(now.year,now.month,fn_utf8)

    # s3.upload_file(full_fn, BUCKET_NAME, s3_full_fn)

    convert_sjis_to_utf8_2(full_fn,full_fn_utf8)

    s3.upload_file(full_fn_utf8, BUCKET_NAME, s3_full_fn_utf8)

    os.remove(full_fn)
    os.remove(full_fn_utf8)

    return s3_full_fn_utf8

'''
def convert_sjis_to_utf8(fn):
    # Shift_JIS ファイルのパス
    shiftjis_csv_path = fn
    # UTF-8 ファイルのパス
    ftitle, fext = os.path.splitext(fn)
#    os.rename(f, ftitle + '_img' + fext)    
    utf8_csv_path = ftitle + '_utf8' + fext

    # 文字コードを utf-8 に変換して保存
    fin = codecs.open(shiftjis_csv_path, "r", "shift_jis")
    fout_utf = codecs.open(utf8_csv_path, "w", "utf-8")
    for row in fin:
        fout_utf.write(row)
    fin.close()
    fout_utf.close()
    return utf8_csv_path
'''

def convert_sjis_to_utf8_2(fn,fn_utf8):
    # Shift_JIS ファイルのパス
    shiftjis_csv_path = fn
    # UTF-8 ファイルのパス
    utf8_csv_path = fn_utf8

    # 文字コードを utf-8 に変換して保存
    fin = codecs.open(shiftjis_csv_path, "r", "shift_jis")
    fout_utf = codecs.open(utf8_csv_path, "w", "utf-8")
    for row in fin:
        fout_utf.write(row)
    fin.close()
    fout_utf.close()
