import socket
import threading
import sys


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
        # else:
        #     print("Client's username is empty")

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
