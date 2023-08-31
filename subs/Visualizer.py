import cv2
import numpy as np

class Vizualizer:
    def __init__(self, height = 480, width = 640):
        self.height = height
        self.width = width
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.font_scale = 0.5
        self.color = (0,0,0)  # Text color in BGR format
        self.thickness = 2

    def process(self, image, spears):
        for spear in spears:

            cv2.rectangle(image, (int(spear.box[0]), int(spear.box[1])),
                                 (int(spear.box[2]), int(spear.box[3])), (0, 0, 160), 1)
            p = np.where(spear.mask == 1)
            x, y = p[0], p[1]
            image[x, y, 2] = 150


            cv2.circle(image, (spear.top_point[0], spear.top_point[1]), 1, (0, 255, 0), 2)
            cv2.circle(image, (spear.bot_point[0], spear.bot_point[1]), 1, (0, 0, 255), 2)
            cv2.line(image, (spear.top_point[0], spear.top_point[1]), (spear.bot_point[0], spear.bot_point[1]), (255, 0, 0), 1)
            rounded_length = '{:.2f}'.format(spear.lenght)

        return image


