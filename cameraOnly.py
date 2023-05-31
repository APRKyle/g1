from subs.Camera import Camera
from subs.VideoInterface import Streamer

output = Streamer(ip = '192.168.1.108', port = 5000)
camera = Camera()

camera.initCamera()
output.initStreamer()


while True:


    camera.getData()
    image = camera.image

    output.Render(image)

