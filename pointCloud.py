from yolo_inferencing.PostProcessor import PostProcessor
from yolo_inferencing.PreProcessor import PreProcessor
from yolo_inferencing.EngineProcessor import EngineProcessor

from subs.Camera import Camera
from subs.VideoInterface import Streamer
from subs.AsparagusProcessor import AsparagusProcessor
from subs.Pather import Pather
from subs.Visualizer import Vizualizer
from subs.Communicator import Communicator
from subs.Spear import Spear

import cv2
import numpy as np
import traceback

output = Streamer(ip = '192.168.1.232', port = 5000)
camera = Camera()

ep = EngineProcessor('/home/andrii/Gus2/networks/yolo2/model.engine')
prp = PreProcessor()
pop = PostProcessor(iou_threshold = 0.8, class_threshold = 0.85,
                 input_height = 480, input_width = 640, img_height = 480, img_width = 640,
                  num_masks = 32)


ep.initalize()
camera.initCamera()
output.initStreamer()


ignore_distance = 300
botk = 0.05
topk = 0.05



def split_into_n_pices(n , mask):
    dist = mask[0].max() - mask[0].min()
    step = dist//n
    c = mask[0].min()
    part = mask[np.logical_and(mask[0] >=c, mask[0] <= c + step)]
    print(part)
    v  = np.mean(part, axis = 1)
    print(v)
    return v


try:
    while True:


        camera.getData()
        image = camera.image
        image_data = prp.process(image)
        net_output = ep.process(image_data)
        boxes, masks, classid = pop.process(net_output)
        spears = []

        if len(classid) != 0:


            for idx, (box, mask) in enumerate(zip(boxes, masks)):

                mask[np.logical_and(mask == 1, camera.depthNP == 0)] = 0  # stereo dispaired pixels distance check
                mask[np.logical_and(mask == 1, camera.depthNP > ignore_distance)] = 0  # unreachable pixel ignorance

                if np.all(np.all(mask == 0)):
                    continue

                mask = mask.astype(np.uint8)
                asparagusMask = np.where(mask == 1)
                asparagus = np.array([asparagusMask[0], asparagusMask[1]])

                v = split_into_n_pices(3, asparagus)
                cv2.circle(image, (v[0], v[1]), 4, (255,0,0), 3)

                image[asparagus[0], asparagus[1], 1] = 120



        output.Render(image)

except Exception as e:
    traceback.print_exc()
    ep.deinitialize()
finally:
    ep.deinitialize()