import socket
import threading
import cv2
import pickle
import struct
import datetime
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter import PhotoImage
import time
import os
import sys

DARK_GREY = '#121212'
MEDIUM_GREY = '#1F1B24'
OCEAN_BLUE = '#464EB8'
WHITE = "white"
FONT = ("Helvetica", 17)
BUTTON_FONT = ("Helvetica", 15)
SMALL_FONT = ("Helvetica", 13)
GREAT_SMALL_FONT = ("Helvetica", 8)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = '10.0.105.119'
POST = 55555 # use any port from 0 to 65535
running = True

def add_message(message):
    message_box.config(state=tk.NORMAL)
    message_box.insert(tk.END, message + '\n')
    message_box.see(tk.END)
    message_box.config(state=tk.DISABLED)

def send_message():
    message = message_textbox.get()
    if message != '':
        client.sendall(message.encode())
        message_textbox.delete(0, len(message))
    else:
        messagebox.showerror("Empty message", "Message cannot be empty")

def register_peer(username):
    message = f"REGISTER {username}"

    print(f"Register: {message}")
    client.sendall(message.encode())

def connect():
    # connect to server
    username  = username_textbox.get().strip()
    if(username == ""):
        messagebox.showerror("Invalid username", "Username cannot be empty")
        return
    try:
        client.connect((HOST, POST))
        
        register_peer(username) # Register the peer with the server
        username_textbox.config(state=tk.DISABLED)
        username_button.config(state=tk.DISABLED)
        stream_button.config(state=tk.NORMAL)
        message_button.config(state=tk.NORMAL)
        guest_button.config(state=tk.DISABLED)

        # Start a thread to listen for messages from the server
        threading.Thread(target=listen_for_messages_from_server, args=(client, )).start()
    except:
        messagebox.showerror("Unable to connect to server", f"Unable to server {HOST} {POST}")

def send_request_live_stream():
    client.sendall("START_LIVE".encode())
    print("start live")
        
def start_live_stream():
    print("Starting live stream...")
    send_request_live_stream()

    cap = cv2.VideoCapture(0)
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            cv2.imshow("Live Stream", frame)
            # Mã hóa khung hình
            result, encoded_frame = cv2.imencode('.jpg', frame, encode_param)
            data = pickle.dumps(encoded_frame, 0)
            size = len(data)

            # Gửi dữ liệu video đến server
            client.sendall(struct.pack(">L", size) + data)

            if cv2.waitKey(1) == ord('`'):
                print("Stopping live")
                break
    except Exception as e:
        print(f"Error during live stream: {e}")
    finally:
        cap.release()
        cv2.destroyAllWindows()
        client.sendall("ACK")

# Function to connect live stream the video
def connect_live():
    print(f"Connected to live stream")

    data = b""
    payload_size = struct.calcsize(">L")
    print("Payload size:", payload_size)

    while True:
        try:
            while len(data) < payload_size:
                packet = client.recv(4096)
                if not packet:
                    print("Client disconnected.")
                    return
                data += packet

            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack(">L", packed_msg_size)[0]
            print(f"Message size: {msg_size}")

            while len(data) < msg_size:
                packet = client.recv(4096)
                if not packet:
                    print("Incomplete frame received, skipping...")
                    break
                data += packet

            frame_data = data[:msg_size]
            data = data[msg_size:]

            frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
            frame = cv2.imdecode(frame['frame'], cv2.IMREAD_COLOR)

            cv2.imshow("Fetch Live Stream", frame)
            if cv2.waitKey(1) == ord('`'):
                break
        except Exception as e:
            print(f"Error receiving live stream: {e}")
            break

    cv2.destroyAllWindows()

# Function to connect as a guest
def connect_as_guest():
    try:
        client.connect((HOST, POST))
        client.sendall("GUEST".encode())  # Đăng ký với server
        username_button.config(state=tk.DISABLED)
        stream_button.config(state=tk.DISABLED)
        message_button.config(state=tk.DISABLED)
        guest_button.config(state=tk.DISABLED)

        # Bắt đầu lắng nghe tin nhắn từ server
        threading.Thread(target=listen_for_messages_from_server, args=(client,)).start()
    except Exception as e:
        messagebox.showerror("Unable to connect to server", f"Error: {e}")

root = tk.Tk()
root.geometry("620x600")
root.title("Messenger client")
root.resizable(False, False)

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=4)
root.grid_rowconfigure(2, weight=1)

top_frame = tk.Frame(root, width=620, height=100, bg=DARK_GREY)
top_frame.grid(row=0, column=0, sticky=tk.NSEW)

middle_frame = tk.Frame(root, width=620, height=400, bg=MEDIUM_GREY)
middle_frame.grid(row=1, column=0, sticky=tk.NSEW)

bottom_frame = tk.Frame(root, width=620, height=100, bg=DARK_GREY)
bottom_frame.grid(row=2, column=0, sticky=tk.NSEW)

username_lable = tk.Label(top_frame, text="Enter username: ", font=FONT, bg=DARK_GREY, fg=WHITE)
username_lable.pack(side=tk.LEFT, padx=10)

