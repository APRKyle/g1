import cv2
import numpy as np


class PreProcessor:
    def __init__(self, network_input_height = 480, network_input_width = 640):
        self.height = network_input_height
        self.width  = network_input_width
    def process(self, image_ori):
        image = cv2.resize(image_ori, (self.width, self.height))
        image = (1.0 / 255.0) * image.transpose((2, 0, 1))
        image = image[np.newaxis, :, :, :].astype(np.float32)

        return image

