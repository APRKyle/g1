import cv2, struct, socket
from subs.Camera import Camera
from subs.VideoInterface import Streamer
import time

cam = Camera()
cam.initCamera()

output = Streamer(ip = '192.168.1.232', port = '5000')
output.initStreamer()

try:
    while True:
        image, _, _ = cam.getData()
        output.Render(image)

except KeyboardInterrupt:
    cv2.destroyAllWindows()

    # Close the socket
    output.close()



