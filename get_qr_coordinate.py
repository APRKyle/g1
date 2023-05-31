from calibration.QRTracker import Tracker
from subs.Camera import Camera
from subs.VideoInterface import Streamer

camera = Camera()
tracker = Tracker(camera=camera)
camera.initCamera()
output = Streamer(ip='192.168.1.108')

while True:
    camera.getData()
    c = tracker.get_coordinate()
    print(c)
    output.Render(camera.image)