username_textbox = tk.Entry(top_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=23)
username_textbox.pack(side=tk.LEFT)

username_button = tk.Button(top_frame, text="Join", font=SMALL_FONT, bg=OCEAN_BLUE, fg=WHITE, command=connect)
username_button.pack(side=tk.LEFT, padx=(15, 5))

stream_button = tk.Button(top_frame, text="Live", font=SMALL_FONT, bg=OCEAN_BLUE, fg=WHITE,
                          command=start_live_stream)
stream_button.pack(side=tk.LEFT, padx=5)
stream_button.config(state=tk.DISABLED)

message_textbox = tk.Entry(bottom_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=35)
message_textbox.pack(side=tk.LEFT, padx=10)

message_button = tk.Button(bottom_frame, text="Send", font=MEDIUM_GREY, bg=OCEAN_BLUE, fg=WHITE, command=send_message)
message_button.pack(side=tk.LEFT, padx=(10, 0))
message_button.config(state=tk.DISABLED)

guest_button = tk.Button(bottom_frame, text="Guest", font=SMALL_FONT, bg=OCEAN_BLUE, fg=WHITE, 
                         command=connect_as_guest)
guest_button.pack(side=tk.LEFT, padx=(5, 0))
guest_button.config(state=tk.NORMAL)

message_box = tk.Text(middle_frame, font=SMALL_FONT, bg=MEDIUM_GREY, fg=WHITE, width=62, height=26, wrap=tk.WORD)
message_box.config(state=tk.DISABLED)
message_box.pack(side=tk.LEFT, fill=tk.BOTH)

online_box = tk.Text(middle_frame, font=GREAT_SMALL_FONT, bg=DARK_GREY, fg=WHITE, width=10, height=26, wrap=tk.NONE)
online_box.config(state=tk.DISABLED)
online_box.pack(side=tk.RIGHT, fill=tk.BOTH)

def update_online_users(user):
    online_box.config(state=tk.NORMAL)
    online_box.insert(tk.END, f"{user}\n")
    online_box.see(tk.END)
    online_box.config(state=tk.DISABLED)

def update_offline_users(user):
    online_box.config(state=tk.NORMAL)
    lines = online_box.get(1.0, tk.END).splitlines()  # Lấy tất cả các dòng trong online_box
    online_box.delete(1.0, tk.END)  # Xóa toàn bộ nội dung
    for line in lines:
        if line.strip() != user:  # Chỉ thêm lại các user không phải là user cần xóa
            online_box.insert(tk.END, f"{line}\n")
    online_box.config(state=tk.DISABLED)

def reconnect_to_server():
    global running
    attempts = 0
    max_attempts = 5
    while attempts < max_attempts:
        try:
            print(f"Attempting to reconnect... ({attempts + 1}/{max_attempts})")
            client.close()
            # client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((HOST, POST))
            print("Reconnected to the server.")
            running = True
            threading.Thread(target=listen_for_messages_from_server, args=(client,)).start()
            return True
        except Exception as e:
            print(f"Reconnect attempt {attempts + 1} failed: {e}")
            attempts += 1
            time.sleep(5)  # Chờ 5 giây trước khi thử lại
    print("Failed to reconnect after 5 attempts. Exiting...")
    running = False
    close_client()
    return False

def listen_for_messages_from_server(client):

    global running
    while running:
        try:
            message = client.recv(2048).decode("utf-8")
            print(f"Listen message: {message}")
            if message != '':
                if message.startswith("ONLINE_USERS~"):
                    user = message.split('~')[1]
                    update_online_users(user)
                    client.sendall("ACK".encode())

                elif message.startswith("ADD_ONLINE_USERS~"):
                    user = message.split("~")[1]
                    update_online_users(user)

                elif message.startswith("OFFLINE_USERS~"):
                    user = message.split('~')[1]
                    update_offline_users(user)

                elif message.startswith("LIVE_STREAM~"):
                    
                    threading.Thread(target=connect_live, args=()).start()
                
                elif message.startswith("HISTORY"):
                    fulcontent = ' '.join(message.split(' ')[1:])
                    username = fulcontent.split('~')[0]
                    content = fulcontent.split('~')[1]
                    add_message(f"[{username}] {content}")
                    client.sendall("ACK".encode())
                    
                else:
                    username = message.split('~')[0]
                    content = message.split('~')[1]
                    add_message(f"[{username}] {content}")
            else:
                messagebox.showerror("Error", "Message received from client is empty")
        except ConnectionResetError:
            print("Connection to the server was lost.")
            messagebox.showerror("Error", "Connection to the server was lost.")
            running = False
            if not reconnect_to_server():
                break
        except UnicodeDecodeError:
            pass
        except Exception as e:
            print(f"Error listen message: {e}")
            break

def close_client():
    global running
    running = False
    try:
        client.close()  # Đóng socket
        print("\nClient socket closed.")
    except Exception as e:
        print(f"Error while closing client socket: {e}")
    finally:
        root.destroy()
        os._exit(0)

root.protocol("WM_DELETE_WINDOW", close_client)

def main():
    root.mainloop()

if __name__ == '__main__':
    main()