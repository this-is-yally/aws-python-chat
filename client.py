import socket
from threading import Thread
from datetime import datetime
from colorama import Fore, init

separator_token = "<SEP>"

SERVER_HOST = "3.67.10.70"
SERVER_PORT = 8080

s = socket.socket()

print(f"[*] Connecting to {SERVER_HOST}:{SERVER_PORT}...")
s.connect((SERVER_HOST, SERVER_PORT))
print("[+] Connected.")
name = input("Write your name: ").strip()

def listen_for_messages():
    while True:
        message = s.recv(1024).decode()
        print("\n" + message)

t = Thread(target=listen_for_messages)
t.daemon = True
t.start()

while True:
    # input message we want to send to the server
    to_send = input()
    
    # a way to exit the program
    if to_send.lower() == 'q':
        break
    
    # Remove color formatting before sending the message
    to_send = to_send.replace(Fore.RESET, "")
    
    # Add the datetime, name, and the separator
    date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    to_send = f"[{date_now}] {name}{separator_token}{to_send}"
    
    # Finally, send the message
    s.send(to_send.encode())

s.close()
