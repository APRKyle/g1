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


class Streamer:
    def __init__(self, ip = '192.168.1.232', port = 5000):
        self.receiver_ip =  ip
        self.receiver_port = port

    def initStreamer(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.receiver_port, self.receiver_port))

    def Render(self, image):
        frame_data = cv2.imencode('.jpg', image)[1].tostring()
        size = len(frame_data)
        data = struct.pack('<L', size) + frame_data
        self.sock.sendall(data)

    def close(self):
        self.sock.close()


