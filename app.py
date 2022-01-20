from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')  # route는 url 생성하는 함수 ## /만 쓴거는 ip만 써도 나오는 기본 주소
def hell():
    return '<h1> Hello Flask!! <h1>' # 내가 보내야할 정보가 있다면 return 값에 넣어주기

@app.route("/hello")
def hi():
    name1 = "mango"
    return render_template('hello.html', name = name1)  # http://172.20.40.79:8080 이 뒤에 /hello 를 적어줘야 열림

@app.route('/test')
def test():
    # 수행해야할 로직이 여기 들어온다(예: 디비에서 데이터를 끌어온다는지..)
    return "test"

if __name__ == '__main__':
    app.run("0.0.0.0", port=8080)

