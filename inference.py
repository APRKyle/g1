from yolo_inferencing.PostProcessor import PostProcessor
from yolo_inferencing.PreProcessor import PreProcessor
from yolo_inferencing.EngineProcessor import EngineProcessor

from subs.Camera import Camera

import cv2
import numpy as np
import time


camera = Camera()


ep = EngineProcessor('/home/andrii/Gus2/networks/yolo_asparagus/model.engine')
prp = PreProcessor()
pop = PostProcessor(iou_threshold = 0.62, class_threshold = 0.75,
                 input_height = 480, input_width = 640, img_height = 480, img_width = 640,
                  num_masks = 32)
ep.initalize()



camera.initCamera()

c = 0
tt = 0
for i in range(10):
    c+=1
    t = time.time()
    image, depthRS, depthNP = camera.getData()

    image_data = prp.process(image)
    output = ep.process(image_data)
    boxes, masks, classid = pop.process(output)
    tt+= time.time() - t
    print(f' inference time: {time.time() - t}')

print(f' averate inference time: {tt/c}')

ep.deinitialize()