from yolo_inferencing.PostProcessor import PostProcessor
from yolo_inferencing.PreProcessor import PreProcessor
from yolo_inferencing.EngineProcessor import EngineProcessor

from subs.Camera import Camera
from subs.VideoInterface import Output
import cv2
import numpy as np
import time
image = cv2.imread('/home/andrii/Gus2/asparagus.png')


ep = EngineProcessor('/home/andrii/Gus2/networks/yolo_asparagus/model.engine')
prp = PreProcessor()
pop = PostProcessor(iou_threshold=0.62, class_threshold=0.75,
                    input_height=480, input_width=640, img_height=480, img_width=640,
                    num_masks=32)
ep.initalize()





image_data = prp.process(image)
net_output = ep.process(image_data)
boxes, masks, classid = pop.process(net_output)


np.save('boxes.npy', boxes)
np.save('masks.npy', masks)
np.save('class.npy', classid)
ep.deinitialize()