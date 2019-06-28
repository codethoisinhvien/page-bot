import os
import  json
import requests
from flask import Flask,jsonify,request

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
page_token='EAAFS8KvsJCoBAIkf6pMsAaS86XwHxR90pewZB6nTVCGhrQaxNNsg1Bxgu67mzdDpRw6fHuft5MPqySfjrjWB2SUkI6ZAPgzNKk7rfFDzqMZBxjgLG18ePmzDGdrxs87GJGU4lL4ZAvhEloZBDx4OoqrZBVzqbq6AjM7gcKspY6S44HKvZCUR8B4'
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

if __name__ == '__main__':
    app.run(debug=True)