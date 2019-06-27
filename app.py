import os
from flask import Flask,jsonify

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
@app.route('/hello')
def hello():
    return "hello"
@app.route('/api/test')
def send():
    return jsonify({"user":"pt","message":"đã xem"})
if __name__ == '__main__':
    app.run()