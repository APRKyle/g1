import cv2
from pyzbar.pyzbar import decode


class Tracker:
    def __init__(self, camera):
        self.camera = camera
        self.qrDecoder = cv2.QRCodeDetector()

    def get_coordinate(self):
        image = self.camera.image
        barcode = decode(image)
        try:
            mid_x = barcode[0][2][0] + int(barcode[0][2][2] / 2)
            mid_y = barcode[0][2][1] + int(barcode[0][2][3] / 2)
            coord = self.camera._calculatePix3D([mid_x, mid_y])
            coord = list(map(lambda x: int(round(x, 3) * 1000), coord))
            return coord
        except Exception as e:
            return None

if __name__ == '__main__':
    from calibration.QRTracker import Tracker
    from subs.Camera import Camera
    from subs.VideoInterface import Streamer

    camera = Camera()
    tracker = Tracker(camera = camera)
    camera.initCamera()
    output = Streamer(ip = '192.168.1.108')

    while True:
        camera.getData()
        c = tracker.get_coordinate()
        print(c)
        output.Render(camera.image)






