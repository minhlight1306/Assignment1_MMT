import pickle
import struct 
import cv2
import socket
import datetime

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('10.229.242.30', 55555))
cap = cv2.VideoCapture(0)
img_counter = 0
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
while True:
	sendingTime = datetime.datetime.now()
	ret, frame = cap.read()
	cv2.imshow("P2P Live Stream (Client)", frame)
	result, frame = cv2.imencode('.jpg', frame, encode_param)
	dictionary = {
		"frame": frame,
        "time": sendingTime
	}
	
	data = pickle.dumps(dictionary, 0)
	size = len(data)
	if cv2.waitKey(1) == ord('q'):
		break
	client_socket.sendall(struct.pack(">L", size) + data)
	img_counter += 1
cap.release()
print('Close the socket')
client_socket.close()