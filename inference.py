from yolo_inferencing.PostProcessor import PostProcessor
from yolo_inferencing.PreProcessor import PreProcessor
from yolo_inferencing.EngineProcessor import EngineProcessor

import cv2
image = cv2.imread('humans.jpg')
print(f'IMAGE SHAPE: {image.shape}')

img_height, img_width = image.shape[:2]


ep = EngineProcessor('/home/andrii/GUS/SegmentationOn2GB_08_02_2023/networks/segmentation/yolo2/yolov8.engine')
prp = PreProcessor()
pop = PostProcessor(iou_threshold = 0.3, class_threshold = 0.1,
                 input_height = 320, input_width = 640, img_height = 320, img_width = 640,
                  num_masks = 32)
ep.initalize()





image_data = prp.process(image)
output = ep.process(image_data)
import numpy as np
np.save('output0.npy', output[0])
np.save('output1.npy', output[1])
print(f'boxes shape: {output[0].shape}')
print(f' masks shape: {output[1].shape}')
boxes, masks, class_ids = pop.process(output)


# boxes: 1,116, 4200
# masks 1,32,80,160

# boxes shape: (266240,)
#  masks shape: (316680,)