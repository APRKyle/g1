import cv2
import numpy as np


class PreProcessor:
    def __init__(self):
        pass
    def process(self, image_ori):
        image = cv2.resize(image_ori, (640, 320))
        image = (1.0 / 255.0) * image.transpose((2, 0, 1))

        return image

