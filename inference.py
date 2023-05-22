from yolo_inferencing.PostProcessor import PostProcessor
from yolo_inferencing.PreProcessor import PreProcessor
from yolo_inferencing.EngineProcessor import EngineProcessor

import cv2
image = cv2.imread('/home/andrii/Gus2/humans.jpg')
print(f'IMAGE SHAPE: {image.shape}')

img_height, img_width = image.shape[:2]


ep = EngineProcessor('/home/andrii/Gus2/networks/yolo_w640_w480_c80/yolov8n-seg_h480_w640.onnx')
prp = PreProcessor()
pop = PostProcessor(iou_threshold = 0.3, class_threshold = 0.1,
                 input_height = 480, input_width = 640, img_height = 480, img_width = 640,
                  num_masks = 32)
ep.initalize()


import time


image_data = prp.process(image)
t = time.time()
output = ep.process(image_data)
print(time.time() - t)


boxes, masks, class_ids = pop.process(output)


# boxes: 1,116, 4200
# masks 1,32,80,160

# boxes shape: (266240,)
#  masks shape: (316680,)