from yolo_inferencing.PostProcessor import PostProcessor
from yolo_inferencing.PreProcessor import PreProcessor
from yolo_inferencing.EngineProcessor import EngineProcessor

import cv2


ep = EngineProcessor('/home/andrii/GUS/SegmentationOn2GB_08_02_2023/networks/segmentation/yolo/model.engine')
prp = PreProcessor()
pop = PostProcessor(iou_threshold = 0.4, class_threshold = 0.4,
                 input_height = 416, input_width = 320, img_height = 416, img_width = 320,
                  num_masks = 32)
ep.initalize()



image = cv2.imread('humans.jpg')
print(f'IMAGE SHAPE: {image.shape}')

image_data = prp.process(image)
output = ep.process(image_data)

print(f'boxes shape: {output[0].shape}')
print(f' masks shape: {output[1].shape}')
boxes, masks, class_ids = pop.process(output)

print(boxes)
# boxes: 1,116, 4200
# masks 1,32,80,160

# boxes shape: (266240,)
#  masks shape: (316680,)