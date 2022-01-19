import pymysql
conn = pymysql.connect(host = '', db='pbldb', port=3306,passwd='', user='admin')
print(conn)
