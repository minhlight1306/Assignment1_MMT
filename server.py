import socket
import threading
import cv2
import pickle
import numpy as np
import struct
import datetime


HOST = '10.0.113.167'
POST = 55555 # use any port from 0 to 65535
LISTENER_LIMIT = 5
active_clients = []
nicknames = []

# Function to listen for upcoming mess from a client
def listen_for_messages(client, username):
    while True:
        try:
            message = client.recv(2048).decode("utf-8")
            if message != '':
                final_msg = username + '~' + message
                send_message_to_all(final_msg)
            else:
                print(f"The message send from client {username} is empty")
        except ConnectionResetError:
            print(f"Client {username} has disconnected from the server")
            break
        except Exception as e:
            print(f"Error receiving message from {username}: {e}")
            break
    if username in nicknames:
        nicknames.remove(username)
    if client in active_clients:        
        active_clients.remove(client)

def send_message_to_client(client, message):
    client.sendall(message.encode())

# Function to send any new mess to all the client connected to this clients
def send_message_to_all(message):
    for user in active_clients:
        send_message_to_client(user, message)

# Function to live stream the video
def live_stream(client):
    data = b""
    payload_size = struct.calcsize(">L")
    while True:
        while len(data) < payload_size:
            data += client.recv(4096)
            if not data:
                live_stream(client)

        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack(">L", packed_msg_size)[0]
        print("msg_size: {}".format(msg_size))
        recivDate = datetime.datetime.now()

        while len(data) < msg_size:
            container = client.recv(4096)
            if not container:
                live_stream(client)
            data += container

        frame_data = data[:msg_size]
        data = data[msg_size:]
        frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
        print("delay: {}".format(recivDate - frame['time']))
        frame = cv2.imdecode(frame['frame'], cv2.IMREAD_COLOR)

        cv2.imshow("Live Stream", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Function tp handle client
def handle(client):
    while True:
        message = client.recv(2048).decode("utf-8")
        if message != '':
            if message in active_clients:
                print(f"Client {message} is already connected to server")
                client.close()
                break

            active_clients.append(client)
            nicknames.append(message)
            prompt_message = "SERVER~" + f"{message} has joined the server!"
            send_message_to_all(prompt_message)
            break
        # live stream
        # create a button to start live

    threading.Thread(target=listen_for_messages, args=(client, message)).start()

def main():
    # create a socket class object
    # AF_INET: we are going to use IPv4
    # SOCK_STREAM: we are using TCP
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((HOST, POST))
        print(f"Running the server on {HOST} and {POST}")
    except Exception as e:
        print(f'Unable to bind to host {HOST} and {POST}: {e}')
        return

    server.listen(LISTENER_LIMIT)

    while True:
        client, address = server.accept()
        print(f"Successfully connected with {address[0], address[1]}")

        threading.Thread(target=handle, args=(client, )).start()

if __name__ == '__main__':
    main()
