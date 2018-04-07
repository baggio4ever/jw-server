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

logger = logging.getLogger()
logger.setLevel(logging.INFO)
 
s3 = boto3.client('s3')
BUCKET_NAME = os.environ['bucketName']

# http://minus9d.hatenablog.com/entry/2015/07/07/225304

# 気象庁
# http://www.data.jma.go.jp/obd/stats/data/mdrr/docs/csv_dl_readme.html


def hello(event, context):
    # アクセスするURL
    # 最高気温
    url_highest = "http://www.data.jma.go.jp/obd/stats/data/mdrr/tem_rct/alltable/mxtemsadext00_rct.csv"

    # 最低気温
    url_lowest = "http://www.data.jma.go.jp/obd/stats/data/mdrr/tem_rct/alltable/mntemsadext00_rct.csv"

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
        "message": "Go Serverless v1.0! Your function executed successfully!",
#        "filename": fn,
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

def download_csv_upload_to_s3(download_url,attr):
    # URLにアクセスする
    now = date.today()
    fn = now.strftime('%Y%m%d') + '_'+attr+'.csv'
    fn_utf8 = now.strftime('%Y%m%d') + '_'+attr+'_utf8.csv'
    full_fn = '/tmp/' + fn
    full_fn_utf8 = '/tmp/' + fn_utf8
    urllib.request.urlretrieve(download_url,full_fn)
#    html = urllib.request.urlopen(url)

    s3.upload_file(full_fn, BUCKET_NAME, fn)

    convert_sjis_to_utf8_2(full_fn,full_fn_utf8)

    s3.upload_file(full_fn_utf8, BUCKET_NAME, fn_utf8)

    os.remove(full_fn)
    os.remove(full_fn_utf8)


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
