import socket
import time
import requests
import threading

token = 'bot1971405735:AAFNwbmSxHAESBNn4jHDGpEa9YtyP5LXKJY'

def send_message(message):
    requests.get('https://api.telegram.org/' + token + '/sendMessage', {'chat_id': 849757625, 'text': message})

if __name__ == "__main__":
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
                elif(time.time() - start > 0.4 and abs(z) > 9 and abs(x) < 2 and abs(y) < 2):
                    print(s_factor)
            else:
                falling = False
            #if time.time() - start > 2:
            #    start = time.time()
            #    threading.Thread(target=send_message, args=(message,), daemon=True).start()