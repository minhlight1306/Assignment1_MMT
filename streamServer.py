import socket
import cv2
import pickle
import numpy as np
import struct
import datetime

serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind(('10.229.242.30', 55555))
serv.listen(5)
print("Ready to serve . . .")

def startConnection(serv):
    conn, addr = serv.accept()
    data = b""
    payload_size = struct.calcsize(">L")
    print("payload_size: {}".format(payload_size))

    while True:
        while len(data) < payload_size:
            packet = conn.recv(4096)
            if not packet:
                print("Client disconnected.")
                return
            data += packet

        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack(">L", packed_msg_size)[0]
        print("msg_size: {}".format(msg_size))

        while len(data) < msg_size:
            packet = conn.recv(4096)
            if not packet:
                print("Incomplete frame received, skipping...")
                break
            data += packet

        frame_data = data[:msg_size]
        data = data[msg_size:]

        frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
        print("delay: {}".format(datetime.datetime.now() - frame['time']))
        frame = cv2.imdecode(frame['frame'], cv2.IMREAD_COLOR)

        cv2.imshow('Fetch Video', frame)
        if cv2.waitKey(1):
            break

    conn.close()

while True:
    startConnection(serv)