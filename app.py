from flask import Flask, request
import requests, os
app = Flask(__name__)
VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN", "asif123")
@app.route("/")
def home(): return "Bot is running"
@app.route("/webhook", methods=["GET"])
def verify():
    if request.args.get("hub.verify_token") == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return "fail", 403
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    try:
        value = data['entry'][0]['changes'][0]['value']
        if 'messages' in value:
            from_num = value['messages'][0]['from']
            msg = value['messages'][0]['text']['body']
            token = os.environ.get("WHATSAPP_TOKEN")
            phone_id = os.environ.get("PHONE_NUMBER_ID")
            url = f"https://graph.facebook.com/v19.0/{phone_id}/messages"
            headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
            payload = {"messaging_product":"whatsapp","to":from_num,"text":{"body":f"Asif bhai ka bot: {msg}"}}
            requests.post(url, headers=headers, json=payload)
    except: pass
    return "OK", 200
