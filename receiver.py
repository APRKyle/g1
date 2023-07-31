import numpy as np
import struct
import cv2
import socket

def receive_frame(sock):
    # Receive the size of the frame
    size_data = b''
    while len(size_data) < 4:
        size_data += sock.recv(4 - len(size_data))
    size = struct.unpack('<L', size_data)[0]

    # Receive the frame data
    frame_data = b''
    while len(frame_data) < size:
        frame_data += sock.recv(size - len(frame_data))

    # Decode and display the frame
    frame = cv2.imdecode(np.frombuffer(frame_data, dtype=np.uint8), cv2.IMREAD_COLOR)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    cv2.imshow('Received Stream', frame)
    cv2.waitKey(1)


receiver_ip = '0.0.0.0'  # Listen on all available interfaces
receiver_port = 5000

# Create a socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((receiver_ip, receiver_port))
sock.listen(1)

# Accept incoming connection
conn, addr = sock.accept()

try:
    while True:
        # Receive and display the frame
        receive_frame(conn)
except KeyboardInterrupt:
    conn.close()
    sock.close()
    cv2.destroyAllWindows()