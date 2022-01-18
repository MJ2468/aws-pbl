import pymysql
conn = pymysql.connect(host = 'database-1.c2zw45njcc7u.ap-northeast-2.rds.amazonaws.com', db='pbldb', port=3306,passwd='pblworking1234', user='admin')
print(conn)
