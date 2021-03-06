import pymysql

import boto3

ssm = boto3.client('ssm')
parameter = ssm.get_parameter(Name='/myweb/database1_password', WithDecryption=True)
db_password = parameter['Parameter']['Value']

# parameter로 db 비밀번호 설정하기
conn = pymysql.connect(host = 'database-1.c2zw45njcc7u.ap-northeast-2.rds.amazonaws.com', db='pbldb',
                       port=3306, passwd=db_password, user='admin')


