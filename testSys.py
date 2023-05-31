from yolo_inferencing.PostProcessor import PostProcessor
from yolo_inferencing.PreProcessor import PreProcessor
from yolo_inferencing.EngineProcessor import EngineProcessor

from subs.Camera import Camera
from subs.VideoInterface import Streamer
from subs.AsparagusProcessor import AsparagusProcessor
from subs.Pather import Pather
from subs.Visualizer import Vizualizer
from subs.Communicator import Communicator

import cv2
import numpy as np
import traceback

output = Streamer(ip = '192.168.1.108', port = 5000)
camera = Camera()

ep = EngineProcessor('/home/andrii/Gus2/networks/yolo_asparagus/model.engine')
prp = PreProcessor()
pop = PostProcessor(iou_threshold = 0.8, class_threshold = 0.85,
                 input_height = 480, input_width = 640, img_height = 480, img_width = 640,
                  num_masks = 32)
asparagusProcessor = AsparagusProcessor(topk = 0.06, botk = 0.06, camera = camera)
pather = Pather(min_lenght = 0, min_dist = 100000)
viz = Vizualizer()
coms = Communicator(nav_required=True, arm_required=True)

coms.initComs()
ep.initalize()
camera.initCamera()
output.initStreamer()



while True:

    a = int(input('Propmt (1 - Go NAV; 2 - Stop Nav; 3 - Send dummy cords)'))
    print(f'Input is: {a}')
    if a == 1:
        coms._sendGoToNav()
    if a == 2:
        coms._sendStopToNav()
    if a == 3:
        coms._sendCoordsToArm([1,1,1])

    print(f'NAV State: {coms.NAV_SHOULD_MOVE}')
    print(f'Sig from NAV: {coms.NAV_IS_STOPPED}')
