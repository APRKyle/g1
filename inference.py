from yolo_inferencing.PostProcessor import PostProcessor
from yolo_inferencing.PreProcessor import PreProcessor
from yolo_inferencing.EngineProcessor import EngineProcessor

from subs.Camera import Camera
from subs.VideoInterface import Output
from subs.AsparagusProcessor import AsparagusProcessor
from subs.Pather import Pather

import cv2
import numpy as np
import time

output = Output(path = 'video.mp4')
camera = Camera()


ep = EngineProcessor('/home/andrii/Gus2/networks/yolo_asparagus/model.engine')
prp = PreProcessor()
pop = PostProcessor(iou_threshold = 0.62, class_threshold = 0.75,
                 input_height = 480, input_width = 640, img_height = 480, img_width = 640,
                  num_masks = 32)
asparagusProcessor = AsparagusProcessor(topk = 0.06, botk = 0.06)
pather = Pather(camera = camera, min_lenght = 1000000, min_dist = 100000)

ep.initalize()
camera.initCamera()
output.initOutput()


try:
    while True:

        image, depthRS, depthNP = camera.getData()

        image_data = prp.process(image)
        net_output = ep.process(image_data)
        boxes, masks, classid = pop.process(net_output)
        spears = asparagusProcessor.process(boxes, masks)
        stopSignal, spear = pather.processSpears(spears, depthRS)
        print(f' stop signal: {stopSignal}')
        output.Render(image)

except Exception as e:
    print(f'Error: {e}')
    ep.deinitialize()
finally:
    ep.deinitialize()