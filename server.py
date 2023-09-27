import socket
from threading import Thread
import logging
import sys

# Constants
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5002
separator_token = "<SEP>"

# Global variables
client_sockets = set()
error_flag = False

# Create the server.log file if it doesn't exist
with open('server.log', 'w'):
    pass

# Initialize the logger
logging.basicConfig(filename='server.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def monitor_logs():
    global error_flag
    while True:
        with open('server.log', 'r') as log_file:
            for line in log_file:
                if "ERROR" in line:
                    error_flag = True
                    print("Error detected in logs. Server will terminate.")
                    return
        if error_flag:
            break

log_monitor_thread = Thread(target=monitor_logs)
log_monitor_thread.daemon = True
log_monitor_thread.start()

def listen_for_client(cs):
    global error_flag
    while True:
        try:
            msg = cs.recv(1024).decode()
        except Exception as e:
            print(f"[!] Error: {e}")
            client_sockets.remove(cs)
        else:
            msg = msg.replace(separator_token, ": ")

            if msg.lower() == "exit":
                # Log the message as an error and set the error flag
                logging.error("Received 'exit' message.")
                error_flag = True
                break

            # Log the message
            logging.info(msg)

            for client_socket in client_sockets:
                client_socket.send(msg.encode())

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(5)
    print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

    while True:
        try:
            if error_flag:
                break
            client_socket, client_address = server_socket.accept()
            print(f"[+] {client_address} connected.")
            client_sockets.add(client_socket)

            t = Thread(target=listen_for_client, args=(client_socket,))
            t.daemon = True
            t.start()
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()
