import os
import  json
import requests
from flask import Flask,jsonify,request,sessions,request
from flask_socketio import SocketIO,send,emit,join_room,leave_room,disconnect
import threading
import pika
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
page_token='EAAFS8KvsJCoBAIkf6pMsAaS86XwHxR90pewZB6nTVCGhrQaxNNsg1Bxgu67mzdDpRw6fHuft5MPqySfjrjWB2SUkI6ZAPgzNKk7rfFDzqMZBxjgLG18ePmzDGdrxs87GJGU4lL4ZAvhEloZBDx4OoqrZBVzqbq6AjM7gcKspY6S44HKvZCUR8B4'
socketio = SocketIO(app)
users = []
params = pika.URLParameters("amqp://mpjwnvkj:xdUQ4XXvUe-ctLuYrEiWExl3ISo3Batm@hornet.rmq.cloudamqp.com/mpjwnvkj")

@app.route('/',methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        print(request.args.get("hub.verify_token"))
        if not request.args.get("hub.verify_token") == 'phongthien':
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200
@app.route('/api/test')
def send():
    return jsonify({"user":"pt","message":"đã xem"})

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message

                    sender_id = messaging_event["sender"]["id"]  # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"][
                        "id"]  # the recipient's ID, which should be your page's facebook ID
                    message_text = messaging_event["message"]["text"]  # the message's text

                    send_message(sender_id, "go go go ")
                    push_message(message_text,"customer")

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass
    print(data)
    return "ok", 200
def send_message(recipient_id, message_text):



    params = {
        "access_token": page_token
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        print(r.status_code)
@socketio.on('connect')
def connect():
    print("connect")
    print( request.sid)
    id=request.sid;

    user=request.args.get("token", None)
    print(request.args.get("token", None))
    check=True
    for item in users:
        if  item["user"]==user:
            item["count"]=item["count"]+1
            check=False
    if check==True:
        users.append({"user":user,"count":1})

    emit("connect",users,broadcast=True)


@socketio.on('message')
def handleMessage(message):

    emit(message["username"],message)
    push_message(json.dumps(message),"server")
@socketio.on('disconnect')
def test_disconnect():
    user = request.args.get("token", None)
    check = True
    for item in users:
        if item["user"] == user:
            item["count"] = item["count"]-1
            if item["count"]<=0:
                users.remove(item)


def push_message(message,user):
    print(message)
    connection = pika.BlockingConnection(
        params)
    channel = connection.channel()

    channel.queue_declare(queue=user)

    channel.basic_publish(exchange='', routing_key='phongthien', body=message)
    print(message)
def receive_message(user):
    connection = pika.BlockingConnection(
       params)
    channel = connection.channel()

    channel.queue_declare(queue='hello')

    print(user)
    if user=="customer":
       channel.basic_consume(queue=user, on_message_callback=callback_user, auto_ack=True)
    else:
       channel.basic_consume(queue=user, on_message_callback=callback_server, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')


    channel.start_consuming()


def callback_user(ch, method, properties, body):
    print("re",body.decode('utf8'))
    a= body.decode('utf8')
    print(a)
    emit('phongthiendequan24',{"user":"giang","message":a} , broadcast=True)
def callback_server(ch, method, properties, body):
    print("resp",body)

if __name__ == '__main__':

    socketio.run(app, debug=True)
