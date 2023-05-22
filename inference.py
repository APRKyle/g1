from yolo_inferencing.PostProcessor import PostProcessor
from yolo_inferencing.PreProcessor import PreProcessor
from yolo_inferencing.EngineProcessor import EngineProcessor

import cv2
import numpy as np

image = cv2.imread('/home/andrii/Gus2/asparagus.jpg')
print(f'IMAGE SHAPE: {image.shape}')

img_height, img_width = image.shape[:2]


ep = EngineProcessor('/home/andrii/Gus2/networks/yolo_w640_w480_c80/yolo.engine')
prp = PreProcessor()
pop = PostProcessor(iou_threshold = 0.3, class_threshold = 0.1,
                 input_height = 480, input_width = 640, img_height = 480, img_width = 640,
                  num_masks = 32)
ep.initalize()


import time
tt = 0
c = 0

c+=1
image_data = prp.process(image)
t = time.time()
output = ep.process(image_data)
tt += (time.time() - t)
print(f' inference time : {time.time() - t}')
boxes, masks, class_ids = pop.process(output)


for b, m in zip(boxes, masks):
    b = list(map(lambda x: int(x), b))
    cv2.rectangle(image, (b[0], b[1]), (b[2], b[3]), (255,0,0), 1)
    p = np.where(m == 1)
    x, y = p[0], p[1]
    image[x, y, 1] = 200
cv2.imwrite('output.jpg', image)


# boxes: 1,116, 4200
# masks 1,32,80,160

# boxes shape: (266240,)
#  masks shape: (316680,)