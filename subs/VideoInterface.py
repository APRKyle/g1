import jetson.utils
import socket
import cv2
import struct



class Output:
    def __init__(self, ip=None, path=None):

        self.ip = ip
        self.videoPath = path

    def initOutput(self):

        if self.ip:
            self.streamOutput = jetson.utils.videoOutput(f'rtp://{self.ip}:15000')

        if self.videoPath:
            self.videoSaver = jetson.utils.videoOutput(f'file://{self.videoPath}')



    def Render(self, image):
        output = jetson.utils.cudaFromNumpy(image)
        if self.ip:
            self.streamOutput.Render(output)
        if self.videoPath:
            self.videoSaver.Render(output)


import json

class Streamer:
    def __init__(self, ip='192.168.1.108', port=5000):
        self.receiver_ip = ip
        self.receiver_port = port

    def initStreamer(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.receiver_ip, self.receiver_port))

    def Render(self, image, data_array):
        # Serialize the image and additional data (data_array) to JSON
        frame_data = cv2.imencode('.jpg', image)[1].tostring()
        data = {
            'image': frame_data.decode('latin1'),  # Convert bytes to string for JSON serialization
            'data_array': data_array.tolist()  # Convert the NumPy array to a list for JSON serialization
        }
        json_data = json.dumps(data).encode('utf-8')

        # Send the JSON data with the size header
        size = len(json_data)
        data = struct.pack('<L', size) + json_data
        self.sock.sendall(data)

    def close(self):
        self.sock.close()


