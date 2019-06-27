import os
from flask import Flask,jsonify,request

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
@app.route('/hello')
def hello():
    return "hello"

@app.route('/api/test')
def send():
    return jsonify({"user":"pt","message":"đã xem"})

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    print(data)
    return "ok", 200

if __name__ == '__main__':
    app.run(debug=True)