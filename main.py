import socket
import time
import requests
import threading
from vars import TELEGRAM_USER_ID

def save_and_send_message(message, user):
    print("There has been a fall; waiting for message saving and sending API response...")
    r = requests.post(url = " https://k6yz5w2j2l.execute-api.us-east-1.amazonaws.com/dev/", json = {"message": str(message), "user": str(user), "chat_id": TELEGRAM_USER_ID})
    print(r.text)
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
