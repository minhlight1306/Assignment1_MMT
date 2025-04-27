import os
import socket
import threading
import cv2
import pickle
import numpy as np
import struct
import datetime
import time


HOST = '192.168.0.114'
POST = 55555 # use any port from 0 to 65535
LISTENER_LIMIT = 5
active_clients = []
nicknames = []
message_history = []
peers = {}  # {username: (socket, (ip, port))}
live_stream_info = None  # (username, ip, port)

# Function to listen for upcoming mess from a client
def listen_for_messages(client, username, address):
    while True:
        try:
            message = client.recv(2048).decode("utf-8")
            print(f"Listen message : {message}")
            if not message:
                print(f"Listen for message failed from {username}")
                continue
            if message.startswith("START_LIVE"):
                break
            if message != "ACK":
                final_msg = username + '~' + message
                send_message_to_all(final_msg)

        except ConnectionResetError:
            disconnect_message = f"{username} has disconnected from the server!"
            print(f"{username} on {address[0], address[1]} has disconnected from the server!")
            # Thông báo khi người dùng ngắt kết nối
            if client in active_clients:
                active_clients.remove(client)
            if username in peers:
                del peers[username]
            # if live_stream_info and live_stream_info[0] == username:
            #     live_stream_info = None
            if username in nicknames:
                send_message_to_all(f"OFFLINE_USERS~{username}")
                nicknames.remove(username)
            client.close()
            send_message_to_all("SERVER~" + disconnect_message)
            # send_online_users(client)
            break
        except Exception as e:
            print(f"Error receiving message from {username}: {e}") 

def send_message_to_client(client, message):
    client.sendall(message.encode())

# Function to send any new mess to all the client connected to this clients
def send_message_to_all(message):
    if not message.startswith("ADD_ONLINE_USERS"):
        message_history.append(message)  # Lưu tin nhắn vào lịch sử
    for user in active_clients:
        send_message_to_client(user, message)

def send_message_history(client):
    for message in message_history:
        while True:
            send_message_to_client(client, "HISTORY " + message)  # Gửi lịch sử tin nhắn
            ack = client.recv(1024).decode()         # Chờ xác nhận từ client
            if ack == "ACK":
                break  # Nếu nhận được ACK, tiếp tục với tin nhắn tiếp theo
            else:
                print("Resending message:", message)  # Nếu không nhận được ACK, gửi lại

def send_online_users(client):
    for user in nicknames:
        while True:
            send_message_to_client(client, "ONLINE_USERS~" + user)
            ack = client.recv(1024).decode()
            if ack == "ACK":
                break
            else:
                print("Resending user:", user)


# Function tp handle client
def handle(client, addr):
    global peers, live_stream_info
    is_live = False
    while True:
        try:
            message = client.recv(2048).decode("utf-8")
            print(f"Handle message from {addr}: {message}")
            if not message:
                continue
            if message.startswith("REGISTER"):
                username = message.split()[1]
                if username in nicknames:
                    print(f"Client {username} is already connected to server")
                    client.close()
                    break
                peers[username] = (client, addr) #save socket and address
                
                nicknames.append(username)
                if len(active_clients) > 0:
                        send_message_to_all(f"ADD_ONLINE_USERS~{username}")
                        time.sleep(1)

                active_clients.append(client)
                # Gửi lịch sử tin nhắn cho người dùng mới
                send_message_history(client)

                # Thông báo người dùng mới tham gia
                prompt_message = f"SERVER~{username} has joined the server!"
                send_message_to_all(prompt_message)
                time.sleep(1)
                # Gửi danh sách người dùng đang online
                send_online_users(client)
                listen_for_messages(client, username, addr)  # Listen for messages from the client

                # threading.Thread(target=listen_for_messages, args=(client, usermane)).start()

            elif message.startswith("GUEST"):
                username = f"Guest{datetime.datetime.now().strftime('%H%M%S')}"  # Tạo username mặc định
                active_clients.append(client)
                # nicknames.append(username)
                peers[username] = (client, addr)

                send_message_history(client)
                send_online_users(client)
                listen_for_messages(client, username, addr)

            elif message.startswith("START_LIVE"):
                if live_stream_info is not None:
                        send_message_to_client(client, "ERROR~Another live stream is already active.")
                        continue
                
                listening_port = addr[1] + 1
                sending_port = addr[1] + 2
                live_stream_info = (username, addr[0], listening_port, sending_port)
                print(f"{username} started live streaming on ports {listening_port} (listen) and {sending_port} (send)")
                send_message_to_client(client, f"READY~{addr[0]}:{listening_port}:{sending_port}")

            elif message == "BEGIN":
                if username.size() <= 1:
                    continue
                for peer_username, (peer_socket, peer_addr) in peers.items():
                    if peer_username != username:
                        try:
                            send_message_to_client(peer_socket, f"LIVE_STREAM~{addr[0]}:{live_stream_info[2]}:{live_stream_info[3]}")
                        except Exception as e:
                            print(f"Error sending live stream info to {peer_username}: {e}")
                    # break
            else:
                if message == "ACK":
                    send_message_to_client(client, "ACK")
                listen_for_messages(client, username, addr)
        except:
            pass


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

        threading.Thread(target=handle, args=(client, address)).start()

if __name__ == '__main__':
    main()
