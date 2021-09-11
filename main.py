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
    doc_ref = db.collection(u'quedas').document()
    doc_ref.set({
        'usuario': user,
        'timestamp': datetime.now()
    })
    requests.get('https://api.telegram.org/' + os.getenv("BOT_TOKEN") + '/sendMessage', {'chat_id': os.getenv("TELEGRAM_USER_ID"), 'text': message})

if __name__ == "__main__":
    save_and_send_message("test","test")
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as so:
        HOST = ''
        PORT = 5555
        so.bind((HOST, PORT))
        start = time.time()
        falling = False
        while True:
            message, address = so.recvfrom(8192)
            x,y,z = str(message).split(',')[2:]
            x = float(x.strip())
            y = float(y.strip())
            z = float(z.strip()[:-1])
            s_factor = (x**2 + y**2 + z**2)**(1/2)
            if abs(s_factor) > 10 or abs(s_factor) < 9:
                if(not falling):
                    start = time.time()
                    falling = True
                elif(time.time() - start > 0.6 and abs(z) > 15 or abs(x) > 15 or abs(y) > 15):
                    threading.Thread(target=save_and_send_message, args=(message,address[0]), daemon=True).start()
                    falling = False
            else:
                falling = False