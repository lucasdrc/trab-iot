import json
import requests
import firebase_admin
import requests
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime
from vars import BOT_TOKEN, FIREBASE_CERT_PATH

cred = credentials.Certificate(FIREBASE_CERT_PATH)
firebase_admin.initialize_app(cred)
db = firestore.client()

def main(event, _):
    message = json.loads(event["body"])["message"]
    user = json.loads(event["body"])["user"]
    chat_id = json.loads(event["body"])["chat_id"]
    doc_ref = db.collection("quedas").document()
    doc_ref.set({"usuario": user, "timestamp": datetime.now()})
    requests.get(
        f"https://api.telegram.org/{BOT_TOKEN}/sendMessage",
        {"chat_id": chat_id, "text": message},
    )

    body = {
        "message": "Fall event successfully registered",
        "input": { message: message, user: user }
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
