import socket, cv2, pickle, struct
from subs.Camera import Camera

cam = Camera()
cam.initCamera()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_name = socket.gethostname()
host_ip = '192.168.1.240'
print('HOST IP:', host_ip)
port = 9999
socket_address = (host_ip, port)

server_socket.bind(socket_address)


server_socket.listen(5)
print("LISTENING AT:", socket_address)



while True:
    client_socket, addr = server_socket.accept()
    print('GOT CONNECTION FROM:', addr)

    image, _, _ = cam.getData()
    print(image.shape)

    a = pickle.dumps(image)
    message = struct.pack("Q", len(a)) + a
    client_socket.sendall(message)

