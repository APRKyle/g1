from yolo_inferencing.PostProcessor import PostProcessor
from yolo_inferencing.PreProcessor import PreProcessor
from yolo_inferencing.EngineProcessor import EngineProcessor

from subs.Camera import Camera
from subs.VideoInterface import Output
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
        net_output = ep.process(image_data)
        boxes, masks, classid = pop.process(net_output)
        print(classid)
        for b, m in zip(boxes, masks):
            b = list(map(lambda x: int(x), b))
            cv2.rectangle(image, (b[0], b[1]), (b[2], b[3]), (255, 0, 0), 1)
            p = np.where(m == 1)
            x, y = p[0], p[1]
            image[x, y, 1] = 200
        if c >2:
            tt += time.time() - t
        output.Render(image)

except KeyboardInterrupt:
    print(f' averate inference time: {tt/c}')
    ep.deinitialize()
finally:
    ep.deinitialize()