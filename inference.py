from yolo_inferencing.PostProcessor import PostProcessor
from yolo_inferencing.PreProcessor import PreProcessor
from yolo_inferencing.EngineProcessor import EngineProcessor

from subs.Camera import Camera
from subs.VideoInterface import Output
import cv2
import numpy as np
import time

output = Output(ip = '192.168.1.232')
camera = Camera()


ep = EngineProcessor('/home/andrii/Gus2/networks/yolo_asparagus/model.engine')
prp = PreProcessor()
pop = PostProcessor(iou_threshold = 0.62, class_threshold = 0.75,
                 input_height = 480, input_width = 640, img_height = 480, img_width = 640,
                  num_masks = 32)
ep.initalize()



camera.initCamera()
output.initOutput()

c = 0
tt = 0
try:
    while True:
        c+=1
        t = time.time()
        image, depthRS, depthNP = camera.getData()

        image_data = prp.process(image)
        output = ep.process(image_data)
        boxes, masks, classid = pop.process(output)
        tt+= time.time() - t
        print(type(image))
        image = np.array(image)
        print(image.shape)
        output.Render(image)

except KeyboardInterrupt:
    print(f' averate inference time: {tt/c}')
    ep.deinitialize()
finally:
    ep.deinitialize()