import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox

DARK_GREY = '#121212'
MEDIUM_GREY = '#1F1B24'
OCEAN_BLUE = '#464EB8'
WHITE = "white"
FONT = ("Helvetica", 17)
BUTTON_FONT = ("Helvetica", 15)
SMALL_FONT = ("Helvetica", 13)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = '10.0.113.167'
POST = 55555 # use any port from 0 to 65535

def add_message(message):
    message_box.config(state=tk.NORMAL)
    message_box.insert(tk.END, message + '\n')
    message_box.config(state=tk.DISABLED)

def connect():
    # connect to server
    username  = username_textbox.get().strip()
    if(username == ""):
        messagebox.showerror("Invalid username", "Username cannot be empty")
        return
    try:
        client.connect((HOST, POST))
        print(f"Successfully connect to server")
        add_message("[SERVER] Successfully connected to the server")
        client.sendall(username.encode())
        username_textbox.config(state=tk.DISABLED)
        username_button.config(state=tk.DISABLED)

        threading.Thread(target=listen_for_messages_from_server, args=(client, )).start()
    except:
        messagebox.showerror("Unable to connect to server", f"Unable to server {HOST} {POST}")
        return


def send_message():
    message = message_textbox.get()
    if message != '':
        client.sendall(message.encode())
        message_textbox.delete(0, len(message))
    else:
        messagebox.showerror("Empty message", "Message cannot be empty")

root = tk.Tk()
root.geometry("600x600")
root.title("Messenger client")
root.resizable(False, False)

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=4)
root.grid_rowconfigure(2, weight=1)

top_frame = tk.Frame(root, width=600, height=100, bg=DARK_GREY)
top_frame.grid(row=0, column=0, sticky=tk.NSEW)

middle_frame = tk.Frame(root, width=600, height=400, bg=MEDIUM_GREY)
middle_frame.grid(row=1, column=0, sticky=tk.NSEW)

bottom_frame = tk.Frame(root, width=600, height=100, bg=DARK_GREY)
bottom_frame.grid(row=2, column=0, sticky=tk.NSEW)

username_lable = tk.Label(top_frame, text="Enter username: ", font=FONT, bg=DARK_GREY, fg=WHITE)
username_lable.pack(side=tk.LEFT, padx=10)

username_textbox = tk.Entry(top_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=23)
username_textbox.pack(side=tk.LEFT)

username_button = tk.Button(top_frame, text="Join", font=SMALL_FONT, bg=OCEAN_BLUE, fg=WHITE, command=connect)
username_button.pack(side=tk.LEFT, padx=15)

message_textbox = tk.Entry(bottom_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=38)
message_textbox.pack(side=tk.LEFT, padx=10)

message_button = tk.Button(bottom_frame, text="Send", font=MEDIUM_GREY, bg=OCEAN_BLUE, fg=WHITE, command=send_message)
message_button.pack(side=tk.LEFT, padx=10)

message_box = scrolledtext.ScrolledText(middle_frame, font=SMALL_FONT, bg=MEDIUM_GREY, fg=WHITE, width=67, height=26)
message_box.config(state=tk.DISABLED)
message_box.pack(side=tk.TOP)



def listen_for_messages_from_server(client):
    while True:
        message = client.recv(2048).decode("utf-8")
        if message != '':
            username = message.split('~')[0]
            content = message.split('~')[1]

            add_message(f"[{username}] {content}")
        else:
            messagebox.showerror("Error", "Message received from client is empty")

def main():

    root.mainloop()

if __name__ == '__main__':
    main()