import firebase_admin
import socket
import time
import requests
import threading
import os
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

cred = credentials.Certificate(os.getenv("FIREBASE_CERT_PATH"))
firebase_admin.initialize_app(cred)
db = firestore.client()


def save_and_send_message(message, user):
    print("There has been a fall")
    doc_ref = db.collection("quedas").document()
    doc_ref.set({"usuario": user, "timestamp": datetime.now()})
    requests.get(
        f"https://api.telegram.org/{os.getenv('BOT_TOKEN')}/sendMessage",
        {"chat_id": os.getenv("TELEGRAM_USER_ID"), "text": message},
    )
    return


def clean_and_cast_to_float(s):
    return float(s.strip().replace("'", ""))


if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as so:
        HOST = ""
        PORT = 5555
        so.bind((HOST, PORT))
        start = time.time()
        falling = False
        while True:
            message, address = so.recvfrom(8192)
            accX, accY, accZ = map(clean_and_cast_to_float, str(message).split(",")[2:5])
            s_factor = (accX ** 2 + accY ** 2 + accZ ** 2) ** 0.5
            if not 9 < abs(s_factor) < 10:
                if not falling:
                    start = time.time()
                    falling = True
                elif time.time() - start > 0.6 and any(val > 15 for val in [accX, accY, accZ]):
                    threading.Thread(
                        target=save_and_send_message,
                        args=(message, address[0]),
                        daemon=True,
                    ).start()
                    falling = False
            else:
                falling = False
