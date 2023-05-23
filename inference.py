from yolo_inferencing.PostProcessor import PostProcessor
from yolo_inferencing.PreProcessor import PreProcessor
from yolo_inferencing.EngineProcessor import EngineProcessor

from subs.Camera import Camera
from subs.VideoInterface import Output
from subs.AsparagusProcessor import AsparagusProcessor
from subs.Pather import Pather
from subs.Communicator import Communicator

import cv2
import numpy as np
import time

output = Output(path = 'video.mp4')
camera = Camera()
coms   = Communicator()


ep = EngineProcessor('/home/andrii/Gus2/networks/yolo_asparagus/model.engine')
prp = PreProcessor()
pop = PostProcessor(iou_threshold = 0.62, class_threshold = 0.75,
                 input_height = 480, input_width = 640, img_height = 480, img_width = 640,
                  num_masks = 32)
asparagusProcessor = AsparagusProcessor(topk = 0.06, botk = 0.06)
pather = Pather(camera = camera, min_lenght = 0, min_dist = 100000)

ep.initalize()
camera.initCamera()
output.initOutput()

armReady = None
# try:
while True:

    armSignal = coms._readSignalFromArm()
    if armSignal == 'A':
        armReady = True

    image, depthRS, depthNP = camera.getData()

    image_data = prp.process(image)
    net_output = ep.process(image_data)
    boxes, masks, classid = pop.process(net_output)


    spears = asparagusProcessor.process(boxes, masks)
    stopSignal, spear, spear3d = pather.processSpears(spears, depthRS)

    if stopSignal:
        coms._sendStopToNav()

    else:
        coms._sendGoToNav()

    stopConf = coms._readNavSignal()

    if stopConf:



        if armReady and spear is not None:
            coms._sendCoordsToArm(spear3d)
            armReady = False


    for b, m in zip(boxes, masks):
        b = list(map(lambda x: int(x), b))
        cv2.rectangle(image, (b[0], b[1]), (b[2], b[3]), (0, 0, 160), 1)
        p = np.where(m == 1)
        x, y = p[0], p[1]
        image[x, y, 2] = 150

    if spear is not None:
        cv2.circle(image, (spear[0]), 1, (0,255,0), 2)
        cv2.circle(image, (spear[1]), 1, (0,255,0), 2)
        cv2.line(image, spear[0], spear[1], (255,0,0), 1)

    output.Render(image)

# except Exception as e:
#     print(f'Error: {e}')
#     ep.deinitialize()
# finally:
#     ep.deinitialize()