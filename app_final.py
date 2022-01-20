import pymysql
import boto3
import os
from flask import Flask, request, jsonify, session, Response, render_template, redirect, send_file
from flask_restful import reqparse, abort, Api, Resource
from werkzeug.security import check_password_hash, generate_password_hash


ssm = boto3.client('ssm')
parameter = ssm.get_parameter(Name='/myweb/database1_password', WithDecryption=True)
db_password = parameter['Parameter']['Value']

app = Flask(__name__)
api = Api(app)



@app.route('/')
def index():
    return "/board를 url 뒤에 붙여줘야 열립니다."


def upload_file_to_bucket(file):
    BUCKET_NAME = 's3-borard-files-mj'
    S3_KEY = 'images/' + file.filename
    s3 = boto3.client('s3')
    s3.put_object(Bucket=BUCKET_NAME, Body=file, key=S3_KEY, ContentType=file.content_type)


@app.route('/board/write', methods=['POST'])
def write():
    if request.method == 'POST':
        name = request.form.get('name', False)
        passwd = request.form.get('passwd', False)
        title = request.form.get('title', False)
        content = request.form.get('content', False)
        file = request.files['file']
        error = None

        if not name:
            error = 'name이 유효하지 않습니다.'
        elif not passwd:
            error = 'passwd가 유효하지 않습니다.'
        elif not title:
            error = 'title이 유효하지 않습니다.'
        elif not content:
            error = 'content가 유효하지 않습니다.'

        print(file)
        print(file.content_length)
        if file:
            image_url = upload_file_to_bucket(file)
            print(image_url)

        if error is None:
            db = pymysql.connect(host='database-1.c2zw45njcc7u.ap-northeast-2.rds.amazonaws.com', db='pbldb',
                                 port=3306, passwd=db_password, user='admin')
            cursor = db.cursor()
            cursor.execute('Insert into board (name, passwd, title, content) VALUES (%s, %s, %s, %s)',
                           (name, generate_password_hash(passwd), title, content))
            if file:
                cursor.execute('SELECT LAST_INSERT_ID()')
                result = cursor.fetchall()
                board_id = result[0][0]
                cursor.execute('Insert INTO board_file(board_id, file_name, s3_bucket, s3_path, mime_type) Values( %s, %s, %s, %s, %s)',
                (board_id, file.filename, 's3-borard-files-mj', 'images/' + file.filename, file.content_type))
                db.commit()
                cursor.close()
                db.close()

            return redirect('/board')

@app.route('/baord/down', methods = ['get'])
def download():
    board_id = request.args['id']
    db = pymysql.connect(host='database-1.c2zw45njcc7u.ap-northeast-2.rds.amazonaws.com', db='pbldb',
                         port=3306, passwd=db_password, user='admin')
    curs = db.cursor(pymysql.cursors.DictCursor)
    sql = 'select * from board_file where board_id = %s'
    curs.execute(sql, (board_id))
    result = curs.fetchone()
    curs.close()
    db.close()

    print("result: ", result)
    if result:
        BUCKET_NAME = 's3-borard-files-mj'
        key = result['s3-board-files']
        file_content_type = result['mime_type']
        s3 = boto3.client('s3')

        print(file)

        return Response(file['Body'].read(), mimetype= file_content_type, headers= )

@app.route('/board')
def board_list():
    db = pymysql.connect(host='database-1.c2zw45njcc7u.ap-northeast-2.rds.amazonaws.com', db='pbldb',
                         port=3306, passwd=db_password, user='admin')
    curs = db.cursor(pymysql.cursors.DictCursor)
    sql = 'select * from board order by id desc'
    curs.execute(sql)
    result = curs.fetchall()
    curs.close()
    db.close()
    print(result)
    return render_template(('board_list.html'), result=result)


@app.route('/board/writeform')
def board_writeForm():
    return render_template('board_writeform.html')

@app.route('/board/view')
def board_view():
    board_id = request.args['id']
    print('board_id: ' + board_id)
    db = pymysql.connect(host='database-1.c2zw45njcc7u.ap-northeast-2.rds.amazonaws.com', db='pbldb',
                         port=3306, passwd=db_password, user='admin')
    curs= db.cursor(pymysql.cursors.DictCursor)
    sql = 'select * from board where id = %s'
    curs.execute(sql, (board_id))
    result = curs.fetchone()
    curs.close()
    db.close()
    print(result)

    return render_template('board_view.html', result= result)


if __name__ == '__main__':
    app.run("0.0.0.0", port=8080)

