from calibration.QRTracker import Tracker
from subs.Camera import Camera
from subs.VideoInterface import Streamer

camera = Camera(imageHeight=720, imageWidth=1280, fps=15)
tracker = Tracker(camera=camera)
camera.initCamera()
output = Streamer(ip='192.168.1.108')
output.initStreamer()

while True:
    camera.getData()
    c = tracker.get_coordinate()
    if c is not None:
        print(c)

    # tracker.gc2()
    output.Render(camera.image)