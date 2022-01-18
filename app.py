from flask import Flask

app = Flask(__name__)

@app.route('/')
def hell():
    return 'Hello Flask'

@app.route('/test')
def test():
    # 수행해야할 로직이 여기 들어온다(예: 디비에서 데이터를 끌어온다는지..)
    return "test"

if __name__ == '__main__':
    app.run("0.0.0.0", port=8080)

