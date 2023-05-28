from yolo_inferencing.PostProcessor import PostProcessor
from yolo_inferencing.PreProcessor import PreProcessor
from yolo_inferencing.EngineProcessor import EngineProcessor

from subs.Camera import Camera
from subs.VideoInterface import Streamer
from subs.AsparagusProcessor import AsparagusProcessor
from subs.Pather import Pather
from subs.Communicator import Communicator

import cv2
import numpy as np
import traceback

output = Streamer()
camera = Camera()
coms   = Communicator()


ep = EngineProcessor('/home/andrii/Gus2/networks/yolo_asparagus/model.engine')
prp = PreProcessor()
pop = PostProcessor(iou_threshold = 0.7, class_threshold = 0.8,
                 input_height = 480, input_width = 640, img_height = 480, img_width = 640,
                  num_masks = 32)
asparagusProcessor = AsparagusProcessor(topk = 0.06, botk = 0.06)
pather = Pather(camera = camera, min_lenght = 0, min_dist = 100000)

ep.initalize()
camera.initCamera()
output.initStreamer()
coms.initComs()

armReady = None
try:
    while True:
        spears = None
        spear = None
        spear3d = None
        armSignal = coms._readSignalFromArm()
        if armSignal == 'A':
            armReady = True

        image, depthRS, depthNP = camera.getData()

        image_data = prp.process(image)
        net_output = ep.process(image_data)
        boxes, masks, classid = pop.process(net_output)


        spears = asparagusProcessor.process(boxes, masks)
        stopSignal, spear, spear3d = pather.processSpears(spears, depthRS)

        if armReady and spear3d is not None:

            coms._sendCoordsToArm(spear3d)
            armReady = False


        for b, m in zip(boxes, masks):
            b = list(map(lambda x: int(x), b))
            cv2.rectangle(image, (b[0], b[1]), (b[2], b[3]), (0, 0, 160), 1)
            p = np.where(m == 1)
            x, y = p[0], p[1]
            image[x, y, 2] = 150

        if spear is not None:
            cv2.circle(image, (spear[0][0], spear[0][1]), 1, (0,255,0), 2)
            cv2.circle(image, (spear[1][0], spear[1][1]), 1, (0,0,255), 2)
            cv2.line(image, (spear[0][0], spear[0][1]), (spear[1][0], spear[1][1]), (255,0,0), 1)

        output.Render(image)

except Exception as e:
    traceback.print_exc()
    ep.deinitialize()
finally:
    ep.deinitialize()