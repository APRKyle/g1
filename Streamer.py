import cv2, struct, socket
from subs.Camera import Camera

cam = Camera()
cam.initCamera()


def send_frame(frame, sock):
    # Serialize the frame as a string
    frame_data = cv2.imencode('.jpg', frame)[1].tostring()

    # Get the size of the frame
    size = len(frame_data)

    # Pack the size and frame data as a struct
    data = struct.pack('<L', size) + frame_data

    # Send the frame data over the socket
    sock.sendall(data)



receiver_ip = '192.168.1.232'
receiver_port = 5000


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((receiver_ip, receiver_port))

try:
    while True:
        image, _, _ = cam.getData()
        send_frame(image, sock)
except KeyboardInterrupt:
    cv2.destroyAllWindows()

    # Close the socket
    sock.close()



