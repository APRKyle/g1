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

    def process_tests(self, image, data):

        # flag_description
        # [length, min, max]
        # length:
        #   0 - low on length
        #   1 - good on length
        # min:
        #   0 - far from robot
        #   1 - close to robot
        # max:
        #   0 - closer then max dist
        #   1 - further then reach
        def description(a):
            if   a == [0,0,0]: return 'LEN <  MIN_LEN * PP > MIN_DIST_TRUCK * PP < MAX_DIST_ARM'
            elif a == [0,0,1]: return 'LEN <  MIN_LEN * PP > MIN_DIST_TRUCK * PP > MAX_DIST_ARM'
            elif a == [0,1,0]: return 'LEN <  MIN_LEN * PP < MIN_DIST_TRUCK * PP < MAX_DIST_ARM'
            elif a == [1,0,0]: return 'LEN >= MIN_LEN * PP > MIN_DIST_TRUCK * PP < MAX_DIST_ARM'
            elif a == [1,0,1]: return 'LEN >= MIN_LEN * PP > MIN_DIST_TRUCK * PP > MAX_DIST_ARM'
            elif a == [1,1,0]: return 'LEN >= MIN_LEN * PP < MIN_DIST_TRUCK * PP < MAX_DIST_ARM'
            elif a == [0,1,1]: return 'LEN <  MIN_LEN * PP > MIN_DIST_TRUCK * PP > MAX_DIST_ARM'
            elif a == [1,1,1]: return 'LEN >= MIN_LEN * PP > MIN_DIST_TRUCK * PP > MAX_DIST_ARM'



        for spear, flags in data.items():
            text = description(flags)
            text = text.split('*')
            text.append(f'len: {str(spear.lenght)[:6]}')
            text.append(f'distance2rob: {str(np.linalg.norm(spear.arm_bot_3d))[:6]}')


            midpoint = spear.skeleton[len(spear.skeleton) // 2]

            #rectangle
            x, y = midpoint[0] - 100, midpoint[1] - 100
            width, height = 150, 180
            color_rectangle = (0, 0, 0)  # Black
            cv2.rectangle(image, (x, y), (x + width, y + height), color_rectangle, thickness=-1)

            #text

            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.5
            font_color = (255, 255, 255)
            font_thickness = 2
            for t in text:
                y = y + 30
                position = (x, y)
                cv2.putText(image, t, position, font, font_scale, font_color, font_thickness)

        return image





