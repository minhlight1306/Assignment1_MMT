import os
import socket
import threading
import cv2
import pickle
import numpy as np
import struct
import datetime
import time
import sys


HOST = '10.0.105.119'
POST = 55555 # use any port from 0 to 65535
LISTENER_LIMIT = 5
active_clients = []
nicknames = []
message_history = []
peers = {}  # {username: (socket, (ip, port))}
current_name = None
live_stream_info = None  # (ip, port)
is_live = False
is_closed = False

# Function to listen for upcoming mess from a client
def listen_for_messages(client, username, address):
    global is_live, is_closed, live_stream_info
    while True:
        try:
            message = client.recv(2048).decode("utf-8")
            print(f"Listen message : {message}")
            if not message:
                print(f"Listen for message failed from {username}")
                continue
            if message.startswith("START_LIVE"):
                is_live = True
                live_stream_info = client  # Lưu socket của client phát live
                print(f"{username} started live streaming.")
                send_message_to_all_except(client, f"LIVE_STREAM~")
                time.sleep(1)
                # handle_live_stream(client)
                threading.Thread(target=handle_live_stream, args=(client,)).start()
                # break
            if message != "ACK":
                final_msg = username + '~' + message
                send_message_to_all(final_msg)
            # if message == "ACK":
            #     is_live = False
        # except UnicodeDecodeError:
        #     pass
        except ConnectionResetError:
            disconnect_message = f"{username} has disconnected from the server!"
            print(f"{username} on {address[0], address[1]} has disconnected from the server!")
            # Thông báo khi người dùng ngắt kết nối
            if client in active_clients:
                active_clients.remove(client)
            if username in peers:
                del peers[username]
            if username in nicknames:
                send_message_to_all(f"OFFLINE_USERS~{username}")
                nicknames.remove(username)
            client.close()
            if is_closed == False:
                send_message_to_all("SERVER~" + disconnect_message)
            is_closed = True
            break
        except Exception as e:
            print(f"Error receiving message from {username}: {e}") 

def send_message_to_client(client, message):
    client.sendall(message.encode())

# Function to send any new mess to all the client connected to this clients
def send_message_to_all(message):
    if not message.startswith("ADD_ONLINE_USERS") and not message.startswith("OFFLINE_USERS") and not message == "LIVE_STREAM~":
        if len(message_history) >= 10000:
            message_history.clear()
        message_history.append(message)  # Lưu tin nhắn vào lịch sử
    for user in active_clients:
        send_message_to_client(user, message)

def send_message_to_all_except(client, message):
    if not message.startswith("ADD_ONLINE_USERS") and not message.startswith("OFFLINE_USERS") and not message == "LIVE_STREAM~":
        if len(message_history) >= 10000:
            message_history.clear()
        message_history.append(message)  # Lưu tin nhắn vào lịch sử
    for user in active_clients:
        if user != client:
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

def handle_live_stream(client):
    global is_live
    try:
        while is_live:
            # Nhận kích thước dữ liệu
            packed_msg_size = client.recv(4)
            if not packed_msg_size:
                break
            msg_size = struct.unpack(">L", packed_msg_size)[0]

            # Nhận dữ liệu video
            data = b""
            while len(data) < msg_size:
                packet = client.recv(4096)
                if not packet:
                    break
                data += packet

            # Gửi dữ liệu video đến các client khác
            for other_client in active_clients:
                if other_client != client:
                    try:
                        other_client.sendall(struct.pack(">L", len(data)) + data)
                    except Exception as e:
                        print(f"Error sending video to client: {e}")
    except Exception as e:
        print(f"Error in live stream: {e}")
    finally:
        is_live = False
        print("Live stream ended.")

# Function tp handle client
def handle(client, addr):
    global peers, live_stream_info, is_live, is_closed, current_name, username
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
                current_name = username
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
                # peers[username] = (client, addr)

                is_closed = True
                send_message_history(client)
                send_online_users(client)
                listen_for_messages(client, username, addr)
            else:
                pass
        except:
            if is_closed:
                is_closed = False
                break
            else:
                disconnect_message = f"{username} has disconnected from the server!"
                print(f"{username} on {addr[0], addr[1]} has disconnected from the server!")
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
                is_closed = True
                break
    # listen_for_messages(client, username, addr)

def listen_for_exit(server):
    while True:
        print("Type 'exit' to stop the server")
        command = sys.stdin.readline().strip()
        if command.lower() == "exit":
            print("Shutting down the server...")
            server.close()
            os._exit(0)

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

    threading.Thread(target=listen_for_exit, args=(server,), daemon=True).start()

    try:
        while True:
            try:
                client, address = server.accept()
                print(f"Successfully connected with {address[0], address[1]}")
                threading.Thread(target=handle, args=(client, address)).start()
            except OSError:
                print("Server socket closed")
                break
    except KeyboardInterrupt:
        print("\nShutting down the server...")
        server.close()
        os._exit(0)

if __name__ == '__main__':
    main()
